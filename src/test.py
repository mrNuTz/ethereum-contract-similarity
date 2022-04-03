from typing import List
from pandas.core.frame import DataFrame
from common import Id1Id2FloatT
import numpy as np
import plot

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
  return dict(sorted(colToSeparation.items(), key=lambda item: -item[1]))

def similarityMatrix(pairs: List[Id1Id2FloatT]) -> np.ndarray:
  # res = np.ndarray()
  return

def saveHistogram(
  df, column, title='hist', filename=None, bins=10, range=(0, 1), alpha=1,
  density=True, **kwargs
):
  plot.saveHistogram(
    [df[df['isInner'] == False][column], df[df['isInner']][column]],
    title=f'{title} hist {column}',
    filename=filename,
    label=['cross group', 'same group'],
    bins=bins,
    range=range,
    alpha=alpha,
    density=density,
    #histtype='stepfilled',
    **kwargs)
