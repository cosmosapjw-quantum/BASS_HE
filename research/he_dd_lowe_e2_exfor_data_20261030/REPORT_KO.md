# BASS_HE EXFOR 저에너지 E2 및 측정구간 물리 데이터 연구보고서 (2026-10-30)

실측 원본 네 개 M0011/M0826/M0034/M0475를 IAEA-NDS/exfor_master@939a14d7bba1ddce51975cb5e8711ce96b3b0871 고정 소스로 읽었다. 원본 정확 바이트, SHA256, Git blob을 재현했으며, 선택된 같은 핵반응 행은 총 75개(신규 57)다. 반드시 구분: M0011 저자표 21행, M0826 에너지구간·각도구간 13행, M0034 1980 논문 CURVE 편찬 23행, 기존 M0475 18행이다. 이는 독립 실험 75회의 의미가 아니다.

이번 결과: 실제 출처 M0011 안의 같은 E에서 전기사중극 E2 SIG/전체 SIG 7개 exact Fraction 비율 (83/87,47/58,49/62,127/511,178/479,51/152,43/216); 원본 점에 대해 frozen Q=23.84647820 MeV 적용한 정확한 생성 K_pair=E−Q, SIG(E)*K_pair와 각도별 DA(E,theta)*K_pair; M0826 구간 support를 올바르게 보존; M0011과 M0034 출처 근접성·비독립성과 원본 5% beam systematic를 provenance대로 분리했다. E2는 전기사중극 multipolarity이고 광자 입사빔 편광도가 아니다. 원문의 E2 분해 기법 및 공분산을 확인하지 않았으므로 가상 joint CI를 만들지 않았다. 원본 330 MeV total SIG 없음.

파일: sources/*.x4 원본 네 개, src/build_source_atlas.py 정확 유리수 계산과 source byte 검사, src/plot_sources.py 실측점/구간 출처 그림 4개, tests/test_source_atlas.py 35개, tests/independent_cpp_source.cpp, results/EXFOR_MULTI_SOURCE_ATLAS.json, CSV 두 개 및 provenance 결과, SOURCE_MANIFEST.json, DAG_DELTA.json, reproducible run script와 handoff. 실제 실행: Python35/35 PASS; C++100 독립 알고리즘 75/75행 및 E2 7개 PASS; Wolfram 7 exact fractions/threshold; plotted 4 figures inspected. Native distinct-author R6/C9 NOT_RUN.

DAG: 기존 Central28/88, HE physical14/18, 이전 highE atlas2/2는 변동 없음. 이번 독립 SOURCE DATA DAG D1 원본 바이트, D2 M0011 동일 E E2/total, D3 M0826 물리 구간 및 원전 계보 완료; D4 원전 수치추출·detector/covariance 공증 미완료. 따라서 scoped data3/4, canonical physical delta0. kappa=null,R_event=null,heat_rate=null,physical_activation=false,L4=false,production=HOLD.

다음: Arkatov1972/1978/1980 및 Arends1976 full original methods를 확보하여 E2 추출·같은 실험의 데이터 중복 여부, detector acceptance, counting을 검증. 수식 σK를 실제 event rate/heat로 승격하기 전에 cosmological MeV photon phase-space, proper helium target, nonthermal D_fast stopping and C_V source를 가져올 것. 이전 전체 solver IVP 및 4501LP 반복 미실행.
