from common import IdCodePairs, IdStringPairs, IdStringPair
import hashes.ppdeep_mod as _ppdeep_mod
import hashes.ppdeep as _ppdeep

def ppdeep_mod(codes: IdCodePairs) -> IdStringPairs:
  return [IdStringPair(id, _ppdeep_mod.hash(code)) for id, code in codes]

def ppdeep(codes: IdCodePairs) -> IdStringPairs:
  return [IdStringPair(id, _ppdeep.hash(code)) for id, code in codes]
