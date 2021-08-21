from typing import Dict, List

from pandas.core.frame import DataFrame
from common import Id1Id2FloatT
from util import fst
import numpy as np

def buildComparisonColumns(methodToGroupToComps: Dict[str, Dict[str, List[Id1Id2FloatT]]]):
  groupToComps = fst(methodToGroupToComps.values())
  comps = [t for comps in groupToComps.values() for t in comps]
  isCross = len(fst(groupToComps.keys())) == 2

  if isCross:
    group1 = (group1 for (group1, group2), comps in groupToComps.items() for t in comps)
    group2 = (group2 for (group1, group2), comps in groupToComps.items() for t in comps)
  else:
    group1 = [group for group, comps in groupToComps.items() for t in comps]
    group2 = group1

  columns = {
    'isInner': [not isCross] * len(comps),
    'id1': (id1 for id1, id2, val in comps),
    'id2': (id2 for id1, id2, val in comps),
    'group1': group1,
    'group2': group2,
  }
  columns.update({
    methodKey: (val for comps in groupToComps.values() for id1, id2, val in comps)
    for methodKey, groupToComps in methodToGroupToComps.items()
  })
  return columns

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
