import psycopg2
import psycopg2.extras
from util import drop0x
from common import IdCodePairs

conn = psycopg2.connect('dbname=e user=rapha password=lilpeep@Hohenems')

def getCodesViaIds(codeIds) -> IdCodePairs:
  cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
  cur.execute('select id, dat as code from bindata where id = ANY(%s);', (codeIds,))
  return cur.fetchall()

def getCodesViaAccountIds(aid) -> IdCodePairs:
  cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
  cur.execute('select b.id, dat as code from bindata b, contract2 c where c.aid = any(%s) and c.cdeployed = b.id' , (aid,))
  return cur.fetchall()

def getCodesViaAddresses(address) -> IdCodePairs:
  cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
  address = [bytes.fromhex(drop0x(a)) for a in address]
  cur.execute("""select b.id, dat as code from bindata b, contract2 c, account a
    where a.addr = any(%s) and c.cdeployed = b.id and a.id = c.aid
    """ , (address,))
  return cur.fetchall()
