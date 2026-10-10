# BASS_HE E13C5 — PR19 후속 refinement와 계보 연결

현재 진입 문서는 **CONTINUATION_REPORT_KO.md**와 **NCP_LOCAL_CODEX_HANDOFF_KO.md**다. 이미 완료된 PR19의 선택 12-path E13C5 위에 OFF0/OFF700의 N512 refinement와 정확한 mode별 가중 reduction을 더한다.

- `LINEAGE_ADDENDUM_KO.md`: PR17 → PR18 → PR19 계보와 최초 intake 누락을 바로잡은 근거.
- `CONTINUATION_REPORT_KO.md`: 이번 실제 결과·유도·기존 결과와의 비교·의미와 한계.
- `REPORT_KO.md` / `THEORY.md`: 두 OFF 경로 incoming·representation·anchor enclosure의 상세 원기록.
- `INDEPENDENT_REVIEW.json`: 두-track 과학 판정.
- `INDEPENDENT_LINEAGE_REVIEW.json`: PR19 연결·exact reduction·새 NCP 실행에 대한 추가 독립 판정. 실제 파일의 판정이 admission을 결정한다.
- `NCP_CONTINUATION_CONTRACT.json` / `CONTINUATION_LOCK.json`: 새 NCP 실행의 source/input identity와 예산.
- `code/ncp_continue.py`: 기본값은 verify-only. `--execute`는 fresh N512 두 경로 계산 한 번 뒤 그 fresh 결과의 exact reduction을 순서대로 실행한다.
- `NEXT_DAG.json`: 선택 부분집합의 오차 예산과 아직 포함하지 않은 spectral node contribution의 계약이 다음 연구 질문이다.

Scientific archive와 NCP_READY 백업본에는 필요한 captured inputs·선행 결과·코드·리뷰·실행문이 모두 들어 있다. NCP_READY의 외부 `DELIVERY_RECEIPT.json`이 실제 Git core와 내부 scientific ZIP identity를 기록한다. 실행 당시 절대 경로는 provenance이며 새 runner는 이 패키지 내부 상대경로를 사용한다.

기존 `REPORT_KO.md`와 `PLAN.json`의 PR17 intake 및 E13C6 제안은 계보 복구 전의 기록이다. 최신 순서는 continuation 문서와 reconciled DAG를 따른다. 교체한 초기 README/DAG/handoff/state는 `evidence/pre_reconciliation/`에 보존했다.

범위는 고정된 captured gas·mask·source branch·energy anchor에서의 선택 경로 enclosure다. Full first2, physical/production, 실제 atomic photon/heat/recoil과 receiver adoption의 기존 HOLD/OPEN 경계는 유지된다. 저장 또는 Git publication을 실제 NCP 실행이나 recipient ACK로 세지 않는다.
