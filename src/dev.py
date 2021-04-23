
import db, pre, hash, compare, util, common, vis, out
import contract.opcodes as opcodes
import pandas as pd

codes = db.selectIdCodeTs("""
WITH candidates AS (
  SELECT
    array_agg(DISTINCT ct.cdeployed) codes
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON c.code = ct.cdeployed
  GROUP BY
    es.name,
    c.signatures
  HAVING
    count(DISTINCT c.skeleton) > 1
    AND array_length(c.signatures, 1) = 19
)
SELECT
  u.code codeid,
  dat
FROM
  candidates,
  unnest(candidates.codes) u (code),
  contract2 ct,
  bindata b
WHERE
  b.id = u.code and
  u.code = ct.cdeployed
  AND EXISTS (
    SELECT
    FROM
      esverifiedcontract es
    WHERE
      es.aid = ct.aid)
GROUP BY
  1,
  2
LIMIT 1000;
""")

print(f'selected {len(codes)}')

print('pre')
skel = codes #util.runConcurrent(pre.firstSectionSkeleton, codes)

print('hashing1')
hashes = util.runConcurrent(hash.ppdeep_mod, skel)
print('hashing2')
fours = util.runConcurrent(hash.fourbytes, codes)
print('hashing3')
counts = util.runConcurrent(hash.countBytes, skel)
print('hashing4')
lzjd = util.runConcurrent(hash.lzjd1, skel)

print('pairs1')
hashPairs = util.allToAllPairs(hashes)
print('pairs2')
foursPairs = util.allToAllPairs(fours)
print('pairs3')
countsPairs = util.allToAllPairs(counts)
print('pairs4')
lzjdPairs = util.allToAllPairs(lzjd)


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

print('correlate')
df = pd.DataFrame({
  #'id1': [id1 for id1, id2, val in hashLevenstine],
  #'id2': [id2 for id1, id2, val in hashLevenstine],
  'hashLevenstine': [val for id1, id2, val in hashLevenstine],
  'hashJaccard': [val for id1, id2, val in hashJaccard],
  'foursJaccard': [val for id1, id2, val in foursJaccard],
  'countsSimilarity': [val for id1, id2, val in countsSimilarity],
  'countsSimilarityNoZeros': [val for id1, id2, val in countsSimilarityNoZeros],
  'lzjdSimilarity': [val for id1, id2, val in lzjdSimilarity]
})
print('write')
corr = df.corr(method='kendall')
out.write_out(corr, '19_full')
