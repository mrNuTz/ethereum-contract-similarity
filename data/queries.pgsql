-- verified contracts with minimum number of signatures
SELECT
  code,
  encode(addr, 'hex') AS addr,
  name,
  array_length(signatures, 1) AS sigs,
  length(dat) AS size
FROM
  esverifiedcontract
  JOIN contract2 ON esverifiedcontract.aid = contract2.aid
  JOIN code2 ON contract2.cdeployed = code2.code
  JOIN account ON account.id = esverifiedcontract.aid
  JOIN bindata ON bindata.id = code2.code
WHERE
  array_length(signatures, 1) > 20;

-- candidates.csv
-- count ... Anzahl der Contracts mit gleichem Namen und Signaturen
-- name ... Name
-- aids ... interne ids der Accounts
-- accounts ... Ethereum-Adressen dazu
SELECT
  count(es.aid),
  es.name,
  array_agg(es.aid) aids,
  array_agg(account (es.aid)) accounts
FROM
  esverifiedcontract es
  JOIN contract2 ct ON es.aid = ct.aid
  JOIN code2 c ON c.code = ct.cdeployed
GROUP BY
  es.name,
  c.signatures
HAVING
  count(DISTINCT c.skeleton) > 1;

-- candidate_codes.csv.
-- name ... Name des Contracts
-- addresses ... Liste von Ethereum-Adressen, wo überall derselbe code zu finden is
-- codeid ... interne Code id
-- code ... deployter bytecode
WITH sims AS (
  SELECT
    es.name,
    array_agg(DISTINCT ct.cdeployed) codes
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON c.code = ct.cdeployed
  GROUP BY
    es.name,
    c.signatures
  HAVING
    count(DISTINCT c.skeleton) > 1
)
SELECT
  sims.name,
  array_agg(account (ct.aid)) addresses,
  u.code codeid,
  bindata (u.code) code
FROM
  sims,
  unnest(sims.codes) u (code),
  contract2 ct
WHERE
  u.code = ct.cdeployed
  AND EXISTS (
    SELECT
    FROM
      esverifiedcontract es
    WHERE
      es.aid = ct.aid)
GROUP BY
  1,
  3,
  4;

