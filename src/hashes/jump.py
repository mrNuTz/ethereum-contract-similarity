from typing import List

from pyLZJD.lzjd import digest
from hashlib import sha1
import Levenshtein

def h(b: bytes) -> str:
  return chr(sha1(b).digest()[0] + 0xb0)

def hash(code: bytes) -> str:
  jumpi = b'\x57'
  chunks = code.split(jumpi)
  return ''.join(h(chunk) for chunk in chunks)

def similarity(a: str, b: str) -> float:
  return 1 - (Levenshtein.distance(a, b) / max(len(a), len(b)))
