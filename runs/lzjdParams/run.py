import sys, os
from typing import Callable
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, test
import datasets.solcOptions as solcOptions
import pandas as pd

idToCode, idToMeta, *_ = solcOptions.load()

def lzjd32(codes):
  return hash.lzjd1(codes, hash_size=32, mode=None, false_seen_prob=0)
def lzjd64(codes):
  return hash.lzjd1(codes, hash_size=64, mode=None, false_seen_prob=0)
def lzjd128(codes):
  return hash.lzjd1(codes, hash_size=128, mode=None, false_seen_prob=0)
def lzjd256(codes):
  return hash.lzjd1(codes, hash_size=256, mode=None, false_seen_prob=0)
def lzjd512(codes):
  return hash.lzjd1(codes, hash_size=512, mode=None, false_seen_prob=0)
def lzjd1K(codes):
  return hash.lzjd1(codes, hash_size=1024, mode=None, false_seen_prob=0)

def byteBagJaccard(pairs):
  return similarity.byteBagJaccard(pairs, excludeZeros=0)

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
    'ncd': hash.ncd,
    'lzjd32': lzjd32,
    'lzjd64': lzjd64,
    'lzjd128': lzjd128,
    'lzjd256': lzjd256,
    'lzjd512': lzjd512,
    'lzjd1K': lzjd1K,
  }

  methodToHashes = {
    (p, h): util.concurrent(hashToFunction[h])(preToCodes[p])
    for p in preToCodes.keys() for h in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  hashToCompareFunction = {
    'ncd': similarity.ncd,
    'lzjd32': similarity.lzjd,
    'lzjd64': similarity.lzjd,
    'lzjd128': similarity.lzjd,
    'lzjd256': similarity.lzjd,
    'lzjd512': similarity.lzjd,
    'lzjd1K': similarity.lzjd,
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
  write.saveGml2((idToMeta[id] for id, code in codes), df, filename=name + '.gml')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd32', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd64', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd128', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd256', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd512', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw ncd', 'raw lzjd1K', title=name + ' scatter', colorBy='isInner')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

if __name__ == '__main__':
  run(lambda m: m.o and m.runs == 200 and m.abi == 2, 'versions at o1 runs200 abi2')
  run(lambda m: m.o and m.runs == 200 and m.v == '0.5.16' , 'abis at 0.5.16 o1 runs200')
  run(lambda m: m.o and m.v == '0.8.4' and m.abi == 2, 'runs at 0.8.4 o1 abi2')
  run(lambda m: m.runs == 200 and m.v == '0.8.4' and m.abi == 2, 'enabled at runs200 0.8.4 abi2')
  run(lambda m: True, 'all')
