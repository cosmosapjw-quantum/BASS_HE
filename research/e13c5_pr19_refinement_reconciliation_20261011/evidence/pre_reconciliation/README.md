# BASS_HE E13C5 — incoming and anchor enclosure

OFF node 0과 700의 두 captured three-segment photon track에 incoming correction/error, cumulative moment error, exact-frozen/native representation, signed energy-anchor error를 전파한 연구 패키지다.

`REPORT_KO.md`는 실제 결과와 한계, `THEORY.md`는 유도, `INDEPENDENT_REVIEW.json`과 `INDEPENDENT_REVIEW_KO.md`는 별도 reviewer의 최종 판정이다. Numeric source/input을 검토한 사실과 전역 물리 유효성은 구분한다.

- 실제 실행: N32/P60, N128/P60, N512/P60, N32/P80. 각 실행에서 네 local enclosure를 새로 계산하고 동일한 두 E13C4 local enclosure를 재사용했다.
- Runtime: Python 표준 라이브러리만으로 과학 계산 및 NCP host parity를 실행한다. 이미 생성된 figure를 다시 그릴 때만 matplotlib/numpy가 필요하다.
- NCP: `NCP_LOCAL_CODEX_HANDOFF_KO.md`, `NCP_EXECUTION_CONTRACT.json`, `EXECUTION_LOCK.json`을 읽는다. `--execute` 없이 runner를 호출하면 과학 계산은 수행되지 않는다.
- 전달: NCP_READY 외부 묶음의 `00_START_HERE_KO.md`와 delivery receipt에 실제 Git core/ZIP/backup identity가 있다. 필요한 scientific inputs와 인계문은 모두 묶음 안에 포함된다.
- `evidence/ncp_boundary_fixtures/`의 작은 synthetic packages 및 실패 log는 runner 경계 검사다. 실제 NCP 실행 또는 물리 계산으로 세지 않는다.
- 보존된 independent control 최초 실패 두 종류는 test fixture 선택 및 audit field-name adapter 문제다. 현재 production scientific source/result 실패로 분류하지 않는다.

기존 기준은 `baseline_RCT=OFF`, actual atomic photon/heat/recoil `null`, physical/production `HOLD`, HE-F2/F09 `OPEN`, receiver `SEPARATE`, legacy Gamma alias `3.543295 FAIL`이다. 두 track 이외 full spectral/gas history나 native aggregate reduction은 인증하지 않았다.

Manifest와 hash는 파일 identity를 뜻한다. 과학적 admission은 독립 판정의 명시된 범위에 따른다.
