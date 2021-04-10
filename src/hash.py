from common import IdCodeTs, IdStrTs, IdStrT, IdSigsTs, IdSigsT
import hashes.ppdeep_mod as _ppdeep_mod
import hashes.ppdeep as _ppdeep
from contract.fourbytes import signatures

def ppdeep_mod(codes: IdCodeTs) -> IdStrTs:
  return [IdStrT(id, _ppdeep_mod.hash(code)) for id, code in codes]

def ppdeep(codes: IdCodeTs) -> IdStrTs:
  return [IdStrT(id, _ppdeep.hash(code)) for id, code in codes]

def fourbytes(codes: IdCodeTs) -> IdSigsTs:
  return [IdSigsT(id, signatures(code)) for id, code in codes]
