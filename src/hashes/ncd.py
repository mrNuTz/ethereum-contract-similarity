import lzma

_lzma_filters = [
  {
    "id": lzma.FILTER_LZMA2,
    "preset": 9 | lzma.PRESET_EXTREME,
    "dict_size": 40 * 1024, # a big enough dictionary, but not more than needed, saves memory
    "lc": 3,
    "lp": 0,
    "pb": 0, # assume ascii
    "mode": lzma.MODE_NORMAL,
    "nice_len": 273,
    "mf": lzma.MF_BT4
  }
]

def Z(contents: bytes) -> int:
  return len(lzma.compress(contents, format=lzma.FORMAT_RAW, filters=_lzma_filters))

def NCD(Za: int, Zb: int, a: bytes, b: bytes):
  Zab = Z(a + b)
  return (Zab - min(Za, Zb)) / max(Za, Zb)

def similarity(Za: int, Zb: int, a: bytes, b: bytes):
  return (Za + Zb - Z(a + b)) / max(Za, Zb)
