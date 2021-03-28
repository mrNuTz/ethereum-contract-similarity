select encode(addr, 'hex') from account where id = 485783246;

select c.aid, e.name, cdeployed, bindata(cdeployed) as hex
from
  esverifiedcontract e
  join contract2 c on e.aid = c.aid
where cdeployed = 758253816;

SELECT * from esverifiedcontract limit 10;

-- select only code with distinct skeletons from es verified contracts and group by name + signatures
