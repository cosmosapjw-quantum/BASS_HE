# E13C5 lineage reconciliation: 두 OFF track의 refinement를 기존 선택 집합에 넣기

## 상태와 범위

**근거 상태: derived, actual source read.** 이 문서는 연구 owner의 요청으로 작성한 이론 기여이며 기존 PASS의 재선언 또는 최종 decision review가 아니다. 새 coefficient/solver 실행과 원격 쓰기를 수행하지 않았다. 실제 Fraction identity·containment·reduction 계산은 별도 recurrence contributor의 산출물이 판정한다.

직접 읽은 원본은 기존 PR19의 `first2/cover.py`, `CONTRACT.md`, `REPORT.md`, `NEXT_DAG.json`, `START.json`, `independent_review.md`, `RESULTS.json`의 schema·selector·첫 path 전체 summary, PR18의 `pilot/pilot.py` 전체, 새 `code/path_enclosure.py` 전체와 `PLAN.json`, 새 `N512_P60.json`의 schema다. 실제 읽은 파일 identity는 `READ_IDENTITIES.json`에 보존한다. 기존 review 파일은 controller-delivered 결과의 transcription임을 명시한다. 따라서 이 문서에서는 이를 독립 검토가 새로 이루어진 근거로 취급하지 않는다.

기존 결과는 \(m\in\{\mathrm{OFF,KF,GM}\}\), \(p\in\{0,700,1620,2344\}\)의 **12개 captured path / 36 segments**, N128/P60다. 새 결과는 같은 OFF node 0과 700의 3 segments씩을 N512/P60으로 둘러싼 refinement다. 기존 12-path 실행을 이번 턴의 새 과학 실행으로 세거나, 다음 미실행 과제로 다시 지정하지 않는다.

## 1. 합성 전에 확인할 동일한 exact target

두 archive에서 같은 이름을 쓴다는 사실만으로 semantic equality가 성립하지 않는다. 교체 대상 두 path에 대해 다음 입력 정의가 같아야 한다.

1. `(mode,node,step,segment)`의 정확한 선택과 순서, 시작 photon stock, source switch와 opacity masks.
2. Captured row 및 stage의 exact binary64 lifts: affine gas endpoints, \(a,h,E_0,f_0,q_f,\lambda_{if}\), \(\eta\), positive quadrature weight.
3. 동일한 inherited `Coefficients`·`integrands`·`directed_interval` 정의. Constants, Verner fit, c/H normalization, epsilon, binding energies 및 branch cutoffs가 바뀌지 않아야 한다.
4. Photon continuous seam, 매 adjacent seam의 \(E_{\mathrm{next},0}-E_{\mathrm{prev},h}\) anchor, outflow 0 및 initial incoming defect 0.
5. Moment target은 captured segment 값을 exact-lift하고 합한 reference와 비교한 동일한 true integral이다. Native aggregate의 binary64 reduction과 spectral quadrature error는 별개의 target이다.

새 input key·stage/source identity와 기존 START/pilot PIN의 matching이 아직 계산되지 않았다면 이 항목을 `PENDING_EXACT_MATCH`로 둔다. Hash는 동일한 원본 bytes의 증거이며 실제 arithmetic inclusion의 대체물이 아니다.

## 2. 두 incoming 표현의 관계

기존 코드의 식은 incoming interval \(I_a\ni e_a\)에 대해

\[
C_X=J_X+g_XI_a+[-R_X,R_X],\qquad
S=\sup|I_a|+B_r,\qquad R_X=S T_X.
\]

새 코드는 \(I_a=c+[-\eta,\eta]\) 형태의 enclosure를 사용하여

\[
X_1\in J_X+g_Xc,\qquad
|X-X_1|\le |g_X|\eta+(|c|+\eta+B_r)T_X
\]

로 center와 radius를 나눈다. 두 방식은 같은 exact differential equation과 moment target을 둘러쌀 수 있다. Interval dependency와 rounding 순서가 달라 numerical endpoints는 같을 필요가 없다. **기존 \(g_XI_a\)에는 incoming uncertainty가 이미 들어 있으므로 추가 \(|g_X|\eta\)를 또 더하지 않는다.**

기존 cover는 species별 effective remainder를 합한다. 새 코드는 유효한 effective/triangle bound의 작은 값 및 direct total-count/total-heat bound를 사용한다. 이는 enclosure 폭과 계산 경로의 차이이며 정확한 count/heat 정의의 변경이 아니다. 새 total-count에서는 incoming gain이 \(1-e^{-Lh}\)이고 photon gain은 \(e^{-Lh}\)임을 유지한다.

### 실제 reuse guard의 제한

`cover.py`의 OFF700 reused incoming 검사는 `(Ia-old['Ia']).contains(0)`다. 이것은 두 interval의 **overlap**만 보장한다. 일반적인 reuse admission에는 현재 incoming interval이 reused certificate가 가정한 incoming 안에 포함되거나, actual endpoint equality가 성립해야 한다.

원본 `pilot.py`는 `DP=Pf-n+corrected_P`, `Pend=n+DP`, 다음 `Ia=DP+n-f0`를 사용하고 cover는 `Ia=previous_Pend-f0`를 사용한다. 동일 arithmetic 및 입력에서는 equality가 기대되지만 실제 저장 endpoints로 확인해야 한다. 이번 데이터에서 equality 또는 필요한 containment가 확인되면 이 약한 일반 guard가 이 세 reused 결과의 admission을 막지는 않는다. 확인되지 않으면 해당 reused path를 valid predecessor로 승격할 수 없다. 기존 guard를 수정했다는 선언만으로 이미 실행된 결과의 provenance를 변경하지 않는다.

원본 pilot의 `integrate`는 unchanged E13C4 Jet2 whole-cell range, signed midpoint sum과 \(hM_j/(24N^3)\) 반경을 N128에 적용한다. OFF700의 `source_on=True` 고정은 세 selected row의 실제 source branch와 일치한다. Pilot의 `frozen`, representation, incoming 및 anchor 식에서 새로운 물리적 모델 차이는 발견하지 않았다. 이는 actual source comparison 범위의 진술이며 전체 원자모델을 검증했다는 의미가 아니다.

## 3. 비교할 필드의 정확한 대응

| 기존 target | 새 target 및 변환 |
|---|---|
| Segment `Pend` | `outputs.P1.true_absolute_interval` |
| Segment `DP` | `outputs.P1.true_minus_captured_interval` |
| `continuous_minus_frozen[X]` | Exact continuous-minus-frozen target; 새 native-correction interval과 바로 비교하지 않고 representation을 일치시킨다. |
| `frozen_minus_captured[X] + continuous_minus_frozen[X]` | `outputs[X].true_minus_captured_interval` |
| `cumulative_correction[X]` | `cumulative_moment_corrections[X].interval` |
| `weighted_reduction[X]`, X는 moment/source | Positive weight × `true_moment_enclosures[X]` |
| `weighted_reduction.P_final` | Positive weight × `final_photon.true_absolute_interval` |
| `weighted_reduction.anchor` | Positive weight × `summed_true_anchor_eV` |
| `energy_endpoint_minus_captured_erg` | Exact lifted epsilon × 새 eV native energy-stock correction target |
| `captured_segment_to_node_reduction` | 변하지 않은 capture input의 별도 representation record로 보존; 새 solver 결과로 대체하지 않는다. |

기존 reduction에는 dedicated `H_total_eV`가 없다. 총 heat를 비교하려면 기존 species heat interval의 합과 새 dedicated total-heat interval이 **같은 exact species sum**을 가리킨다고 명시한다. 두 interval의 폭과 endpoints가 같아야 하는 것은 아니다. Dedicated total route를 새 field로 제공하면, species interval의 합에서 계산한 total route와 구분하여 기록한다.

Native energy endpoint는 \(U_{\rm cap}/\epsilon\)와 \(E_hn_{\rm cap}\)의 차이를 포함해야 한다. 기존 output의 erg quantity와 새 eV quantity를 number interval처럼 직접 비교하거나 epsilon을 두 번 적용하지 않는다.

## 4. Positive-weight replacement theorem

각 mode의 선택 집합을 \(S_m=\{0,700,1620,2344\}\), 정확한 positive weight를 \(w_{m,p}>0\), observable exact value를 \(X_{m,p}\)라 하자. Mode는 서로 다른 gas history이므로 **OFF/KF/GM를 하나의 물리적 합으로 합치지 않는다.** 저장된 구조도 mode별 세 reduction이다.

\[
M_{m,X}^{\rm sel}=\sum_{p\in S_m}w_{m,p}X_{m,p}.
\]

기존 인증 interval을 \(I^{128}_{m,p,X}\), 새 두 OFF interval을 \(I^{512}_{\mathrm{OFF},p,X}\)라 하면 교체 aggregate는

\[
I^{\rm replace}_{\mathrm{OFF},X}
=\sum_{p\in\{1620,2344\}}w_{\mathrm{OFF},p}I^{128}_{\mathrm{OFF},p,X}
+\sum_{p\in\{0,700\}}w_{\mathrm{OFF},p}I^{512}_{\mathrm{OFF},p,X}.
\]

KF/GM의 네 path는 그대로다. 각 chosen interval이 같은 exact target을 포함하면 양의 scaling과 Minkowski sum이 위 aggregate의 inclusion을 보장한다. 새로운 source/coefficient evaluation은 필요하지 않는다. 저장된 decimal endpoints와 exact-lift weight를 Fraction으로 읽어 endpoint를 정확히 더하고, decimal artifact를 출력한다면 마지막 변환만 outward로 시행할 수 있다.

이미 rounded aggregate에서 old interval contributions를 빼는 `old_aggregate-old_path0-old_path700+new_path0+new_path700`는 불필요한 dependency inflation을 만든다. Endpoint만 교체하는 임의 조작은 정당한 interval subtraction조차 아니다. **유지하는 path record에서 합계를 재구성한다.**

### Compatibility, containment, validity의 분리

- \(I^{512}\cap I^{128}\ne\varnothing\)는 같은 exact target이라는 가정 아래 numerical compatibility다. 이것만으로 어느 interval의 validity도 증명되지 않는다.
- \(I^{512}\subseteq I^{128}\)가 성립하면 같은 target에 대해 enclosure를 좁혔다는 더 강한 진술을 할 수 있다. 전 path/observable의 실제 endpoint 검사 결과에 제한한다.
- 새 interval이 old interval 안에 들어 있지 않아도 독립적으로 valid하다면 replacement는 가능하다. 이 경우 `nested refinement` 또는 old aggregate 전체에 대한 containment를 주장하지 않는다.
- 두 interval이 disjoint하면 단순 폭 비교로 선택하지 않고 definition, arithmetic, data identity 또는 representation mismatch를 조사한다. 명확한 근거 없이 midpoint를 평균내거나 hull로 넓혀 failure를 숨기지 않는다.
- 두 valid interval의 intersection도 same-target theorem으로 valid하지만 이는 별도의 결합 방법이다. 이번 교체 계약의 primary는 새 path interval로 대체하는 것이며 사후 intersection을 조용히 추가하지 않는다.

Count/energy/heat ledger interval이 zero를 포함하는 것은 필요한 consistency evidence다. 폭이 넓은 interval의 zero inclusion 하나는 error budget 또는 물리 precision의 입증이 아니다. Cross-output correlations를 실제 joint uncertainty distribution이나 parameter posterior로 해석하지 않는다.

## 5. 교체 이후 남는 과학적 질문

이미 확보된 결과는 선택된 네 energy location의 mode별 합이다. 이를 full first2 quadrature sum으로 확장하려면

\[
M_{m,X}^{\rm full}
=M_{m,X}^{\rm sel}
+\sum_{p\notin S_m} w_{m,p}X_{m,p}
\]

의 complement를 인증해야 한다. 특히 **continuous-minus-native correction은 signed**이므로 selected correction의 작음, 같은 부호 또는 threshold별 대표점 선택으로 missing-node correction을 제한할 수 없다. 기존 branch-cover points의 enclosure를 줄이는 것과 아직 포함되지 않은 spectral weight를 인증하는 것은 서로 다른 작업이다.

따라서 다음 작은 과제는 기존 결과만으로 (a) mode/path/observable별 weighted width, (b) incoming·local midpoint·coefficient remainder·representation·anchor의 남은 budget을 가능한 분해 범위에서 기록하고, (c) unselected complement를 제한하는 향후 계약의 필요 입력·branch partition·상계를 정하는 것이다. Existing output이 특정 budget을 따로 저장하지 않았다면 `NOT_IDENTIFIABLE_FROM_SAVED_FIELDS`로 두고 가짜 기여율을 만들지 않는다.

Full first2 solver expansion은 이 문서의 execution action이 아니다. 다음 실제 계산을 정할 때는 complement coverage가 필요한지, 기존 selected subset의 dominant numerical radius를 줄이는 것이 필요한지 먼저 구별하고 별도의 resource-bound contract에 묶는다. `E13C6` 번호를 자동으로 만들거나 이미 수행된 12-path cover를 다시 실행하지 않는다.

## 6. 이론 기여의 완료 기준

이 문서는 exact identity admission, direct-Ia/center-radius compatibility, representation field mapping, mode별 positive-weight theorem, reuse overlap caveat와 다음 연구 경계를 고정했다. 실제 old/new endpoint match, revised weighted reduction, source-bound carry reuse 그리고 최종 독립 decision은 별도 evidence가 통제한다. Physical/production HOLD, actual atomic moments null, HE-F2/F09 OPEN, receiver SEPARATE, legacy Gamma alias 3.543295 FAIL은 그대로다.
