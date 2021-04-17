from common import IdStrT, IdCodeT
import base64 as _base64
import util
from typing import List

def hex(codes: List[IdCodeT]) -> List[IdStrT]:
  return [IdStrT(id, code.hex()) for id, code, in codes]

def base64(codes: List[IdCodeT]) -> List[IdStrT]:
  return [IdStrT(id, _base64.b64encode(code)) for id, code, in codes]

def oneByteDebugEncoding(codes: List[IdCodeT]) -> List[IdStrT]:
  return [IdStrT(t.id, util.oneByteDebugEncoding(t.code)) for t in codes]
