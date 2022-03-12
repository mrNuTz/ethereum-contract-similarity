-- select groups
WITH groups1 AS (
  SELECT DISTINCT ON (es.name)
    es.name AS name,
    c.signatures AS sigs,
    array_agg((encode(a.addr, 'hex'), c.code, c.skeleton)) accounts
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON c.code = ct.cdeployed
    JOIN account a ON a.id = es.aid
  WHERE
    array_length(c.signatures, 1) BETWEEN 15 AND 25
  GROUP BY
    es.name,
    c.signatures
  HAVING
    count(DISTINCT c.skeleton) BETWEEN 5 AND 10
  ORDER BY
    es.name,
    c.signatures
),
groups2 AS (
  SELECT DISTINCT ON (sigs)
    name,
    accounts
  FROM
    groups1
  ORDER BY
    sigs
)
SELECT
  count(*)
FROM
  groups2;

-- expand groups
WITH groups1 AS (
  SELECT DISTINCT ON (es.name)
    es.name AS name,
    c.signatures AS sigs,
    array_agg((encode(a.addr, 'hex'), c.code, c.skeleton)) accounts
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON c.code = ct.cdeployed
    JOIN account a ON a.id = es.aid
  WHERE
    array_length(c.signatures, 1) BETWEEN 15 AND 25
  GROUP BY
    es.name,
    c.signatures
  HAVING
    count(DISTINCT c.skeleton) BETWEEN 5 AND 10
  ORDER BY
    es.name,
    c.signatures
),
groups2 AS (
  SELECT DISTINCT ON (sigs)
    name,
    accounts
  FROM
    groups1
  ORDER BY
    sigs
)
SELECT DISTINCT ON (name, skel)
  name,
  addr,
  code,
  encode(b.dat, 'hex') bin
FROM
  groups2,
  unnest(groups2.accounts) u (addr text,
    code int,
    skel int)
  JOIN bindata b ON b.id = code
ORDER BY
  name,
  skel,
  addr;

