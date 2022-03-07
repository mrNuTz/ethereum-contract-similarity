# Ethereum contract similarity measure evaluation framework
## Summary
- Ethereum-Contract similarity-measure evaluation framework.
- Includes test-data, similarity-measures and tools for exploration and evaluation.

## Elevator Pitch
For usage see `./runs/solcOptions/` and `./runs/wallets/`, they contain sample test runs.

`hash.ncd` and `hash.jumpHash` pre-filtered with `opfilter.highFStatPred` appear to perform the best.

`ncd` is Normalized Compression Distance, it works best on unfiltered Codes.

`opfilter.highFStatPred` is based on the [solc-version-testset](https://github.com/mrNuTz/solc-version-testset)
- OP-Codes with high f-statistic are selected.
- Same contracts compiled with different solc options and versions form the groups.

`jumpHash` is a chunk hash:
1. Split by `JUMPI` into chunks.
1. Hash each chunk with `sha1`.
1. Map the first byte to a unicode character.
1. Concatenate the unicode characters to a hash-string.
1. Compare the hash-strings via levenshtein.

## Requirements
- install python3 with pip
- This tool uses python [venv](https://docs.python.org/3/library/venv.html).
  - Basically the venv needs to be active before running code and not active when working with other
  python code.
- Install the modules listed in `requirements.txt` into the `venv`.
  - Alternatively run the commands in `./setup.bat` from windows cmd, `./setup.ps1` from powershell or `setup.sh`
  from bash to initialize the venv and install the required python modules.

## Running Test-Runs
- The runs are at `./runs/*/run.py`
- Simply run python3 with active `venv` like `$ python3 runs/solcOptions/run.py`
- The results are stored at `./runs/*/out/*`.

## File tree
- `./data/` Test data.
- `./runs/` Individual test runs.
- `./src/` The evaluation framework code.

## Evaluation framework `./src`
- `./src/contract/` : [gsalzer/ethutils](https://github.com/gsalzer/ethutils) - EVM-Code definitions and decomposition.
  - `./src/contract/fourbytes.py` : Extract fourbyte signature.
  - `./src/contract/fourbytes_tbl.py` : Function Jump-table.
  - `./src/contract/opcodes.py` : EVM-OP-Codes definitions.
  - `./src/contract/structure.py` : Code decomposition and skeletonization.
- `./src/datasets/` : Import datasets.
  - `./src/datasets/proxies.py` : Import proxies dataset from `./data/proxies/`.
  - `./src/datasets/solcOptions.py` : Import solcOptions dataset from `./data/many-solc-versions/`.
  - `./src/datasets/wallets.py` : Import wallets dataset from `./data/wallets/`.
- `./src/hashes/` : Hash implementations.
  - `./src/hashes/bz.py` : BZ-Hash
  - `./src/hashes/jump.py` : JUMP-Hash
  - `./src/hashes/ncd.py` : Normalized Compression Distance
  - `./src/hashes/ppdeep.py` : ssdeep in pure python.
  - `./src/hashes/ppdeep_mod.py` : Modified ssdeep.
- `./src/common.py` : Type definitions.
- `./src/db.py` : Read codes from DB as types defined in `common.py`.
- `./src/hash.py` : Exports all hashes implemented in `hashes/`.
- `./src/opfilter.py` : OP-Code filter predicates.
- `./src/plot.py` : Plot functions (`scatter`).
- `./src/pre.py` : Code pre-processing (`skeleton`, `firstSection`)
- `./src/similarity.py` : Exports all similarity-measures.
- `./src/test.py` : Common test-run code (`separation` statistic).
- `./src/util.py` : Common static functions (`concurrent` list-precessing, `allPairs`).
- `./src/vis.py` : Code visualization (`hex`).
- `./src/write.py` : Save text files (`saveCsv`, `saveGml`).

## Data-sets `./data`
- `./data/wallets/` : Categorized wallet contracts.
- `./data/proxies/` : Categorized proxy contracts.
- `./data/many-solc-versions/` :
  [solc-versions-testset](https://github.com/mrNuTz/solc-version-testset) -
  Ethereum contracts compiled with different solc versions and options

## Test-runs `./runs`
- `./runs/byteDistribution/` : Calculates f-stat value for every OP-Code.
- `./runs/byteFiltersOnSolcVersions/` : Evaluate OP-Codes filters.
- `./runs/bzHash/` : Evaluate bzHash options.
- `./runs/fStatFilter/` : `opfilter.highFStatPred` on two contracts.
- `./runs/lzjdParams/` : Evaluate `lzjd` options.
- `./runs/many-solc-versions/` : Compare many similarity measures using [solc-versions-testset](https://github.com/mrNuTz/solc-version-testset).
- `./runs/proxies/` : Compare many similarity measures using `./data/proxies/`.
- `./runs/solcOptions/` : Compare many similarity measures using [solc-versions-testset](https://github.com/mrNuTz/solc-version-testset).
- `./runs/wallets/` : Compare many similarity measures using `./data/wallets/`.
