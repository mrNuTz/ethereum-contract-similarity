from common import IdStrT, IdSigsT, IdCodeT, IdCountsT
import hashes.ppdeep_mod as _ppdeep_mod
import hashes.ppdeep as _ppdeep
from contract.fourbytes import signatures
import functools
from typing import List

def ppdeep_mod(codes: List[IdCodeT]) -> List[IdStrT]:
  return [IdStrT(id, _ppdeep_mod.hash(code)) for id, code in codes]

def ppdeep(codes: List[IdCodeT]) -> List[IdStrT]:
  return [IdStrT(id, _ppdeep.hash(code)) for id, code in codes]

def fourbytes(codes: List[IdCodeT]) -> List[IdSigsT]:
  return [IdSigsT(id, signatures(code)) for id, code in codes]

def countBytes(codes: List[IdCodeT]) -> List[IdCountsT]:
  def reducer(counts, b):
    counts[b] = counts[b] + 1 if b in counts else 1
    return counts

  return [
    IdCountsT(id, functools.reduce(reducer, code, {}))
    for id, code in codes]
