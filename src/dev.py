
import db, pre, hash, compare, util, common, vis, out, plot
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
counts = util.runConcurrent(hash.countBytes, skel)
print('hashing4')
lzjd = util.runConcurrent(hash.lzjd1, skel)
print('hashing5')
sizes = util.runConcurrent(hash.size, skel)

print('pairs1')
hashPairs = util.allToAllPairs(hashes)
print('pairs2')
foursPairs = util.allToAllPairs(fours)
print('pairs3')
countsPairs = util.allToAllPairs(counts)
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
countsSimilarity = util.runConcurrent(compare.countsSimilarity, countsPairs, False)
print('compare5')
countsSimilarityNoZeros = util.runConcurrent(compare.countsSimilarity, countsPairs, True)
print('compare6')
lzjdSimilarity = util.runConcurrent(compare.lzjd, lzjdPairs)
print('compare7')
sizeDiff = util.runConcurrent(compare.sizeDiff, sizePairs)

print('correlate')
df = pd.DataFrame({
  'id1': [id1 for id1, id2, val in hashLevenshtein],
  'id2': [id2 for id1, id2, val in hashLevenshtein],
  'hashLevenshtein': [val for id1, id2, val in hashLevenshtein],
  'hashJaccard': [val for id1, id2, val in hashJaccard],
  'foursJaccard': [val for id1, id2, val in foursJaccard],
  'countsSimilarity': [val for id1, id2, val in countsSimilarity],
  'countsSimilarityNoZeros': [val for id1, id2, val in countsSimilarityNoZeros],
  'lzjdSimilarity': [val for id1, id2, val in lzjdSimilarity],
  'sizeDiff': [val for id1, id2, val in sizeDiff],
})
print('write')
corr = df.corr(method='kendall')
out.write_out(df.to_csv(), 'dataframe.csv')
out.write_out(corr, 'unique_sigs_len20')

print('plot')
plot.scatter(df, 'foursJaccard', 'hashLevenshtein', newFigure=True)
plot.scatter(df, 'foursJaccard', 'countsSimilarityNoZeros', newFigure=True)
plot.scatter(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.scatter(df, 'lzjdSimilarity', 'hashLevenshtein', newFigure=True)
plot.qq(df, 'foursJaccard', 'hashLevenshtein', newFigure=True)
plot.qq(df, 'foursJaccard', 'countsSimilarityNoZeros', newFigure=True)
plot.qq(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.qq(df, 'lzjdSimilarity', 'hashLevenshtein', newFigure=True)
