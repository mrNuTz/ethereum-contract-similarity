from common import IdCodeT, IdCodeTs, Id1Id2FloatT, Id1Id2FloatTs, IdStrT, IdStrTs
import hashes.ppdeep_mod, hashes.ppdeep, util, math
from typing import Callable, Tuple, List

def concurrent(hashes: IdStrTs, comparePairsFn: Callable, *args, chunkSizeMin=100) -> Id1Id2FloatTs:
  pairs = util.allToAllPairs(hashes)
  return util.runConcurrent(comparePairsFn, pairs, *args, chunkSizeMin=chunkSizeMin)

def sequential(hashes: IdStrTs, comparePairsFn: Callable, *args, chunkSizeMin=None) -> Id1Id2FloatTs:
  pairs = util.allToAllPairs(hashes)
  return comparePairsFn(pairs, *args)

def ppdeep(pairs):
  return [ Id1Id2FloatT(a.id, b.id, hashes.ppdeep.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod(pairs):
  return [ Id1Id2FloatT(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod_jaccard(pairs):
  return [
    Id1Id2FloatT(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str, useJaccard=True))
    for a, b in pairs
  ]

def jaccardIndex(pairs, res = 100):
  return [
    Id1Id2FloatT(a[0], b[0], util.normalize(0, 1, res, util.jaccardIndex(a[1], b[1])))
    for a, b in pairs
  ]
