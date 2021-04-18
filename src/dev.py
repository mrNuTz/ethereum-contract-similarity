import db, pre, hash, compare, util, common, vis
import contract.opcodes as opcodes

#print(hash.ppdeep_mod(codes))
#print(compare.ppdeep_mod(hash.ppdeep_mod(pre.firstSectionSkeleton(codes))))
#print(compare.ppdeep_mod_jaccard(hash.ppdeep_mod(pre.firstSectionSkeleton(codes))))
#print(hash.fourbytes(pre.firstSection(codes)))

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
offset 200
limit 6;
""")


hashes = util.runConcurrent(hash.ppdeep_mod, codes)
fours = util.runConcurrent(hash.fourbytes, codes)
counts = util.runConcurrent(hash.countBytes, codes)

hashPairs = util.allToAllPairs(hashes)

hashLevenstine = util.runConcurrent(compare.ppdeep_mod, hashPairs)
hashJaccard = util.runConcurrent(compare.ppdeep_mod_jaccard, hashPairs)
foursJaccard = util.runConcurrent(compare.jaccardIndex, util.allToAllPairs(fours))
countsSimilarity = util.runConcurrent(compare.countsSimilarity, util.allToAllPairs(counts), True)

print(hashLevenstine)
print(hashJaccard)
print(foursJaccard)
print(countsSimilarity)
