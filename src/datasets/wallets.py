import lzma, util
from typing import Dict, List, NamedTuple
from common import IdCodeT

class Meta(NamedTuple):
  id: int
  skeleton: int
  type: str
  address: str

class Dataset(NamedTuple):
  idToCode: Dict[int, IdCodeT]
  idToMeta:  Dict[int, Meta]
  skeletonToIds: Dict[int, List[int]]

def load():
  res = Dataset({},{},{})

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

    res.idToCode[meta.id] = code
    res.idToMeta[meta.id] = meta

    skels = res.skeletonToIds.get(meta.skeleton, [])
    skels.append(meta.id)
    res.skeletonToIds[meta.skeleton] = skels

  return res
