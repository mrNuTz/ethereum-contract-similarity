import os, re
from typing import Dict, NamedTuple
from common import IdCodeT

class Meta(NamedTuple):
  id: str
  group: str
  v: str
  abi: int
  o: bool
  runs: int

class Dataset(NamedTuple):
  idToCode: Dict[int, IdCodeT]
  idToMeta:  Dict[int, Meta]

def load():
  def parseMeta(id):
    (group, v, abi, o, runs) = re.search('(\S+) - (\S+) (\S+) (\S+) (\S+)', id).groups()
    return Meta(id, group, v[1:], int(abi[-1:]), o == 'o1', int(runs[4:]))

  codeDir = 'data/many-solc-versions'
  idToCode = {
    (_id := filename.replace('.hex', '')): IdCodeT(
      _id,
      bytes.fromhex(open(f'{codeDir}/{filename}', mode='r').read()))
    for filename in os.listdir(codeDir)
  }
  idToMeta = {
    id: parseMeta(id) for (id, code) in idToCode.values()
  }

  return Dataset(idToCode, idToMeta)
