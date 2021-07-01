# compare preprocessing methods (raw code, skeleton, firstSectionSkeleton)

import sys, os, re, random
from typing import Callable, NamedTuple
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis, test
import contract.opcodes as opcodes
import pandas as pd
from common import Id1Id2FloatT, IdCodeT, IdFloatT, IdStrT

codeDir = 'data/many-solc-versions'
idToCode = {
  (_id := filename.replace('.hex', '')): IdCodeT(
    _id,
    bytes.fromhex(open(f'{codeDir}/{filename}', mode='r').read()))
  for filename in os.listdir(codeDir)
}

class Meta(NamedTuple):
  group: str
  v: str
  abi: int
  o: bool
  runs: int

def parseMeta(id):
  (group, v, abi, o, runs) = re.search('(\S+) - (\S+) (\S+) (\S+) (\S+)', id).groups()
  return Meta(group, v[1:], int(abi[-1:]), o == 'o1', int(runs[4:]))

idToMeta = {
  id: parseMeta(id) for (id, code) in idToCode.values()
}

def cheatHash(codes):
  return [ IdStrT(id, idToMeta[id].group) for id, code in codes ]
def cheatCompare(ps):
  return [
    Id1Id2FloatT(
      h1.id, h2.id,
      2 if h1.str == h2.str else 1)
    for h1, h2 in ps
  ]

def run(metaPredicate: Callable[[Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].group for id, code in codes)}')
  print(f'codes len: {len(codes)}')
  print('')

  preToCodes = {
    'raw': codes,
    'skeletons': util.concurrent(pre.skeleton)(codes),
    'firstSectionSkeletons': util.concurrent(pre.firstSectionSkeleton)(codes),
  }

  hashToFunction = {
    'ppdeep': hash.ppdeep,
    'ppdeep_mod': hash.ppdeep_mod,
    'byteBag': hash.byteBag,
    'lzjd': hash.lzjd1,
    'cheat': cheatHash
  }

  methodToHashes = {
    (p, h): util.concurrent(hashToFunction[h])(preToCodes[p])
    for p in preToCodes.keys() for h in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  hashToCompareFunction = {
    'ppdeep': compare.ppdeep,
    'ppdeep_mod': compare.ppdeep_mod,
    'byteBag': compare.byteBagJaccard,
    'lzjd': compare.lzjd,
    'cheat': cheatCompare
  }

  methodToComps = {
    method: util.concurrent(hashToCompareFunction[method[1]])(pairs)
    for (method, pairs) in methodToPairs.items()
  }

  comps1 = tuple(util.fst(methodToComps.values()))

  columns = {
    'isInner': (idToMeta[id1].group == idToMeta[id2].group for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].group for id1, id2, val in comps1),
    'group2': (idToMeta[id2].group for id1, id2, val in comps1),
  }
  columns.update({
    ' '.join(method): (val for id1, id2, val in comps)
    for method, comps in methodToComps.items()
  })

  df = pd.DataFrame(columns)
  corr = df.corr(method='kendall')

  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

run(lambda m: m.o and m.runs == 200 and m.abi == 2, 'versions at o1 runs200 abi2')
run(lambda m: m.o and m.runs == 200 and m.v == '0.5.16' , 'abis at 0.5.16 o1 runs200')
run(lambda m: m.o and m.v == '0.8.4' and m.abi == 2, 'runs at 0.8.4 o1 abi2')
run(lambda m: True, 'all')
