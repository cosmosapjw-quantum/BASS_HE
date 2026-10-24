# PWBE 현재 인계 — scoped science admitted, presentation open

## 위치와 현재 결과

Repository: cosmosapjw-quantum/BASS_HE. Target branch: `research/he-ang-pwbe-spin-azimuth-20261024` (아직 생성·게시하지 않음). Base는 PR96 delivery `32f9227a9abef814bb009a87272c44be74941163`, tree `8cc5f2e029b8172231b6073e9817ef8cff42088b`다. 최신 조사 중앙 HEAD는 `9f410bf0f4b5d14d1e6b7c17cd2e23a916f241c9`이며, 실제 게시 전에 다시 확인한다.

이번 child의 기여는 **DERIVED_PWBE_MODEL_INPUT_AVAILABLE**이다. Weigold FIAS-R-39 Eqs19–20의 exact-swapped direct/exchange 진폭과 독립적으로 유도한 unpolarized spin trace를 연결해 continuous pointwise joint TDCS와 상대 방위각 조건부 법칙을 구성했다. 인쇄된 Eq21의 −2DX는 보존하며 unpolarized law로 채택하지 않았다. Buică의 BO exchange와 구별한다. Source Table1은 전사·사용하지 않았고 empirical fit도 수행하지 않았다.

R6는 실제 PASS, R7은 실제 evaluator 1회에서 10개 boolean이 True다. 새 bounded child는 네 번 실행했다. 초기 14 methods는 12 PASS/2 assertion FAIL, root의 한정 repair 뒤 해당 두 methods만 PASS, 여섯 geometry 분석은 PASS, plot의 첫 draw는 Mathtext 문법으로 FAIL했다. 최종 14 methods의 근거는 **초기 12 PASS + targeted 2 PASS**이며 전체 14를 다시 실행하지 않았다.

Root가 승인한 plot의 세 Mathtext label 수정만 정적으로 적용했다. 원본·diff·before/after hash는 `reviews/C8-PLOT-01_BEFORE/`에 있다. **NOT_RERENDERED**이며 추가 renderer/import/compile이나 다섯 번째 child는 없다. C8은 PARTIAL이고 실제 figure/render/visual review는 OPEN이다. 실제 C9와 root는 PASS_SCOPED_SCIENCE_PRESENTATION_OPEN을 채택했다. Science S는 20 stages assessed / 17 complete / C8 partial / R10+C10 publication pending으로 기록한다. 이후 실제 delivery D에서 19 complete / C8 partial을 기록하며 20/20 완료로 보고하지 않는다.

## 실제 수치·비용 근거

`RESULTS_KO.md`에는 저장된 `results/AZIMUTH_ANALYSIS.json`에서만 전사한 Kbar·cos(phi)·pair-dot 비교표가 있다. 독립 quadrature는 Cartesian q norm, raw source D/X 진폭, 두 nuclear subtraction, source transition prefactor와 1/4+3/4 spin trace를 직접 사용했다. Analytic closed routine을 integrand로 쓰지 않았다. G1–G6의 N64/256/1024/2048 기록과 최종 1e-10 기준을 유지했다.

네 child와 runner의 측정 누적은 CPU **1.966445초**, wall **2.079161265000039초**다. 새 allocation은 CPU8/wall30, reserve는 1회 사용/0회 잔여다. 초기 test FAIL과 plot FAIL을 포함했으며 cap 초과는 없다. Host/model/I/O와 remote 전체 CPU는 UNKNOWN_NOT_ZERO이고 end_to_end_cpu_cap_established=false다. 과거 비용·실패·unknown과 예산은 초기화하거나 전용하지 않았다. 이전 science·Wolfram 재실행, 새 IVP, full CCC/Hex solve, global angle/energy 적분, source fitting과 physical consumer activation은 수행하지 않았다.

## 실제 저장과 다음 전달

B1은 실제 dual upload와 별도 metadata readback을 완료했다. 210830 bytes, 37 members, local uploaded SHA256은 `4a3f1c5c2e9e7941d113c6217befcf51167eb0f0cb48c58bc0ab87d3652e8b49`다. Drive ID는 `1mkc6jKqa2trgI_5gjm1UV3DABSGTmrmu`, Dropbox ID는 `id:BSpOijBcT10AAAAAAD_9Zg`다. 실제 영수증은 `delivery/B1_BACKUP_ACK.json`에 있으며 independent remote SHA256은 검증하지 않았다. B1의 과거 PENDING/NOT_RUN 필드는 그 checkpoint 시점의 상태로 보존했다.

아직 Science S / Central C / Delivery D / Central E 게시와 B2/B3 ACK는 없다. 향후 B2는 실제 게시된 S/C bytes와 private context 원본을 포함한다. `pwbe_ops/PRIVATE_CONTEXT_RAW.json`을 `private_context/CONTEXT_RAW.json`으로 보존한다: 18454 bytes, SHA256 `36421a87bc4a41039613c85d6ee7ede4f561610dfaca9c4f724cf9b071ae2f74`. 이 context는 NOT_ADOPTED이며 공개 Git에는 ASSESSMENT의 pointer/hash만 둔다. Source PDF·전체 추출문·페이지 PNG·raw web excerpt는 공개와 백업 패키지에서 제외하고 원전 URI/hash로 복원한다. 전체 1326 branch/860 PR inventory와 root backup inventory는 private B1 supplement에 있고, Git에는 compact 선택·pointer만 둔다.

## 남은 의무와 다음 행동

Parent HE-ANG은 SOURCE_INPUT_PENDING, physical_provider_admitted=false를 유지한다. Analytic PWBE joint model input은 확보했으며 남은 의무는 plane-wave 물리 정확도/calibration, finite-mass recoil, consumer admission 및 required support/uncertainty다. Conditional law의 finite 실행 근거는 실제 C9/root의 scoped admission을 받았다. Full-angle/energy total sigma 적분은 수행하지 않았다.

다음은 root의 실제 Science S/C 게시, exact S/C B2 ACK와 후속 D/E/B3 전달이다. 현재 추가 renderer나 child는 승인되지 않았다. Root가 expected-SHA/nonforce additive draft 게시와 실제 checkpoint 전달을 수행하며 merge/activation하지 않는다. C9-NB-01, C23E, 다른 owner의 OPEN/scoped 상태, REC PR225의 별도 unmerged observation, PHYS86 실제1099/1099, PHYS85 incomplete raw, PHYS84 WAIT, ANGTHERM02 READ_ONLY를 보존한다.
