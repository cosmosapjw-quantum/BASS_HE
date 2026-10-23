# 실행자 인계 — 저장 증거 검증이 기본 행동

대상은 `cosmosapjw-quantum/BASS_HE`, branch `research/he-ang-provider-contract-20261023`, unit `research/he_ang_provider_contract_20261023`이다. `delivery/PUBLISHED_PINS.json`의 과학 pin과 이후 delivery pin을 구별한다. 실제 branch HEAD가 expected와 다르면 차이를 먼저 읽고 lease를 갱신한다. 기존 source/suite를 재작성하거나 반복 실행하는 지시가 아니다.

```text
1. 현재 AGENTS와 실제 Git HEAD, 중앙0f9d 고정 계약 및 병렬 owner 변경을 읽는다.
2. 최종 capsule SHA256과 내부 MANIFEST를 검증하여 새 경로에 복원한다.
   unit/와 stage_archives/를 함께 보존한다. 원래 절대경로가 없어도
   verify_saved.py --archive-dir <stage_archives>가 저장 archive를 찾는다.
3. unit의 CONTRACT.json/BUDGET.json/RESOURCE_LEDGER.json을 비교한다.
   3개 START/FINISH, 실패0, unknown0인 이번 단위의 누적 비용을 보존한다.
   이전 단위의 UNKNOWN_NOT_ZERO 기록은 별도 intake에 남아 있다.
4. 기본 실행:
   python <unit>/verify_saved.py --unit <unit> --archive-dir <stage_archives>
          --output <새로운 검증 보고서 경로>
   저장 manifest/receipt/archive/20단계 ACK를 읽는 명령이며 과학을 실행하지 않는다.
5. PASS_SAVED_EVIDENCE 이후 결과를 재사용한다. code/controls.py,
   theory/check_witness.py, code/compare_saved_witness.py를 재실행하지 않는다.
6. 새 과학 실행은 변경된 dependency와 별도 source-admission 계약을 먼저 명시한다.
   frozen 계약·허용 범위·누적 예산·실제 입력 hash·oracle·출력 책임이 정해진 뒤
   run_bounded.py와 append-only receipt를 사용한다. 실패를 삭제하거나 비용을0으로
   바꾸지 않는다. 명목 잔여 예산을 다른 연구 단위에 전용하지 않는다.
7. 독립 검토 완료된 변경만 expected-SHA push한다. no_merge/no_activation 유지.
```

호스트 문제가 있으면 해당 환경 경계만 최소 수정한다. 물리 전제·오차·허용 판정·substantive 설계 변경은 연구 대화로 돌려 근거와 새 DAG를 정한다. 이 실행자 handoff의 목표는 실제 source/frame/event 증거를 이어 쓰는 것이며 기존 연구를 재시작하는 것이 아니다.
