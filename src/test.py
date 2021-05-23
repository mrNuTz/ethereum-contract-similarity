from typing import Dict, List
from common import Id1Id2FloatT
from util import fst


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
