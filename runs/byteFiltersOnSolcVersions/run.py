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


def significant(op: int):
  OP = opcodes.opcode_by_value_or_missing(op)
  return (
    OP.is_log() or OP.is_storage() or OP.is_sys_op() or OP.is_env_info() or OP.is_block_info()
    or OP == opcodes.SHA3 or OP == opcodes.GAS)

groupToSignificantAndZero = util.mapDict(groupToSkeletons, lambda skel: pre.setBytesZero(skel, significant))
groupToSignificantOnly = util.mapDict(groupToSkeletons, lambda skel: pre.filterBytes(skel, significant))


print('hash')
methodToGroupToHashes = {
  'ppdeep-significantAndZero': util.mapDict(groupToSignificantAndZero, util.concurrent(hash.ppdeep_mod)),
  'ppdeep-significantOnly': util.mapDict(groupToSignificantOnly, util.concurrent(hash.ppdeep_mod)),
  'ppdeep-skeleton': util.mapDict(groupToSkeletons, util.concurrent(hash.ppdeep_mod)),
  'byteBag-significantOnly': util.mapDict(groupToSignificantOnly, util.concurrent(hash.byteBag)),
  'byteBag-skeleton': util.mapDict(groupToSkeletons, util.concurrent(hash.byteBag)),
  'lzjd1-significantAndZero': util.mapDict(groupToSignificantAndZero, util.concurrent(hash.lzjd1)),
  'lzjd1-significantOnly': util.mapDict(groupToSignificantOnly, util.concurrent(hash.lzjd1)),
  'lzjd1-skeleton': util.mapDict(groupToSkeletons, util.concurrent(hash.lzjd1)),
}

print('pairs')
methodToGroupToInnerPairs = util.mapDict(
  methodToGroupToHashes,
  lambda groupToHashes: util.mapDict(groupToHashes, util.allToAllPairs))

methodToGroupToCrossPairs = util.mapDict(
  methodToGroupToHashes,
  lambda groupToHashes: util.allCrossGroupPairs(groupToHashes))

def comp(method: str):
  def go(pairs):
    if method.startswith('byteBag'):
      return util.concurrent(compare.byteBagJaccard)(pairs, excludeZeros=True)
    elif method.startswith('ppdeep'):
      return util.concurrent(compare.ppdeep_mod)(pairs)
    elif method.startswith('lzjd1'):
      return util.concurrent(compare.lzjd)(pairs)
  return go

print('compare')
methodToGroupToInnerComps = {
  method: util.mapDict(groupToPairs, comp(method)) for method, groupToPairs
    in methodToGroupToInnerPairs.items()
}
methodToGroupToCrossComps = {
  method: util.mapDict(groupToPairs, comp(method)) for method, groupToPairs
    in methodToGroupToCrossPairs.items()
}

print('build data frames')
df_inner = pd.DataFrame(test.buildComparisonColumns(methodToGroupToInnerComps))
df_cross = pd.DataFrame(test.buildComparisonColumns(methodToGroupToCrossComps))
df_all = pd.concat([df_inner, df_cross])

print('correlate')
corr_inner = df_inner.corr(method='kendall')
corr_cross = df_cross.corr(method='kendall')
corr_all = df_all.corr(method='kendall')

print('write')
write.saveStr(df_inner.to_csv(), 'comparisons_inner.csv')
write.saveStr(corr_inner, 'correlations_inner.txt')
write.saveStr(df_cross.to_csv(), 'comparisons_cross.csv')
write.saveStr(corr_cross, 'correlations_cross.txt')
write.saveStr(df_all.to_csv(), 'comparisons_all.csv')
write.saveStr(corr_all, 'correlations_all.txt')
write.saveCsv([[name, id] for name, ts in groupToCodes.items() for id, code in ts], filename='ids.csv')

print('plot')
scatterPairs = util.allToAllPairs(list(methodToGroupToHashes.keys()))

for a,b in scatterPairs:
  plot.saveScatter(df_all, a, b, colorBy='isInner')
