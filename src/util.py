import concurrent.futures
import math
from typing import List, Tuple, Callable, Dict
from datetime import datetime

def drop0x(hex):
 return (None if hex is None else hex[2:] if hex[0:2] == "0x" else hex)

def chunkList(list, n):
  return [ list[i : i + n] for i in range(0, len(list), n) ]

def allToAllPairs(list: List) -> List[Tuple]:
  length = len(list)
  return [ (list[i], list[j]) for i in range(0, length) for j in range(i + 1, length) ]

def allPairs(l1: List, l2: List) -> List[Tuple]:
  return [(a,b) for a in l1 for b in l2]

def allIntergroupPairs(groups: Dict[str, List[Tuple]]) -> Dict[Tuple[str, str], List[Tuple]]:
  return { (a,b): allPairs(groups[a], groups[b]) for a, b in allToAllPairs(list(groups)) }

def jaccardIndex(list1, list2):
  a = set(list1)
  b = set(list2)
  aSize = len(a)
  bSize = len(b)
  if (aSize + bSize) == 0:
    return 1
  intersectionSize = len(a.intersection(b))
  return intersectionSize / (aSize + bSize - intersectionSize)

CPU_COUNT = 48
_executor = concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT)

def runConcurrent(chunkFn: Callable[[List], List], inputs: List, chunkSizeMin=100, *args, **kwargs) -> List:
  chunkSize = max(chunkSizeMin, math.ceil(len(inputs) / CPU_COUNT))
  chunks = chunkList(inputs, chunkSize)

  outputs = []
  if (len(chunks) > 1):
    futures = [ _executor.submit(chunkFn, chunk, *args, **kwargs) for chunk in chunks ]
    for future in futures:
      outputs.extend(future.result())
  else:
    for chunk in chunks:
      outputs.extend(chunkFn(chunk, *args, **kwargs))
  return outputs

def concurrent(chunkFn: Callable[[List], List], chunkSizeMin=100) -> Callable[[List], List]:
  def go(inputs: List, *args, **kwargs):
    return runConcurrent(chunkFn, inputs, *args, **kwargs, chunkSizeMin=chunkSizeMin)
  return go

def normalize(mi, ma, resolution, val):
  span = ma - mi
  shifted = val - mi
  scaled = shifted * (resolution / span)
  return max(0, min(resolution - 1, int(scaled)))

def oneByteDebugEncoding(bs: bytes, startUtfCode=0xb0) -> str:
  return ''.join(chr(b + startUtfCode) for b in bs)

def timestamp() -> str:
  return datetime.now().strftime('%Y%m%d-%H%M%S')

def mapDict(d: Dict, fn: Callable, *args, **kwargs) -> Dict:
  return { k: fn(v, *args, **kwargs) for k, v in d.items() }

#def hotspot():
#  return
#
#def parallelize_dataframe(df, func, n_cores=4):
#  df_split = np.array_split(df, n_cores)
#  pool = Pool(n_cores)
#  df = pd.concat(pool.map(func, df_split))
#  pool.close()
#  pool.join()
#  return df

def readCsv(path, sep=',') -> List[List[str]]:
  file = open(path, mode='r')
  return [line.rstrip('\n').split(sep) for line in file]
