import sys, os, re
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis
import contract.opcodes as opcodes
import pandas as pd
from common import IdCodeT

codeDir = _runDir + '/codes'
codesList = [
  IdCodeT(filename, bytes.fromhex(open(f'{codeDir}/{filename}', mode='r').read()))
  for filename in os.listdir(codeDir)
]
codes = {}
for t in codesList:
  group = re.search('(\w+) - ', t.id).group(1)
  if group in codes:
    codes[group].append(t)
  else:
    codes[group] = [t]

groupSizes = util.mapDict(codes, lambda codes: len(codes))
print('selected ' + str(groupSizes))

print('skeletize')
skeletons = util.mapDict(codes, util.concurrent(pre.firstSectionSkeleton))

print('hash')
ppdeep = util.mapDict(skeletons, util.concurrent(hash.ppdeep_mod))
fourbytes = util.mapDict(codes, util.concurrent(hash.fourbytes))
byteBag = util.mapDict(skeletons, util.concurrent(hash.byteBag))
lzjd1 = util.mapDict(skeletons, util.concurrent(hash.lzjd1))
size = util.mapDict(skeletons, hash.size)

print('inner pairs')
ppdeep_inPairs = util.mapDict(ppdeep, util.allToAllPairs)
fourbytes_inPairs = util.mapDict(fourbytes, util.allToAllPairs)
byteBag_inPairs = util.mapDict(byteBag, util.allToAllPairs)
lzjd1_inPairs = util.mapDict(lzjd1, util.allToAllPairs)
size_inPairs = util.mapDict(size, util.allToAllPairs)

print('outter pairs')
ppdeep_outPairs = util.allIntergroupPairs(ppdeep)
fourbytes_outPairs = util.allIntergroupPairs(fourbytes)
byteBag_outPairs = util.allIntergroupPairs(byteBag)
lzjd1_outPairs = util.allIntergroupPairs(lzjd1)
size_outPairs = util.allIntergroupPairs(size)

print('compare in')
ppdeep_inComps = util.mapDict(ppdeep_inPairs, util.concurrent(compare.ppdeep_mod))
byteBag_inComps = util.mapDict(byteBag_inPairs, util.concurrent(compare.byteBagJaccard), excludeZeros=True)
lzjd1_inComps = util.mapDict(lzjd1_inPairs, util.concurrent(compare.lzjd))
size_inComps = util.mapDict(size_inPairs, util.concurrent(compare.sizeSimilarity))
fourbytes_inComps = util.mapDict(fourbytes_inPairs, util.concurrent(compare.jaccardIndex))

print('compare out')
ppdeep_outComps = util.mapDict(ppdeep_outPairs, util.concurrent(compare.ppdeep_mod))
byteBag_outComps = util.mapDict(byteBag_outPairs, util.concurrent(compare.byteBagJaccard), excludeZeros=True)
lzjd1_outComps = util.mapDict(lzjd1_outPairs, util.concurrent(compare.lzjd))
size_outComps = util.mapDict(size_outPairs, util.concurrent(compare.sizeSimilarity))
fourbytes_outComps = util.mapDict(fourbytes_outPairs, util.concurrent(compare.jaccardIndex))

print('correlate in')
df_in = pd.DataFrame({
  'isIn': [True] * sum(len(vs) for vs in ppdeep_inComps.values()),
  'id1': [id1 for group, comps in ppdeep_inComps.items() for id1, id2, val in comps],
  'id2': [id2 for group, comps in ppdeep_inComps.items() for id1, id2, val in comps],
  'fourbytes': [val for group, comps in fourbytes_inComps.items() for id1, id2, val in comps],
  'ppdeep': [val for group, comps in ppdeep_inComps.items() for id1, id2, val in comps],
  'byteBagJaccard': [val for group, comps in byteBag_inComps.items() for id1, id2, val in comps],
  'lzjd1': [val for group, comps in lzjd1_inComps.items() for id1, id2, val in comps],
  'size': [val for group, comps in size_inComps.items() for id1, id2, val in comps],
})

corr_in = df_in.corr(method='kendall')
write.saveStr(df_in.to_csv(), 'comparisons_in.csv')
write.saveStr(corr_in, 'correlations_in.txt')

print('plot in')
plot.scatter(df_in, 'ppdeep', 'byteBagJaccard', name='inScatter', newFigure=True)
plot.scatter(df_in, 'ppdeep', 'lzjd1', name='inScatter', newFigure=True)
plot.scatter(df_in, 'ppdeep', 'size', name='inScatter', newFigure=True)
plot.scatter(df_in, 'byteBagJaccard', 'lzjd1', name='inScatter', newFigure=True)
plot.scatter(df_in, 'byteBagJaccard', 'size', name='inScatter', newFigure=True)
plot.scatter(df_in, 'lzjd1', 'size', name='inScatter', newFigure=True)

print('correlate out')
df_out = pd.DataFrame({
  'isIn': [False] * sum(len(vs) for vs in ppdeep_outComps.values()),
  'id1': [id1 for groupPair, comps in ppdeep_outComps.items() for id1, id2, val in comps],
  'id2': [id2 for groupPair, comps in ppdeep_outComps.items() for id1, id2, val in comps],
  'fourbytes': [val for groupPair, comps in fourbytes_outComps.items() for id1, id2, val in comps],
  'ppdeep': [val for groupPair, comps in ppdeep_outComps.items() for id1, id2, val in comps],
  'byteBagJaccard': [val for groupPair, comps in byteBag_outComps.items() for id1, id2, val in comps],
  'lzjd1': [val for groupPair, comps in lzjd1_outComps.items() for id1, id2, val in comps],
  'size': [val for groupPair, comps in size_outComps.items() for id1, id2, val in comps],
})

corr_out = df_out.corr(method='kendall')
write.saveStr(df_out.to_csv(), 'comparisons_out.csv')
write.saveStr(corr_out, 'correlations_out.txt')

print('plot out')
plot.scatter(df_out, 'ppdeep', 'byteBagJaccard', name='outScatter', newFigure=True)
plot.scatter(df_out, 'ppdeep', 'lzjd1', name='outScatter', newFigure=True)
plot.scatter(df_out, 'ppdeep', 'size', name='outScatter', newFigure=True)
plot.scatter(df_out, 'byteBagJaccard', 'lzjd1', name='outScatter', newFigure=True)
plot.scatter(df_out, 'byteBagJaccard', 'size', name='outScatter', newFigure=True)
plot.scatter(df_out, 'lzjd1', 'size', name='outScatter', newFigure=True)

print('correlate all')
df_all = pd.concat([df_in, df_out])

corr_all = df_all.corr(method='kendall')
write.saveStr(df_all.to_csv(), 'comparisons_all.csv')
write.saveStr(corr_all, 'correlations_all.txt')
write.saveCsv([[name, id] for name, ts in codes.items() for id, code in ts], name='ids.csv')

print('plot all')
plot.scatter(df_all, 'ppdeep', 'byteBagJaccard', name='allScatter', newFigure=True, colorBy='isIn')
plot.scatter(df_all, 'ppdeep', 'lzjd1', name='allScatter', newFigure=True, colorBy='isIn')
plot.scatter(df_all, 'ppdeep', 'size', name='allScatter', newFigure=True, colorBy='isIn')
plot.scatter(df_all, 'byteBagJaccard', 'lzjd1', name='allScatter', newFigure=True, colorBy='isIn')
plot.scatter(df_all, 'byteBagJaccard', 'size', name='allScatter', newFigure=True, colorBy='isIn')
plot.scatter(df_all, 'lzjd1', 'size', name='allScatter', newFigure=True, colorBy='isIn')

