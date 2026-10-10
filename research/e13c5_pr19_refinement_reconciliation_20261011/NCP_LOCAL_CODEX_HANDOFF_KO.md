# NCP Local Codex handoff — E13C5 / PR19 refinement

이 문서 전체가 실행 계약이다. 사용자는 BASS_HE의 다음 물리 연구 루프와 이 NCP 인계를 요청했고, 별도 전달파일을 추가로 받지 않아도 진행할 수 있도록 백업본에 필요한 파일을 모두 넣으라고 했다. **NCP_READY ZIP 한 개**로 진행한다. 이번 작업은 기존 PR19의 선택 12-path 계산과 연결된 두 OFF 경로의 N512 host parity 및 정확한 mode별 합산이다.

## 1. 현재 기준과 읽을 문서

Repository: `cosmosapjw-quantum/BASS_HE`.
현재 이어갈 연구 branch: `research/e13c5-first2-branch-cover-20261011`, draft PR19.
이번 작업의 intake parent: `e25039b3a53031ce37800cebefb51200aa5a63a2`, tree `fe861762030cb7b669512fdfa3be8f2c0a188d2c`.
PR18 `48f648cd905cd8c232ae43abe97745ac6a96dec2` 및 PR17 `8fc3fb14dd33da10efa86c97c4beb9b0d12eeaad`는 선행 계보다. 더 오래된 PR17 상태로 되돌리지 않는다.

**실제 이번 scientific core commit/tree와 내부 archive 이름·크기·SHA는 외부 `DELIVERY_RECEIPT.json`을 읽는다.** 이 handoff는 봉인 전에 미래 commit이나 자기 archive hash를 예측하지 않는다. 원격 branch에 문서만 추가되었다는 이유로 이미 완료된 과학 실행을 다시 돌리지 않는다. 동일 source와 동일 work unit의 실제 NCP 성공 반환이 이미 있다면 그 반환을 검사해 재사용하고 중복 실행하지 않는다.

먼저 다음을 읽는다.

1. `CONTINUATION_REPORT_KO.md`와 `LINEAGE_ADDENDUM_KO.md`.
2. `INDEPENDENT_REVIEW.json`, `INDEPENDENT_LINEAGE_REVIEW.json`의 실제 scoped verdict.
3. `NCP_CONTINUATION_CONTRACT.json`, `CONTINUATION_LOCK.json`, `NEXT_DAG.json`.
4. 실패가 있거나 의미를 확인해야 할 때만 관련 source와 raw evidence를 추가로 읽는다.

원래 `REPORT_KO.md`·`PLAN.json`은 계보 복구 전 두-track 실행 기록이며 수정하지 않았다. 현재 다음 노드와 실행 순서는 위 continuation 문서가 소유한다. 선행 12-path cover는 이미 완료되어 있고, whole first2는 계속 `HOLD_RESOURCE_AUTHORIZATION`이다.

## 2. 백업본으로만 materialize

지정된 백업 위치에서 이름이 `BASS_HE_E13C5_NCP_READY_20261011_sha_*.zip`인 이번 인계본을 가져온다. 정확한 파일명과 전체 SHA는 전달 메시지 또는 외부 backup ACK를 사용한다. Dropbox의 기존 프로젝트 위치는 `/BASS_DERIVATION_DOSSIERS_20260912/`, Google Drive parent는 `1pkohlay5eIfFJsBwPZ_yn2jIZONZjesI`다. 사용자에게 별도 입력 파일을 다시 요청하지 않는다.

먼저 외부 ZIP의 SHA·크기를 실제값과 비교한다. 새 디렉터리에 안전하게 풀고 `NCP_READY_MANIFEST.json`의 모든 파일 크기·SHA를 확인한다. ZIP의 absolute path, `..`, symlink, 중복 member는 거부한다. 이 외부 ZIP에는 다음이 포함되어 있다.

- `00_START_HERE_KO.md`
- 이 실행문 사본
- `DELIVERY_RECEIPT.json`
- scientific archive 및 그 내부 FILE_MANIFEST
- 원본 physics code와 필요한 local certificate/captured controls
- PR19·PR18의 정확한 결과·코드·START 사본
- 독립 리뷰·새 reducer·두 종류 execution lock

내부 ZIP은 receipt의 `scientific_archive.file_name`, `bytes`, `sha256`으로 다시 확인한 뒤 새 경로에 풀고 `FILE_MANIFEST.json`을 검증한다. 이 package만으로 아래 실행이 가능하다. 과거 `/tmp/E13C5-DyIbg0hn`이나 별도 E13C4 ZIP을 materialize할 필요가 없다. 과거 code의 절대경로는 provenance용 사본이며 `cover.py`·`pilot.py`는 실행하지 않는다.

Git은 실제 core와 새 경로의 소스를 확인하는 전달 경로다. 기존 작업물이 있는 checkout을 덮어쓰지 말고 격리된 checkout 또는 검증한 archive 경로를 사용한다. 이 isolated research job을 위해 전체 native 프로젝트나 test suite를 실행하지 않는다.

## 3. 이번에 실행할 정확한 작업

실행 환경은 **CPython 3.12.x, 표준 라이브러리, Linux**다. 가용한 Python 중 일치하는 interpreter를 고르고 그 경로를 기록한다. Package의 numerical core나 Decimal precision을 변경해서 환경을 맞추지 않는다.

- 새 물리 계산: **N512/P60, OFF node 0·700, 경로당 세 segment**, 한 번.
- 동일한 E13C4 local certificate 두 개를 재사용하고 네 local enclosure를 새로 계산한다. 새 coefficient evaluation은 **4096**이다.
- 그 fresh `physics/RESULTS.json`을 입력으로 **exact Fraction reduction 한 번**을 순서대로 실행한다.
- 기존 12-path 결과 중 OFF0·OFF700만 새 enclosure로 교체한다. OFF1620·2344 및 KF/GM의 여덟 경로는 유지한다.
- OFF/KF/GM은 서로 다른 gas history다. Mode별 네 node 합을 각각 유지하고 세 mode를 하나의 물리량으로 합하지 않는다.

동시에 사용할 layout은 **process 1 / thread 1 / MPI 0**이다. Host inventory는 원 runner가 CPU affinity, cgroup, memory, lscpu, Python/libmpdec와 launcher environment를 기록한다. 이를 실제 NCP host와 대조한다. 64-core 보유 여부를 이번 작은 Decimal work unit의 병렬 성능 근거로 삼지 않는다.

과학 child timeout은 **180초**, 주소공간은 **1 GiB**다. 바깥 physics wrapper의 205초는 host intake와 종료 기록을 포함한다. 이어지는 exact reduction은 **60초 / 1 GiB**다. 자동 retry, N/P 변경, 전체 first2 확장은 없다. 동일 과학 job은 한 번만 실행한다.

Package root에서 아래 하나의 Python block을 실행할 수 있다. 먼저 root를 현재 디렉터리로 정하고, 실제 승인된 NCP에 있는지 host를 확인한 뒤 사용한다. 출력 디렉터리는 자동으로 새 이름을 쓴다.

```python
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, sys, uuid

package = Path.cwd().resolve()
assert (package / 'CONTINUATION_LOCK.json').is_file()
assert (package / 'INDEPENDENT_LINEAGE_REVIEW.json').is_file()
# 위 두 독립 판정 문서의 실제 scoped PASS와 제한을 읽은 후 실행한다.
name = 'E13C5_NCP_RETURN_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
out = package.parent / 'NCP_RETURNS' / name
command = [sys.executable, str(package / 'code/ncp_continue.py'),
           '--package', str(package), '--out', str(out), '--execute']
print(json.dumps({'command': command, 'fresh_output': str(out)}, ensure_ascii=False))
completed = subprocess.run(command, check=False)
print('ACTUAL_EXIT', completed.returncode)
print('RETURN_DIRECTORY', out)
if completed.returncode:
    raise SystemExit('실패 기록과 checkpoint를 보존하고 원인을 반환한다. 동일 과학 실행을 자동 재시도하지 않는다.')
```

CLI로는 `python3 code/ncp_continue.py --package <검증한 package> --out <아직 없는 새 경로> --execute`다. `--execute`를 생략하면 `VERIFY_ONLY_READY`이고, 물리·reduction 실행은 둘 다 `NOT_RUN`이다. 준비 확인 결과를 실제 NCP 성공으로 올리지 않는다.

## 4. 성공의 조건

최종 `NCP_CONTINUATION_RESULT.json.status`는 실제 실행 후 **`PASS_SCOPED_HOST_PARITY_AND_REDUCTION`**이어야 한다. 다음 조건을 함께 읽는다.

- `actual_new_host_physics_invocations=1`, `actual_exact_reduction_invocations=1`.
- 물리 단계의 actual exit 0, fresh source/input identity가 execution lock과 일치.
- `physics/PARITY.json`이 fresh output을 비교했으며 전체 deterministic numerical projection이 일치.
- Physics numerical SHA: `f4d0f8c7e37e5c8a013ab133af748173f3ef1a8247f413f4798fdb3518c04a86`.
- Reducer가 실제 fresh `physics/RESULTS.json`의 SHA를 `input_identities.current.sha256`에 기록하고 wrapper가 이를 직접 확인.
- Reducer status `PASS_SCOPED_POSTPROCESSING`, failed/disjoint 0. NCP 형식은 **774 checks, 302 comparisons**다. Chat의 optional N128 diagnostic 포함 결과 1180/604와 구별한다.
- `reduction/NUMERICAL_PROJECTION.json`의 **파일 전체 bytes** SHA는 `f0681b18032e4de92db2a4d4c867d00895cf761bbdb5a57c571fba6e0e01bb69`, **419,815 bytes**다.
- 별도 `numerical_projection_sha256`은 마지막 newline을 제외한 canonical-object hash다. 파일 SHA와 혼동하지 않는다.
- 19개 잠긴 파일과 `CONTINUATION_LOCK.json` 자체가 실행 전후 동일하다.

Photon·heat 보정의 수치 일치나 interval overlap을 새로운 물리 데이터의 검증으로 해석하지 않는다. 이는 고정된 captured model에서의 scoped host parity와 conditional exact reduction이다.

## 5. 실패·반환·다음 단계

Lock mismatch, unsupported Python, parity mismatch, nonzero exit, timeout, disjoint interval, 현재 결과 대신 오래된 결과의 입력 SHA, projection mismatch는 모두 해당 단계의 실패다. **새 디렉터리의 첫 stdout/stderr, RUN, checkpoint, 실제 exit와 source identity를 보존한다.** 실패 후 baseline을 바꾸거나 tolerance를 완화하거나 P/N을 올려 PASS를 만드는 행동은 이 계약에 없다. 실행 시작 전 환경 문제인지 실제 계산을 소비했는지 구분하고, 소비한 동일 job을 자동 재시도하지 않는다.

반환에는 전체 새 output directory, `RETURN_MANIFEST.json`, 실제 host·Python·메모리·wall·exit 요약, source/parity 결과, first failure가 있으면 그 원문을 포함한다. 증거가 없는 성공 문자열이나 기존 chat 결과를 새 NCP 반환으로 복사하지 않는다. Remote publication 또는 백업 ACK도 recipient 실행 ACK를 대신하지 않는다.

이미 허용된 전달 범위에서 새 반환은 최신 연구 branch의 이 task 아래 `ncp_returns/<unique>/`에 additive·nonforce로 기록하고, 지정 백업 위치에는 unique name으로 create-only 저장한다. Source package를 덮어쓰거나 merge하지 않는다. 다른 project의 reserved run이나 다른 사람에게 직접 보내는 메시지는 이 작업에 포함되지 않는다. 반환을 보낼 수 있는 surface가 없으면 로컬 완성 결과·archive·실제 blocker를 보존한다.

다음 연구 노드는 **`E13C5_SELECTED_SUBSET_BUDGET_AND_MISSING_NODE_COMPLEMENT_CONTRACT`**다. 저장된 interval을 이용해 선택 부분집합의 남은 수치 폭과 아직 포함하지 않은 spectral node의 signed contribution을 분리하고, branch partition·상계·자원 계약을 정한다. 자동 E13C6 지정이나 full first2 실행은 하지 않는다.

보존할 상태: `baseline_RCT=OFF`; actual atomic photon/heat/recoil `null`; physical/production `HOLD`; HE-F2/F09 `OPEN`; receiver adoption `SEPARATE`; legacy Gamma alias `3.543295 FAIL`; uniform full-path certificate `false`.
