WITH candidates AS (
  SELECT
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
    AND array_length(c.signatures, 1) = 20
)
SELECT
  u.code codeid,
  bindata (u.code) code
FROM
  candidates,
  unnest(candidates.codes) u (code),
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
  2;

