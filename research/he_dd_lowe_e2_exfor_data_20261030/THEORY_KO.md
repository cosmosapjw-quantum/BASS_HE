# HE-DD | Source-locked low-energy EXFOR and E2 multipolarity research

2026-10-30. Parent BASS_HE Draft PR113 immutable HEAD da989b83bb37ee4256a1a80ba9400dfe48559084. New isolated add-only research. Scientific objective: real physical measured cross-section data, not another numerical-optimization study.

## Original source identity, measurement grain and independence

IAEA-NDS/exfor_master commit 939a14d7bba1ddce51975cb5e8711ce96b3b0871. Four raw original .x4 files, full SHA256, Git blob and sizes are locked to source manifest and code. 75 selected source rows, of which 57 are new relative to prior M0475. These are not 75 independent experiments.

- M0011 (Arkatov 1978, UFZ 23,918): M0011002 total SIG: 14 AUTHOR TABLE point energies 26 to 65 MeV, MICRO-B; M0011003 EP,SIG: 7 AUTHOR TABLE point energies 26,28,30,32,34,36,38 MeV, MICRO-B, COMMON POLAR 2. EXFOR EP indicates electric multipolarity E2, not incident photon-beam polarization.
- M0826 (Arkatov 1972 YF 16,12 / translated 1973): M0826002 total SIG: four source photon-energy BINS [30,40],[40,50],[50,60],[60,75] MeV, MICRO-B; M0826003 differential DA: nine 20-degree CM ANGLE BINS covering 0 to 180 degrees, COMMON incident photon energy [30,50] MeV, MU-B/SR, STATUS(CURVE). Original ERR-S statistical plus ERR-SYS photon intensity not higher than 5 percent. The 5% is not a measured detector acceptance uncertainty and cannot transfer to another experiment.
- M0034 (Arkatov 1980 SNP 31,157, compilation revised 2026-02-26): M0034005 total SIG14 and M0034006 E2 EP,SIG9, both STATUS(CURVE) figure digitizations. The other M0034002–4 are gamma-n/gamma-p channels, EXCLUDED. M0011/M0034 have related Arkatov provenance, and their independence is NOT established. Do not pool two sources as independent Gaussian campaigns.
- M0475 (Arends 1976 PLB62,411): preserved 12 DA (213,258,330 MeV × CM 46,61,73,87 deg) NB/SR; six SIG (201,225,253,285,320,359 MeV) NB. NO measured 330 MeV total SIG.

## Mathematical map directly tied to source

Metric (-,+,+,+), frozen parent PR104 rest energies M_alpha*c^2=3727.3794118 MeV and m_d*c^2=1875.61294500 MeV. Q=2m−M=23.84647820 MeV, lab photon threshold E_thr=Q+Q^2/(2M)=23.922758940396704688 MeV. Per exclusive gamma+He4→d+d event at target rest, K_plus+K_minus=E_gamma−Q. This angular-independent identity gives point-coordinate reported SIG(E)(E−Q), or reported DA(E,theta)(E−Q) with original source units and source ERR-S multiplied by the same nonrandom factor. These are experimental reported cross sections multiplied by birth kinetic energy, NOT heating rates, stopping rates, total event calibration or source photon flux.

Within the M0011 source only and EXACT MATCHING incident energies, nominal reported E2/total fractions:
26MeV 83/87 (0.954023), 28MeV 47/58 (0.810345), 30MeV 49/62 (0.790323), 32MeV 127/511 (0.248532), 34MeV 178/479 (0.371608), 36MeV 51/152 (0.335526), 38MeV 43/216 (0.199074). Their original total/E2 cross-covariance and E2 extraction method remain UNKNOWN. Do not manufacture confidence intervals by assuming statistical independence. At 26 MeV generated kinetic pair energy=2.1535218 MeV, reported total sigmaK=1.873563966 microbarn MeV, reported E2 sigmaK=1.787423094 microbarn MeV.

Provenance example: M0011 E32 reported E2 1.27±0.80 microbarn, but M0034 E32 curve digitization E2 2.72±0.52 microbarn; total values M0011 E32 5.11±0.71 and M0034 E32.2 5.20±0.66 microbarn. Differences in origin, detector analysis, digitization and E2 extraction are unresolved. This is a source lineage investigation, NOT a proven physical discrepancy or independent confirmation.

For M0826 photon-energy bins [a,b], assuming positive identical photon-energy averaging weights between published sigma_bar and a hypothetical sigma(E) (ASSUMPTION, not established instrument fact), positivity gives sigma_bar*(a−Q) ≤ weighted sigma(E)(E−Q) ≤ sigma_bar*(b−Q). These are CONDITIONAL support bounds, NOT measured bin center values. CM angular range observations are intervals; render midpoint only for visualization with horizontal interval whisker, never declare it a measured point.

## Verification and admission
Reproduced locally from exact 4 sources: Python3 targeted 35/35 PASS, compileall PASS; separate C++100 direct original source parser 75/75 rows with seven E2 ratio checks PASS; Wolfram exact rational ratios and recoil-correct threshold PASS; four source-data figures plotted, directly inspected. Source, code, test, C++ and figure generator readback Git blob byte-identity checked. Not an independently authored R6/C9 review; native-subagent NOT_RUN. Historical IVPs, full science suite, 4501-node LP NOT_RUN.

Original physical Central28/88, HE14/18 and prior high-energy data2/2 unchanged; new scoped low-energy data DAG D1-D3 COMPLETE, D4 original E2 extraction/efficiency/covariance PENDING = 3/4, physical delta0. kappa=null, R_event=null, heat_rate=null, D_fast_pool=null, physical_activation=false, L4=false, production=HOLD. Next actual objective: source-lock 1972/1978/1980 original Arkatov detector/E2 methods and Arends1976 event normalization; then source a real physical MeV photon distribution, target rest frame, D_fast stopping/deposition and C_V.
