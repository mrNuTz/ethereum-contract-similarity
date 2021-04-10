from common import IdCodePair, IdCodePairs, IdIdFloatTriple, IdIdFloatTriples, IdStringPair, IdStringPairs
import hashes.ppdeep_mod
import hashes.ppdeep
import util

def _ppdeep_mod(pairs):
  return [ IdIdFloatTriple(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod(hashes: IdStringPairs) -> IdIdFloatTriples:
  incides = util.allToAllIndices(len(hashes))
  inputs = [ (hashes[i], hashes[j]) for i, j in incides ]
  return util.runParallel(_ppdeep_mod, inputs)

def _ppdeep_mod_jaccard(pairs):
  return [
    IdIdFloatTriple(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str, useJaccard=True))
    for a, b in pairs
  ]

def ppdeep_mod_jaccard(hashes: IdStringPairs) -> IdIdFloatTriples:
  incides = util.allToAllIndices(len(hashes))
  inputs = [ (hashes[i], hashes[j]) for i, j in incides ]
  return util.runParallel(_ppdeep_mod_jaccard, inputs)

def _ppdeep(pairs):
  return [ IdIdFloatTriple(a.id, b.id, hashes.ppdeep.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep(hashes: IdStringPairs) -> IdIdFloatTriples:
  incides = util.allToAllIndices(len(hashes))
  inputs = [ (hashes[i], hashes[j]) for i, j in incides ]
  return util.runParallel(_ppdeep, inputs)

def jaccardIndex(list1, list2) -> IdIdFloatTriple:
  a = set(list1)
  b = set(list2)
  aSize = len(a)
  bSize = len(b)
  intersectionSize = len(a.intersection(b))
  return intersectionSize / (aSize + bSize - intersectionSize)
