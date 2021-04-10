import concurrent.futures
import math

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

def allToAllIndices(length):
  return [ (i, j) for i in range(0, length) for j in range(i + 1, length) ]

CPU_COUNT = 48

_executor = concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT)

def runParallel(fn, inputs, chunkSizeMin=100):
  chunkSize = max(chunkSizeMin, math.ceil(len(inputs) / CPU_COUNT))
  chunks = chunkList(inputs, chunkSize)

  outputs = []
  if (len(chunks) > 1):
    futures = { _executor.submit(fn, chunk) for chunk in chunks }
    for future in concurrent.futures.as_completed(futures):
      outputs.extend(future.result())
  else:
    for chunk in chunks:
      outputs.extend(fn(chunk))
  return outputs
