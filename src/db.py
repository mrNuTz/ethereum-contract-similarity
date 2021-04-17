import psycopg2
import psycopg2.extras
from util import drop0x
from common import IdCodeT
from typing import Tuple, List

conn = psycopg2.connect('dbname=e user=rapha password=lilpeep@Hohenems')

def getCodesViaIds(codeIds) -> List[IdCodeT]:
  cur = conn.cursor()
  cur.execute('select id, dat as code from bindata where id = ANY(%s);', (codeIds,))
  return [IdCodeT(r[0], bytes(r[1])) for r in cur.fetchall()]

def getCodesViaAccountIds(aid) -> List[IdCodeT]:
  cur = conn.cursor()
  cur.execute('select b.id, dat as code from bindata b, contract2 c where c.aid = any(%s) and c.cdeployed = b.id' , (aid,))
  return [IdCodeT(r[0], bytes(r[1])) for r in cur.fetchall()]

def getCodesViaAddresses(address) -> List[IdCodeT]:
  cur = conn.cursor()
  address = [bytes.fromhex(drop0x(a)) for a in address]
  cur.execute("""select b.id, dat as code from bindata b, contract2 c, account a
    where a.addr = any(%s) and c.cdeployed = b.id and a.id = c.aid
    """ , (address,))
  return [IdCodeT(r[0], bytes(r[1])) for r in cur.fetchall()]

def selectIdCodeTs(query: str, vars: Tuple = None) -> List[IdCodeT]:
  cur = conn.cursor()
  cur.execute(query, vars)
  return [IdCodeT(r[0], bytes(r[1])) for r in cur.fetchall()]
