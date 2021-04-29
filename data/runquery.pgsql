with ids as (
  SELECT
    min(es.aid) aid,
    min(c.code) code,
    count(es.aid) count,
    c.skeleton
  FROM
    esverifiedcontract es
    JOIN contract2 ct ON es.aid = ct.aid
    JOIN code2 c ON ct.cdeployed = c.code
  WHERE
    --es.name = 'ADZbuzzCommunityToken'
    es.name = 'AdminUpgradeabilityProxy'
  GROUP BY
    c.skeleton
)
select
  --encode(a.addr, 'hex') address, count, (select count(*) from message where receiver = ids.aid)
  ids.code, b.dat
from
  ids
  join account a on a.id = ids.aid
  join bindata b on b.id = ids.code
where
  (select count(*) from message where receiver = ids.aid) > 0;
