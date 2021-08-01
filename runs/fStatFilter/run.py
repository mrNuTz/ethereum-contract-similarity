import sys, os, re, random
from typing import Callable, NamedTuple
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis, test, filter
import contract.opcodes as opcodes
import pandas as pd
from common import Id1Id2FloatT, IdCodeT, IdFloatT, IdStrT

codeDir = 'data/many-solc-versions'
idToCode = {
  (_id := filename.replace('.hex', '')): IdCodeT(
    _id,
    bytes.fromhex(open(f'{codeDir}/{filename}', mode='r').read()))
  for filename in os.listdir(codeDir)
}

codes = [util.fst(idToCode.values())]

codes = pre.firstSectionSkeleton(codes)

filtered = pre.setBytesZero(codes, filter.highFStatPred)
mangled = pre.filterBytes(codes, filter.highFStatPred)

print(util.oneByteDebugEncoding(util.fst(codes).code))
print()
print(util.oneByteDebugEncoding(util.fst(filtered).code))
print()
print(util.oneByteDebugEncoding(util.fst(mangled).code))
print()

hashes = hash.jumpHash([*codes, *filtered, *mangled])

for id, hash in hashes:
  print(hash)
  print()
