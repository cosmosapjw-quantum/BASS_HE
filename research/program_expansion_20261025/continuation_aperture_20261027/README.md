# HE-EXP-APERTURE-07

유한 lab 극각창의 CM 역상과 같은 사건의 두 딸입자 관측을 정확한 유리수 하한·상한으로 계산한다. γ,a와 양성 Bernstein 밀도를 고정한 조건부 reference이며, 실제 M0475 normalization·full angular law/flux·deuteron deposition은 계속 열린 물리 입력이다.

선택된 실행 범위는 이론 R1–R10과 구현 C1–C10의 한 번의 루프다. 단계별 새 source checkpoint를 백업·게시하고, 실제 결과와 비용을 기록한다. 기존 ANGULAR06 5개 완료 제품을 계승하고 새 제품 3개를 추가하여 시작은 **5/11**, 세 새 제품을 검증하면 **8/11**이다. 중앙 원 DAG는 **28/88**, 이번 HE delta는 0이다. 서로 다른 DAG의 수를 더하지 않는다.

## 기준과 주요 파일

- 기준 local delivery: `d0477e8c5459ff41ac54ccf37cefe9ced009c1b9`.
- 게시된 동일 tree source P06: `12702837bf3b2dd2af6439efe08ec4088e3adc90`.
- 선행 central publication: `8af3e56dcaa27a8362b2bf74d6fb3c8edd859413`, actual expected `74aff0740d1812c732466563a9c66108a3a4d8fd`, force=false.
- `CONTRACT_KO.md`: 가정, 식, 숫자 모델, 정확도·자원 및 소유권.
- `LOOP_PROGRESS.json`: 실제 단계별 완료 근거. source/backup의 post-commit ACK는 외부 단계 영수증에 있다.
- `preflight/`: 게시 후 조사와 선행 publication 확인.

PHOTON05의 24/24 PASS, plotCPU4.40726504>4s FAIL, workflowPARTIAL과 당시4complete+1partial+3physicalopen/8을 보존한다. HE101 C8PARTIAL_EXPORT19/20 reserve0 PASS/FAIL/FAIL도 유지한다. 선행 science/test/plot·백업 재실행과 예산 초기화는 없다. 입자수·열용량·rest/binding·비열적 에너지의 단일 소유권을 유지한다.
