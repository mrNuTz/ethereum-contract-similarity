import sys, os, itertools
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, vis, test, filter
import datasets.solcOptions as solcOptions

idToCode,_ = solcOptions.load()

codes = itertools.islice(idToCode.values(), 2)
codes = [ (id, skel) for id, skel in pre.firstSectionSkeleton(codes) ]
filtered = [ ('0 ' + id, code) for id, code in pre.setBytesZero(codes, filter.highFStatPred) ]
mangled = [ ('_ ' + id, code) for id, code in pre.filterBytes(codes, filter.highFStatPred) ]

codes = [*codes, *filtered, *mangled]
write.saveCsv([ (id, util.oneByteDebugEncoding(code)) for id, code in codes ], 'codes.csv')
hashes = hash.jumpHash(codes)
write.saveCsv(hashes, 'hashes.csv')
pairs = util.allToAllPairs(hashes)
sims = similarity.jump(pairs)
write.saveCsv(sims, 'sims.csv')
