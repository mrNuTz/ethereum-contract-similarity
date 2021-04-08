import base64
import db
import pre
import hash
import compare
import util

codes = db.getCodesViaAddresses([
  '0x4d486b807c444238aaac55d685605cdf7a3dad36',
  '0xe492efdae10dd2ee3954f03c4416fac96bef0b5a',
  '0xbd11eae443ef0e96c1cc565db5c0b51f6c829c0b'
])

print(compare.ppdeep(hash.ppdeep(pre.noOp(codes))))
print(compare.ppdeep(hash.ppdeep(pre.firstSection(codes))))
print(compare.ppdeep(hash.ppdeep(pre.skeleton(codes))))
print(compare.ppdeep(hash.ppdeep(pre.firstSectionSkeleton(codes))))

print(compare.ppdeep_mod(hash.ppdeep_mod(pre.noOp(codes))))
print(compare.ppdeep_mod(hash.ppdeep_mod(pre.firstSection(codes))))
print(compare.ppdeep_mod(hash.ppdeep_mod(pre.skeleton(codes))))
print(compare.ppdeep_mod(hash.ppdeep_mod(pre.firstSectionSkeleton(codes))))
