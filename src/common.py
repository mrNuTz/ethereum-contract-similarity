from typing import NamedTuple, List

class IdCodeT(NamedTuple):
  id: int
  code: bytes
IdCodeTs = List[IdCodeT]

class IdStrT(NamedTuple):
  id: int
  str: str
IdStrTs = List[IdStrT]

class Id1Id2FloatT(NamedTuple):
  id1: int
  id2: int
  float: float
Id1Id2FloatTs = List[Id1Id2FloatT]

class IdSigsT(NamedTuple):
  id: int
  sigs: List[bytes]
IdSigsTs = List[IdSigsT]
