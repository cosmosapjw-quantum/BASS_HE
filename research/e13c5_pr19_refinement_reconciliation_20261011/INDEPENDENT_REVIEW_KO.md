# BASS_HE E13C5 독립 판정

## 판정과 범위

**PASS_SCOPED — open blocking finding 0개.** OFF node 0과 700의 세 captured segment씩, 네 실제 seam을 연결한 조건부 enclosure를 해당 범위에서 채택할 수 있다. 이 판정은 `PLAN.json`의 fixed gas·branch·mask·energy-anchor 정의와 exact binary64 lift, 검토한 interval arithmetic 및 saved input identity에 조건부다. 전체 spectral aggregate, coupled gas history 또는 production 물리 모델을 승격하지 않는다.

**외부 lineage admission은 별도로 `HOLD_PENDING_RECONCILIATION`이다.** 검토 종료 직전에 owner가 다른 recovery/first2/pilot publication 영수증을 발견했다고 알렸다. Reviewer는 그 원문을 아직 읽지 않았으므로 전역 최신 E13C5, 다른 branch보다 앞선 연구 순서 또는 중복 없는 publication을 확인하지 않는다. 이 항목은 현재 두 track의 수학적 판정과 분리하며 owner의 실제 receipt/branch 조사가 끝날 때까지 외부 통합 순서를 확정하지 않는다.

검토자는 `/root/e13c5_independent_review`다. Candidate 이론·구현·실험 acceptance 설계 및 contributor control 작성에 참여하지 않았다. 별도 context에서 고정된 코드, 입력, 원 실행 결과, 유도, 검산 및 인계 계약을 읽었다. Reviewer가 직접 작성·실행한 코드는 저장 N512/P60 결과의 정확 유리수 감사뿐이다. 공유한 captured 데이터와 local interval을 독립 물리 데이터나 새로운 원자 모델로 표현하지 않는다.

실행 모델과 physmath router를 확인하고 GPT-6 Astra research/coding v4.0.0의 시작 문서, core, 독립 검토·수학 검증 phase를 읽었다. 빈 harness template은 이전 연구 결과로 사용하지 않았다. Git intake base `8fc3fb14dd33da10efa86c97c4beb9b0d12eeaad`는 owner가 제공한 문맥이다. Reviewer가 remote HEAD를 다시 조회한 것은 아니다. 실제 읽은 파일과 SHA-256, 읽기 범위는 `evidence/review/READ_FILE_IDENTITIES.json` 및 `INDEPENDENT_REVIEW.json`에 고정한다.

## 핵심 수학 및 구현 검토

### 1. Incoming 오차의 정의와 서로 다른 gain

`THEORY.md`의 \(e=P-F\), \(e'+\Lambda e=r\), \(e_1'+Le_1=r\), \(e_1(0)=c\) 정의에서 출발한다. 비음수 opacity와 frozen photon stock에 대해

\[
\|e\|_\infty\le |c|+\eta+B_r
\]

가 성립하고, 코드의 `S_upper`는 이 세 항의 외향 상계다. 새로운 incoming 때문에 생기는 coefficient-variation 항을 zero-incoming remainder로 잘못 읽지 않았다. 임의의 고정된 O(1) incoming에서는 remainder 일부가 coefficient variation에 선형일 수 있다는 제한도 이론 문서에 있다.

Photon endpoint의 gain은 \(W=e^{-Lh}\), total count의 gain은 \(1-W\)다. 따라서 incoming 불확실성이 있으면 \(R_P+R_{A,\mathrm{tot}}=\delta_a\)이며 두 remainder가 서로 정확히 반대라는 E13C4의 local0 관계를 그대로 복사할 수 없다. `frozen_outputs_and_gains`와 `remainder_bounds`는 각 species/count/energy/heat/redshift gain을 따로 사용한다. Total absorbed energy에도 \(g_B\eta\)를 먼저 더한 뒤 coefficient remainder의 유효한 두 상계 중 작은 것을 적용한다.

종별 effective kernel과 total heat의 결합 kernel을 보존한다. Total opacity cancellation만으로 species 또는 heat를 인증하는 shortcut이 없다. Source number/energy의 coefficient truncation remainder는 정확히 0이지만, 적분 interval의 수치 반경과 native representation은 계속 포함한다.

### 2. Native 표현과 energy stock

각 output의 후보 interval에 `exact_frozen − captured`를 같은 부호로 더한다. 다음 incoming은 이미 이 표현 차이를 포함한 native photon correction에 `n_prev − f0_next`를 더한 값이다. 실제 네 seam의 captured photon/time/coordinate/weight 연속성과 여섯 row/stage의 원본 CSV 일치를 직접 확인했다. 첫 두 track 시작만 incoming 0이며 후속 네 segment의 중심과 반경을 다시 초기화하지 않는다.

Energy stock은 \(E_h\rho_P\) 하나로 바꾸지 않는다. 코드가 실제 사용하는 표현 항은

\[
\rho_U=E_hF_h-u_{\mathrm{cap}}/\epsilon
\]

이며, \(E_hn-u_{\mathrm{cap}}/\epsilon\)의 별도 차이를 포함한다. 여섯 저장 stock residual interval 모두 비영이다. Captured erg를 eV로 바꾸는 divisor는 상속된 binary64 \(1.602176634\times10^{-12}\)의 exact lift다. Reviewer의 Fraction 검산은 이 변환을 유리수로 직접 재구성했다.

현재 moment baseline은 captured segment increment의 **정확한 실수 합**이다. 이를 native weighted spectral reduction의 결과와 동일시하지 않는다. Native 장부 자체의 residual을 correction 장부에 억지로 0으로 강제하는 코드도 없다.

### 3. Signed anchor와 누적 반경

\(\Delta E=E_{\mathrm{next},0}-E_{\mathrm{prev},h}\)의 부호를 보존하고 \(\Delta E\,[c-\eta,c+\eta]\)를 직접 interval 곱으로 계산한다. 따라서 두 불확실성의 교차항이 빠지지 않는다. 네 seam의 ΔE는 모두 0을 포함하지 않으며 양수 두 개, 음수 두 개다. `anchored` flag가 0인 경우도 energy seam을 버리지 않는다.

합성 energy ledger는

\[
U_f-U_i+\sum(B+Z-Q_E)-\sum\Delta E\,P=0
\]

의 **anchor 차감 부호**를 사용한다. Native photon anchor와 correction anchor의 분할을 함께 기록하며 stock 표현 차이를 heat 또는 redshift에 흡수하지 않는다.

과거 누적 moment 반경은 감쇠하지 않고 새 반경에 더한다. 중심 덧셈에서 생기는 유한 precision 차이도 외향 반경에 들어간다. 각 local firstvariation·frozen 장부와 마지막 true number/energy/heat 장부의 일관성을 확인했다. Ledger가 0을 포함한다는 사실만으로 output enclosure의 타당성을 주장하지 않는다.

### 4. Local interval 재사용과 arithmetic 조건

`directed_interval.py`, `local_enclosure.py`, `run_recorded.py`는 실제 선행 E13C4 파일과 byte-identical이다. 선행 independent review의 채택 범위를 확인했으며, 변경되지 않은 primitive 전체 suite나 old continuous/native/gas solver를 다시 실행하지 않았다.

두 reused local control의 row/stage/mask/source 정의, 동일 N/precision, signed integral, variation bound, midpoint enclosure/radius, derivative 및 domain 기록이 각각의 E13C4 저장값과 일치한다. 나머지 네 control은 새 whole-cell Jet2 및 midpoint 평가를 수행한다. E13C5는 reference 비교 필드를 enclosure 근거로 사용하지 않는다.

표준 interval 연산의 포함관계, whole-cell positive domain, midpoint의 \(hM_j/(24N^3)\) 상계, variation kernel의 절댓값 적분이 함께 근거가 된다. 유효한 반경을 얻는 과정에서 통계적 confidence interval이나 observed refinement gap을 proof로 바꾸지 않았다. 이 판정은 문서화된 CPython Decimal 동작과 검토한 interval 구현에 의존하며 runtime의 proof-assistant 검증을 뜻하지 않는다.

## 실제 실행과 별도 검산

검토한 네 scientific run은 모두 실제 exit 0이며 시작·결과·wrapper 기록의 source/input SHA가 현재 고정된 bytes와 일치한다. 모든 primary/control run은 직렬이다.

| 실행 | Kernel elapsed [s] | Peak RSS [KiB] | 새 coefficient 평가 |
|---|---:|---:|---:|
| N32/P60 | 1.120043743 | 17272 | 256 |
| N128/P60 | 3.810591606 | 15672 | 1024 |
| N512/P60 | 14.929505667 | 15556 | 4096 |
| N32/P80 | 1.153464458 | 15964 | 256 |

각 run은 네 새 local enclosure와 두 재사용 local enclosure를 조합한다. 위 시간은 이번 kernel만의 실제 시간이며 선행 계산 비용 또는 다른 시스템의 성능을 추정하지 않는다. Actual wrapper wall time은 해당 `RUN.json`에 따로 있다.

이론 contributor의 92 exact Fraction/formal-exponential 검사와 별도 recurrence contributor의 76 exact toy 검사, 3,867 saved arithmetic 검사 결과·원 실행 기록을 읽었다. 후자의 1,626개는 interval endpoint 순서, 2,241개는 substantive propagation 산술이다. 같은 실패의 재실행을 새 성공으로 중복 계산하지 않았고, 이 숫자를 서로 다른 물리 증거 개수로 해석하지 않는다.

두 최초 control 실패는 보존됐다. 첫 toy의 잘못된 representation interval이 선택된 상단 endpoint를 포함하여 두 mutation witness가 판별력을 갖지 못했고, 동일 허용 범위의 하단 endpoint로 수정됐다. 첫 saved-audit는 실제와 다른 ledger field 이름으로 KeyError가 났으며 adapter 이름만 수정됐다. Candidate의 tolerance, physical definition 또는 scientific result가 바뀐 finding은 없었다.

Owner의 106 saved-evidence checks는 OWNER_SELF_REVIEW다. Figure 배치 수정 후 같은 106개 검사를 재실행한 것은 추가 독립 과학 증거로 세지 않는다. 최종 보고서와 figure는 두 track의 correction, deterministic radius, 반올림 표시 및 physical ceiling을 명확히 구분한다.

### Reviewer가 직접 실행한 감사

현재 global ledger의 interval 폭은 작은 anchor보다 크므로, 장부가 0을 포함한다는 조건만으로 anchor 생략을 검출할 수 없다. 이 구체적 위험에 대해 reviewer는 `exact_native_anchor_audit.py`를 별도로 작성하여 **저장된 N512/P60 자료만** 정확 Fraction으로 검산했다.

검산 범위는 native energy conversion/stock residual, signed representation, energy 후보의 완전한 반경, photon/count/energy incoming gain, 네 signed anchor product, 다음 incoming 및 누적 energy/heat/source/redshift 반경, global energy 장부의 anchor 차감이다.

**실제 138 PASS, 0 FAIL, exit 0, wall 0.064206606초, child peak RSS 11,636 KiB.** Source SHA-256은 `be26a798d9d9b86332e6a4b83668f207f6a24cb9b0253d9eec7838910a2cdfc2`이며 실행 전후 동일했다. Candidate import, 새 coefficient evaluation, continuous solver, native run 및 gas advance는 모두 0회다. 원본 stdout/stderr와 실제 실행 identity는 `evidence/review/EXACT_NATIVE_ANCHOR_EXECUTION.json`에 있다.

이 감사 역시 saved local interval에 조건부이며 그 자체로 독립 physical model 또는 continuous-reference accuracy certificate를 제공하지 않는다.

## 결과 범위와 재현 계약

N512/P60의 native 기준 보정과 절대 반경은 다음과 같다. 표는 반올림한 표시이며 exact certificate는 원본 JSON 전체 endpoint다.

| Track | 최종 photon correction | Photon radius | 누적 heat correction [eV norm.] | Heat radius [eV norm.] |
|---|---:|---:|---:|---:|
| OFF/0 | +3.214625618963e−13 | 1.607172671488e−18 | −3.265004694823e−14 | 4.721279916137e−19 |
| OFF/700 | +1.917944394720e−13 | 8.110833422178e−19 | −2.090850458786e−12 | 9.709034947585e−18 |

`EXECUTION_LOCK.json`의 10개 실제 파일을 확인했다. N512 numerical projection의 SHA-256은 `f4d0f8c7e37e5c8a013ab133af748173f3ef1a8247f413f4798fdb3518c04a86`이며 lock과 일치한다.

NCP 계약은 CPython 3.12.x, N512/P60, process/thread 각각 1, 1 GiB, child wall 180초, scientific attempt 1회다. 실제 새 결과의 producer/input SHA와 모든 deterministic track·incoming·representation·anchor·moment·ledger·rounding 자료를 비교한다. 기존 directory를 거부하고, source mismatch·timeout·numerical mismatch를 보존하며, tolerance 또는 baseline을 바꾸는 자동 재시도가 없다. Synthetic runner 경계 7개 PASS는 물리 실행 또는 실제 NCP 실행의 증거로 세지 않는다.

실제 Chat 준비 확인은 `VERIFY_ONLY_PASS`, scientific execution `NOT_RUN`이다. NCP에서 실제 child와 새 parity가 모두 성공할 때만 `PASS_SCOPED_HOST_PARITY`를 반환할 수 있다. E13C4 실행 반환의 scoped search에서 발견하지 못한 상태도 전역 미실행 증명으로 바꾸지 않았다.

## 남은 경계와 종료

| 항목 | 판정 이후 상태 |
|---|---|
| 선택한 두 OFF track의 incoming/representation/anchor enclosure | PASS_SCOPED |
| 첫 구간 초기조건 | 각 track에서 exact incoming 0 |
| 후속 photon·moment 오차 | 모두 운반, reset 없음 |
| 모든 spectral node/native aggregate reduction | 미인증 |
| uniform full path 또는 coupled gas history | 미인증 |
| baseline RCT / actual atomic photon·heat·recoil | OFF / null |
| physical / production | HOLD / HOLD |
| HE-F2/F09 / receiver adoption | OPEN / SEPARATE |
| legacy Gamma alias | 3.543295 FAIL |
| 실제 NCP host parity | NOT_RUN, 이후 actual evidence 필요 |

검토한 패키지 DAG가 제안한 다음 scientific node는 `E13C6_SPECTRAL_WEIGHTED_AGGREGATE_AND_REDUCTION_ENCLOSURE`다. 이는 아직 확인 중인 외부 recovery/first2 branch를 통합한 전역 최신 연구 순서를 보증하지 않는다. 이 NCP replay가 다음 이론 설계나 full first2 확장을 수행하는 계약은 아니다.

필요한 scoped correctness review를 마쳤으며 추가 old solver 실행이나 재귀적인 전체 review는 필요하지 않다. 이후 owner는 이번 판정을 참조하는 CLOSEOUT/state, manifest, archive, Git publication과 backup receipt를 완결할 수 있다. 그 operational 결과는 본 scientific review가 선확인한 사실이 아니며 별도 실제 기록을 따른다. Bound source/input/PLAN/numerical evidence/theory/report/handoff에 과학적 변경이 있으면 영향 범위와 byte identity를 다시 명시해야 한다.

`state/RESEARCH_STATE.json`은 읽은 시점의 progress snapshot으로서 frozen scientific contract에 포함하지 않는다. 판정 후 `CLOSEOUT.json`, `state/CLAIM_LEDGER.json`, state pointer를 실제 판정과 evidence에 맞추는 갱신, lineage 조사 결과를 추가하는 별도 addendum, manifest 및 delivery receipt 생성은 허용된 후속 정리다. 기존 scientific report/handoff의 내용이 달라지면 그 새 부분과 최종 identity를 추가로 확인한다. 이 절차는 새 물리 계산 또는 같은 전체 리뷰의 반복을 요구하지 않는다.
