import sys, os
from typing import Callable
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, test
import pandas as pd
import datasets.solcOptions as solcOptions

idToCode, idToMeta, *_ = solcOptions.load()

def bzJumpi2(codes):
  return hash.bzJumpi(codes, chunkRes=2)
def bzJumpi4(codes):
  return hash.bzJumpi(codes, chunkRes=4)
def bzJumpi8(codes):
  return hash.bzJumpi(codes, chunkRes=8)
def bzFixedLen32_2(codes):
  return hash.bzFixedLen(codes, chunkLen=32, chunkRes=2)
def bzFixedLen64_2(codes):
  return hash.bzFixedLen(codes, chunkLen=64, chunkRes=2)
def bzFixedLen128_2(codes):
  return hash.bzFixedLen(codes, chunkLen=128, chunkRes=2)
def bzFixedLen256_2(codes):
  return hash.bzFixedLen(codes, chunkLen=256, chunkRes=2)
def bzFixedLen256_4(codes):
  return hash.bzFixedLen(codes, chunkLen=256, chunkRes=4)
def bzFixedLen64_8(codes):
  return hash.bzFixedLen(codes, chunkLen=64, chunkRes=8)
def bzFixedLen256_8(codes):
  return hash.bzFixedLen(codes, chunkLen=256, chunkRes=8)
def bzFixedLen1024_8(codes):
  return hash.bzFixedLen(codes, chunkLen=1024, chunkRes=8)

def run(metaPredicate: Callable[[solcOptions.Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].group for id, code in codes)}')
  print(f'codes len: {len(codes)}')
  print('')

  preToCodes = {
    'raw': codes,
    'skel': util.concurrent(pre.firstSectionSkeleton)(codes),
  }

  hashToFunction = {
    'bzJumpi2': bzJumpi2,
    'bzJumpi4': bzJumpi4,
    'bzJumpi8': bzJumpi8,
    'bzFixedLen32_2': bzFixedLen32_2,
    'bzFixedLen64_2': bzFixedLen64_2,
    'bzFixedLen128_2': bzFixedLen128_2,
    'bzFixedLen256_2': bzFixedLen256_2,
    'bzFixedLen256_4': bzFixedLen256_4,
    'bzFixedLen64_8': bzFixedLen64_8,
    'bzFixedLen256_8': bzFixedLen256_8,
    'bzFixedLen1024_8': bzFixedLen1024_8,
  }

  methodToHashes = {
    (p, h): util.concurrent(hashToFunction[h])(preToCodes[p])
    for p in preToCodes.keys() for h in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  hashToCompareFunction = {
    'bzJumpi2': similarity.levenshtein,
    'bzJumpi4': similarity.levenshtein,
    'bzJumpi8': similarity.levenshtein,
    'bzFixedLen32_2': similarity.levenshtein,
    'bzFixedLen64_2': similarity.levenshtein,
    'bzFixedLen128_2': similarity.levenshtein,
    'bzFixedLen256_2': similarity.levenshtein,
    'bzFixedLen256_4': similarity.levenshtein,
    'bzFixedLen64_8': similarity.levenshtein,
    'bzFixedLen256_8': similarity.levenshtein,
    'bzFixedLen1024_8': similarity.levenshtein,
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
  plot.saveScatter(df, 'raw bzFixedLen256_2', 'raw bzJumpi2', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw bzFixedLen256_4', 'raw bzJumpi4', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw bzFixedLen256_8', 'raw bzJumpi8', title=name + ' scatter', colorBy='isInner')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

if __name__ == '__main__':
  run(lambda m: m.o and m.runs == 200 and m.abi == 2, 'versions at o1 runs200 abi2')
  run(lambda m: m.o and m.runs == 200 and m.v == '0.5.16' , 'abis at 0.5.16 o1 runs200')
  run(lambda m: m.o and m.v == '0.8.4' and m.abi == 2, 'runs at 0.8.4 o1 abi2')
  run(lambda m: m.runs == 200 and m.v == '0.8.4' and m.abi == 2, 'enabled at runs200 0.8.4 abi2')
  run(lambda m: True, 'all')
