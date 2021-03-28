from common import IdCodePairs, IdStringPairs, IdStringPair
import hashes.ppdeep_mod as _ppdeep_mod

def ppdeep_mod(codes: IdCodePairs) -> IdStringPairs:
  return [IdStringPair(id, _ppdeep_mod.hash(code)) for id, code in codes]
