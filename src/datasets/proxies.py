import lzma, util, ast, re
from typing import Dict, List, NamedTuple, Set
from common import IdCodeT

class Meta(NamedTuple):
  id: int
  skeleton: int
  type: str
  signatures: Set[int]
  address: str

class Dataset(NamedTuple):
  idToCode: Dict[int, IdCodeT]
  idToMeta:  Dict[int, Meta]
  skeletonToIds: Dict[int, List[int]]

def load():
  res = Dataset({},{},{})

  def parseMeta(line):
    (id, skeleton,_type, signatures, address) = re.search('^([^,]*),([^,]*),([^,]*),("?\{[0-9,-]*\}"?),([^,]*),', line).groups()
    return Meta(int(id), int(skeleton), _type, ast.literal_eval(signatures), address)

  file = lzma.open('data/proxies/proxies.csv.xz', mode='rt')
  lines = iter(file)
  next(lines)
  for line in lines:
    line = line.rstrip('\n')
    meta = parseMeta(line)
    (bytecode,) = re.search(',([^,]+)$', line).groups()
    code = IdCodeT(meta.id, bytes.fromhex(util.drop0x(bytecode)))

    res.idToCode[meta.id] = code
    res.idToMeta[meta.id] = meta

    skels = res.skeletonToIds.get(meta.skeleton, [])
    skels.append(meta.id)
    res.skeletonToIds[meta.skeleton] = skels

  return res
