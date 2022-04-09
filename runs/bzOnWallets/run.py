import sys, os
from typing import Callable
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, test, opfilter
import pandas as pd
import datasets.wallets as wallets

def highFOnly(codes):
  return pre.filterBytes(codes, opfilter.highFStatPred)
def highF0(codes):
  return pre.setBytesZero(codes, opfilter.highFStatPred)
def highFOnlyV2(codes):
  return pre.filterBytes(codes, opfilter.highFStatV2Pred)
def highF0V2(codes):
  return pre.setBytesZero(codes, opfilter.highFStatV2Pred)

def bzJumpi02(codes): return hash.bzJumpi(codes, chunkRes=2)
def bzJumpi04(codes): return hash.bzJumpi(codes, chunkRes=4)
def bzJumpi08(codes): return hash.bzJumpi(codes, chunkRes=8)
def bzJumpi16(codes): return hash.bzJumpi(codes, chunkRes=16)

(idToCode, idToMeta, typeToIds, skeletonToIds, fstIdPerSkel) = wallets.load()

def run(metaPredicate: Callable[[wallets.Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].type for id, code in codes)}')
  print(f'codes len: {len(codes)}')
  print('')

  preToCodes = {
    'raw': codes,
    'skeletons': util.concurrent(pre.skeleton)(codes),
    'fstSecSkel': util.concurrent(pre.firstSectionSkeleton)(codes),
  }
  preToCodes.update({
    'fStat_V1': util.concurrent(highFOnly)(preToCodes['fstSecSkel']),
    'fStat0V1': util.concurrent(highF0)(preToCodes['fstSecSkel']),
    'fStat_V2': util.concurrent(highFOnlyV2)(preToCodes['fstSecSkel']),
    'fStat0V2': util.concurrent(highF0V2)(preToCodes['fstSecSkel']),
  })

  hashToFunction = {
    'bzJumpi02': bzJumpi02,
    'bzJumpi04': bzJumpi04,
    'bzJumpi08': bzJumpi08,
    'bzJumpi16': bzJumpi16,
  }

  methodToHashes = {
    (p, h): util.concurrent(hashToFunction[h])(preToCodes[p])
    for p in preToCodes.keys() for h in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  print('compare')
  hashToCompareFunction = {
    'bzJumpi02': similarity.levenshtein,
    'bzJumpi04': similarity.levenshtein,
    'bzJumpi08': similarity.levenshtein,
    'bzJumpi16': similarity.levenshtein,
  }
  methodToComps = {
    method: util.concurrent(hashToCompareFunction[method[1]])(pairs)
    for (method, pairs) in methodToPairs.items()
  }

  print('dataframe')
  comps1 = tuple(util.fst(methodToComps.values()))
  columns = {
    'isInner': (idToMeta[id1].type == idToMeta[id2].type for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].type for id1, id2, val in comps1),
    'group2': (idToMeta[id2].type for id1, id2, val in comps1),
  }
  columns.update({
    ' '.join(method): (val for id1, id2, val in comps)
    for method, comps in methodToComps.items()
  })
  df = pd.DataFrame(columns)

  print('correlate')
  corr = df.corr(method='kendall')
  separations = test.separation(df)
  qDists = test.qDist(df)

  print('write')
  write.saveCsv(separations.items(), filename=name + ' separations.csv')
  write.saveCsv(qDists.items(), filename=name + ' qDists.csv')
  write.saveGml((idToMeta[id] for id, code in codes), df, filename=name + '.gml')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

  print('plot')
  for method in methodToPairs.keys():
    test.saveHistogram(df, ' '.join(method), name)
    plot.saveViolin(df, ' '.join(method), name)

if __name__ == '__main__':
  run(lambda m: m.id in fstIdPerSkel, 'all')

  write.saveStr(
    '\n'.join(util.mdImg(f[:-4], f'./{f}') for f in plot.listPngFiles()),
    filename='README.md')
