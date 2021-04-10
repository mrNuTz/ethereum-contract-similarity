from common import IdCodeTs
from contract.structure import decompose, skeletize

def firstSection(codes: IdCodeTs) -> IdCodeTs:
  return [(id, decompose(code)[0][1]) for id, code in codes]

def firstSectionSkeleton(codes: IdCodeTs) -> IdCodeTs:
  return [(id, skeletize(decompose(code)[:1])) for id, code in codes]

def skeleton(codes: IdCodeTs) -> IdCodeTs:
  return [(id, skeletize(decompose(code))) for id, code in codes]

def noOp(codes: IdCodeTs) -> IdCodeTs:
  return codes
