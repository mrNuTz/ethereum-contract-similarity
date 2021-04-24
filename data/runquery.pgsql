WITH ids AS (
  SELECT
    min(es.aid) aid,
    min(c.code) code
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON ct.cdeployed = c.code
  WHERE
    array_length(c.signatures, 1) = 20
  GROUP BY
    c.signatures
  HAVING
    count(es.aid) = 1
)
SELECT
  ids.code --, b.dat
FROM
  ids
  JOIN bindata b ON ids.code = b.id
LIMIT 400;

