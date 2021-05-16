import sys, os
sys.path.insert(1, 'src')
import write, plot
_outDir = os.path.dirname(os.path.abspath(__file__)) + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import db, pre, hash, compare, util, common, vis
import contract.opcodes as opcodes
import pandas as pd

codes = db.selectIdCodeTs("""
with ids as (
  SELECT
    min(es.aid) aid,
    min(c.code) code,
    count(es.aid) count,
    c.skeleton
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON ct.cdeployed = c.code
  WHERE
    --es.name = 'ADZbuzzCommunityToken'
    es.name = 'AdminUpgradeabilityProxy'
  GROUP BY
    c.skeleton
)
select
  --encode(a.addr, 'hex') address, count, (select count(*) from message where receiver = ids.aid)
  ids.code, b.dat
from
  ids
  join account a on a.id = ids.aid
  join bindata b on b.id = ids.code
where
  (select count(*) from message where receiver = ids.aid) > 0;
""")

print(f'selected {len(codes)}')

print('pre')
skel = util.runConcurrent(pre.firstSectionSkeleton, codes)

print('hashing1')
hashes = util.runConcurrent(hash.ppdeep_mod, skel)
print('hashing2')
fours = util.runConcurrent(hash.fourbytes, codes)
print('hashing3')
byteBag = util.runConcurrent(hash.byteBag, skel)
print('hashing4')
lzjd = util.runConcurrent(hash.lzjd1, skel)
print('hashing5')
sizes = util.runConcurrent(hash.size, skel)

print('pairs1')
hashPairs = util.allToAllPairs(hashes)
print('pairs2')
foursPairs = util.allToAllPairs(fours)
print('pairs3')
byteBagPairs = util.allToAllPairs(byteBag)
print('pairs4')
lzjdPairs = util.allToAllPairs(lzjd)
print('pairs5')
sizePairs = util.allToAllPairs(sizes)

print('compare1')
hashLevenshtein = util.runConcurrent(compare.ppdeep_mod, hashPairs)
print('compare2')
hashJaccard = util.runConcurrent(compare.ppdeep_mod_jaccard, hashPairs)
print('compare3')
foursJaccard = util.runConcurrent(compare.jaccardIndex, foursPairs)
print('compare4')
byteBagJaccard = util.runConcurrent(compare.byteBagJaccard, byteBagPairs, excludeZeros=False)
print('compare5')
byteBagJaccardNoZeros = util.runConcurrent(compare.byteBagJaccard, byteBagPairs, excludeZeros=True)
print('compare6')
lzjdSimilarity = util.runConcurrent(compare.lzjd, lzjdPairs)
print('compare7')
sizeSimilarity = util.runConcurrent(compare.sizeSimilarity, sizePairs)

print('correlate')
df = pd.DataFrame({
  'id1': [id1 for id1, id2, val in hashLevenshtein],
  'id2': [id2 for id1, id2, val in hashLevenshtein],
  'hashLevenshtein': [val for id1, id2, val in hashLevenshtein],
  'hashJaccard': [val for id1, id2, val in hashJaccard],
  'foursJaccard': [val for id1, id2, val in foursJaccard],
  'byteBagJaccard': [val for id1, id2, val in byteBagJaccard],
  'byteBagJaccardNoZeros': [val for id1, id2, val in byteBagJaccardNoZeros],
  'lzjdSimilarity': [val for id1, id2, val in lzjdSimilarity],
  'sizeSimilarity': [val for id1, id2, val in sizeSimilarity],
})
print('write')
corr = df.corr(method='kendall')
write.saveStr(df.to_csv(), 'comparisons.csv')
write.saveStr(corr, 'correlations.txt')
write.saveStr('\n'.join([str(id) for id, code in codes]), 'ids.csv')

print('plot')
plot.scatter(df, 'foursJaccard', 'hashLevenshtein', newFigure=True)
plot.scatter(df, 'foursJaccard', 'byteBagJaccardNoZeros', newFigure=True)
plot.scatter(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.scatter(df, 'lzjdSimilarity', 'hashLevenshtein', newFigure=True)
plot.qq(df, 'foursJaccard', 'hashLevenshtein', newFigure=True)
plot.qq(df, 'foursJaccard', 'byteBagJaccardNoZeros', newFigure=True)
plot.qq(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.qq(df, 'lzjdSimilarity', 'hashLevenshtein', newFigure=True)
