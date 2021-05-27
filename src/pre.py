from common import IdCodeT, IdAnyT, IdSigTblT
from contract.structure import decompose, skeletize
from typing import Callable, Any, List
from contract.fourbytes_tbl import signatureTbl as _signatureTbl

def firstSection(codes: List[IdCodeT]) -> List[IdCodeT]:
  return [IdCodeT(id, decompose(code)[0][1]) for id, code in codes]

def firstSectionSkeleton(codes: List[IdCodeT]) -> List[IdCodeT]:
  return [IdCodeT(id, skeletize(decompose(code)[:1])) for id, code in codes]

def skeleton(codes: List[IdCodeT]) -> List[IdCodeT]:
  return [IdCodeT(id, skeletize(decompose(code))) for id, code in codes]

def noOp(codes: List[IdCodeT]) -> List[IdCodeT]:
  return codes

def filterBytes(codes: List[IdCodeT], predicate: Callable[[int], bool]) -> List[IdCodeT]:
  return [IdCodeT(id, bytes(filter(predicate, code))) for id, code, in codes]

def setBytesZero(codes: List[IdCodeT], predicate: Callable[[int], bool]) -> List[IdCodeT]:
  return [IdCodeT(id, bytes(map(lambda b: b if predicate(b) else 0, code))) for id, code, in codes]

def mapCodes(codes: List[IdCodeT], fn: Callable[[IdCodeT], Any]) -> List[IdAnyT]:
  return [IdAnyT(t.id, fn(t)) for t in codes]

def signatureTbl(codes: List[IdCodeT]) -> List[IdSigTblT]:
  return [IdSigTblT(id, _signatureTbl(code)) for id, code in codes]
