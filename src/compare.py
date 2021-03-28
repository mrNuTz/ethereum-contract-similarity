from common import IdCodePair, IdCodePairs, IdIdFloatTriple, IdStringPair
import hashes.ppdeep_mod
import util

def _ppdeep_mod(pairs):
  return [ IdIdFloatTriple(a.id, b.id, hashes.ppdeep_mod.compare(a.str, b.str)) for a, b in pairs ]

def ppdeep_mod(codes: IdCodePairs) -> IdIdFloatTriple:
  incides = util.allToAllIndices(len(codes))
  inputs = [ (codes[i], codes[j]) for i, j in incides ]
  return util.runParallel(_ppdeep_mod, inputs)
