
SELECT
  DISTINCT on (c.skeleton)
  es.aid,
  c.code,
  es.name,
  array_length(c.signatures, 1)
FROM
  esverifiedcontract es
  JOIN contract2 ct ON es.aid = ct.aid
  JOIN code2 c ON ct.cdeployed = c.code
  join account a on a.id = es.aid
WHERE
  a.addr = decode('9f8F72aA9304c8B593d555F12eF6589cC3A579A2', 'hex');
  --c.signatures = (SELECT c.signatures FROM code2 c WHERE c.code = 262134103);

SELECT
  DISTINCT ON (c.skeleton)
  c.code,
  length(b.dat),
  now()
FROM
  esverifiedcontract es
  JOIN contract2 ct ON es.aid = ct.aid
  JOIN code2 c on c.code = ct.cdeployed
  JOIN bindata b ON c.code = b.id
WHERE
  --abs(array_length(c.signatures,1) / (SELECT array_length(c.signatures, 1) FROM code2 c WHERE c.code = 242474230) - 1) < 0.05
  --and jaccard(c.signatures, (SELECT c.signatures FROM code2 c WHERE c.code = 242474230)) > 0.9;
  c.signatures = (SELECT c.signatures FROM code2 c WHERE c.code = 242637223);
