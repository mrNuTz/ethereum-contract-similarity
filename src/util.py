import concurrent.futures, math, os
import numpy as np
from typing import List, Tuple, Callable, Dict, TypeVar, Iterable
from datetime import datetime
T = TypeVar('T')
U = TypeVar('U')

def drop0x(hex):
 return (None if hex is None else hex[2:] if hex[0:2] == "0x" else hex)

def chunkList(list, n):
  return [ list[i : i + n] for i in range(0, len(list), n) ]

def allToAllPairs(list: List[T]) -> List[Tuple[T,T]]:
  length = len(list)
  return [ (list[i], list[j]) for i in range(0, length) for j in range(i + 1, length) ]

def allPairs(l1: List[T], l2: List[U]) -> List[Tuple[T,U]]:
  return [(a,b) for a in l1 for b in l2]

def allCrossGroupPairs(groups: Dict[str, List[Tuple[T]]]) -> Dict[Tuple[str, str], List[Tuple[T,T]]]:
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

def levenshteinDistance(s, t) -> int:
	'''
	Implementation by Christopher P. Matthews
	'''
	if s == t: return 0
	elif len(s) == 0: return len(t)
	elif len(t) == 0: return len(s)
	v0 = [None] * (len(t) + 1)
	v1 = [None] * (len(t) + 1)
	for i in range(len(v0)):
		v0[i] = i
	for i in range(len(s)):
		v1[0] = i + 1
		for j in range(len(t)):
			cost = 0 if s[i] == t[j] else 1
			v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
		for j in range(len(v0)):
			v0[j] = v1[j]
	return v1[len(t)]

CPU_COUNT = os.cpu_count()
_executor = concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT)

def concurrent(chunkFn: Callable[[List[T]], List[U]], chunkSizeMin=1) -> Callable[[List[T]], List[U]]:
  def go(inputs: List, *args, **kwargs):
    chunkSize = max(chunkSizeMin, math.ceil(len(inputs) / CPU_COUNT))
    chunks = chunkList(inputs, chunkSize)
    outputs = []
    if len(chunks) > 1:
      futures = [ _executor.submit(chunkFn, chunk, *args, **kwargs) for chunk in chunks ]
      for future in futures:
        outputs.extend(future.result())
    else:
      for chunk in chunks:
        outputs.extend(chunkFn(chunk, *args, **kwargs))
    return outputs
  return go

def discretize(mi, ma, resolution, val):
  span = ma - mi
  shifted = val - mi
  scaled = shifted * (resolution / span)
  return max(0, min(resolution - 1, int(scaled)))

def sdFromMean(x: Iterable) -> Iterable:
  x = np.fromiter(x, float)
  return (x - x.mean()) / x.std()

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

def fst(iterable: Iterable[T]) -> T:
  return next(iter(iterable))

def snd(iterable: Iterable[T]) -> T:
  i = iter(iterable)
  next(i)
  return next(i)
