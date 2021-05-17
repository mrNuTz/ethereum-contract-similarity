from typing import NamedTuple, List, Any, Dict, Union

class IdCodeT(NamedTuple):
  id: Union[int,str]
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

class IdFloatT(NamedTuple):
  id: int
  float: float

class IdSigTblT(NamedTuple):
  id: int
  sigTbl: Dict[bytes, int]
