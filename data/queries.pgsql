-- select encode(addr, 'hex') from account where id = 485783246;
-- bindata(cdeployed) as hex
-- select only code with distinct skeletons from es verified contracts and group by name + signatures

select
  code, encode(addr, 'hex') as addr, name,
  array_length(signatures, 1) as sigs, length(dat) as size
from
  esverifiedcontract
  join contract2 on esverifiedcontract.aid = contract2.aid
  join code2 on contract2.cdeployed = code2.code
  join account on account.id = esverifiedcontract.aid
  join bindata on bindata.id = code2.code
where
  array_length(signatures, 1) > 20
limit 5;


select
  count(*)
from
  esverifiedcontract
  join contract2 on esverifiedcontract.aid = contract2.aid
  join code2 on contract2.cdeployed = code2.code
  join account on account.id = esverifiedcontract.aid
  join bindata on bindata.id = code2.code
where
  array_length(signatures, 1) > 20;