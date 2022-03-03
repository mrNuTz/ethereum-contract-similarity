# Ethereum Smart Contract Similarity Hashing Toolkit

## Summary
- Toolkit for Ethereum Smart Contract similarity-measure evaluation and testing.
- Includes test-data and various similarity-measures.

## Setup
- This tool uses python [venv](https://docs.python.org/3/library/venv.html), get familiar with it
  at a basic level.
- Run the commands in `./setup.bat` from windows cmd, `./setup.ps1` from powershell or `setup.sh`
  from bash to initialize the venv and install the required python modules.

## Desc
For usage see runs/solcOptions and runs/wallets, they contain sample test runs.

hash.ncd and hash.jumpHash pre-filtered with opfilter.highFStatPred appear to perform the best.

ncd is Normalized Compression Distance, it works best on unfiltered Codes.

opfilter.highFStatPred is based on the data-set https://github.com/mrNuTz/solc-options-data-base
- opcodes with high f-statistic are selected
- same contracts compiled with different solc options and versions form the groups

jumpHash is a chunk hash
- split by JUMPI
- hash with sha1 and take the first byte
- map to a unicode character and concatenate
- compare via levenshtein
