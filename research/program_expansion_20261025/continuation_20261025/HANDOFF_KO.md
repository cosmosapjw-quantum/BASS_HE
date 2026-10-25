# BASS_HE 후속 연구 인계 — HE-EXP-INTAKE-01

이 파일은 고정 인계 c456b05e0f1c53faa3ae36720826f43e57c06a91의 후속 기록이다. 현재 코드·원자료·검증은 이 디렉터리에 있고 게시/백업의 실제 SHA와 provider ACK는 delivery/ 기록을 사용한다. 작성 시점의 전달 단계는 진행 중이며 실제 ACK 이후 갱신한다.

## 먼저 읽기

1. 현재 AGENTS.md, research/program-expansion-20261025의 실제 HEAD, HE101 owner research/he-ang-finitemass-cba-20261025의 실제 HEAD, 다른 owner PR과 WU/REC/CR 입력 변화.
2. RESULT.json, RESULTS_KO.md, DAG.json, LOOP_PROGRESS.json.
3. evidence/validation/RESOURCE_LEDGER.json, pair_source/reviews/INDEPENDENT_REVIEW_FINAL.json, exchange/PAIR_INDEPENDENT_REVIEW.md.
4. species/SPECIES_PROVIDER_REGISTRY.json, species/EXPLICIT_TRANSPORT_SOURCE_INVENTORY.json, sources/SOURCE_PROVENANCE.json.
5. pair_source/SELECTED_H_HE_SOURCE.json, pair_source/THEORY_KO.md, exchange/THEORY_KO.md.
6. evidence/inherited/HE101_RESOURCE_LEDGER.json 및 HE101_CLAIM_GATE.json; 소진 비용과 열린 C8을 그대로 보존한다.

## 재사용할 완료 결과

- WU32 supplied rows: atomic charge20+n1+electron pool2+synthetic extension9. 합성 확장을 실제 공급자로 승격하지 않는다.
- 실제 elemental scalar provider18(PI6/RR6/CI6), explicit transport27pairs/243Q expressions. Thermal-integral/DCS/joint-law 타입을 유지한다.
- H–He9Q행 및 기존Q11/Q22 일치. source Tstar50–50000K, 외삽0, 새fit평가0.
- 조건부 finite-mass moment map, Maxwell heat/linear drag 유도, thermal count/Cv/internal/binding/nonthermal ownership, common-bulk drift tensor 구현.
- 31 distinct methods에 대한 최종 scoped evidence. 실제36method-executions/5process outcomesPASS/PASS/PASS/FAIL/PASS. 원04FAIL은1ULP exact-equality oracle 문제이며05는해당1method만PASS. 원failure code/test bytes도04디렉터리에 보존.
- 검증 실행 구간 CPU0.282464889/wall0.280453644998488s, cap8/30, repairused1/verificationcontinuation1. 준비·모델·provider·IO는 별도이며 UNKNOWN_NOT_ZERO를 보존한다. 기존 allocation을 새 이름으로 초기화하지 않는다.
- Source compiler249-check, HE34/35, HE101 suite 재실행0. HE101C8PARTIAL_EXPORT/19of20/reserve0/actualPASS_FAIL_FAIL은 그대로다.

## 정확한 다음 작업

WU의 실제 isotope/state/mass 자료와 선택된 H–He source label의 대응을 결정하고, 선택 Tstar에서 실제 Qbar11 값과 calibrated source uncertainty를 공급한다. 준비된 pair_source/conditional_h_he_moments 인터페이스는 그 입력을 받는다. 물리적 평가에는 해당 source-validity 계약과 별도 명시 수치 allocation을 먼저 고정한다. 위 구현 검증의 남은 초를 physical campaign 예산으로 바꾸지 않는다.

조건부 유도:
Tstar=(mbTa+maTb)/(ma+mb), mu=mamb/(ma+mb),
gbar=sqrt(8kBTstar/(pi mu)),
G=4kB na nb mu/(ma+mb) gbar Qbar11,
Qa=G(Tb−Ta), Qb=−Qa,
K=(4/3)na nb mu gbar Qbar11.
열식은zero drift, K는small-drift1차다. Finite-drift O(U²) heating은 별도 same-event 분배를 필요로 한다.

다음 source가 scalar rate/thermal integral만 제공하면 full differential law나 recoil cross moment를 채우지 않는다. Mass number A를 kg mass로 사용하지 않는다. REC-HD parser는 REC owner가 제공하며 p/o-H2, exact50/100/200K와 미확정 vibrational state를 유지한다. WU nuclear/weak daughter payload와 CR stopping은 선택한 채널에서만 조건부 의존한다.

열 count는 thermal pool의 Gamma_th다. Nonthermal birth를 즉시thermal count/heat로 더하지 않는다. Population-derived binding/internal/rest energy의 derivative witness와 별도 evolved RHS를 중복 소유하지 않는다. Common-T/u reduction은 실제 시간척도·관측량 오차가 필요하다.

## 게시와 보존

검증된 확장 경로만 additive 갱신하고 expected SHA/force=false를 사용한다. HE101 owner나 다른 owner branch를 수정하지 않는다. 소스 ZIP은 이 작업의 재현 가능한 소스·입력·검증 패키지이며 전체 저장소 Git history archive는 아니다. 두 provider 성공 응답·ID·size를 확인한 뒤에만 이중 백업으로 표시한다. 원 source PDF는 공개 재배포하지 않는다.

physical_provider_admitted=false, global_physical_completion=null, L4_ready=false, production=NOT_APPROVED, activation=false를 유지한다.

