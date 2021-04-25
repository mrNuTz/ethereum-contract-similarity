
import db, pre, hash, compare, util, common, vis, out, plot
import contract.opcodes as opcodes
import pandas as pd

codes = db.selectIdCodeTs("""
WITH ids AS (
  SELECT
    min(es.aid) aid,
    min(c.code) code
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON ct.cdeployed = c.code
  WHERE
    array_length(c.signatures, 1) = 20
  GROUP BY
    c.signatures
  HAVING
    count(es.aid) = 1
)
SELECT
  ids.code,
  b.dat
FROM
  ids
  JOIN bindata b ON ids.code = b.id
LIMIT 400;
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
hashLevenstine = util.runConcurrent(compare.ppdeep_mod, hashPairs)
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
  #'id1': [id1 for id1, id2, val in hashLevenstine],
  #'id2': [id2 for id1, id2, val in hashLevenstine],
  'hashLevenstine': [val for id1, id2, val in hashLevenstine],
  'hashJaccard': [val for id1, id2, val in hashJaccard],
  'foursJaccard': [val for id1, id2, val in foursJaccard],
  'countsSimilarity': [val for id1, id2, val in countsSimilarity],
  'countsSimilarityNoZeros': [val for id1, id2, val in countsSimilarityNoZeros],
  'lzjdSimilarity': [val for id1, id2, val in lzjdSimilarity],
  'sizeDiff': [val for id1, id2, val in sizeDiff],
})
print('write')
corr = df.corr(method='kendall')
out.write_out(corr, 'unique_sigs_len20')

print('plot')
plot.scatter(df, 'foursJaccard', 'hashLevenstine', newFigure=True)
plot.scatter(df, 'foursJaccard', 'countsSimilarityNoZeros', newFigure=True)
plot.scatter(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.scatter(df, 'lzjdSimilarity', 'hashJaccard', newFigure=True)
plot.qq(df, 'foursJaccard', 'hashLevenstine', newFigure=True)
plot.qq(df, 'foursJaccard', 'countsSimilarityNoZeros', newFigure=True)
plot.qq(df, 'foursJaccard', 'lzjdSimilarity', newFigure=True)
plot.qq(df, 'lzjdSimilarity', 'hashJaccard', newFigure=True)
