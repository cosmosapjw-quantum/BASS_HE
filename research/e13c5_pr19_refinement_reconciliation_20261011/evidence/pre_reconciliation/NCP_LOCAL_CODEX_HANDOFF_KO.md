# NCP local Codex handoff — BASS_HE E13C5

## 실행할 작업

BASS_HE의 `E13C5_FIXED_PATH_INCOMING_AND_ANCHOR_ENCLOSURE` 결과를 NCP 호스트에서 **동일한 두 track, N512/P60, 직렬 1회** 실행하고, 새 output 전체의 deterministic numerical projection을 봉인된 Chat 연구 결과와 대조한다. 새 연구 설계나 full first2 확장은 이 work unit에 포함되지 않는다.

사용자는 다음 물리 연구 루프와 그 NCP handoff를 요청했고, 전달에 필요한 파일을 백업에 모두 포함해 추가 ChatGPT 첨부 없이 실행할 수 있도록 요청했다. 이 NCP_READY 묶음에는 시작 안내, 이 인계문, 과학 패키지 ZIP, 실제 Git/backup identity가 담긴 delivery receipt가 함께 있다. `00_START_HERE_KO.md`에서 출발한다. 이전 E13C4 ZIP 또는 다른 첨부를 별도로 받을 필요가 없다.

실행자는 현재 실제 파일·접근 권한·호스트 상태를 확인한다. 아래 결과를 예상 PASS로 채우지 않는다. 기존 Drive/Dropbox 접근 또는 이미 내려받은 백업 파일을 이용한다. 접근이 없으면 `BLOCKED_ACCESS`와 실제 원인을 남기며, 실행했다고 쓰지 않는다. 계정·토큰을 출력하거나 새 권한을 만들어 우회하지 않는다.

## 기준 자료와 scientific ceiling

상속된 repository는 `cosmosapjw-quantum/BASS_HE`, branch는 `research/shared-c64-crossrepo-20260928`, PR은 17이다. E13C5 intake HEAD는 `8fc3fb14dd33da10efa86c97c4beb9b0d12eeaad`, 선행 E13C4 scientific core는 `d1bb3ff33b7a448e3c08fc7b41467e2a7f94a146`이다. **이번 E13C5의 실제 publication core와 archive hash는 외부 `DELIVERY_RECEIPT.json`의 `scientific_core_commit` 및 `scientific_archive` 필드를 읽는다.** 봉인 전 문서 안에 미래 commit이나 자기 ZIP hash를 미리 넣지 않는다.

복원 후 먼저 다음 파일을 읽는다.

1. `README.md`, `REPORT_KO.md`, `PHYSICAL_RESULT.json`
2. `PLAN.json`, `THEORY.md`, `NCP_EXECUTION_CONTRACT.json`
3. `INDEPENDENT_REVIEW.json`, `INDEPENDENT_REVIEW_KO.md`
4. `EXECUTION_LOCK.json`, `FILE_MANIFEST.json`, `NEXT_DAG.json`
5. 실행할 `code/ncp_execute.py` 및 `code/path_enclosure.py`

Independent decision이 `PASS_SCOPED`가 아니거나 blocking finding이 남아 있으면 실행을 중단하고 그 실제 상태를 반환한다. SHA는 identity 근거이며 과학 판정이나 사용자 권한을 스스로 만들어 주지 않는다.

이번 claim은 captured gas·source branch·opacity mask·energy anchor가 고정된 OFF node 0과 700의 세 구간 경로에만 적용한다. Primary initial defect는 각 track 첫 구간에서 정확히 0이다. 이후 incoming photon correction과 반경은 초기화하지 않는다. 누적 moment 반경도 감쇠하거나 버리지 않는다. Baseline moment는 captured segment increment들을 exact real로 합한 값이며, 모든 spectral node의 native aggregate reduction은 아직 인증되지 않았다.

보호 상태는 `baseline_RCT=OFF`, actual atomic photon/heat/recoil `null`, physical/production `HOLD`, HE-F2/F09 `OPEN`, receiver adoption `SEPARATE`, legacy Gamma alias `3.543295 FAIL`, uniform full-path certificate `false`다. E13C4 NCP 반환은 해당 시점의 scoped search에서 발견되지 않았다. 이것은 다른 곳에서 실행되지 않았다는 전역 증명이 아니다. 이번 E13C5 NCP job도 실제 실행 전에는 `NOT_RUN`이다.

## 완전한 입력과 실행 범위

| Track | 순서대로 실행할 captured ID | 포함된 경계 |
|---|---|---|
| OFF / node 0 | OFF/1/0/0 → OFF/2/0/0 → OFF/2/0/1 | stage 전환, source on→off |
| OFF / node 700 | OFF/1/700/0 → OFF/2/700/0 → OFF/2/700/1 | stage 전환, HeI active→inactive |

`inputs/PATH_CONTROLS.json`에 여섯 row와 stage 값이 들어 있다. 원시 OFF CSV와 그 identity도 포함되어 있다. `inputs/e13c4/N512_P60.json` 및 `inputs/e13c4/SIX_CONTROLS.json`은 동일한 두 local enclosure를 재사용하는 고정 입력이다. 따라서 한 번의 새 NCP 실행은 네 local integral을 새로 평가하고, 두 local integral을 재사용하면서 두 세구간 경로를 새로 조립한다. 새 coefficient evaluation 수는 4096이다. 이 재사용을 새 coefficient 계산 또는 새 E13C4 물리 실행으로 세지 않는다.

`directed_interval.py`와 `local_enclosure.py`는 선행 검토된 코드와 byte-identical이다. E13C5는 별도 `path_enclosure.py`에서 incoming gain, remainder, exact-frozen/native representation, energy-stock residual, signed anchor와 누적 moment를 결합한다.

## 복원과 호스트 확인

묶음을 별도의 새 디렉터리에 풀고, outer manifest와 scientific ZIP의 SHA-256을 delivery receipt와 비교한다. ZIP 내부 경로에 절대경로나 `..`가 없음을 확인한 다음 새 디렉터리에만 복원한다. 기존 결과 디렉터리에 덮어쓰지 않는다. 과학 패키지 manifest의 모든 payload hash와 `EXECUTION_LOCK.json`의 identity를 확인한다. 이 검사는 전송한 입력의 동일성을 확인한다.

과거 로그의 `/workspace/scratch/...` 경로는 Chat 연구 당시 기록이다. NCP에서 그 경로가 존재한다고 가정하지 않는다. 복원된 패키지 루트의 실제 절대 경로를 사용한다. Python은 **CPython 3.12.x**, 표준 라이브러리 `decimal`, `fractions`만 필요하다. Matplotlib은 이미 생성된 그림을 다시 그릴 때만 필요하며 이 NCP work unit에서는 그림을 재생성하지 않는다. 가상환경이나 global package를 바꿀 필요가 없다.

가용 CPU affinity, cgroup CPU/memory, Python/libmpdec 및 thread/MPI environment는 runner의 `HOST.json`으로 기록된다. 선택 layout은 process 1, thread 1, MPI 없음, memory limit 1 GiB, child wall timeout 180초다. `mpirun`이나 여러 worker를 붙이지 않는다. 다른 Python을 써야 한다면 실행 전에 가용한 3.12 interpreter를 선택한다. source/lock/baseline을 수정해 환경 차이를 숨기지 않는다.

## 실제 명령

Local Codex는 확인된 패키지 루트에서 아래 명령을 실행한다. `NCP_RESULT_E13C5_001`은 존재하지 않는 새 출력 디렉터리여야 한다. 이미 존재하면 그 결과를 보존하고 새로운 이름을 선택하되, 이전 물리 실행이 시작된 적 있는지 먼저 확인한다.

```bash
python3 code/ncp_execute.py \
  --out "$(pwd)/NCP_RESULT_E13C5_001" \
  --execute \
  --timeout 180
```

현재 작업 디렉터리를 바꾸지 않는 경우에는 `--package`에 복원된 루트의 실제 절대 경로를 지정하고, interpreter와 script도 확인된 경로를 사용한다. `--execute` 없이 실행하면 `VERIFY_ONLY_PASS`, `scientific_execution=NOT_RUN`, `new_result_accuracy=NOT_EVALUATED`다. 이 상태를 실제 재현 성공으로 쓰지 않는다. 준비 검사를 반드시 별도 한 번 더 실행할 필요는 없으며, `--execute` 실행 자체가 동일 preflight를 포함한다.

Runner는 source/inputs/PLAN/기준 결과를 먼저 검사하고, 새로운 `RESULTS.json`과 그 source identity를 검증한 다음 numerical parity를 계산한다. 다음의 모든 값은 comparison에 포함된다.

- 두 track의 모든 local integrals, derivative bounds, domain 기록
- incoming 중심·반경과 각 observable gain/remainder
- signed native representation, native energy-stock residual
- 네 anchor의 부호·interval endpoint products·다음 incoming
- 누적 count·energy·heat·redshift·source, 완성된 ledger
- input checks, 4096 새 coefficient 평가 수, 두 reuse 기록, rounding operation counts

제외되는 것은 environment, 절대 경로, 시작/종료 시각, elapsed time, RSS 같은 호스트 메타데이터뿐이다. 새로운 숫자를 저장된 결과로 복사하거나 baseline을 교체하지 않는다.

예상 numerical projection SHA-256:

`f4d0f8c7e37e5c8a013ab133af748173f3ef1a8247f413f4798fdb3518c04a86`

실제 NCP 성공 조건은 `PASS_SCOPED_HOST_PARITY`, `scientific_execution=ACTUALLY_EXECUTED`, `new_result_accuracy=SCOPED_PARITY_PASS`, `new_output_parity_checked=true` 및 실제 child exit 0이다. 이는 변경된 호스트에서의 scoped 재현 성공이며 physical/production 승격이 아니다.

## 실패 처리와 실행 횟수

물리 child가 시작되기 전의 파일 경로·가용 interpreter 선택 문제는 원인을 기록하고 source를 바꾸지 않는 범위에서 고칠 수 있다. child 시작 후 timeout, nonzero exit, identity mismatch, numerical mismatch가 생기면 최초 stdout/stderr/checkpoint를 보존하고 `FAILED` 또는 `TIMEOUT`을 반환한다. 같은 scientific work unit을 자동으로 다시 실행하거나 N/P, tolerance, branch, source mask를 바꾸지 않는다. 새로운 실행이 필요한 원인과 변경안을 보고한다. 별도 승인된 새로운 work unit 없이 full first2, full spectrum, gas/Newton/native/old continuous solver로 확장하지 않는다.

이번 runner는 Git push·PR 댓글·메시지 전송·백업 업로드를 자동으로 수행하지 않는다. NCP 결과의 publication은 실제 현재 승인과 기존 작업 경로가 확인된 경우에만 그 범위에서 한다. merge·force-push·production enable은 이 작업에 포함되지 않는다.

## 반환할 완결 결과

새 출력 디렉터리를 그대로 보존하고 다음 파일을 반환 묶음에 포함한다.

| 파일 | 의미 |
|---|---|
| `NCP_RESULT.json` | 실제 status, 실행 횟수, argv, exit, wall time, peak RSS |
| `IDENTITY_CHECK.json`, `HOST.json`, `ARITHMETIC_SMOKE.json` | 실행 전 identity와 실제 호스트 기록 |
| `RESULTS.json`, `RESULTS_START.json`, `RESULTS_CHECKPOINT.json` | 새 계산 결과와 source·시작·진행 기록 |
| `stdout.txt`, `stderr.txt`, `PARITY.json` | 원 로그 및 새 결과의 실제 parity |
| `NCP_REPORT_KO.md` | 실행자가 작성한 한국어 판정 및 제한 |
| `RETURN_MANIFEST.json` | 반환 파일들의 size와 SHA-256; 자기 자신 제외 |

실패 단계 때문에 생성되지 않은 파일은 `MISSING_EXPECTED_AT_THIS_STAGE`로 설명한다. 성공한 것처럼 빈 파일을 만들어 채우지 않는다. 반환 묶음은 예를 들어 `BASS_HE_E13C5_NCP_RETURN_<actual_UTC>_sha_<hash12>.zip`으로 만들며, 실행자가 실제 생성한 hash를 이름에 쓴다. 이미 승인된 반환 백업 경로가 사용 가능한 경우 그곳에 create-only로 저장한다. 제공한 파일의 추가 다운로드는 전송 상태가 모호한 경우에만 한다.

한국어 보고서에는 실제 패키지/lock/core identity, interpreter/libmpdec/CPU/memory/layout, 실제 명령과 시간·exit·RSS, 계산했는지 여부, fresh source 및 numerical parity, 두 node의 photon/heat correction과 반경, 관찰된 실패, 보존 상태와 다음 최소 행동을 쓴다. 보고서의 성공 근거는 실제 output이며 이 handoff의 예상 수치가 아니다.
