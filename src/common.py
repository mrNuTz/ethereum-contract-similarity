from typing import NamedTuple, List

class IdCodePair(NamedTuple):
  id: int
  code: bytes
IdCodePairs = List[IdCodePair]

class IdStringPair(NamedTuple):
  id: int
  str: str
IdStringPairs = List[IdStringPair]

class IdIdFloatTriple(NamedTuple):
  id1: int
  id2: int
  val: float
IdIdFloatTriples = List[IdIdFloatTriple]

class IdSignaturesPair(NamedTuple):
  id: int
  sigs: List[bytes]
IdSignaturesPairs = List[IdSignaturesPair]
