import lzma, util
from typing import Dict, List, NamedTuple, Set
from common import IdCodeT

class Meta(NamedTuple):
  id: int
  skeleton: int
  type: str
  address: str

class Dataset(NamedTuple):
  idToCode: Dict[int, IdCodeT]
  idToMeta:  Dict[int, Meta]
  groupToIds: Dict[int, List[int]]
  skeletonToIds: Dict[int, List[int]]
  fstIdPerSkel: Set[int]

def load():
  idToCode: Dict[int, IdCodeT] = {}
  idToMeta:  Dict[int, Meta] = {}
  skeletonToIds: Dict[int, List[int]] = {}
  typeToIds: Dict[int, List[int]] = {}
  fstIdPerSkel: Set[int] = {}

  def parseMeta(row):
    (id, skeleton, wType, address, _) = row
    return Meta(int(id), int(skeleton), wType, address)

  file = lzma.open('data/wallets/wallets.csv.xz', mode='rt')
  lines = iter(file)
  next(lines)
  for line in lines:
    row = line.rstrip('\n').split(',')
    meta = parseMeta(row)
    (_, _, _, _, bytecode) = row
    code = IdCodeT(meta.id, bytes.fromhex(util.drop0x(bytecode)))

    idToCode[meta.id] = code
    idToMeta[meta.id] = meta

    if meta.skeleton in skeletonToIds:
      skeletonToIds[meta.skeleton].append(meta.id)
    else:
      skeletonToIds[meta.skeleton] = [meta.id]

    if meta.type in typeToIds:
      typeToIds[meta.type].append(meta.id)
    else:
      typeToIds[meta.type] = [meta.id]

  fstIdPerSkel = { util.fst(ids) for skel, ids in skeletonToIds.items() }
  return Dataset(idToCode, idToMeta, typeToIds, skeletonToIds, fstIdPerSkel)
