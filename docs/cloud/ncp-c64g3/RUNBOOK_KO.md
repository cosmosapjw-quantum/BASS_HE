# c64-g3 Python 실행기 runbook

이 실행기는 `plan` commit `4e775fdb61e72fd75f956fe0a83064e37e0522da`에서 분기한 구현이다. 과학 기준은 `ac09160bae74f051e5e2e17d8a1cde4084576c16`이다. 현재 과학 PROMOTE는 HOLD다. Eq55, 새 production transport, full-Nmax, continuum 계산은 실행 대상이 아니다.

## 로컬 확인

Python 3.11 이상에서 격리 venv를 만들고 `python -m pip install -e '.[cloud,test]'`를 설치한다. `python scripts/run_cloud_replay.py preflight`는 checkout과 실행 binding을 출력한다. `python -m pytest -q tests/cloud`는 실행기 계약과 장애 주입을 검증한다.

`docs/cloud/ncp-c64g3/RUN_PROFILE_DESIGN.json`은 실행 profile이 아니다. `preflight`가 출력한 `source_commit`을 그대로 사용해 별도 JSON을 만든다.

```json
{"source_commit":"<preflight의 source_commit>","backend":"python","storage_mode":"local_sandbox"}
```

로컬 bounded scratch에서 `python scripts/run_cloud_replay.py run --profile /tmp/profile.json --out /tmp/bass-he-run-001 --workers 2`를 실행한다. `run`은 기존 run을 덮어쓰지 않는다. 중단 후에는 `python scripts/run_cloud_replay.py resume --out /tmp/bass-he-run-001`을 사용한다. `status --out ...`는 DB와 결과 파일을 reconcile하고, `export --out ...`는 SQLite 일관 snapshot과 완료 결과만 새 checkpoint에 담는다. `resume --retry-failed --out ...`는 기록된 runtime 실패에 한해 명시적으로 최대 한 번 더 시도한다. 과학 거절은 retry하지 않는다.

`run`은 control/wrong-pair, 7 endpoints, 14 D0, 42 finite-rho case 순서로 barrier를 통과한다. 32/64 panel은 서로 다른 case로 계산한다. 완료된 결과는 검증 후 재사용한다. RUN_BINDING 불일치나 payload 손상은 중단한다.

## NCP host에 적용할 때

이 repository만으로는 host 접근, VM 사용 예산, mounted volume, provider credentials가 주어지지 않는다. host 담당자가 승인된 c64-g3 identity와 예산, `/srv/bass-he` ext4 데이터 mount, non-root `bass-he` 계정, pinned checkout/venv를 확인한 뒤 `storage_mode`를 `mounted_host`로 설정한다. profile에는 실측 `worker_rss_p95_bytes`를 추가한다. `run --workers N`의 초기 상한은 32이며 실제 dispatch는 affinity, cgroup CPU/memory와 ready case 수로 제한된다. unknown limit 또는 mount 부재는 차단된다.

`deploy/ncp-c64g3/bass-he-replay@.service`는 설치 전 참고 template이다. 해당 host에서 `bass_he.cloud.resources.inventory()`와 `render_service(profile, host)`로 실제 bytes 기준 MemoryHigh/MemoryMax가 들어간 unit을 생성하고 검토한다. 이 작업에서는 service 설치·시작, SSH 단절/reboot 검증을 하지 않았다. 결제 대상 cloud replay와 calibration은 별도 host admission 뒤 실행한다. Codex 세션을 supervisor로 사용하지 않는다.

checkpoint export는 로컬 파일 생성까지 지원한다. provider adapter contract는 `upload_segment(path, expected_digest) -> ProviderReceipt`이다. 연결된 두 provider 및 자격 증명이 없으므로 Google Drive/Dropbox ACK와 실제 독립 restore는 미수행이다. upload ACK는 restore 검증을 뜻하지 않는다.

Numba 원본 source/tests/lock이 없으므로 명시적 `numba` 요청은 `ACCELERATOR_PAYLOAD_UNAVAILABLE`로 실패한다. Python backend만 지원한다. 과학적 독립 검수와 PROMOTE는 실행기 PASS와 별개다.

host admission 후 calibration은 승인된 동일 stage의 `CaseSpec` JSON 배열을 `--cases`에 주고 `python scripts/benchmark_cloud_workers.py --profile /srv/bass-he/profile.json --cases /srv/bass-he/approved_cases.json --out /srv/bass-he/runs/calibration-001`로 시작한다. 각 arm은 새 PERF namespace에서 3회 실행하며, 과학 결과 개수에는 넣지 않는다. 현재 환경에서는 host/예산 부재로 실행하지 않았다.
