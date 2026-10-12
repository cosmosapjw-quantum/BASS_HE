# BASS_HE 개발계획 개정 — 과학적 결과와 소비자 오차예산 우선

2026-10-12 · 결정: **SCIENTIFIC_FAST_TRACK_RESET** · 범위: BASS_HE의 향후 개발 우선순위와 REI/BASS 연동 권고

## 1. 이번에 바꾸는 결정

**E13C11의 추가 포함 구간 정밀화를 자동 다음 작업에서 대기로 옮긴다. 다음 공동 과학 마일스톤은 기존 REI 전자 이력과 BASS의 Liouville/편광 Thomson 수송을 연결한 방향별 반응 비교다.** BASS_HE는 해당 결과에 필요할 때 선택하는 원자 입력·국소 수치 기준을 제공한다. 원자물리 전체의 완료를 축약 재이온화나 처방된 이력의 수송 계산이 기다리게 하지 않는다.

이 문서는 사용자의 감사 반영 요청에 따른 **계획 변경**이다. E13C10 패키지의 `NEXT_DAG.json.next_node`가 제안한 `HE_E13C11_SECOND_INTEGRAL_BOUND_LOCAL01`의 자동 우선순위를 대체한다. 봉인된 과거 state, 입력, 코드, 실패, 포함 구간, 독립 채택 판정은 그대로 과거 결과의 권위다. 새 계획의 상태는 [ACTIVE_DAG.json](research/scientific_priority_reset_20261012/ACTIVE_DAG.json)에 있다. 숫자가 큰 노드 이름이나 파일 수정 시각만으로 다음 과학 작업을 선택하지 않는다.

실제 반영 저장소는 `cosmosapjw-quantum/BASS_HE`다. 아래 REI와 BASS 작업은 소비자 소유 저장소에 대한 구체적인 연동 권고이며, 이번 변경을 그 저장소의 코드 변경·실행·채택으로 표시하지 않는다. 변경은 additive draft로 게시한다. 기존 owner PR의 병합 또는 force update는 포함하지 않는다.

## 2. 감사에서 채택한 점과 정정한 사실

감사 입력은 사용자가 제공한 27,686-byte 텍스트이며 SHA-256은 `ba4822f20d706d8c1841aaa7f934b8386fdf1e577de63e6578ca266e211807a4`다. 감사의 논지를 실제 source와 대조했다. 원문에 남은 검색 서비스의 `GitHub+2` 같은 표시는 근거 링크로 재사용하지 않았다.

| 감사의 쟁점 | 확인한 현재 사실 | 개발계획에 반영 |
|---|---|---|
| 원자물리 통합이 첫 과학 결과를 지연시킴 | PR104 DAG와 BASS_HE 공통 계약은 이미 CR/RCT/HH를 reduced baseline의 필수조건에서 제외한다. 다만 PR104의 후속 중심은 N1/N2→N3 full native다. [S3,S5] | 기존 비차단 원칙을 실제 다음 작업 순서에 적용한다. 이미 있던 분리를 새 발명으로 기록하지 않는다. |
| native가 129개 중 1개만 진행 | 최신 C12 후보는 그 상태다. 이전 128/256-energy 후보는 전구간을 실행했지만 spectral 비교가 실패했다. 수용된 full native 과학 이력은 HOLD다. [S4] | 실행 불능과 수렴 미채택을 구별한다. 완료된 native 후보와 최신 checkpoint를 보존하고 자동 연장은 대기한다. |
| 방향 수송을 먼저 완성할 필요 | REI에는 collisionless characteristic 코드가 있고, BASS에는 실제 native 편광 Thomson 연산자가 있다. N4의 reduced 전자 이력→proper-time opacity/finite visibility 수신도 이미 완료됐다. [S6–S8] | 새 Liouville, 새 Thomson, 새 전자-density adapter를 각각 만드는 노드를 삭제한다. 실제 남은 일은 기존 입력과 충돌 연산자의 연결 및 방향 반응 비교다. |
| 국소 정밀도를 계속 올리는 문제 | E13C8의 전체 유한 수치 폭은 이미 매우 작다. E13C10은 선택 경로의 폭을 더 줄였으나 소비자·물리·연속극한 채택을 제공하지 않는다. [S1,S2] | E13C11은 소비자 결과에 대한 기여가 확인될 때 재개한다. |
| 고에너지 tail의 물리적 누락 | 감사의 200 eV HeII heating 수치는 이번 최소 대조에서 재검증하지 않았다. PR110은 50 keV 위 source-energy tail을 gas-heating 오차와 구분한다. [S4] | 향후 열·이온화 coupling에서 종별 Γ와 heating moment의 tail을 따로 평가한다. source 에너지 누락률을 가열 오차로 바꾸지 않는다. |

PR112의 합성 RCT stepper와 PR113의 저장된 warm RCT-OFF 진단도 C12 전구간 이력의 완료 증거가 아니다. 이번 source 확인은 각 branch의 해당 scope에 한정된다. 모든 관련 저장소의 모든 최신 연구를 전수 감사한 것은 아니다.

## 3. 보존하는 과학적 기준선과 사용할 수 있는 입력

### 유한 수치 결과

| 결과 | 유지하는 판정 | 다음 작업에서의 용도 |
|---|---|---|
| E13C8 OFF, 2,440 paths / 4,884 segments | `PROMOTE_SCOPED_FULL_FINITE_CAPTURED_OFF` | 동일 captured 첫 두 step 문제의 수치 기준. 완료된 NCP 2,331개 작업과 전체 합산을 재실행하지 않는다. |
| E13C9 선택 경로 | 기존 국소 signed Volterra 채택 | 같은 고정 문제에서 재사용 가능한 방법·결과 |
| E13C10 5 paths / 12 segments, 170개 raw 구간 | `PROMOTE_SCOPED_LOCAL_SIGNED_CURVATURE_FIRST` | 선택 경로의 더 좁은 포함 구간. 새 full population 계산으로 외삽하지 않는다. |
| E13C10 full population | `NOT_RUN` | 현재 계획에서 자동 실행하지 않는다. |
| 이 E13 계보의 physical / continuum / production / receiver | `HOLD` | 별도 근거가 필요한 주장 범위. 원자 연구 전체 또는 다른 consumer lane 전체의 상태로 확대하지 않는다. |

E13C8의 저장된 상대 **전체** 구간 폭은 `P_final` 약 `1.07071908e-13`, `H_total_eV` 약 `5.76346954e-13`, HeII heat 약 `3.58382563e-11`이다. $w=U-L$, midpoint $m=(L+U)/2$에 대한 $w/|m|$이며 상대 반폭과 두 배 차이가 난다. 이는 고정 유한 문제의 수치 포함 폭이다. 실제 원자율·재이온화·연속 스펙트럼의 물리 오차가 이 값이라는 뜻은 아니다. 아직 수치화되지 않은 model error가 반드시 지배한다고 단정하지도 않는다. [S1]

E13C10에서 남은 양의 반폭 상계 중 second-integral rectangle이 약 98.83%라는 사실은 국소 알고리즘 연구 후보를 알려 준다. 그것만으로 다음 과학 우선순위나 NCP 필요성이 결정되지 않는다. 기존 함수의 exact/frozen exponential 및 Volterra 보정 구조도 보존한다. 지수 적분을 처음 도입하는 새 과제로 만들지 않는다. [S2]

### 실제 원자 입력과 잘못된 재사용의 방지

B3 v0.1.1에는 GM25/W82와 KF96의 명시적 scalar thermal-rate/count 선택이 이미 구현돼 있다. 공통 비교 온도는 1000–10000 K이며 source를 평균·합산·자동 교대하지 않는다. 기존 REI 반환의 범위는 조건부 optional local RHS binding이고 default OFF다. 그 반환의 source physical admission 및 production stepper integration은 false다. 실제 photon spectrum, mean emission energy, heat, recoil, inverse rate, source uncertainty는 scalar rate에서 복원할 수 없는 별도 입력이다. [S9,S10]

E13C8의 P는 photon stock/H, A는 absorption count/H, B/H/Z는 eV/H의 누적량이다. 시간 좌표는 `ln a`이며, 이 계보는 제조 external source의 고정 gas path 문제다. 따라서 P/H 결과를 순간 `Gamma_s [s^-1]`, 체적 가열률 또는 실제 RCT 방출 스펙트럼으로 자동 export하지 않는다. E13C2의 A/heat 보정을 기존 gas algebraic residual에 투영한 계산도 이미 있다. 그 old solver TOL에 대한 비율은 continuum 또는 EoR 오차예산이 아니다. 이 projection을 다시 계산하는 노드도 만들지 않는다. [S5,S11]

## 4. 연구 경로와 실제 다음 마일스톤

공통 배경의 평균 scale factor·proper clock·tetrad 규약을 재사용한다. 각 경로는 자신의 근사와 결과 범위 안에서 독립적으로 닫을 수 있다.

| 경로 / 소유 | 목표와 다음 산출물 | 완료 기준 | 계산 배치 |
|---|---|---|---|
| **A — REI reduced history** / rei_bianchi | PR104의 Q, 구간 τ, source/C/T/IC scenario 결과를 기준선으로 재사용 | 이미 채택된 reduced 범위 유지. 전체 CMB τ나 방향 수송으로 재명명하지 않음 | 저장 결과 읽기·그림 재사용은 HERE. 완료 적분 반복 없음 |
| **B — prescribed-history 방향 수송** / rei_bianchi + bass | 기존 N4 전자 이력을 실제 편광 Thomson 호출에 연결. 공통 배경에서 방향 스펙트럼·편광과 대조군을 한 결과 묶음으로 산출 | 아래 B1의 반응 비교, 새 연결에 필요한 시간·각도·스펙트럼 검증, 명시된 근사·오차. BASS_HE full native 완료에 의존하지 않음 | 설계·코드·대표 pilot·후처리 HERE 우선 |
| **C — 최소 feedback** / rei_bianchi | B의 범위가 닫힌 뒤 필요한 H/He Γ·heating moment로 one-way와 two-way 결과 비교 | 같은 IC/source/background에서 어떤 feedback이 목표 반응을 바꾸는지 제시. 종별 수·전하·에너지 ownership 및 moment tail 기록 | 짧은 대조 HERE; 실제 긴 독립 scenario 묶음만 NCP 후보 |
| **D — 원자·고충실도 연구** / BASS_HE·CR·RCT·HH 및 native owner | 기존 결과 보존, 구체적인 소비자 요청 또는 독립 원자물리 질문에 대한 선택적 보정 | 대상 observable, 필요한 정보·정밀도, 그 계산으로 바뀔 판단이 명시됨 | E13C11과 새 전체 finite 실행은 대기. 필요성과 비용이 확인된 subset만 재개 |

### B1: 다음 공동 과학 작업을 구체화

**질문:** 같은 평균 팽창률과 같은 전자 이력 아래에서, 방향별 Liouville 전파와 Thomson 산란이 등방 대조군과 구별되는 spectrum/linear-polarization 반응을 만드는가? 그 반응은 전자 이력 선택에 얼마나 민감한가?

기준 구간은 기존 reduced 입력의 mean-volume z=20→4다. 우선 이미 수신된 FLRW와 초기 $r=s/H=+0.1$ 자료를 재사용한다. 이 r은 진단용 시나리오이며 관측 허용값이라는 의미가 아니다. 공통 source/초기 복사장·geometry·clock·화면 기저를 기록하고, 기존 transport benchmark의 입력을 재사용한다. R15의 integrated photon emissivity만으로 에너지 스펙트럼을 만들어 내지 않는다. 이 구간의 모든 초기광자·방출 source 및 외부 tail이 갖는 가정을 명시한다.

최소 비교는 다음 여섯 경우다. 같은 입출력 정의와 수치법을 쓴다. 네 기본 대조에 두 전자 이력 대조를 더해 geometry와 history의 영향을 분리한다.

1. **F:** FLRW geometry + 해당 reduced electron history.
2. **M:** Bianchi 사례와 같은 mean $H(a)$를 갖는 등방 test background + Bianchi 사례의 동일 $n_e(a)$. 이는 평균팽창 효과를 분리하는 대조군이다.
3. **B:** Bianchi geometry + M과 동일 $n_e(a)$, 같은 source/초기 복사장. B−M이 일차 방향 반응이다.
4. **B0:** B와 같은 조건에서 collision depth만 0. B−B0으로 실제 산란의 기여를 분리한다. 이는 새 물리 모형의 채택이 아닌 진단 대조군이다.
5. **B_F:** B와 같은 geometry·H·source에서 FLRW reduced 전자 이력을 같은 mean-a 축에 처방한다.
6. **M_F:** M과 같은 geometry·H·source에서 B_F와 동일한 전자 이력을 처방한다. 전자 이력에 대한 방향 반응의 민감도는 `[B−M](ne_B)−[B_F−M_F](ne_F)`로 비교한다.

두 history의 비교는 동일한 B proper clock과 공통 mean-a 구간에서 한다. N4의 서로 다른 proper-time 셀 평균 `ne_eff`를 같은 시각의 점밀도처럼 복사하지 않는다. 원 producer의 저장된 Q(a)·밀도·closure와 기존 cell optical-depth 정의를 재사용해 두 history를 같은 규칙으로 재투영하고, 모든 B/M 쌍에 같은 history 표현을 쓴다. 이때 새 시간 보간·재투영의 영향은 새로운 연결의 수치오차로 기록한다. 이미 완료된 재이온화 ODE나 N4 수신을 통째로 다시 실행하는 작업은 아니다.

N4의 `ne_eff_m3`는 proper cell-mean density이고 시간은 proper seconds다. 충돌 깊이는 $x_i=c\sigma_T\bar n_{e,i}\Delta t_i$로 기존 상수 규약을 유지해 전달한다. 추가 $a^{-3}$, $1+z$, Doppler 인자를 붙이지 않는다. 이미 기록된 REI/BASS의 σT 차이는 기존 상수비 처리로 유지한다. 단순히 collisionless 코드에 xe 파일을 읽히는 것은 scattering 연결이 아니다. 실제 `pol_collide::collide`/`collide_modeb`에 x가 전달되고, B0가 같은 코드에서 정확히 무충돌 한계를 선택하도록 연결한다. 기존 배열·에너지·coherency tensor 규약을 존중한다. [S6–S8]

일차 출력은 적색편이·에너지별 무차원 quadrupole 비

\[
q_2(E,t)=\frac{\int d\Omega\,P_2(\mu)I_E(t,\mathbf n)}{\int d\Omega\,I_E(t,\mathbf n)},\qquad
P_2(\mu)=\tfrac12(3\mu^2-1),
\]

와 Δq2=B−M이다. μ는 공통 orthonormal tetrad에서 photon 방향과 LRS 전단축의 내적이다. 분모가 0인 구간은 정의 불가로 표시한다. 보조 출력은 정한 screen basis의 Stokes 및 $p_L=\sqrt{Q_S^2+U_S^2}/I$다. p_L도 I=0에서는 정의 불가 mask를 사용한다. filling factor Q와 Stokes Q를 구분한다. 그림은 J0/J2 또는 q2, polarization, paired numerical difference를 함께 보여 준다. 아직 전체 line-of-sight/observer tail이 없으므로 이 그림을 관측 CMB $C_\ell$, total optical depth 또는 fixed-observed-z 예측으로 부르지 않는다.

기존 전자 셀 평균이 같은 optical depth를 주더라도 Liouville과 산란의 결합에서 내부 시간 순서가 자동으로 같아지지 않는다. 새 연결에 한해 시간 셀 분할·각도 분해능·필요한 스펙트럼 보간을 각각 확인하고, 기존 opacity reader와 전체 원자 suite를 다시 인증하지 않는다. 저온·비상대론적 전자에 대한 elastic Thomson/test-field 근사를 명시한다. 더 정밀한 thermal redistribution이나 backreaction은 이번 첫 결과의 범위가 아니다.

**성공은 유의한 신호를 반드시 찾는 것이 아니다.** Δq2 또는 편광 반응이 수치 분해능 안에서 구별되는지, 아니면 상한·미해결로 남는지를 한 결과로 판정하면 된다. 신호를 주장하려면 paired 반응의 관측된 수치 불확실성을 반응 크기의 10% 이하로 제어하는 것을 첫 benchmark 목표로 둔다. 이 10%는 탐색적 반응의 해석 정밀도이며 원자율·모든 bin·full native의 tolerance로 전파하지 않는다. 0에 가까운 반응에는 상대값을 나누지 않고 실제 null 대조와 refinement에서 얻은 절대 범위와 한계를 보고한다. 이것은 관측 제약이나 엄밀 구간 증명으로 표시하지 않는다.

대표 case가 짧으면 여섯 비교와 필요한 새 연결 검사를 HERE에서 끝낸다. 정한 짧은 pilot으로 결론이 안 나면 실제 실패·비용·다음 한 가지 판별 실험을 남긴다. 결과가 작다는 이유만으로 무제한 정밀화 또는 NCP campaign을 생성하지 않는다. **B1 결과물은 CSV/그림/해석을 포함한 하나의 실행 가능한 결과 묶음이며, 새 계약 문서만 생성한 상태는 완료가 아니다.** 이번 턴은 이 개발계획을 고정한 단계로 B1 수치 실행은 NOT_RUN이다.

## 5. 물리적 해석과 오차예산

### 평균팽창 반응과 방향 반응을 구분

현재 축약 모형이

\[
\frac{dQ}{d\ln a}=\frac{S-RQ}{H},\qquad
\frac{d\tau}{d\ln a}=\frac{c\sigma_T n_e}{H}
\]

만 사용한다면 같은 H, S, R, IC와 같은 closure는 같은 Q와 τ를 준다. cap/event를 포함하면 그 규칙도 같아야 한다. LRS Bianchi I의 $s_0^2a^{-6}$ 평균팽창 항은 이 scalar 문제에서 FLRW의 유효 stiff 성분과 대응된다. 이는 선언된 축약 방정식에 대한 직접 유도이며 Bianchi 물리 전체의 no-go 정리가 아니다. B−M 비교가 필요한 이유다. 공통 proper-time 경계의 homogeneous non-tilted τ를 방향별 observed-redshift τ와 혼동하지 않는다. [S3]

PR104의 Δτ≈−2.61122e−5와 fesc/C/T 변화에 대한 값은 모델별 scenario 비교다. posterior 또는 통계적 model uncertainty가 아니다. 예컨대 그 특정 Δτ를 10% 정밀도로 읽고자 한다면 paired 수치오차를 약 2.6e−6 아래로 두는 것이 해당 목표의 한 기준이다. 이 예시를 이번 q2의 절대 허용오차나 모든 내부 Γ의 1e−4 요구로 바꾸지 않는다. [S3]

### 수치, 모형, 입력을 같은 오차로 합치지 않음

관측량 $O$의 paired 반응 ΔO에 대해 시간·각도·에너지 수치오차, closure 선택, source/rate family 변화, 관측 해석을 각각 기록한다. 원자 입력 오차 δk의 1차 영향 $\delta O\simeq(\partial O/\partial k)\delta k$는 민감도 근사다. 비선형 remainder나 입력의 확률모형 없이 엄밀 상계·통계 신뢰구간이라 부르지 않는다. 공통 rate 오류가 paired 차이에서 항상 상쇄된다고 가정하지도 않는다.

비등방 복사장에는 방향 적분을 포함해

\[
\Gamma_s=\int d\Omega\int_{E_s}^{\infty}\frac{I_E(\mathbf n)}{E}\sigma_s(E)\,dE,
\quad
\mathcal H_s=\int d\Omega\int_{E_s}^{\infty}\frac{I_E(\mathbf n)}{E}\sigma_s(E)(E-E_s)\,dE
\]

를 사용한다. Γ는 표적당 s^-1, ℋ는 표적당 energy/time이며 체적 가열률은 $n_s\mathcal H_s$다. $I_E$의 에너지 단위와 dE, cross section 및 에너지 변환을 일치시킨다. angle-averaged J_E convention에서는 ∫dΩ가 4π와 대응한다. 기존 photon number-density convention을 쓸 때는 공통 계약의 c 인자를 사용하며 두 convention을 섞지 않는다. [S5]

Track C에서 이 모멘트를 표 또는 few-group closure로 줄일 때는 HI/HeI/HeII threshold, 가열의 excess-energy 가중치, 상단 tail을 따로 다룬다. 같은 photon energy를 열과 secondary ionization에 중복 배정하거나 scalar RCT k에서 spectrum을 가정해 복원하지 않는다. 필요한 모멘트가 없으면 그 RCT 경로를 optional로 남기고 이미 정의된 축약 경로를 계속한다.

## 6. 검증·전달과 NCP 사용 정책

| 항목 | 개정 원칙 |
|---|---|
| 구조적 물리·단위 | 핵수·전하, photon/energy ownership, positivity, normalization, frame/clock 및 source domain은 계속 확인한다. ledger는 적절한 절대·정규화 잔차를 사용하며 0에 가까운 midpoint로 나눈 상대 폭을 줄이는 일을 목표로 삼지 않는다. |
| 새 구현 검사 | 실제 바뀐 seam, 신규 가정, 새 데이터에 필요한 검사만 수행한다. 동일 의존성의 완료 증거는 재사용한다. |
| 과학적 정확도 | 선택한 paired observable에 맞춰 정한다. 기존 full native gate에서 실패한 결과를 새 reduced gate로 통과했다고 고치지 않는다. |
| 독립 검토 | 주요 과학 주장, 알고리즘 변경 또는 채택 시 실시한다. 문구 수정마다 새 과학 인증·전수 실행을 열지 않는다. |
| 기록·백업 | 긴 작업의 checkpoint, 새 과학 결과, 중요한 계획 전환을 보존한다. 작은 수정마다 전체 nested archive를 재포장·재다운로드하지 않는다. |
| 이번 전달 | 계획·DAG·handoff·source index·짧은 검토를 한 additive PR와 작은 delta package로 남긴다. 기존 E13C10 complete backup은 참조한다. |

**현재 새 NCP work unit은 0개다.** theory, 설계, 코드, 짧은 controls/pilot, 저장값 후처리는 HERE에서 수행한다. NCP는 유의미한 긴 미실행 작업이 실제로 있을 때 사용한다.

NCP 후보는 서로 독립인 background/history/source/closure 시나리오를 우선한다. 각도들은 Thomson 산란으로 결합되므로 독립 광선처럼 무조건 분리하지 않는다. 시간 의존성이 있는 한 trajectory의 연속 step도 독립 작업이 아니다. 주파수 분할은 redshift 보간과 kernel의 의존성을 확인한 경우에만 사용한다.

NCP 이관 때는 다음 다섯 항목을 **하나의 실행 packet** 안에서 채운다.

1. 비교할 과학 질문, 출력 observable과 paired accuracy 기준, 기존 결과가 그 판단을 막는 이유.
2. source/input/model identity와 이미 완료된 work를 제외한 최소 독립 작업 목록.
3. HERE의 대표 실행에서 측정한 wall/CPU/RSS, 작업 수와 편차, 이관·초기화·I/O를 포함한 예상 완료시간. 추정과 실측을 구별한다.
4. 실제 host의 CPU topology·affinity/quota·NUMA·가용 RAM을 반영한 rank/thread 선택. 64×1 또는 혼합 구성을 이름만으로 채택하지 않는다. BLAS/OpenMP 중첩을 막고 실제 가용 RAM의 최소 20%를 남긴다.
5. fresh output/checkpoint, 기존 완료 cache 재사용, 첫 실패 보존, HERE에서의 합산·과학 판정 경로. 이미 끝난 campaign을 성능 증명용으로 통째로 재실행하지 않는다.

E13C8의 과거 64 computing MPI ranks / 2,331 paths / 약 2,037.83초는 그 완료 작업의 실행 기록이다. 새 수송 계산의 예상 속도나 64배 가속을 입증하지 않는다. 128GB를 채우는 것이 목표도 아니다. [S1] 기존 E13 P60 의미는 해당 계보에 유지하며, 다른 consumer의 선언된 binary64 근사를 이 P60 인증과 혼합하지 않는다. [S12]

## 7. E13C11과 full native를 다시 여는 조건

E13C11은 `PARKED_PENDING_OBSERVABLE_NEED`다. 다음 둘 중 하나가 구체적인 연구 질문으로 성립할 때 재평가한다.

- 실제 소비자 observable의 필요한 수치 정밀도가 기존 finite 결과에 의해 제한되고, E13C11의 개선이 그 제한을 줄일 수 있다.
- 별도 원자·수치해석 연구로서 signed second-integral enclosure의 새 정리·비교 결과가 독립 과학 목표로 선택된다.

어느 경우든 기존 국소 상계의 가장 큰 항이라는 사실만으로 재개하지 않는다. 새 full population은 위 과학 목적과 최소 미실행 work list가 함께 필요하다. Full native C12의 원래 실패·budget·checkpoint 상태를 초기화하거나 기존 tolerance를 몰래 바꾸지 않는다. frozen-state stiffness 진단은 선택적 수치 연구로 둘 수 있으나 A/B의 완료를 차단하지 않는다.

다음 BASS_HE 연구 요청을 받을 때는 이 계획과 ACTIVE_DAG를 먼저 읽는다. 구체적인 소비자 수요가 없는 동안 E13C11 대신 새 인증·API·잔차 projection 작업을 발명하지 않는다. 공동 B1의 설계·코드·짧은 실행을 HERE에서 진행할 수 있으며, 결과 또는 실제 blocker를 남기는 것이 다음 목표다.

## 8. 출처와 상태

아래는 이번 계획에 사용한 source-pinned 기준이다. 상세 byte/Git identity 및 읽은 범위는 [SOURCE_INDEX.json](research/scientific_priority_reset_20261012/SOURCE_INDEX.json)에 둔다. 문헌상의 물리, 직접 유도, 저장된 수치 결과, 구현 존재와 아직 미실행인 계획을 구별한다.

- **S1** — [E13C8 finite observables](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/e13c8_full_finite_reduction_20261011/analysis/FINITE_OBSERVABLES.json), [state](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/e13c8_full_finite_reduction_20261011/CURRENT_STATE.json).
- **S2** — [E13C10 state](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/e13c10_first_midpoint_bound_local_20261012/CURRENT_STATE.json), [이전 next DAG](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/e13c10_first_midpoint_bound_local_20261012/NEXT_DAG.json), [utility memo](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/e13c10_first_midpoint_bound_local_20261012/analysis/NCP_SCIENTIFIC_UTILITY_MEMO_KO.md).
- **S3** — [REI PR104 report](https://github.com/cosmosapjw-quantum/rei_bianchi/blob/f66929c23ea3fa6e39dd4808e5b27d136c568a03/research/broad_history_20261010/REPORT_KO.md), [DAG](https://github.com/cosmosapjw-quantum/rei_bianchi/blob/f66929c23ea3fa6e39dd4808e5b27d136c568a03/research/broad_history_20261010/DAG.json).
- **S4** — [REI native candidate report](https://github.com/cosmosapjw-quantum/rei_bianchi/blob/17f8d0daa72e0f76a49cde01b110f650a6688c42/research/accel02_20261011/REPORT_KO.md), [C12 current handoff](https://github.com/cosmosapjw-quantum/rei_bianchi/blob/17f8d0daa72e0f76a49cde01b110f650a6688c42/research/accel02_20261011/q1b/c12/HANDOFF.json).
- **S5** — [기존 공통 인터페이스와 비차단 원칙](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/docs/atomic_reionization_handoff_20261004_v1/common/INTERFACE_CONTRACT_KO.md).
- **S6** — [REI Bianchi-I characteristic source](https://github.com/cosmosapjw-quantum/rei_bianchi/blob/17f8d0daa72e0f76a49cde01b110f650a6688c42/rust/rei_microphysics/src/bianchi_i.rs).
- **S7** — [BASS native polarized Thomson source](https://github.com/cosmosapjw-quantum/bass/blob/2325a42c0954e949bb57f53976d0c9a9d9a9a362/_rustcore/src/kinetic/pol_collide.rs).
- **S8** — [N4의 이미 완료된 전자 이력 수신](https://github.com/cosmosapjw-quantum/bass/blob/2325a42c0954e949bb57f53976d0c9a9d9a9a362/research/accel02_n4_20261011/REPORT_KO.md).
- **S9** — [B3 v0.1.1 export contract](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/shared_c64/20261003/EOR_B3_ATOMIC_EXPORT_v1/contract/ATOMIC_EXPORT_CONTRACT.json).
- **S10** — [조건부 local RHS 반환](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/docs/atomic_reionization_handoff_20261004_v1/threads/BASS_HE/consumer_returns/REI-HE-RCT01_20261005/HE_F2_RCT_CONSUMER_RETURN.json).
- **S11** — [E13C2 이론·단위](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/docs/atomic_reionization_handoff_20261004_v1/threads/BASS_HE/runs/HE-E13C2-VARIABLE-COEFFICIENT_20261010/THEORY.md), [기존 residual projection](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/docs/atomic_reionization_handoff_20261004_v1/threads/BASS_HE/runs/HE-E13C2-VARIABLE-COEFFICIENT_20261010/PHYSICAL_RESULT.json).
- **S12** — [기존 HPC 정책](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/research/shared_c64/20261001/NCP64_NATIVE_MPI_20261001T0520Z/HPC_POLICY_KO.md), [AGENTS.md](https://github.com/cosmosapjw-quantum/BASS_HE/blob/3c20b6e9dcd099a4f5ac23208445225f959fd1e5/AGENTS.md).

**이번 계획 변경의 실행:** source·저장 결과 읽기와 계획 작성. 새 physics/ODE/path/coefficient/MPI/NCP 실행 0, 과거 과학 suite 재실행 0. B1·C 및 E13C11의 새 수치 결과를 생성하지 않았다.
