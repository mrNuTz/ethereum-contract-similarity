
import db, pre, hash, compare, util, common, vis
import contract.opcodes as opcodes
import pandas as pd

codes = db.selectIdCodeTs("""
select
  code as id, dat as code
from
  esverifiedcontract
  join contract2 on esverifiedcontract.aid = contract2.aid
  join code2 on contract2.cdeployed = code2.code
  join account on account.id = esverifiedcontract.aid
  join bindata on bindata.id = code2.code
where
  array_length(signatures, 1) > 20
offset 10000
limit 500;
""") + db.selectIdCodeTs("""
select
  code as id, dat as code
from
  esverifiedcontract
  join contract2 on esverifiedcontract.aid = contract2.aid
  join code2 on contract2.cdeployed = code2.code
  join account on account.id = esverifiedcontract.aid
  join bindata on bindata.id = code2.code
where
  array_length(signatures, 1) > 20
offset 30000
limit 500;
""")

print('hashing1')
hashes = util.runConcurrent(hash.ppdeep_mod, codes)
print('hashing2')
fours = util.runConcurrent(hash.fourbytes, codes)
print('hashing3')
counts = util.runConcurrent(hash.countBytes, codes)
print('hashing4')
lzjd = util.runConcurrent(hash.lzjd1, codes)

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
print(df.corr(method='kendall'))
