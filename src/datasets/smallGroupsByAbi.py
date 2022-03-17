import lzma, util
from typing import Dict, List, NamedTuple, Set
from common import IdCodeT

class Meta(NamedTuple):
  id: int
  name: str
  address: str

class Dataset(NamedTuple):
  idToCode: Dict[int, IdCodeT]
  idToMeta:  Dict[int, Meta]
  groupToIds: Dict[int, List[int]]

def load():
  idToCode: Dict[int, IdCodeT] = {}
  idToMeta:  Dict[int, Meta] = {}
  nameToIds: Dict[int, List[int]] = {}

  def parseMeta(row):
    (name, address, id, _) = row
    return Meta(int(id), name, address)

  file = lzma.open('data/smallGroupsByAbi/codes.csv.xz', mode='rt')
  lines = iter(file)
  next(lines)
  for line in lines:
    row = line.rstrip('\n').split(',')
    meta = parseMeta(row)
    (_, _, _, bytecode) = row
    code = IdCodeT(meta.id, bytes.fromhex(util.drop0x(bytecode)))

    idToCode[meta.id] = code
    idToMeta[meta.id] = meta

    if meta.name in nameToIds:
      nameToIds[meta.name].append(meta.id)
    else:
      nameToIds[meta.name] = [meta.id]

  return Dataset(idToCode, idToMeta, nameToIds)
