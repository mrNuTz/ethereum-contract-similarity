import bz2
from util import discretize, sdFromMean

def bzCompRatio(bs: bytes):
  return len(bz2.compress(bs)) / len(bs) if len(bs) > 0 else 1

def hashFixedLen(bs:bytes, chunkLen=200, chunkRes=8) -> str:
  l = len(bs)
  if l == 0:
    return []
  pad = chunkLen - (l % chunkLen)
  l += pad
  bs += b'\x00' * pad
  res = [bzCompRatio(bs[i:i+chunkLen]) for i in range(0, l, chunkLen)]
  res = sdFromMean(res)
  return ''.join(chr(0xb0 + discretize(-2, 2, chunkRes, val)) for val in res)

def hashJumpi(bs:bytes, chunkRes=8) -> str:
  jumpi = b'\x57'
  res = [bzCompRatio(chunk) for chunk in bs.split(jumpi)]
  res = sdFromMean(res)
  return ''.join(chr(0xb0 + discretize(-2, 2, chunkRes, val)) for val in res)
