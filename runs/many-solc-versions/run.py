import sys, os, re
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis, test
import contract.opcodes as opcodes
import pandas as pd
from common import IdCodeT

codeDir = 'data/many-solc-versions'
codesList = [
  IdCodeT(filename, bytes.fromhex(open(f'{codeDir}/{filename}', mode='r').read()))
  for filename in os.listdir(codeDir)
]
groupToCodes = {}
for t in codesList:
  group = re.search('(\w+) - ', t.id).group(1)
  if group in groupToCodes:
    groupToCodes[group].append(t)
  else:
    groupToCodes[group] = [t]

groupSizes = util.mapDict(groupToCodes, lambda codes: len(codes))
print('selected ' + str(groupSizes))

print('skeletize')
groupToSkeletons = util.mapDict(groupToCodes, util.concurrent(pre.firstSectionSkeleton))

print('hash')
methodToGroupToHashes = {
  'fourbytes': util.mapDict(groupToCodes, util.concurrent(hash.fourbytes)),
  'ppdeep': util.mapDict(groupToSkeletons, util.concurrent(hash.ppdeep_mod)),
  'byteBag': util.mapDict(groupToSkeletons, util.concurrent(hash.byteBag)),
  'lzjd1': util.mapDict(groupToSkeletons, util.concurrent(hash.lzjd1)),
  'size': util.mapDict(groupToSkeletons, hash.size),
}

print('inner pairs')
methodToGroupToInnerPairs = util.mapDict(
  methodToGroupToHashes,
  lambda groupToHashes: util.mapDict(groupToHashes, util.allToAllPairs))

print('cross pairs')
methodToGroupToCrossPairs = util.mapDict(
  methodToGroupToHashes,
  lambda groupToHashes: util.allCrossGroupPairs(groupToHashes))

print('compare inner')
methodToGroupToInnerComps = {
  'fourbytes': util.mapDict(methodToGroupToInnerPairs['fourbytes'], util.concurrent(compare.jaccardIndex)),
  'ppdeep': util.mapDict(methodToGroupToInnerPairs['ppdeep'], util.concurrent(compare.ppdeep_mod)),
  'byteBagJaccard': util.mapDict(methodToGroupToInnerPairs['byteBag'], util.concurrent(compare.byteBagJaccard), excludeZeros=True),
  'lzjd1': util.mapDict(methodToGroupToInnerPairs['lzjd1'], util.concurrent(compare.lzjd)),
  'size': util.mapDict(methodToGroupToInnerPairs['size'], util.concurrent(compare.sizeSimilarity)),
}

print('compare cross')
methodToGroupToCrossComps = {
  'fourbytes': util.mapDict(methodToGroupToCrossPairs['fourbytes'], util.concurrent(compare.jaccardIndex)),
  'ppdeep': util.mapDict(methodToGroupToCrossPairs['ppdeep'], util.concurrent(compare.ppdeep_mod)),
  'byteBagJaccard': util.mapDict(methodToGroupToCrossPairs['byteBag'], util.concurrent(compare.byteBagJaccard), excludeZeros=True),
  'lzjd1': util.mapDict(methodToGroupToCrossPairs['lzjd1'], util.concurrent(compare.lzjd)),
  'size': util.mapDict(methodToGroupToCrossPairs['size'], util.concurrent(compare.sizeSimilarity)),
}

print('build data frames')
df_inner = pd.DataFrame(test.buildComparisonColumns(methodToGroupToInnerComps))
df_cross = pd.DataFrame(test.buildComparisonColumns(methodToGroupToCrossComps))
df_all = pd.concat([df_inner, df_cross])

print('correlate')
corr_in = df_inner.corr(method='kendall')
corr_out = df_cross.corr(method='kendall')
corr_all = df_all.corr(method='kendall')

print('write')
write.saveStr(df_inner.to_csv(), 'comparisons_in.csv')
write.saveStr(corr_in, 'correlations_in.txt')
write.saveStr(df_cross.to_csv(), 'comparisons_out.csv')
write.saveStr(corr_out, 'correlations_out.txt')
write.saveStr(df_all.to_csv(), 'comparisons_all.csv')
write.saveStr(corr_all, 'correlations_all.txt')
write.saveCsv([[name, id] for name, ts in groupToCodes.items() for id, code in ts], name='ids.csv')

print('plot')
scatterPairs = [
  ('ppdeep', 'byteBagJaccard'),
  ('ppdeep', 'lzjd1'),
  ('ppdeep', 'size'),
  ('byteBagJaccard', 'lzjd1'),
  ('byteBagJaccard', 'size'),
  ('lzjd1', 'size'),
]

for a,b in scatterPairs:
  plot.saveScatter(df_all, a, b, title='allScatter', colorBy='isInner')
