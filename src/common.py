from typing import NamedTuple, List, Any, Dict, Union

IdT = Union[int, str]

class IdCodeT(NamedTuple):
  id: IdT
  code: bytes

class IdStrT(NamedTuple):
  id: IdT
  str: str

class Id1Id2FloatT(NamedTuple):
  id1: IdT
  id2: IdT
  float: float

class IdSigsT(NamedTuple):
  id: IdT
  sigs: List[bytes]

class IdAnyT(NamedTuple):
  id: IdT
  any: Any

class IdLzjdT(NamedTuple):
  id: IdT
  lzjd: Any

class IdCountsT(NamedTuple):
  id: IdT
  counts: Dict[int, int]

class IdFloatT(NamedTuple):
  id: IdT
  float: float

class IdSigTblT(NamedTuple):
  id: IdT
  sigTbl: Dict[bytes, int]

class IdCodeZT(NamedTuple):
  id: IdT
  code: bytes
  z: int

class IdIntsT(NamedTuple):
  id: IdT
  ints: List[int]
