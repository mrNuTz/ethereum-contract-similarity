from typing import  List
from pandas.core.frame import DataFrame
from common import Id1Id2FloatT
import numpy as np

def separation(df: DataFrame):
  colToSeparation = {}
  cols = (c for c in df.columns if c not in ('isInner', 'id1', 'id2', 'group1', 'group2'))
  total = np.count_nonzero(df['isInner'].values)
  for col in cols:
    vals = df[[col, 'isInner']].values
    indices = np.flipud(np.argsort(vals[:, 0]))
    vals = vals[indices]
    correct = sum(1 for i in range(total) if vals[i][1])
    colToSeparation[col] = correct / total if total > 0 else np.nan
  return colToSeparation

def similarityMatrix(pairs: List[Id1Id2FloatT]) -> np.ndarray:
  # res = np.ndarray()
  return
