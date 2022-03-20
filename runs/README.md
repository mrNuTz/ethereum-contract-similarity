# Crude chronology of runs
## candidates evaluation scripts
- ppdeep_mod
  - remove score rounding to differentiate close-match/exact-match, low-score/incomparable
  - don't strip sequences because it makes most pairs incomparable
    - there are long sequences of K chunk-hashes in most hashes
- LZ BZ hash ideas
  - based on ImpHash
  - compression ratio for fixed length chunks
  - bz works better because of short chunks, lz compression is longer than input
- look at individual contracts, hashes, comparisons, segmentation, skeletons
- decompile skeletons
- check some basic statistics
  - number of sections
  - code length
  - opcode frequency

## [unique_sigs_len20](./unique_sigs_len20/)
### meta
- commit dbd159e3add701e040583e91334972a5dbcdc256 runs/byteFiltersOnSolcVersions
- first run
### run
- select 400 unique interfaces of size 20 signatures and get the fist code each
- compare fourbyte, ppdeep_levenshtein, ppdeep_jaccard, lzjd, bytebag, sizeSimilarity
### purpose and takeaways
- develop/test/change framework-functions
- plot scatters of comparison pairs to get a basic grasp of the results
- 1st basic performance indicator
  - evaluate measures by correlating to interface similarity
  - hashes don't look better than size-similarity so far
  - the hashes don't look better than bytebag so far
  - lzjd seams to correlate better to interfaces than ppdeep
  - bytebag: excluding zeros seams to be better
  - compare Levenshtein and Jaccard on ppdeep hashes
    - Levenshtein is better because the function are ordered by signature

## [AdminUpgradeabilityProxy](./AdminUpgradeabilityProxy/)
### meta
- commit dbd159e3add701e040583e91334972a5dbcdc256 runs/byteFiltersOnSolcVersions
- second run
### run
- select codes with unique skeletons from contracts named AdminUpgradeabilityProxy
- compare fourbyte, ppdeep_levenshtein, ppdeep_jaccard, lzjd, bytebag, sizeSimilarity
### purpose and takeaways
- more off the same
- ppdeep_mod remove common_substring detection to get more scores > 0


## [verifiedSameSignaturesDistinctSkeleton](./verifiedSameSignaturesDistinctSkeleton/)
### meta
- commit dbd159e3add701e040583e91334972a5dbcdc256 runs/byteFiltersOnSolcVersions
- third run
- first run with groups
### run
- manually select 5 contracts to form 5 groups
- for each group get codes with distinct skeleton and the same interface
- compare ppdeep, lzjd, bytebag, sizeSimilarity
### purpose and takeaways
- group by same interface
- check correlation within groups and cross groups
- 2nd basic performance indicator
  - check scatters to see if in-group-pairs and cross-groups-pairs are separated
- 3rd basic performance indicator
  - check correlation of pair-similarity-scores with isInner (is in-group or cross-group-comparison)
  - bytebag works better than ppdeep and lzjd on this dataset

## [many-solc-versions](./many-solc-versions/)
### meta
- commit dbd159e3add701e040583e91334972a5dbcdc256 runs/byteFiltersOnSolcVersions
### run
- form groups by contracts compiled with different solc versions
- start with just 5 contracts, not optimization options or abi encoding
- compare ppdeep, lzjd, bytebag, sizeSimilarity
### purpose and takeaways
- scatter
  - ppdeep better than lzjd
  - bytebag better than ppdeep **(&rarr;thesis)**
- isInner correlation
  - all the same

## [byteFiltersOnSolcVersions](./byteFiltersOnSolcVersions/)
### meta
- commit dbd159e3add701e040583e91334972a5dbcdc256 runs/byteFiltersOnSolcVersions
### run
- same as data as before
- test first basic opcode-filter
### purpose and takeaways
- scatter
  - lzjd: skel is better than filter
  - bytebag: filter is better than skel
  - ppdeep: filter better than skel
  - ppdeep filter: not worse than bytebag anymore
  - ppdeep: setting zero better than cutting out **(&rarr;thesis)**
- isInner and fourbyte correlations
  - useless &rarr; start thinking about different number

## add 4 more contracts to solc-versions (5 + 4 = 9)
### meta
- commit d850526f5764380dcdbad1f56a0550d26343a337 add more contracts to many-solc-versions
### purpose and takeaways
- scatter
  - filter: ppdeep finally better than bytebag
  - lzjd still worse than bytebag

## add optimization options to solc-versions-testset
### meta
- commit e18e6b01df1efbd3bc4969d9ad999ce1125f3649 data/many-solc-versions add optimizer variants
### purpose and takeaways
- scatter
  - optimization options cause bigger changes than solc-versions
  - all measures fall apart **(&rarr;thesis)** &rarr; better measures of filter needed &rarr; f-stat-filter

## cluster solc-versions-testset
### meta
- commit 7c0619eb6a8c6282eb38f312069d01811a4c1b8b byteFilterOnSolcVersions: save graph as gml
### purpose and takeaways
- bytebag alone produces nice clusters &rarr; dataset too small **(&rarr;thesis)**
- confirm previous interpretations: optimizations vs versions

## [byteDistribution](./byteDistribution/)
### meta
- commit 51864956b37231e27effcdc1dc17e842eee2078d runs/byteDistibutions:
### purpose and takeaways
- check opcode frequencies
- calc f-stat value for all opcodes to define better opcode-filter

## add another 4 contracts and abi encodings to solc-versions-testset (9 + 4 = 13)
### meta
- 4490b56fa018c0bacfd8bd9bc4a7cba03c1b0a53 solcOptions save scatter and gml
### purpose and takeaways
- get more meaningful results

## [solcOptions](./solcOptions/)
### meta
- 4490b56fa018c0bacfd8bd9bc4a7cba03c1b0a53 solcOptions save scatter and gml
### purpose and takeaways
- check robustness against abi, version, optimization separately

## [fStatFilter](./fStatFilter/)
### meta
- 7f419565253ca1874cedf389b56546b57c3c4db5 visualy check f-stat filtered code
### purpose and takeaways
- most bytes are filtered

## separation measure for similarity-measures performance
## jumpHash
## ncd
## [lzjdParams](./lzjdParams/)
## [bzHash](./bzHash/)
## [wallets](./wallets/)
## [proxies](./proxies/)
## [smallGroupsByAbi](./smallGroupsByAbi/)

