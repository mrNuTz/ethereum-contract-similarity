import math
from typing import List
from pandas.core.frame import DataFrame
from common import Id1Id2FloatT
import numpy as np
import plot
from scipy import stats

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

def overlap(df: DataFrame, bins=20):
  colToOverlap = {}
  cols = (c for c in df.columns if c not in ('isInner', 'id1', 'id2', 'group1', 'group2'))
  for col in cols:
    cross = df[col][df['isInner'] == False]
    same = df[col][df['isInner'] == True]

    cross = 1 - (stats.cumfreq(cross, numbins=bins, defaultreallimits=(0,1)).cumcount / len(cross))
    cross = np.concatenate(([1], cross[:-1]))
    same = stats.cumfreq(same, numbins=bins, defaultreallimits=(0,1)).cumcount / len(same)

    overlap = np.array([cross, same]).min(axis=0).sum() / bins
    colToOverlap[col] = overlap
  return dict(sorted(colToOverlap.items(), key=lambda item: item[1]))

def qDist(df: DataFrame):
  colToDist = {}
  cols = (c for c in df.columns if c not in ('isInner', 'id1', 'id2', 'group1', 'group2'))
  for col in cols:
    cross = df[col][df['isInner'] == False]
    same = df[col][df['isInner'] == True]
    cq1, cq2, cq3 = cross.quantile([.25, .5, .75])
    sq1, sq2, sq3 = same.quantile([.25, .5, .75])
    dist = 0
    if (sq2 - cq2) == 0:
      dist = 0
    elif (sq3 - sq1 + cq3 - cq1) == 0:
      dist = math.inf
    else:
      dist = (sq2 - cq2) / (sq2 - sq1 + cq3 - cq2)
    colToDist[col] = dist
  return dict(sorted(colToDist.items(), key=lambda item: -item[1]))

def similarityMatrix(pairs: List[Id1Id2FloatT]) -> np.ndarray:
  # res = np.ndarray()
  return

def saveHistogram(
  df, column, title=None, filename=None, bins=10, range=(0, 1), alpha=1,
  density=True, **kwargs
):
  plot.saveHistogram(
    (df[column][df['isInner'] == False], df[column][df['isInner'] == True]),
    title=f'{title} hist {column}' if title is not None else f'hist {column}',
    filename=filename,
    label=['cross group', 'same group'],
    bins=bins,
    range=range,
    alpha=alpha,
    density=density,
    #histtype='stepfilled',
    **kwargs)
