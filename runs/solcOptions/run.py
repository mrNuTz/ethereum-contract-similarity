import sys, os, re, random
from typing import Callable, NamedTuple
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, compare, util, vis, test, filter
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
  id: str
  group: str
  v: str
  abi: int
  o: bool
  runs: int

def parseMeta(id):
  (group, v, abi, o, runs) = re.search('(\S+) - (\S+) (\S+) (\S+) (\S+)', id).groups()
  return Meta(id, group, v[1:], int(abi[-1:]), o == 'o1', int(runs[4:]))

idToMeta = {
  id: parseMeta(id) for (id, code) in idToCode.values()
}

def byteBagJaccard(pairs):
  return compare.byteBagJaccard(pairs, excludeZeros=True)

def highFOnly(codes):
  return pre.filterBytes(codes, filter.highFStatPred)
def highF0(codes):
  return pre.setBytesZero(codes, filter.highFStatPred)

def run(metaPredicate: Callable[[Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].group for id, code in codes)}')
  print(f'codes len: {len(codes)}')
  print('')

  preToCodes = {
    'raw': codes,
    'skeletons': util.concurrent(pre.skeleton)(codes),
    'fstSecSkel': util.concurrent(pre.firstSectionSkeleton)(codes),
  }
  preToCodes.update({
    'fStat': util.concurrent(highFOnly)(preToCodes['fstSecSkel']),
    'fStat0': util.concurrent(highF0)(preToCodes['fstSecSkel']),
  })

  hashToFunction = {
    'ppdeep': hash.ppdeep,
    'ppdeep_mod': hash.ppdeep_mod,
    'byteBag': hash.byteBag,
    'lzjd': hash.lzjd1,
    'jump': hash.jumpHash,
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
    'byteBag': byteBagJaccard,
    'lzjd': compare.lzjd,
    'jump': compare.jump,
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
  separations = test.separation(df)

  write.saveCsv(separations.items(), filename=name + ' separations.csv')
  write.saveGml2((idToMeta[id] for id, code in codes), df, filename=name + '.gml')
  plot.saveScatter(df, 'raw lzjd', 'skeletons ppdeep_mod', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'skeletons ppdeep_mod', 'fstSecSkel jump', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'fStat0 ppdeep_mod', 'fStat ppdeep', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'fstSecSkel jump', 'fStat ppdeep', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'fStat0 ppdeep_mod', 'fstSecSkel jump', title=name + ' scatter', colorBy='isInner')
  plot.saveScatter(df, 'raw lzjd', 'fstSecSkel jump', title=name + ' scatter', colorBy='isInner')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

run(lambda m: m.o and m.runs == 200 and m.abi == 2, 'versions at o1 runs200 abi2')
run(lambda m: m.o and m.runs == 200 and m.v == '0.5.16' , 'abis at 0.5.16 o1 runs200')
run(lambda m: m.o and m.v == '0.8.4' and m.abi == 2, 'runs at 0.8.4 o1 abi2')
run(lambda m: True, 'all')
