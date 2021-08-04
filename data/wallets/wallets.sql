select
	code code_id,
	skeleton skeleton_id,
	wtype wallet_type,
	account(max(aid)) latest_deployment_address,
	bindata(code) bytecode
from
	wallet
	natural join contract2
	join code2 on code=cdeployed
where
	not exists(select from proxy where proxy.skeleton = code2.skeleton)
group by 1,2,3,5
order by 3,2,1;

-- The \copy command for the CLI needs query in one line
\copy (select code code_id, skeleton skeleton_id, wtype wallet_type, account(max(aid)) latest_deployment_address, bindata(code) bytecode from wallet natural join contract2 join code2 on code=cdeployed where not exists(select from proxy where proxy.skeleton = code2.skeleton) group by 1,2,3,5 order by 3,2,1) to 'wallets.csv' with csv header
-- COPY 2013
