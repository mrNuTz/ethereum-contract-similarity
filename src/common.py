from typing import NamedTuple, List, Any, Dict

class IdCodeT(NamedTuple):
  id: int
  code: bytes

class IdStrT(NamedTuple):
  id: int
  str: str

class Id1Id2FloatT(NamedTuple):
  id1: int
  id2: int
  float: float

class IdSigsT(NamedTuple):
  id: int
  sigs: List[bytes]

class IdAnyT(NamedTuple):
  id: int
  any: Any

class IdCountsT(NamedTuple):
  id: int
  counts: Dict[int, int]
