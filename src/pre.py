from common import IdCodePairs
from contract.structure import decompose, skeletize

def firstSection(codes: IdCodePairs) -> IdCodePairs:
  return [(id, decompose(code)[0][1]) for id, code in codes]

def firstSectionSkeleton(codes: IdCodePairs) -> IdCodePairs:
  return [(id, skeletize(decompose(code)[:1])) for id, code in codes]

def skeleton(codes: IdCodePairs) -> IdCodePairs:
  return [(id, skeletize(decompose(code))) for id, code in codes]

def noOp(codes: IdCodePairs) -> IdCodePairs:
  return codes
