import psycopg2
import psycopg2.extras
from util import drop0x
from common import IdCodePairs, IdCodePair
from typing import Tuple

conn = psycopg2.connect('dbname=e user=rapha password=lilpeep@Hohenems')

def getCodesViaIds(codeIds) -> IdCodePairs:
  cur = conn.cursor()
  cur.execute('select id, dat as code from bindata where id = ANY(%s);', (codeIds,))
  return [IdCodePair(r[0], bytes(r[1])) for r in cur.fetchall()]

def getCodesViaAccountIds(aid) -> IdCodePairs:
  cur = conn.cursor()
  cur.execute('select b.id, dat as code from bindata b, contract2 c where c.aid = any(%s) and c.cdeployed = b.id' , (aid,))
  return [IdCodePair(r[0], bytes(r[1])) for r in cur.fetchall()]

def getCodesViaAddresses(address) -> IdCodePairs:
  cur = conn.cursor()
  address = [bytes.fromhex(drop0x(a)) for a in address]
  cur.execute("""select b.id, dat as code from bindata b, contract2 c, account a
    where a.addr = any(%s) and c.cdeployed = b.id and a.id = c.aid
    """ , (address,))
  return [IdCodePair(r[0], bytes(r[1])) for r in cur.fetchall()]

def selectIdCodePairs(query: str, vars: Tuple = None) -> IdCodePairs:
  cur = conn.cursor()
  cur.execute(query, vars)
  return [IdCodePair(r[0], bytes(r[1])) for r in cur.fetchall()]
