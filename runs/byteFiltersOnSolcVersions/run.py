import sys, os
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, test
import contract.opcodes as opcodes
import pandas as pd
import datasets.solcOptions as solcOptions

def isSignificant(op: int):
  OP = opcodes.opcode_by_value_or_missing(op)
  return (
    OP.is_log() or OP.is_storage() or OP.is_sys_op() or OP.is_env_info() or OP.is_block_info()
    or OP == opcodes.SHA3 or OP == opcodes.GAS)
def significantOnly(codes):
  return pre.filterBytes(codes, isSignificant)
def significantAndZero(codes):
  return pre.setBytesZero(codes, isSignificant)
def byteBagJaccard(pairs):
  return similarity.byteBagJaccard(pairs, excludeZeros=True)

def main():
  idToCodes, idToMeta, groupToIds, *_ = solcOptions.load()
  codes = list(idToCodes.values())

  groupSizes = util.mapDict(groupToIds, lambda ids: len(ids))
  print('selected ' + str(groupSizes))

  print('pre')
  preToCodes = {
    'skeleton': util.concurrent(pre.firstSectionSkeleton)(codes),
  }
  preToCodes.update({
    'significantAndZero': util.concurrent(significantAndZero)(preToCodes['skeleton']),
    'significantOnly': util.concurrent(significantOnly)(preToCodes['skeleton']),
  })

  print('hash')
  hashToFunction = {
    'ppdeep': hash.ppdeep_mod,
    'byteBag': hash.byteBag,
    'lzjd1': hash.lzjd1,
  }
  hashToPres = {
    'ppdeep': ('significantAndZero', 'significantOnly', 'skeleton'),
    'byteBag': ('significantOnly', 'skeleton'),
    'lzjd1': ('significantAndZero', 'significantOnly', 'skeleton'),
  }
  methodToHashes = {
    (pre, hash): util.concurrent(hashToFunction[hash])(preToCodes[pre])
    for hash, pres in hashToPres.items() for pre in pres
  }

  print('pairs')
  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  print('compare')
  hashToCompareFunction = {
    'ppdeep': similarity.ppdeep_mod,
    'byteBag': byteBagJaccard,
    'lzjd1': similarity.lzjd,
  }
  methodToComps = {
    method: util.concurrent(hashToCompareFunction[method[1]])(pairs)
    for (method, pairs) in methodToPairs.items()
  }

  print('build dataframe')
  comps1 = tuple(util.fst(methodToComps.values()))
  columns = {
    'isInner': (idToMeta[id1].group == idToMeta[id2].group for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].group for id1, id2, val in comps1),
    'group2': (idToMeta[id2].group for id1, id2, val in comps1),
  }
  columns.update({
    f'{method[1]}-{method[0]}': (val for id1, id2, val in comps)
    for method, comps in methodToComps.items()
  })
  df = pd.DataFrame(columns)

  print('correlate')
  corr_inner = df[df['isInner']].corr(method='kendall')
  corr_cross = df[df['isInner'] == False].corr(method='kendall')
  corr_all = df.corr(method='kendall')
  qDists = test.qDist(df)

  print('write')
  write.saveCsv(qDists.items(), filename='qDists.csv')
  write.saveStr(corr_inner.to_string(), 'correlations_inner.txt')
  write.saveStr(corr_cross.to_string(), 'correlations_cross.txt')
  write.saveStr(df.to_csv(), 'comparisons_all.csv')
  write.saveStr(corr_all.to_string(), 'correlations_all.txt')
  write.saveCsv(sorted(idToMeta.values()), filename='meta.csv')
  write.saveGml((idToMeta[id] for id, code in codes), df)

  print('plot')
  for a,b in util.allToAllPairs(list(methodToHashes.keys())):
    plot.saveScatter(df, f'{a[1]}-{a[0]}', f'{b[1]}-{b[0]}', colorBy='isInner')

  for method in methodToPairs.keys():
    plot.saveViolin(df, f'{method[1]}-{method[0]}')

if __name__ == '__main__':
  main()
  write.saveStr(
    '\n'.join(util.mdImg(f[:-4], f'./{f}') for f in plot.listPngFiles()),
    filename='README.md')
