import concurrent.futures
import math
from typing import List, Tuple, Callable

def writeCsvRow(file, row, sep=';'):
  for i in range(0, len(row)):
    if i > 0:
      file.write(sep)
    file.write(str(row[i]))
    file.write('\n')

def drop0x(hex):
 return (None if hex is None else hex[2:] if hex[0:2] == "0x" else hex)

def chunkList(list, n):
  return [ list[i : i + n] for i in range(0, len(list), n) ]

def allToAllPairs(list: List) -> List[Tuple]:
  length = len(list)
  return [ (list[i], list[j]) for i in range(0, length) for j in range(i + 1, length) ]

def jaccardIndex(list1, list2):
  a = set(list1)
  b = set(list2)
  aSize = len(a)
  bSize = len(b)
  intersectionSize = len(a.intersection(b))
  return intersectionSize / (aSize + bSize - intersectionSize)

CPU_COUNT = 48
_executor = concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT)

def runConcurrent(chunkFn: Callable[[List], List], inputs: List, *args, chunkSizeMin=100) -> List:
  chunkSize = max(chunkSizeMin, math.ceil(len(inputs) / CPU_COUNT))
  chunks = chunkList(inputs, chunkSize)

  outputs = []
  if (len(chunks) > 1):
    futures = [ _executor.submit(chunkFn, chunk, *args) for chunk in chunks ]
    for future in futures:
      outputs.extend(future.result())
  else:
    for chunk in chunks:
      outputs.extend(chunkFn(chunk, *args))
  return outputs

def runSequential(chunkFn: Callable[[List], List], inputs: List, *args, chunkSizeMin=None) -> List:
  return chunkFn(inputs, *args)

def normalize(mi, ma, resolution, val):
  span = ma - mi
  shifted = val - mi
  scaled = shifted * (resolution / span)
  return max(0, min(resolution - 1, int(scaled)))

def oneByteDebugEncoding(bs: bytes, startUtfCode=0xb0) -> str:
  return ''.join(chr(b + startUtfCode) for b in bs)
