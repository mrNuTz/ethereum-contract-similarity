import os

runs = (
  'byteFiltersOnSolcVersions',
  'bzHash',
  'bzOnWallets',
  'fStatFilter',
  'lzjdParams',
  'many-solc-versions',
  'proxies',
  'smallGroupsByAbi',
  'solcOptions',
  'wallets',
  'walletsSubset',
)

for r in runs:
  print(f'python {r}.py')
  e = os.system(f"python {os.path.dirname(os.path.abspath(__file__))}/{r}/run.py")
  print(f'\n{r} -> {e}\n')
