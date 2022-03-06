import sys, os, re
from tokenize import group
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util
import pandas as pd
from common import IdCodeT
import datasets.solcOptions as solcOptions

def byteBagJaccard(pairs):
  return similarity.byteBagJaccard(pairs, excludeZeros=True)

def main():
  idToCodes, idToMeta, groupToIds, *_ = solcOptions.load()
  codes = list(idToCodes.values())

  groupSizes = util.mapDict(groupToIds, lambda ids: len(ids))
  print('selected ' + str(groupSizes))

  print('skeletize')
  skeletons = util.concurrent(pre.firstSectionSkeleton)(codes)

  hashToFunction = {
    'fourbytes': hash.fourbytes,
    'ppdeep': hash.ppdeep_mod,
    'byteBag': hash.byteBag,
    'lzjd1': hash.lzjd1,
    'size': hash.size,
  }

  print('hash')
  hashToHashes = {
    hash: util.concurrent(fn)(codes if hash == 'fourbytes' else skeletons)
    for hash, fn in hashToFunction.items()
  }

  print('pairs')
  hashToPairs = {
    hash: util.allToAllPairs(hashes) for hash, hashes in hashToHashes.items()
  }

  hashToCompareFunction = {
    'fourbytes': similarity.jaccardIndex,
    'ppdeep': similarity.ppdeep_mod,
    'byteBag': byteBagJaccard,
    'lzjd1': similarity.lzjd,
    'size': similarity.sizeSimilarity,
  }

  print('compare')
  hashToComps = {
    hash: util.concurrent(hashToCompareFunction[hash])(pairs)
    for (hash, pairs) in hashToPairs.items()
  }

  print('build dataframe')
  comps1 = tuple(util.fst(hashToComps.values()))
  columns = {
    'isInner': (idToMeta[id1].group == idToMeta[id2].group for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].group for id1, id2, val in comps1),
    'group2': (idToMeta[id2].group for id1, id2, val in comps1),
  }
  columns.update({
    hash: (val for id1, id2, val in comps)
    for hash, comps in hashToComps.items()
  })
  df = pd.DataFrame(columns)

  print('correlate')
  corr_in = df[df['isInner']].corr(method='kendall')
  corr_out = df[df['isInner'] == False].corr(method='kendall')
  corr_all = df.corr(method='kendall')

  print('write')
  write.saveStr(corr_in.to_string(), 'correlations_in.txt')
  write.saveStr(corr_out.to_string(), 'correlations_out.txt')
  write.saveStr(df.to_csv(), 'comparisons_all.csv')
  write.saveStr(corr_all.to_string(), 'correlations_all.txt')
  write.saveCsv(sorted(idToMeta.values()), filename='meta.csv')

  print('plot')
  scatterPairs = [
    ('ppdeep', 'byteBag'),
    ('ppdeep', 'lzjd1'),
    ('ppdeep', 'size'),
    ('byteBag', 'lzjd1'),
    ('byteBag', 'size'),
    ('lzjd1', 'size'),
  ]

  for a,b in scatterPairs:
    plot.saveScatter(df, a, b, title='allScatter', colorBy='isInner')

if __name__ == '__main__':
  main()
