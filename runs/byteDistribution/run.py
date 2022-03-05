# Calculate f-statistic on byte value counts using the many-solc-versions data-set with the codes
# compiled from the same source forming the groups.
import functools
import math
import sys, os
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, util
import contract.opcodes as opcodes
from scipy import stats
import numpy as np
import datasets.solcOptions as solcOptions

def main():
  idToCode, _, groupToIds = solcOptions.load()
  codes = list(idToCode.values())

  print('skeletize')
  skeletons = util.concurrent(pre.skeleton)(codes)

  print('byteBags')
  byteBags = util.concurrent(hash.byteBag)(skeletons)

  idToCounts = { id: counts for id, counts in byteBags }

  byteBagTotal = functools.reduce(
    lambda total, bag: { i: total.get(i,0) + bag.get(i,0) for i in range(1,256) },
    map(util.snd, byteBags),
    {})
  byteBagTotal = dict(sorted(byteBagTotal.items(), key=lambda item: -item[1]))
  totalByteCount = sum(byteBagTotal[i] for i in range(1,256))

  byteToGroupToCounts = {
    i: {
      group: [
        idToCounts[id].get(i, 0) for id in ids
      ] for (group, ids) in groupToIds.items()
    } for i in range(1, 256)
  }

  byteToF = util.mapDict(
    byteToGroupToCounts,
    lambda groupToCounts: stats.f_oneway(*groupToCounts.values()).statistic)
  byteToF = dict(sorted(byteToF.items(), key=lambda item:
    0 if math.isnan(item[1]) else -item[1]))

  byteToStats = util.mapDict(
    byteToGroupToCounts,
    lambda groupToCounts: stats.describe(list(c for l in groupToCounts.values() for c in l)))

  print('write')
  distFile = write.openFile('bytesDistribution.csv')
  distFile.write('op,dec,hex,count,percent\n')


  for byte in byteBagTotal.keys():
    distFile.write(f'{opcodes.opcode_by_value_or_missing(byte)},{byte:3d},0x{byte:02x},{byteBagTotal[byte]:7d},{byteBagTotal[byte] / totalByteCount:2.2%}\n')
  distFile.close()

  fFile = write.openFile('f-stat-by-byte.csv')
  fFile.write('op,dec,hex,min,max,mean,sd,f-stat\n')
  for (byte, f) in byteToF.items():
    s = byteToStats[byte]
    fFile.write(f'{opcodes.opcode_by_value_or_missing(byte)},{byte:3d},0x{byte:02x},{s.minmax[0]},{s.minmax[1]},{s.mean:.1f},{np.sqrt(s.variance):.1f},{f:.1f}\n')
  fFile.close()

if __name__ == '__main__':
  main()