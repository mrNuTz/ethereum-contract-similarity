select
	code code_id,
        skeleton skeleton_id,
	wtype wallet_type,
	signatures interface,
	account(max(aid)) latest_deployment_address,
        bindata(code) bytecode
from
	proxy 
        natural join code2
        join contract2 on cdeployed=code
	natural left join wallet
group by 1,2,3,4,6
order by 2,3,1;

-- The \copy command for the CLI needs query in one line
\copy (select code code_id, skeleton skeleton_id, wtype wallet_type, signatures interface, account(max(aid)) latest_deployment_address, bindata(code) bytecode from proxy natural join code2 join contract2 on cdeployed=code natural left join wallet group by 1,2,3,4,6 order by 2,3,1) to 'proxies.csv' with csv header
-- COPY 8175

