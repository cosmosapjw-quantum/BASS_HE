# E13C5: incoming 보정, native 표현 및 energy anchor를 함께 운반하는 합성식

## 범위와 직접 읽은 근거

**상태: derived.** 아래 exact toy의 실제 실행 상태는 `EXACT_TOY_RESULTS.json` 및 `EXECUTION.json`에 별도로 기록한다. 이 문서는 독립 이론 contributor의 산출물이며 후보 구현 또는 최종 decision review가 아니다.

직접 읽은 문서는 GPT-6 Astra research v4.0.0의 `PROJECT_INSTRUCTIONS.md`, research state 템플릿, coding v4.0.0의 `AGENTS.md`, scientific contract와 validation matrix 템플릿, E13C4의 `NEXT_DAG.json`, `THEORY.md` 전체, `code/local_enclosure.py` 전체 및 `inputs/SIX_CONTROLS.json`의 계약과 첫 control 전체다. 실제 adjacent row는 상속된 OFF/GM `SEGMENTS.csv`에서 확인했다. 비어 있는 harness state/contract는 과학적 증거로 사용하지 않았다. 원시 자료 파일의 identity는 `READ_IDENTITIES.json`에 기록한다.

E13C4는 각 captured local initial value에서 incoming defect를 0으로 놓은 certificate다. E13C5가 새로 운반해야 할 것은 photon incoming 값과 그 오차, 이전 구간의 누적 moment 오차, exact frozen과 captured native 값의 차이, 그리고 경계의 energy anchor다. 아래 결과는 동일한 fixed gas path와 branch 정의에만 적용되며 gas evolution의 오차나 원자모델 불확실성을 제한하지 않는다.

## 1. 동일한 segment 모델과 incoming 계약

한 구간의 무차원 변수는 \(u=s-s_a\in[0,h]\), \(s=\ln a\)이며

\[
P'=q-\Lambda P,\qquad F'=q_f-LF,\qquad
F(0)=f_0,\qquad E(u)=E_0e^{-u}.
\]

\(L=\sum_i\lambda_{if}\), \(\Lambda=\sum_i\lambda_i\), \(\delta\lambda_i=\lambda_i-\lambda_{if}\), \(\delta\Lambda=\Lambda-L\), \(\delta q=q-q_f\)다. Captured binary64 값은 정확한 실수로 올린다. Frozen coefficient를 새 midpoint 값으로 교체하지 않는다. Photon과 count는 기존 photons/H/dη 정규화이고, energy·heat·redshift는 eV를 곱한 정규화다. CSV energy 값은 상속된 \(\epsilon\) [erg/eV]의 exact lift로 나누어 같은 단위로 비교한다.

Incoming defect \(e_a=P(0)-f_0\)에 대해 저장할 값은 **중심 \(c\), 인증 반경 \(\eta\ge0\)** 이다.

\[
|e_a-c|\le\eta.\tag{1}
\]

중심도 저장된 decimal 또는 binary64의 어떤 실수 lift인지 고정한다. True defect \(e=P-F\), forcing \(r=\delta q-\delta\Lambda F\), incoming 중심을 쓰는 first variation \(e_1\)는

\[
e'+\Lambda e=r,\qquad e_1'+Le_1=r,\qquad e_1(0)=c.
\]

\(\Lambda\ge0,F\ge0\)와 고정 branch를 전제로

\[
B_r=\int_0^h(|\delta q|+|\delta\Lambda|F)\,du,
\qquad S=|c|+\eta+B_r,
\qquad \|e\|_\infty\le S.\tag{2}
\]

이는 exact integral을 뜻한다. 실제 코드는 whole-cell outward upper bound로 대체한다.

## 2. Incoming firstvariation의 전달 계수

\(J(z,h)=\int_0^h e^{-zu}\,du\), \(J(0,h)=h\)라 하자. 각 observable의 E13C4 zero-incoming 정확한 firstvariation을 \(d_X\)라 놓으면 새로운 firstvariation은

\[
X_1=d_X+g_Xc.\tag{3}
\]

여기서 \(X\)는 local **continuous-minus-exact-frozen increment**이며 source에는 incoming 항이 없다.

| Observable | Incoming gain \(g_X\) |
|---|---|
| endpoint photon \(P_h\) | \(g_P=e^{-Lh}\) |
| species count \(A_i\) | \(\lambda_{if}J(L,h)\) |
| total count | \(LJ(L,h)=1-g_P\) |
| absorbed energy \(B_i\) | \(\lambda_{if}E_0J(L+1,h)\) |
| species heat \(H_i\) | \(\lambda_{if}[E_0J(L+1,h)-\chi_iJ(L,h)]\) |
| total heat | \(LE_0J(L+1,h)-C_fJ(L,h)\), \(C_f=\sum_i\chi_i\lambda_{if}\) |
| redshift \(Z\) | \(E_0J(L+1,h)\) |
| source count \(Q_N\), source energy \(Q_E\) | 0 |
| endpoint photon energy | \(E_hg_P\) |

따라서 exact firstvariation의 ledger는

\[
P_{1,h}+\sum_i A_{1,i}-Q_{1,N}=c,
\qquad E_hP_{1,h}+\sum_iB_{1,i}+Z_1-Q_{1,E}=E_0c.\tag{4}
\]

일반적으로 \(c\ne0\)이므로 오른쪽을 0으로 검사하면 잘못된 ledger다.

## 3. Incoming 불확실성과 remainder

\(\delta_a=e_a-c\), \(R=e-e_1\)라 놓으면

\[
R'+LR=-\delta\Lambda e,\qquad R(0)=\delta_a.
\]

E13C4의 kernel

\[
W(v)=e^{-L(h-v)},\quad K_0(v)=J(L,h-v),\quad
K_E(v)=E(v)J(L+1,h-v),\quad
K_{H_i}=K_E-\chi_iK_0
\]

를 그대로 사용하여

\[
R_P=g_P\delta_a-\int W\delta\Lambda e,
\qquad R_Z=g_Z\delta_a-\int K_E\delta\Lambda e,\tag{5}
\]

\[
R_{A_i}=g_{A_i}\delta_a+
\int[\delta\lambda_i-\lambda_{if}K_0\delta\Lambda]e,
\]

\[
R_{B_i}=g_{B_i}\delta_a+
\int[E\delta\lambda_i-\lambda_{if}K_E\delta\Lambda]e,
\]

\[
R_{H_i}=g_{H_i}\delta_a+
\int[(E-\chi_i)\delta\lambda_i-\lambda_{if}K_{H_i}\delta\Lambda]e.\tag{6}
\]

대괄호 안의 effective kernel을 \(T_X\)로 표시하면 (5)–(6)은

\[
|R_X|\le |g_X|\eta+S\int|T_X|.\tag{7}
\]

로 제한된다. Photon의 적분은 \(H_h=\int W|\delta\Lambda|\), redshift는 \(H_E=\int K_E|\delta\Lambda|\)다. Heat weight가 활성 종에서 구간 전체에 음수가 아님을 확인했을 때만 E13C4의 positive triangle bound도 사용할 수 있다. 두 **완결된 유효 상계** 중 작은 값을 선택하는 것은 가능하나 서로 다른 증명에서 원하는 일부 항만 조합해서는 안 된다.

### 총 count/energy에서 바뀌는 ledger

Incoming 오차가 존재하면 remainder ledger는

\[
R_P+R_{A,\mathrm{tot}}=\delta_a,\qquad
E_hR_P+R_{B,\mathrm{tot}}+R_Z=E_0\delta_a.\tag{8}
\]

이다. E13C4의 \(R_{A,\mathrm{tot}}=-R_P\)는 \(\eta=0\)인 정확한 incoming에만 그대로 쓸 수 있다. 올바른 total-count 상계는

\[
|R_{A,\mathrm{tot}}|\le (1-g_P)\eta+S H_h.\tag{9}
\]

Total absorbed energy는 \(g_{B,\mathrm{tot}}=LE_0J(L+1,h)\)에 대한 incoming 항을 먼저 두고, E13C4의 effective-total 또는 endpoint+redshift **coefficient remainder** 상계 중 작은 것을 합한다.

\[
|R_{B,\mathrm{tot}}|\le g_{B,\mathrm{tot}}\eta+
S\min\left\{\int|E\delta\Lambda-LK_E\delta\Lambda|,\;
E_hH_h+H_E\right\}.\tag{10}
\]

\(E_hB_P+B_Z\)를 incoming 오차가 들어 있는 값으로 바로 계산하여 total energy 상계로 사용하는 것은 (8)의 \(E_0\delta_a\)를 누락한다.

### 수치 중심에 대한 전체 반경

Outward interval \(J_{d_X}\ni d_X\), \(G_X\ni g_X\) 및 exact central number \(c\)가 있으면 \(J_{d_X}+G_Xc\)는 firstvariation enclosure다. 유한 저장 후보 \(\widehat X\)에 대해

\[
\eta_{X,\mathrm{num}}=\max_{x\in J_{d_X}+G_Xc}|x-\widehat X|,
\]

\[
|X-\widehat X|\le\eta_{X,\mathrm{num}}
 +\operatorname{upper}(|G_X|)\eta
 +\operatorname{upper}(S\int|T_X|).\tag{11}
\]

중심 선택의 rounding도 이 firstvariation interval과의 최대 거리에 포함된다. Previous cumulative moment의 반경은 incoming photon처럼 damping하지 않는다. 이전 누적 반경 \(\zeta_X\)는 새 local increment 반경에 더한다.

## 4. Exact frozen, captured native 및 다음 segment

구간 \(j\)의 exact frozen output을 \(F_{j,h}\), captured native photon output을 \(n_j\), 다음 local frozen 초기값을 \(f_{0,j+1}\)라 하자. 각각 정확한 실수 정의다. 다음 구간의 true photon은 photon-continuous seam에서 \(P_{j+1,a}=P_{j,h}\)이므로

\[
e_{j+1,a}=e_{j,h}+\rho_{P,j}+\kappa_j,
\quad \rho_{P,j}=F_{j,h}-n_j,
\quad \kappa_j=n_j-f_{0,j+1}.\tag{12}
\]

\(\rho_P\)는 frozen analytic representation과 native binary64 output의 차이이고, \(\kappa\)는 captured transfer continuity residual이다. 둘을 서로 바꾸거나 local error를 0으로 초기화해서는 안 된다. \(\kappa=0\)이 실제 입력에서 정확히 확인되더라도 \(\rho_P\)는 일반적으로 0이 아니다.

중심 \(c_{j,h}\), 반경 \(\eta_{j,h}\), representation interval \(R_{P,j}\ni\rho_{P,j}\)를 알면

\[
I_{j+1,a}=c_{j,h}+[-\eta_{j,h},\eta_{j,h}]+R_{P,j}+\kappa_j\tag{13}
\]

에서 다음 중심/반경을 선택한다. Native-output correction은 \(P_{j,h}-n_j=e_{j,h}+\rho_{P,j}\)이며 endpoint certificate도 같은 representation 항을 포함한다.

각 moment는 \(\rho_{X,j}=X_{f,j}-X_{\mathrm{cap},j}\)를 따로 계산한다. True moment를 native captured increment들의 **정확한 합**에 비교할 때

\[
\Delta X_{\mathrm{native},j}=X_j-X_{\mathrm{cap},j}
=\Delta X_{\mathrm{frozen},j}+\rho_{X,j}.\tag{14}
\]

누적 보정은 (14)를 순서대로 더하고 이전 누적 interval을 계속 운반한다. 실제 native aggregate가 binary64 reduction으로 만들어졌다면 그 aggregate와 captured increment들의 정확한 합 사이의 reduction residual도 추가해야 한다. E13C5의 소수 track 합을 모든 spectral node의 aggregate certificate로 확대하지 않는다.

### Native energy stock의 별도 표현 항

CSV `u`를 \(U_{\mathrm{cap},j}/\epsilon\)로 변환하여 eV 단위의 captured stock이라 하자. 일반적으로 이것은 \(E_{j,h}n_j\)와 정확히 같지 않다. 따라서

\[
\rho_{U,j}=E_{j,h}F_{j,h}-U_{\mathrm{cap},j}/\epsilon\tag{15}
\]

를 직접 둘러싸거나,

\[
\rho_{U,j}=E_{j,h}\rho_{P,j}
 +[E_{j,h}n_j-U_{\mathrm{cap},j}/\epsilon]\tag{16}
\]

로 두 표현 항을 모두 보존한다. \(E_h\rho_P\)만 더하는 것으로 native energy-stock certificate가 되지는 않는다.

### Native local ledger residual

Captured 값 자체의 number residual을 \(\varepsilon_{N,\mathrm{cap}}=n-f_0+\sum_iA_{\mathrm{cap},i}-Q_{N,\mathrm{cap}}\)라 하자. Native 기준 보정에는

\[
\delta P-e_a+\sum_i\delta A_i-\delta Q_N=-\varepsilon_{N,\mathrm{cap}}\tag{16a}
\]

가 성립한다. Native energy residual을 \(\varepsilon_{E,\mathrm{cap}}=U_{\mathrm{cap}}/\epsilon-E_0f_0+\sum_iB_{\mathrm{cap},i}+Z_{\mathrm{cap}}-Q_{E,\mathrm{cap}}\)라 하면

\[
\delta U-E_0e_a+\sum_i\delta B_i+\delta Z-\delta Q_E
=-\varepsilon_{E,\mathrm{cap}}.\tag{16b}
\]

Captured residual은 일반적으로 0이 아니다. 보정 자체의 ledger를 0으로 강제하는 것은 representation 항을 삭제하는 조작이 된다. (16a)–(16b)에 captured ledger를 더한 **완성된 true ledger**가 0을 포함하는지 검사한다.

## 5. Energy anchor seam 및 ledger 부호

에너지 경계의 양쪽 값을

\[
E_j^-=E_{0,j}e^{-h_j},\quad E_j^+=E_{0,j+1},\quad
d_j=E_j^+-E_j^-
\]

라 하자. Photon number가 연속이고 captured event anchor가 energy를 바꿀 때 stock energy jump는

\[
J_j^{\mathrm{anchor}}=d_jP_{j,h}.\tag{17}
\]

이다. Local energy ledger \(E^-P_h-E_0P_a+B+Z-Q_E=0\)를 합하면 내부 경계에서 \((E_j^--E_j^+)P_j=-d_jP_j\)가 남으므로 전체 ledger는

\[
E_{m,h}P_{m,h}-E_{0,1}P_{1,a}
+\sum_{j=1}^{m}(B_j+Z_j-Q_{E,j})
-\sum_{j=1}^{m-1}J_j^{\mathrm{anchor}}=0.\tag{18}
\]

즉 **왼쪽에서 anchor를 뺀다**. 이를 redshift나 heat에 흡수하면 물리적인 observable 정의를 바꾸므로 별도 표현/anchor ledger로 둔다.

Correction이 exact frozen 기준 \(e_{j,h}=P_{j,h}-F_{j,h}\)이면 anchor correction은 \(d_je_{j,h}\)이고 anchor baseline은 \(d_jF_{j,h}\)다. Native baseline \(d_jn_j\)를 쓸 때는

\[
J_j^{\mathrm{anchor}}-d_jn_j
=d_j(e_{j,h}+\rho_{P,j})\tag{19}
\]

로 representation correction까지 포함한다.

Signed anchor difference에 대한 interval \(D_j\ni d_j\), photon 또는 해당 correction에 대한 중심 \(c_j\), 반경 \(\eta_j\)가 있으면 direct interval product

\[
D_j\,[c_j-\eta_j,c_j+\eta_j]\tag{20}
\]

가 포함관계를 보존한다. Scalar 중심 \(\widehat d_j\)도 사용한다면

\[
|d_je_j-\widehat d_jc_j|
\le |\widehat d_j|\eta_j+|c_j|\eta_{d,j}+\eta_{d,j}\eta_j\tag{21}
\]

이며 \(|d_j-\widehat d_j|\le\eta_{d,j}\)다. 마지막 cross term을 버리면 일반적으로 유효하지 않다. 상계 \(\operatorname{upper}|D_j|\eta_j+|c_j|\eta_{d,j}\)도 유효하다. ΔE가 작아도 exact-lift 차이가 0임을 증명하기 전에는 삭제하지 않는다.

## 6. 가장 작은 실제 seam 집합

기존 OFF capture의 다음 두 photon track만 사용해 모든 새 구조를 판별할 수 있다.

| Track | Ordered segment IDs | 경계 의미 |
|---|---|---|
| OFF / node 0 | (step1,seg0) → (step2,seg0) → (step2,seg1) | macro stage 경계, 그 뒤 source-on → source-off |
| OFF / node 700 | (step1,seg0) → (step2,seg0) → (step2,seg1) | macro stage 경계, 그 뒤 HeI active → inactive; source는 계속 on |

두 track에 필요한 **6개 captured row와 OFF stage 2개**는 이미 보존되어 있다. 네 seam 모두 exact binary64 lift에서 `n_prev == f0_next`, `b_prev == a_next`가 성립한다. Node 0의 `anchored` flag는 모두 0이지만 roundoff에 의한 비영 energy seam은 남는다. Node 700은 step1에서 0, step2의 두 segment에서 1이다. 따라서 flag만 보고 energy seam 항을 제거하면 안 된다.

100-digit Decimal 단일 평가로 관찰한 ΔE의 **진단값**은 다음과 같다. 이 표는 rigorous interval certificate가 아니며 main candidate의 outward interval이 실제 상계의 근거가 되어야 한다.

| Seam | ΔE [eV], diagnostic |
|---|---:|
| node0 step1 → step2 | −1.1100609783191341e−15 |
| node0 step2 seg0 → seg1 | +7.4169661253990395e−16 |
| node700 step1 → step2 | +2.6507244472255264e−15 |
| node700 step2 seg0 → seg1 | −2.1170252325525803e−16 |

Native stock expression \(u/\epsilon-E_hn\)의 같은 진단은 약 10⁻²¹–10⁻²⁰ eV 규모의 비영 값을 준다. 이 크기를 물리적 budget 또는 roundoff 전체 상계로 사용하지 않는다.

## 7. 남는 경계

이 합성식은 coefficient error가 perturbative하게 작은지를 요구하지 않고 유효한 upper bound를 준다. 하지만 incoming \(e_a\)를 \(O(1)\)로 고정하면 \(S\int|T_X|\)의 일부가 coefficient variation에 대해 \(O(\varepsilon)\)다. 이를 일률적인 2차 correction이라고 부를 수 없다. Incoming을 \(O(\varepsilon)\)로 제한할 때에만 해당 remainder의 2차 해석을 회복한다.

두 track의 실제 interval 실행과 독립 decision이 없으면 이 문서만으로 track certificate를 주장하지 않는다. 두 track이 인증되어도 full spectral aggregate, 전체 gas path, 실제 atomic source 및 receiver adoption의 상태는 바뀌지 않는다. `baseline_RCT=OFF`, actual photon/heat/recoil `null`, physical/production `HOLD`, HE-F2/F09 `OPEN`, receiver `SEPARATE`, legacy Gamma alias `3.543295 FAIL`을 유지한다.

## 8. 실제 exact toy 검산

`exact_incoming_anchor_toys.py`는 모든 계수를 `fractions.Fraction`으로 표현하고 \(T=e^{-1}\)의 다항식을 정확히 다룬다. 초월함수의 부호 판별에는 \(e\)의 12차 Taylor 부분합과 \(\frac{1/13!}{1-1/14}\) remainder 상계를 역수로 취한 유리수 interval만 사용했다. 후보 코드, Decimal, binary64 exp를 import하거나 실행하지 않았다.

**실제 92개 검사 PASS, FAIL 0, exit 0, elapsed 0.11691090399835957 s, child peak RSS 10,880 KiB.** 실행 전후 source SHA가 동일하다. Source SHA256은 `797f71c8a532f558972ca3467811f1cd0bf6aa24b556ef0bf9f3a13e942f9e9c`, 결과 SHA256은 `e42b33c7fb13c6afc978734daa6c699c2f9402fffb3f193bf1e135e94369677a`다. 실제 argv·host·시각·exit·source identity는 `EXECUTION.json`에, 모든 판별식은 `EXACT_TOY_RESULTS.json`에 있다. 최초 과학 실패는 없었다.

| 판별 대상 | Exact control의 결과 |
|---|---|
| Constant coefficient, \(c=1/7,\eta=1/8\), \(L=h=1\) | Coefficient variation이 0이어도 endpoint·species·energy·heat·redshift incoming uncertainty가 남는다. 모든 gain identity와 nonzero-incoming ledger를 정확히 확인했다. |
| Total count에 photon bound를 복사 | Count uncertainty \(\eta(1-T)\)는 endpoint bound \(\eta T\)보다 엄밀히 크므로 누락을 검출한다. |
| 누적 moment 오차 | 이전 누적 오차에 \(T\)를 곱하는 잘못된 damping이 엄밀히 작은 상계를 만든다. |
| 두 segment의 native 표현 | \(\rho_P\)와 optional nonzero \(\kappa\)를 운반해야 다음 초기 defect 및 최종 native output 차이가 일치한다. |
| Native energy stock | \(\rho_U\)에는 \(E_hn-U_{\mathrm{cap}}/\epsilon\)가 필요하다. \(E_h\rho_P\)만 쓰는 누락을 검출한다. |
| Native local correction ledger | Number·energy correction ledger는 captured residual의 음수이며 일반적으로 0이 아니다. |
| Positive/negative energy anchor | Global energy ledger는 signed anchor를 뺄 때 정확히 0이다. Native anchor correction에는 \(\rho_P\)도 필요하다. |
| Anchor product uncertainty | Positive, negative, zero central ΔE 모두 exact rational corner를 포함한다. Cross term \(\eta_d\eta\)를 버린 식은 엄밀히 실패한다. |
| \(\delta\Lambda=0\), nonzero incoming, species variation | Photon은 정확하나 \(R_{A_1}=\frac1{32}(1-2T)>0\), \(R_{A_2}=-R_{A_1}\), total absorbed remainder 0, total heat remainder \(+R_{A_1}\)다. Incoming이 고정되면 이 remainder는 coefficient variation에 선형이다. |

이 검산의 근거 상태는 **implementation-verified, exact toy scope**다. 실제 Verner coefficient의 inclusion, 새 interval 전파 코드의 정확성, NCP host parity 또는 full-path certificate를 대신하지 않는다.
