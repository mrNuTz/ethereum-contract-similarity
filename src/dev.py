import db, pre, hash, compare, util, common, vis
import contract.opcodes as opcodes

#print(hash.ppdeep_mod(codes))
#print(compare.ppdeep_mod(hash.ppdeep_mod(pre.firstSectionSkeleton(codes))))
#print(compare.ppdeep_mod_jaccard(hash.ppdeep_mod(pre.firstSectionSkeleton(codes))))
#print(hash.fourbytes(pre.firstSection(codes)))

foo = db.selectIdCodeTs("""
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
limit 1;
""")

for id, counts in hash.countBytes(pre.firstSectionSkeleton(foo)):
  for b, count in counts.items():
    print(f'0x{b:02x}: {count:4d}')
