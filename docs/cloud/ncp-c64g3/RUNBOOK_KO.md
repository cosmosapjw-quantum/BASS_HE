# c64-g3 Python 실행기 runbook

이 실행기는 `plan` commit `4e775fdb61e72fd75f956fe0a83064e37e0522da`에서 분기한 구현이다. 과학 기준은 `ac09160bae74f051e5e2e17d8a1cde4084576c16`이다. 현재 과학 PROMOTE는 HOLD다. Eq55, 새 production transport, full-Nmax, continuum 계산은 실행 대상이 아니다.

## 로컬 확인

Python 3.11 이상에서 격리 venv를 만들고 `python -m pip install -e '.[cloud,test]'`를 설치한다. `python scripts/run_cloud_replay.py preflight --env-out /tmp/ENV_PROVENANCE.json`는 checkout과 실행 binding을 출력하고 NumPy/SciPy/threadpoolctl 설치 distribution의 RECORD SHA256 및 BLAS 정보를 별도 artifact에 고정한다. `python -m pytest -q tests/cloud`는 실행기 계약과 장애 주입을 검증한다.

`docs/cloud/ncp-c64g3/RUN_PROFILE_DESIGN.json`은 실행 profile이 아니다. `preflight`가 출력한 `source_commit`을 그대로 사용해 별도 JSON을 만든다.

```json
{"source_commit":"<preflight의 source_commit>","backend":"python","storage_mode":"local_sandbox"}
```

로컬 bounded scratch에서 `python scripts/run_cloud_replay.py run --profile /tmp/profile.json --out /tmp/bass-he-run-001 --workers 2`를 실행한다. `run`은 기존 run을 덮어쓰지 않는다. 중단 후에는 `python scripts/run_cloud_replay.py resume --out /tmp/bass-he-run-001`을 사용한다. `status --out ...`는 DB와 결과 파일을 reconcile하고, `export --out ...`는 SQLite 일관 snapshot, run profile, event log와 완료 결과만 새 checkpoint에 담는다. Controller는 stage 완료 시와 실행 중 900초 경과 시 로컬 checkpoint를 자동 생성한다. `resume --retry-failed --out ...`는 기록된 runtime 실패에 한해 명시적으로 최대 한 번 더 시도한다. 과학 거절은 retry하지 않는다.

`run`은 control/wrong-pair, 7 endpoints, 14 D0, 42 finite-rho case 순서로 barrier를 통과한다. 32/64 panel은 서로 다른 case로 계산한다. 동일 run의 완료 결과는 검증 후 재사용한다. RUN_BINDING 불일치나 payload 손상은 중단한다. case ID의 `source`는 numerical dependency closure의 SHA256 identity다. solver/모델 계약/endpoint backend 변경 시 ID가 바뀌고 runner/store/docs 변경만으로는 바뀌지 않는다. 전체 checkout commit/tree와 실행 환경은 별도 ExecutionBinding에 남는다.

runner 변경 후 이전 run의 결과를 재사용하려면 새 profile과 새 run directory를 지정해 `run ... --reuse-evidence /tmp/old-run`을 명시한다. importer는 이전 committed payload·ledger SHA256·binding·과학 dependency closure를 검증하고 새 binding 결과에 `IMPORTED_EVIDENCE` provenance를 기록한다. old run은 수정하지 않으며 CLI의 `imported_evidence` 숫자는 fresh 계산 개수와 구분한다. 이 경로는 자동 fresh-current-run 승격이나 과학 PROMOTE가 아니다. 다른 과학 dependency의 증거는 거부한다.

## NCP host에 적용할 때

이 repository만으로는 host 접근, VM 사용 예산, mounted volume, provider credentials가 주어지지 않는다. host 담당자가 승인된 c64-g3 identity와 예산, `/srv/bass-he` ext4 데이터 mount, non-root `bass-he` 계정, pinned checkout/venv를 확인한 뒤 다음 순서로 진행한다. 이 문서의 명령은 host admission 후 사용하며 여기서는 유료 실행하지 않았다.

```bash
python scripts/run_cloud_replay.py preflight --env-out /srv/bass-he/runs/env-001.json
python scripts/run_cloud_replay.py calibrate-memory --storage-mode mounted_host --case control --out /srv/bass-he/runs/memory-001
```

`calibrate-memory`는 승인된 control case 하나를 별도 `PERF_MEMORY` namespace에서 한 worker로 실행한다. 0.05초 간격의 process VmRSS와 service-cgroup `memory.current`를 표본화해 sample count, interval, RSS peak/p95, service peak, 시작 시 controller memory, case/source/binding/thread identity를 `MEMORY_CALIBRATION.json`에 기록한다. 이는 과학 결과 개수에 넣지 않는다. 측정·case gate 실패, 표본 부족, mount/limit 문제는 `BLOCKED_MEMORY_CALIBRATION`이며 추정 RSS fallback이 없다. local sandbox에서도 `--storage-mode local_sandbox --out /tmp/memory-001`로 같은 CLI를 연습할 수 있다.

host runtime profile 예시는 다음과 같다. `worker_rss_p95_bytes`는 사람이 입력하지 않고 receipt에서 읽는다.

```json
{"source_commit":"<preflight의 source_commit>","backend":"python","storage_mode":"mounted_host","memory_calibration_receipt":"/srv/bass-he/runs/memory-001/MEMORY_CALIBRATION.json","controller_reserve_bytes":0,"memory_buffer_bytes":1073741824}
```

`python scripts/run_cloud_replay.py run --profile /srv/bass-he/profile.json --out /srv/bass-he/runs/replay-001 --workers 32`는 receipt의 binding/source/thread/hash를 검증한다. 메모리 계산은 실제 service-cgroup `memory.current`를 먼저 빼고, 향후 controller 성장 reserve와 미사용 safety buffer를 뺀 뒤 worker RSS p95로 추가 여유를 구한다. 현재 controller/worker는 이미 `memory.current`에 포함되므로 다시 빼지 않는다. spawn 전과 dispatch 때 같은 규칙을 적용한다. 0.65M 이상에서 새 dispatch를 멈추며 예상 점유는 0.75M 이하여야 한다. CPU affinity, ancestor/root cgroup limits, ready case 수도 상한이다. 이 중 필요한 값이 unknown이면 차단한다.

`deploy/ncp-c64g3/bass-he-replay@.service`는 설치 전 참고 template이다. 해당 host에서 `bass_he.cloud.resources.inventory()`와 `render_service(profile, host)`로 실제 bytes 기준 MemoryHigh/MemoryMax가 들어간 unit을 생성하고 검토한다. 이 작업에서는 service 설치·시작, SSH 단절/reboot 검증을 하지 않았다. 결제 대상 cloud replay와 calibration은 별도 host admission 뒤 실행한다. Codex 세션을 supervisor로 사용하지 않는다.

checkpoint export는 로컬 파일 생성까지 지원한다. provider adapter contract는 `upload_segment(path, expected_digest) -> ProviderReceipt`이다. 연결된 두 provider 및 자격 증명이 없으므로 Google Drive/Dropbox ACK와 실제 독립 restore는 미수행이다. upload ACK는 restore 검증을 뜻하지 않는다.

Numba 원본 source/tests/lock이 없으므로 명시적 `numba` 요청은 `ACCELERATOR_PAYLOAD_UNAVAILABLE`로 실패한다. Python backend만 지원한다. 과학적 독립 검수와 PROMOTE는 실행기 PASS와 별개다.

host admission 후 worker-count calibration은 승인된 동일 stage의 `CaseSpec` JSON 배열을 `--cases`에 주고 `python scripts/benchmark_cloud_workers.py --profile /srv/bass-he/profile.json --cases /srv/bass-he/approved_cases.json --out /srv/bass-he/runs/calibration-001`로 시작한다. 각 arm은 새 PERF namespace에서 3회 실행하며 과학 결과 개수에는 넣지 않는다. 32 초과 worker를 쓰려면 선택된 arm의 `ADMISSION_RECEIPT.json`을 명시해 `run ... --workers 40 --admit-calibrated-workers /srv/bass-he/runs/calibration-001/ADMISSION_RECEIPT.json`을 실행한다. receipt의 checksum, checkout/environment binding, thread policy, memory receipt가 다르면 거부한다. 42-case finite-rho stage에서 실제 동시 실행 상한은 ready count 42다. 48/56/64 arm 측정에는 그 이상의 승인된 PERF case 목록이 필요하다. 현재 환경에서는 host/예산 부재로 worker sweep 및 유료 replay를 실행하지 않았다.
