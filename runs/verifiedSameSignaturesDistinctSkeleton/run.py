import sys, os
sys.path.insert(1, 'src')
import write, plot
_outDir = os.path.dirname(os.path.abspath(__file__)) + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import db, pre, hash, compare, util, vis
import contract.opcodes as opcodes
import pandas as pd

def verifiedSameSignaturesDistinctSkeleton(addr):
  codeId = db.getCodesViaAddresses([addr])[0].id
  return db.selectIdCodeTs("""
    WITH ids AS (
      SELECT
        min(c.code) code
      FROM
        esverifiedcontract es
        JOIN contract2 ct ON es.aid = ct.aid
        JOIN code2 c on c.code = ct.cdeployed
      WHERE
        c.signatures = (SELECT c.signatures FROM code2 c WHERE c.code = %s)
      GROUP BY
        c.skeleton
    )
    SELECT
      ids.code, b.dat
    FROM
      ids JOIN bindata b ON ids.code = b.id
  """, (codeId,))

codes = {
  'FoMo3Dlong': verifiedSameSignaturesDistinctSkeleton('0xA62142888ABa8370742bE823c1782D17A0389Da1'),
  'Hourglass': verifiedSameSignaturesDistinctSkeleton('0xB3775fB83F7D12A36E0475aBdD1FCA35c091efBe'),
  'UniswapV2Router02': verifiedSameSignaturesDistinctSkeleton('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'),
  'BancorConverterFactory': verifiedSameSignaturesDistinctSkeleton('0xbf1ad26091fb1a50a812807aba2a3dd93f2f0851'),
  'DSToken': verifiedSameSignaturesDistinctSkeleton('0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2'),
}
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
ppdeep_outPairs = util.allCrossGroupPairs(ppdeep)
fourbytes_outPairs = util.allCrossGroupPairs(fourbytes)
byteBag_outPairs = util.allCrossGroupPairs(byteBag)
lzjd1_outPairs = util.allCrossGroupPairs(lzjd1)
size_outPairs = util.allCrossGroupPairs(size)

print('compare in')
ppdeep_inComps = util.mapDict(ppdeep_inPairs, util.concurrent(compare.ppdeep_mod))
byteBag_inComps = util.mapDict(byteBag_inPairs, util.concurrent(compare.byteBagJaccard), excludeZeros=True)
lzjd1_inComps = util.mapDict(lzjd1_inPairs, util.concurrent(compare.lzjd))
size_inComps = util.mapDict(size_inPairs, util.concurrent(compare.sizeSimilarity))

print('compare out')
ppdeep_outComps = util.mapDict(ppdeep_outPairs, util.concurrent(compare.ppdeep_mod))
byteBag_outComps = util.mapDict(byteBag_outPairs, util.concurrent(compare.byteBagJaccard), excludeZeros=True)
lzjd1_outComps = util.mapDict(lzjd1_outPairs, util.concurrent(compare.lzjd))
size_outComps = util.mapDict(size_outPairs, util.concurrent(compare.sizeSimilarity))

print('correlate in')
df_in = pd.DataFrame({
  'isIn': [True] * sum(len(vs) for vs in ppdeep_inComps.values()),
  'id1': [id1 for group, comps in ppdeep_inComps.items() for id1, id2, val in comps],
  'id2': [id2 for group, comps in ppdeep_inComps.items() for id1, id2, val in comps],
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

