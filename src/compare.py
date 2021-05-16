from common import Id1Id2FloatT, IdStrT, IdCountsT, IdAnyT, IdFloatT
import hashes.ppdeep_mod, hashes.ppdeep, util
from typing import Callable, Tuple, List
import pyLZJD

def ppdeep(pairs: List[Tuple[IdStrT, IdStrT]]) -> List[Id1Id2FloatT]:
  return [ Id1Id2FloatT(a.id, b.id, hashes.ppdeep.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod(pairs: List[Tuple[IdStrT, IdStrT]]) -> List[Id1Id2FloatT]:
  return [ Id1Id2FloatT(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod_jaccard(pairs: List[Tuple[IdStrT, IdStrT]]) -> List[Id1Id2FloatT]:
  return [
    Id1Id2FloatT(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str, useJaccard=True))
    for a, b in pairs
  ]

def jaccardIndex(pairs) -> List[Id1Id2FloatT]:
  return [
    Id1Id2FloatT(a[0], b[0], util.jaccardIndex(a[1], b[1]))
    for a, b in pairs
  ]

def byteBagJaccard(pairs: List[Tuple[IdCountsT, IdCountsT]], excludeZeros=False) -> List[Id1Id2FloatT]:
  """Return value in [0,1] where 1 is identical and 0 indicates no similarity."""
  r = range(1, 256) if excludeZeros else range(256)
  return [
    Id1Id2FloatT(
      a.id, b.id,
        sum(min(a.counts.get(i, 0), b.counts.get(i, 0)) for i in r)
        / sum(max(a.counts.get(i, 0), b.counts.get(i, 0)) for i in r))
    for a, b in pairs
  ]

def lzjd(pairs: List[Tuple[IdAnyT, IdAnyT]]) -> List[Id1Id2FloatT]:
  return [ Id1Id2FloatT(a.id, b.id, pyLZJD.sim(a.any, b.any)) for a, b in pairs]

def sizeSimilarity(pairs: List[Tuple[IdFloatT, IdFloatT]]) -> List[Id1Id2FloatT]:
  return [ Id1Id2FloatT(a.id, b.id, min(a.float, b.float) / max(a.float, b.float)) for a, b in pairs ]
