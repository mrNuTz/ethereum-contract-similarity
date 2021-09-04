import sys, os, time
from typing import Callable
sys.path.insert(1, 'src')
import write, plot
_runDir = os.path.dirname(os.path.abspath(__file__))
_outDir = _runDir + '/out'
write.setDir(_outDir)
plot.setDir(_outDir)

import pre, hash, similarity, util, test, opfilter
import pandas as pd
import datasets.wallets as wallets

(idToCode, idToMeta, skeletonToIds, typeToIds, fstIdPerSkel) = wallets.load()
# typeToSkelCount = { t: sum(1 for id in ids if id in fstIdPerSkel) for t, ids in typeToIds.items() }

def byteBagJaccard(pairs):
  return similarity.byteBagJaccard(pairs, excludeZeros=True)
def highFOnly(codes):
  return pre.filterBytes(codes, opfilter.highFStatPred)
def highF0(codes):
  return pre.setBytesZero(codes, opfilter.highFStatPred)
def lzjd(codes):
  return hash.lzjd1(codes, hash_size=256, mode=None, false_seen_prob=0)

def run(metaPredicate: Callable[[wallets.Meta], bool], name: str):
  codes = [idToCode[id] for id, meta in idToMeta.items() if metaPredicate(meta)]

  print(name)
  print(f'groups: {set(idToMeta[id].type for id, code in codes)}')
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
    'lzjd': lzjd,
    'jump': hash.jumpHash,
    'ncd': hash.ncd,
    'fourbytes': hash.fourbytes
  }

  methodToHashes = {
    (p, h): util.concurrent(hashToFunction[h])(preToCodes[p])
    for p in preToCodes.keys() for h in hashToFunction.keys()
  }

  methodToPairs = {
    method: util.allToAllPairs(hashes) for method, hashes in methodToHashes.items()
  }

  hashToCompareFunction = {
    'ppdeep': similarity.ppdeep,
    'ppdeep_mod': similarity.ppdeep_mod,
    'byteBag': byteBagJaccard,
    'lzjd': similarity.lzjd,
    'jump': similarity.jump,
    'ncd': similarity.ncd,
    'fourbytes': similarity.jaccardIndex
  }

  methodToComps = {}
  methodToTime = {}
  for (method, pairs) in methodToPairs.items():
    print('comparing ' + name + ' ' + ' '.join(method))
    start = time.time()
    methodToComps[method] = util.concurrent(hashToCompareFunction[method[1]])(pairs)
    elapsed = time.time() - start
    methodToTime[method] = elapsed
    print(f"{elapsed} sec")

  comps1 = tuple(util.fst(methodToComps.values()))

  columns = {
    'isInner': (idToMeta[id1].type == idToMeta[id2].type for id1, id2, val in comps1),
    'id1': (id1 for id1, id2, val in comps1),
    'id2': (id2 for id1, id2, val in comps1),
    'group1': (idToMeta[id1].type for id1, id2, val in comps1),
    'group2': (idToMeta[id2].type for id1, id2, val in comps1),
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
  plot.saveScatter(df, 'raw ncd', 'fstSecSkel jump', title=name + ' scatter', colorBy='isInner')
  write.saveStr(df.to_csv(), name + ' similarities.csv')
  write.saveStr(corr.to_csv(), name + ' correlations.csv')

run(lambda m: m.id in fstIdPerSkel, 'all')
run(lambda m: m.id in fstIdPerSkel and m.type == 'multisig Gavin Wood/Ethereum/Parity', 'gavin')
run(lambda m: m.id in fstIdPerSkel and m.type == 'multisig Christian Lundkvist', 'lundkvist')
run(lambda m: m.id in fstIdPerSkel and m.type == 'multisig WalletSimple/BitGo forwarder', 'bitgo')
run(lambda m: m.id in fstIdPerSkel and m.type == 'smart GnosisSafe', 'gnosis')
