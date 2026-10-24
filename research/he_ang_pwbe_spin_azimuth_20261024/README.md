# HE-ANG-PWBE-SPIN-AZIMUTH

상태: **R6·R7 PASS, 실제 finite 분석 PASS, C8 presentation PARTIAL, 독립 C9 PASS_SCOPED_SCIENCE_PRESENTATION_OPEN**. Root의 이론·계약을 보존하고 source·조사·기존 원장 참조 및 prescribed scalar reference/tests/분석/plot을 작성했다. Actual B1 양쪽 ACK와 R7 뒤 root GO로 네 child를 실행했다. 초기 12 PASS + targeted 2 PASS, G1–G6 분석 PASS를 보존하며 plot draw 실패 뒤 세 label만 정적으로 고쳤다. 추가 render는 하지 않았다.

## 선택한 작업과 baseline

Weigold FIAS-R-39 (June1978) Eqs19–20의 exact-swapped plane-wave Born exchange 진폭에 독립적으로 유도한 unpolarized spin trace와 relative-azimuth conditional law를 연결하는 단위다. Buică arXiv2306.08573v1 Eq46은 별도 spin-weight 교차 근거이며 BO exchange를 PWBE exchange와 혼합하지 않는다. 자세한 식과 물리 범위는 root 이론에 있다.

- Base: PR96 delivery `32f9227a9abef814bb009a87272c44be74941163`, tree `8cc5f2e029b8172231b6073e9817ef8cff42088b`.
- Target branch: `research/he-ang-pwbe-spin-azimuth-20261024` (아직 생성하지 않음).
- AGENTS: PR96 blob `8119a57e3c9f7b8c22a3532c9f88e430df1cebbf`.
- 최신 조사 중앙: `9f410bf0f4b5d14d1e6b7c17cd2e23a916f241c9`.

## source와 조사

`source/SOURCE_REPORT.md`는 root 원전 보고서의 exact copy다. `SOURCE_MANIFEST.json`에는 실제 본문 확인 URI·버전·PDF 크기/hash와 접근 공백을 남겼다. PDF·전체 추출문·페이지 이미지·raw web excerpts는 새 공개/백업 패키지에 넣지 않고 원전 URI와 hash로 복원한다. Weigold Table1은 OCR/시각 값 불일치 때문에 완전 전사되지 않았으며 **source 전사 데이터는 없다**. 이번 준비에서 source fitting이나 기존 TDCS/DDCS 재정규화를 수행하지 않았다.

`evidence/survey/`에는 7repo1326branches/860openPRs의 compact 상태와 실제 변경·read index·latest HEAD가 있다. 전체 compact inventory와 전체 backup 이름 목록은 Git에 pointer/hash만 남기고, 향후 B1 private supplement에 원본을 넣는다. 이전43docs는 중복 복사하지 않았다. Dropbox4901entries/9pages recursive metadata terminal, Drive1000cap partial을 구별한다. 알려진 B3가 direct metadata에 있으나 raw filter query0인 것은 connector coverage gap이다. REC133/중앙PR225는 실제 public refs로 검증했고 이전 출력·query self-echo는 새 근거에서 제외했다.

## 실행·검토·전달

`LOOP_PROGRESS.json`은 20단계 각각의 현재 근거를 기록한다. R1–R6 root 이론과 독립 PASS가 있으며 C1–C5 준비를 완료했다. Python scalar kernel은 Eqs1–12와 양성 variance form을 구현했다. 14개 targeted test method, G1–G6의 N64/256/1024/2048 독립 원전 진폭 quadrature, 저장 결과 3-panel plot, 새 ID bounded runner를 준비했다. Syntax-only compile5파일은 PASS이며 이 문장은 준비 시점의 syntax 확인이며, 이후 실제 test/analysis/plot 시도는 RESULTS_KO와 ledger에 기록했다. 새 distinct increment CPU8/wall30, planned3children/reserve1(2/10),512MiB/1thread를 고정했고 과거 repair 권한은 제거했다. B1 actual dual ACK/readback은 완료됐으며 publication과 B2/B3는 pending actual이다. 미래 PASS나 provider ACK를 기록하지 않는다.

PR96의 완료20stage와4child/reserve1, DDCS/CCC/HEANG contract/Hex/HE-X1/HE38/D10의 기존 비용·실패·unknown은 `evidence/REUSED_LEDGER_REFERENCES.json`의 기존 pinned 참조로 계승한다. 이전 예산을 초기화하거나 이번 단위에 전용하지 않는다. 이번 host 준비/문서 I/O 비용은 UNKNOWN_NOT_ZERO다.

전체 HE-ANG은 **SOURCE_INPUT_PENDING**이다. source-specific fixed-center PWBE 모형의 후속 검증과 source-qualified finite-mass/full joint physical provider의 의무를 구별한다. 이번 child는 analytic D/X와 continuous pointwise joint density의 **DERIVED_PWBE_MODEL_INPUT_AVAILABLE**을 제공한다. Conditional-phi law는 positive normalization domain에서 실제 finite tests/분석 및 독립 C9/root의 scoped admission을 받았다. 남은 물리 의무는 plane-wave 정확도/calibration, finite-mass recoil, consumer admission 및 required support/uncertainty다. Full-angle/energy sigma integral은 수행하지 않는다. 실제 독립 C9와 root의 scoped admission을 완료했다. 다음은 실제 Science S/C 게시와 B2, 후속 D/E/B3 전달이다. C8 figure/render/visual review는 OPEN이고 추가 child는 승인되지 않았다.

## GO 뒤 준비된 명령

아래는 원래 planned 명령이다. 실제 initial FAIL 뒤 root가 한정 two-method reserve를 승인했고 분석과 plot까지 각1회 실행했다. 현재 재실행하지 않는다. Exact commands/START/FINISH는 evidence/execution에 있다.

```bash
python3 -B code/run_bounded.py 01_tests
python3 -B code/run_bounded.py 02_azimuth_analysis
python3 -B code/run_bounded.py 03_plot
```

Periodic oracle는 production closed routine의 결과를 integrand로 쓰지 않는다. 독립 NumPy Cartesian q norm, raw source amplitude/nuclear subtraction, source transition prefactor와1/4+3/4 spin trace를 직접 평가한다. 실제 source Table1 전사값과 기존 데이터 fit은0개다.

## 현재 scoped 판정

`reviews/ROOT_ADMISSION.json`의 실제 판정은 **PASS_SCOPED_SCIENCE_PRESENTATION_OPEN**이다. Science S는20단계 assessed 중17complete/C8partial/R10+C10pending이며20/20완료가 아니다. C8의 정적 label수정은 NOT_RERENDERED로 유지하고 향후 실제 saved-output render/visual review를 별도 열린 의무로 남긴다. 현재 추가 child나 budget은 승인되지 않았다.
