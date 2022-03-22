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
import datasets.solcOptions as solcOptions

idToCode, idToMeta, *_ = solcOptions.load()

def byteBagJaccard(pairs):
  return similarity.byteBagJaccard(pairs, excludeZeros=True)
def highFOnly(codes):
  return pre.filterBytes(codes, opfilter.highFStatPred)
def highF0(codes):
  return pre.setBytesZero(codes, opfilter.highFStatPred)
def lzjd(codes):
  return hash.lzjd1(codes, hash_size=256, mode=None, false_seen_prob=0)
def bzJumpi4(codes):
  return hash.bzJumpi(codes, chunkRes=4)

def run(metaPredicate: Callable[[solcOptions.Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].group for id, code in codes)}')
  print(f'codes len: {len(codes)}')
  print('')

  preToCodes = {
    'raw': codes,
    'skeletons': util.concurrent(pre.skeleton)(codes),
    'fstSecSkel': util.concurrent(pre.firstSectionSkeleton)(codes),
  }
  preToCodes.update({
    'fStat': util.concurrent(highFOnly)(preToCodes['fstSecSkel']),
    'fStat0': util.concurrent(highF0)(preToCodes['fstSecSkel']),
  })

  hashToFunction = {
    'ssdeep': hash.ssdeep,
    'ppdeep': hash.ppdeep,
    'ppdeep_mod': hash.ppdeep_mod,
    'byteBag': hash.byteBag,
    'lzjd': lzjd,
    'bz': bzJumpi4,
    'jump': hash.jumpHash,
    'ncd': hash.ncd,
  }

  methodToHashes = {
    (pre, hash): util.concurrent(hashToFunction[hash])(preToCodes[pre])
    for pre in preToCodes.keys() for hash in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  hashToCompareFunction = {
    'ssdeep': similarity.ssdeep,
    'ppdeep': similarity.ppdeep,
    'ppdeep_mod': similarity.ppdeep_mod,
    'byteBag': byteBagJaccard,
    'lzjd': similarity.lzjd,
    'bz': similarity.levenshtein,
    'jump': similarity.levenshtein,
    'ncd': similarity.ncd,
  }

  methodToComps = {
    method: util.concurrent(hashToCompareFunction[method[1]])(pairs)
    for (method, pairs) in methodToPairs.items()
  }

  comps1 = tuple(util.fst(methodToComps.values()))

  columns = {
    'isInner': (idToMeta[id1].group == idToMeta[id2].group for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].group for id1, id2, val in comps1),
    'group2': (idToMeta[id2].group for id1, id2, val in comps1),
  }
  columns.update({
    ' '.join(method): (val for id1, id2, val in comps)
    for method, comps in methodToComps.items()
  })

  df = pd.DataFrame(columns)
  corr = df.corr(method='kendall')
  separations = test.separation(df)

  write.saveCsv(separations.items(), filename=name + ' separations.csv')
  write.saveGml((idToMeta[id] for id, code in codes), df, filename=name + '.gml')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

  scatterPairs = {
    ('raw lzjd', 'skeletons ppdeep_mod'),
    ('skeletons ppdeep_mod', 'fstSecSkel jump'),
    ('fStat0 ppdeep_mod', 'fStat ppdeep'),
    ('fstSecSkel jump', 'fStat ppdeep'),
    ('fStat0 ppdeep_mod', 'fstSecSkel jump'),
    ('raw lzjd', 'fstSecSkel jump'),
    ('raw ncd', 'fstSecSkel jump'),
    ('skeletons ssdeep', 'skeletons ppdeep_mod'),
    ('skeletons ssdeep', 'skeletons ppdeep'),
  }
  for a, b in scatterPairs:
    plot.saveScatter(df, a, b, title=name + ' scatter', colorBy='isInner')

  for method in methodToPairs.keys():
    test.saveHistogram(df, ' '.join(method), name)

  write.saveStr(
    '\n'.join(util.mdImg(f[:-4], f'./{f}') for f in plot.listPngFiles()),
    filename='README.md')

if __name__ == '__main__':
  run(lambda m: m.o and m.runs == 200 and m.abi == 2, 'versions at o1 runs200 abi2')
  run(lambda m: m.o and m.runs == 200 and m.v == '0.5.16' , 'abis at 0.5.16 o1 runs200')
  run(lambda m: m.o and m.v == '0.8.4' and m.abi == 2, 'runs at 0.8.4 o1 abi2')
  run(lambda m: m.runs == 200 and m.v == '0.8.4' and m.abi == 2, 'enabled at runs200 0.8.4 abi2')
  run(lambda m: True, 'all')
