# HE29 64코어/128 GB 후속 최적화 연구

2026-10-21 KST 시작. 기준 publication은 `a02ae998570d5a0a4fffdf46299ee77b1c738759`다. 이번 단위는 physmath-research-loop plugin 1.3.0의 새 이론/코딩 연구이며, 이미 끝난 연구·검증은 재사용한다. 초기 standalone 1.0.0 이력과 구분한다.

## 먼저 읽은 실제 변경분

GitHub의 BASS_HE 85개 branch, PR78/79/80, 관련 저장소의 정해진 branch/PR/Actions 범위와 백업 변경분을 읽었다. 최신 관측 범위에서 새 HE29 반환은 발견되지 않았다. 다른 대화 조회는 실제 서비스 오류를 반환했다. 모든 대화나 미게시 실행의 부재를 뜻하지 않는다. 자세한 범위·pagination 한계·실패는 `evidence/*DELTA*`, `PENDING_INVENTORY.json`, `PERSONAL_CONTEXT_RAW.json`에 보존한다.

## 실행 상태

기존 네 Radau+DOP853 기준해는 4/4 admitted, 하나의 runtime cohort다. 원래 09929 분석은 그대로 재사용한다. 과거 ABI1/ABI2 인계를 중복 제거하면 실행 준비가 된 미완료 HE29 과학 작업은 r4/table512 packed canary 한 개다. 다른 모델의 오래된 NOT_RUN이나 연구 HOLD를 임의로 실행 대기열에 넣지 않는다.

이번 NCP 제출·시작은 0, 원격 프로세스는 UNOBSERVED다. Remote Desktop Commander는 호출하지 않는다. 새 controller는 접근 가능한 NCP 실행자가 실제 프로세스/저장 결과/CPU affinity/cgroup/메모리를 관측하고 중복 실행을 차단하도록 준비한다.

## 진행 중인 새 변경

1. proper-time source table의 독립 행을 spawn worker로 계산하고 원래 순서로 조립한다. 같은 runtime/source/spec 및 원래 전체 table SHA를 만족하는 cache만 재사용한다.
2. native protocol의 수치 호출과 순서를 유지하면서 기록의 flush/fsync를 묶는다. 정상 종료·segment·실패 경계에서 확정한다. hard kill 시 마지막 확정 이후 최대 B−1개의 성공 반환 기록이 durable하지 않을 수 있다는 변경된 계약을 명시한다.
3. host 자원과 기존 작업을 먼저 읽고, table/build 병렬도와 solver thread1을 구분하는 실행 경로를 준비한다.

소규모 검증·제조 I/O 측정은 실제 HE29 canary 속도와 구분한다. 원래 물리식·반응률·허용치·admission gate와 full-state 19-ledger norm은 유지한다. 현재 단계별 게시·백업·R/C 상태는 `DAG_STATUS.json`, `DELIVERY.json`에 기록한다.
