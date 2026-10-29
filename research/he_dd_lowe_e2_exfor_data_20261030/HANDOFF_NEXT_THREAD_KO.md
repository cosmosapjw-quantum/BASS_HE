# BASS_HE HE-DD low-energy EXFOR E2 / window source-data next-thread handoff

$physmath-research-loop $scispace $exa $wolfram

PROJECT=cosmosapjw-quantum/BASS_HE
PARENT_PR=113
PARENT_HEAD=da989b83bb37ee4256a1a80ba9400dfe48559084
BRANCH=research/he-dd-lowE-e2-exfor-data-20261030
PR_NUMBER=READ_FRESH_REMOTE
CURRENT_HEAD=READ_FRESH_REMOTE
ROOT=research/he_dd_lowe_e2_exfor_data_20261030

CENTRAL_DAG=28/88
HE_PHYSICAL_DAG=14/18
PARENT_HIGH_E_ATLAS=2/2
NEW_LOW_E_SOURCE_DATA_DAG=3/4
PHYSICAL_COMPLETED_DELTA=0
THEORY_R=9/10
CODING_C=9/10
GIT_STAGE_PUBLICATION=20/20
GOOGLE_DRIVE_STAGE_ACK=20/20
DROPBOX_PAPER_STAGE_ACK=20/20
DISTINCT_AUTHOR_R6_C9=NOT_RUN
NATIVE_SUBAGENT=NOT_RUN

kappa=null
R_event=null
heat_rate=null
D_fast_pool=null
physical_activation=false
L4=false
production=HOLD

## Restore real source and scientific outputs
First read GitHub HEADs and verify PR113 parent SHA has not moved. Then read ROOT/THEORY_KO.md, REPORT_KO.md, DAG_DELTA.json, STAGE_LEDGER.json, SOURCE_MANIFEST.json, results/ORIGINAL_MULTI_EXFOR_PHYSICAL_ATLAS.json, results/RESULTS_SUMMARY.json and DELIVERY_RECEIPT.md. Read exact four raw sources ROOT/sources/{M0011,M0826,M0034,M0475}.x4. Their original IAEA-NDS/exfor_master commit is 939a14d7bba1ddce51975cb5e8711ce96b3b0871.

Four raw Git SHA-1 blobs and source SHA256 are pinned in SOURCE_MANIFEST.json and src/build_source_atlas.py. The original source files in this child tree, and the executable original Python generator, test and alternative C++ parser and plot script are all Git-blob identical to tested local copies:
Python src/build_source_atlas.py blob 5f6d9cc2ea78299df5d0030a0323b22ff31f25dc
Python tests/test_source_atlas.py blob 3763f21af67565df4571ed14720d49abb1e451d9
C++ tests/independent_cpp_source.cpp blob 2c7749c4790098b4cac318bb03c79478257ee4d9
Plot src/plot_sources.py blob 5e02126e3c0dfc1fdf0bbcda928670735a0415ce.

Run from ROOT in a fresh checkout:
  bash REPRODUCE.sh
This runs exact byte source checks, exact Fraction data generator, focused 35/35 unit tests, compileall, g++ C++100 independent 75-row source verifier, 4 measured-source plots. Local current-turn evidence: all these target checks pass. Not a broad repository/production solver IVP.

## Source physics
EXFOR exact selected same reaction code has 75 original rows, 57 newly acquired since parent. M0011: author point total SIG14 and electric E2 EP,SIG7 (COMMON POLAR=2 is multipolarity not beam polarization). M0826: four photon energy BINS and nine CM angular BINS, separate 5% photon intensity systematic. M0034: total14 and E2 9 curve digitizations, likely related Arkatov lineage to M0011, not independent unless methods prove it. M0475: parent M0475002 highE DA12, M0475003 highE total SIG6, **NO 330MeV measured total**.

Exact source-only E2 fractions within M0011 at photon E_gamma=26,28,30,32,34,36,38 MeV are 83/87,47/58,49/62,127/511,178/479,51/152,43/216. No original E2 covariance or experimental extraction independence confirmed. M0011 E32 E2=1.27±0.80microbarn while M0034 E32 curve digitization=2.72±0.52; do not claim new observed physical anomaly without original lineage and method audit.

At alpha-target rest frozen M_alpha*c²=3727.3794118MeV and m_deuteron*c²=1875.61294500MeV, Q=23.8464782MeV and recoil threshold=23.922758940396704688MeV. Source point SIG(E)*[E−Q] is an exact generated-pair kinetic-energy-weighted reported cross section, NOT a rate or heat. M0826 window sigmaK bounds require an explicit common positive window averaging assumption, and angular bins remain bins. Never fabricate bin-center measurement, correlated Gaussian confidence interval, or E330 measured total.

## Backups and DAG
Stage ledger has 20 actual Git stage commits and 20 actual Drive and 20 actual Dropbox Paper text log ACK, two ordered logs read back equal. Google Doc ID 14NneZCLk0EByTjyH4GN0Njlhkdh5WPnGqy3-mBvnS5Y, Dropbox Paper id:BSpOijBcT10AAAAAAEHV0Q. Text acknowledgement and local source ZIP SHA are NOT full ZIP byte restoration from both providers.
Data DAG D1 original 4 source byte lock COMPLETE, D2 same-source E2 ratio plus sigmaK COMPLETE, D3 angle/energy bins plus origin diagnostic COMPLETE_CONDITIONAL, D4 original E2-component/detector acceptance and covariance PENDING. Thus 3/4 data-scoped; Canonical Central28/88 HE14/18 physical progress delta0. Native distinct-author R6/C9 NOT_RUN.

## Next executable physics task, no new process-only meta cycle
Acquire 1972 Arkatov YF16,12; 1978 Arkatov UFZ23,918; 1980 Arkatov SNP31,157 full originals and Arends1976 PLB62,411 original detector counting/efficiency. Recover E2 multipole extraction and joint cross-observable covariance and source lineage, then attempt D4 source qualification. Next require true MeV photon history in proper He target frame and D_fast stopping/deposition and Cv before R_event/heat_rate can be physically activated. Do not replace this by existing REI Puchwein UVB ~eV photons, BASS_CR RR 13.6/24.59eV photons, source-conditional 5% acceptance hypothesis or a guessed 330 total SIG.
No merge, force push, old heavy IVP/full suite or unsupported physical DAG promotion.
