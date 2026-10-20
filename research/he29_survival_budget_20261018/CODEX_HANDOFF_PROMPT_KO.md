# Codex NCP 인계 — HE29 HPC64

고정 실행 code pin: `802a32361288bf5aa0e0d1f63c912768f1a1d407`. 실제63/63 changed-file Git readback PASS. 최신 문서 HEAD와 구분한다. 사용자에게 파일 전송이나 터미널 작업을 요구하지 않는다.

# NCP 실행자 인계: HE29 단일 준비 작업과64코어 자원 배분

이 문서는 NCP에 접근 가능한 실행자를 위한 것이다. 사용자에게 다운로드·업로드·터미널 작업을 요구하지 않는다. ChatGPT 측의 이번 NCP 제출/시작은0이며 원격 process는 UNOBSERVED다. Remote Desktop Commander는 월간 quota/no-retry 금지에 따라 호출하지 않는다. 별도 실행 경로가 실제로 접근 가능할 때만 아래를 수행한다.

## 실행 범위와 고정 identity

실행할 수 있는 미완료 HE29 과학 case는 **m8/GL4/q0,r4/table512 packed canary 한 개**다. 과거 ABI1 canary는 동일 과학 case의 옛 경로다. 네 native Radau+DOP853 pair는 이미4/4 admitted이므로 다시 제출하지 않는다. 저장된09929 budget 분석, transport, 기존 tests/benchmark/clean build를 재실행하지 않는다. 다른 모델의 NOT_RUN을 이 queue에 추가하지 않는다.

| 역할 | 고정값 |
|---|---|
| 새 host/table/trace/canary 실행 code | `802a32361288bf5aa0e0d1f63c912768f1a1d407`; 최신 DELIVERY에서 readback PASS 확인, 문서 HEAD와 구분 |
| 원래 ABI2 core/bridge/solver | `a5d4711460c09b310b78c9692aa62534b7a843d3` |
| watchdog | `ed5adca43f474553a9bce7f5de45d464be5905cb` |
| VigilODE | `a21d573980f66fe02891bd216153443b5352f921` |
| 원래 science / owner | `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f` / `f7830e2f55e7a1938bc3c98f61b60651f8dae474` |
| native binary SHA | `a82e540797322027deaab6e6bcb2bde746de737adeedbf144313598c65f5b7e9` |
| r4/table512 table SHA | `919ca6f42028bffc37cb208916ee5a9927356eb99344fe467f9b98e30e9fddcd` |
| Python | `3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]` |
| NumPy / SciPy | `2.3.5` / `1.17.0` |
| bridge compiler | Rust/Cargo1.94.1,x86_64-unknown-linux-gnu; no-fast-math/generic x86-64/locked graph |

기존 baseline root는 `/root/HE29_REFERENCE_20261020T120000Z`다. `references` 네 pair, `build/he29_owner_server`, `build/RECEIPT.json`, `venv/bin/python`을 실제 읽어 재사용한다. DATA root는 `/root/HE29_NCP_20261020T105630Z/checkouts/baseline1569/research/he29_survival_budget_20261018`이다. controller checkout은 `/root/HE29_NCP_20261020T105630Z/checkouts/controller_ed5adca`다. 이들은 과거 실제 반환에서 읽은 경로이며 현재 존재는 실행자가 관측해야 한다.

## 먼저 새 반환과 실행 중 프로세스를 관측

최신 GitHub/관련 결과 branch/백업 변경분을 다시 읽고, host에서 알려진 `/root/HE29_PACKED_*`, `/root/HE29_HPC64_*`, `/root/HE29_NCP_*`, `/root/HE29_REFERENCE_*`를 확인한다. 새 RESULT/PACKED_RAW/부분 기록이 있으면 source/binary/table/input/runtime identity를 읽고 결과 분석부터 수행한다. 이미 시작된 canary는 다른 output 이름으로 재실행하지 않는다. 실제 process visibility가 없으면 HOLD한다.

`batch_entry.py`는 실제 `/proc`, affinity/cgroup/memory, 다른 과학 작업과 protectedCPU55, shared `/tmp/BASS_HE_HE29_NATIVE.lock`, bounded old-output scan을 확인한다. 저장된 canary가 있으면 raw identity와 경로를 PLAN에 기록하고 실행을 HOLD한다. 이것은 아직 그 반환을 admit했다는 뜻이 아니다. 실제 local scope 외 host·namespace의 부재도 주장하지 않는다. 다른 작업을 종료하거나 기존 파일을 지우지 않는다.

## Git 준비와 한 번의 실행

아래 명령은 **NCP 실행자**가 실제 접근 가능한 host에서 수행한다. 먼저 최신 publication의 DELIVERY를 읽고 고정 code pin으로 분리한 뒤 실행한다. 기존 clone이 있으면 해당 source를 검증하여 재사용해도 된다. 원래1569의 두 overlay는 과거 baseline identity다. 새a5 checkout에 그 shell patch를 다시 적용하지 않는다.

```bash
set -euo pipefail
HE29_FETCH_STAGE="$(mktemp -d /root/HE29_HPC64_SOURCE_XXXXXXXX)"
HE29_SOURCE="$HE29_FETCH_STAGE/source"
git clone --single-branch --branch research/he29-survival-budget-20261018 \
  https://github.com/cosmosapjw-quantum/BASS_HE.git "$HE29_SOURCE"
HE29_LANE=research/he29_survival_budget_20261018/hpc64_20261021
HE29_PY=/root/HE29_REFERENCE_20261020T120000Z/venv/bin/python
HE29_CODE="$("$HE29_PY" -B - "$HE29_SOURCE/$HE29_LANE/DELIVERY.json" <<'PY'
import json,sys
v=json.load(open(sys.argv[1]))
pin=v.get('code_commit')
if (v.get('code_readback_status')!='PASS' or not isinstance(pin,str)
    or len(pin)!=40 or any(c not in '0123456789abcdef' for c in pin)):
    raise SystemExit('HE29_HPC_CODE_PUBLICATION_NOT_VERIFIED')
print(pin)
PY
)"
cp "$HE29_SOURCE/$HE29_LANE/DELIVERY.json" "$HE29_FETCH_STAGE/PUBLICATION_DELIVERY.json"
git -C "$HE29_SOURCE" checkout --detach "$HE29_CODE"
bash "$HE29_SOURCE/$HE29_LANE/ncp/RUN_READY.sh" "$HE29_CODE"
```

RUN_READY는 새 source worktree를 준비하고 baseline을 다시 시작하지 않는다. mode=run으로 필요한 compile, table/cache, 단일 canary를 순서대로 실행한다. 새 run root는 `/root/HE29_HPC64_STAGE_.../run`, cache는 별도의 `/root/HE29_HPC64_TABLE_CACHE`, archive는 같은 stage의 `return`에 만든다. 성공·실패·HOLD를 한 번 기록하며 자동 재시도하지 않는다.

실제 기존 bridge를 별도 경로에서 확인했다면 `HE29_REUSED_BRIDGE_BUILD`로 지정할 수 있다. 지정된 bridge가 잘못되면 조용히 다시 만들지 않고 HOLD한다. 자동 scan은 기존 BUILD_IDENTITY와 library bytes가 원래 verify_build를 만족하는 경우에만 재사용한다. 없을 때만 원래a5 빌더를 호출한다. `HE29_VIGILODE_CHECKOUT`, `HE29_CARGO`, `HE29_RUSTC`, `HE29_CARGO_OFFLINE=1`은 실제 관측한 clean a21 checkout/toolchain/cache를 연결하는 선택 환경변수다. 임의 compiler version으로 바꾸지 않는다. missing Cargo dependency는 frozen lock 계약 안의 환경 준비만 허용한다.

DATA가 이미 존재하면 그대로 `--data-root`로 사용한다. 없을 때는 준비된 원래 `ncp/RESTORE_VERIFIED_INPUTS.py`가 archive SHA를 확인하고22개 DATA만 복원할 수 있다. archive는 `/root/HE29_NCP_20261020T105630Z/incoming/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz`,129635bytes,SHA `a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205`다. 백업 식별자는 Drive `1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi`,Dropbox `id:BSpOijBcT10AAAAAAD_Ncg`다. 실제 실행자는 접근 가능한 백업 경로로 확보한다. 사용자에게 전달 작업을 넘기지 않는다. source/manifest authority는 고정Git에 유지하고 `START_REFERENCES.sh`/`PUBLISH.sh`는 부르지 않는다.

## 계산과 기록 계약

기본 table48 worker/build8 job은 상한이다. 실제 quota/affinity/headroom을 반영하고8CPU, 최소16GiB와 유효 capacity20% 중 큰 memory reserve를 남긴다. 다른 과학 job이 보이면 HOLD한다. solver/native protocol은 thread1, 원래19ledgers를 포함한 full-state norm, rtol1e-10/scaled-atol1e-12 및 원래 admission gate다. table은 same runtime과919ca6… 전체 digest를 만족해야 한다. cache HIT는 이전 build metadata를 보존하며 새 worker 실행으로 세지 않는다.

기록은 기본B256이다. segment/실패/RAW/close에서는 native barrier 후 endpoint를 확정한다. hardkill 때 마지막 fsync 이후 성공 반환 point 최대255개의 trace가 durable하지 않을 수 있다는 변경된 계약을 사용한다. 모든 성공 실행은 complete gzip readback/count 일치 후에만 RESULT를 쓴다. 필요하면 미시작 실행의 `--sync-every 1`을 선택할 수 있지만, B256 결과를 다시1로 돌려 비교하는 새 benchmark를 자동 실행하지 않는다.

원래 canary wall budget900초, 최대3600초이고 source table600초/2GiB allocation estimate를 유지한다. 첫 실패/timeout에서 raw prefix를 반환한다. 허용치·격자·모형을 확대하거나 solver를 개발하지 않는다. source-row 병렬성이나 제조 I/O 배율을 실제 HE29 속도로 적지 않는다. `phase_wall_s`와 반환 전후 scientific gates가 실제 비교 근거다.

## 반환과 후속 분석

RUN_READY는 `MAKE_RETURN.py`로 결과 또는실패의 실제 파일과 raw bridge library를 create-only archive로 묶고, archive를 다시 읽어 모든 payload SHA를 확인한다. provider upload는 수행하지 않으며 그 사실을 receipt에 기록한다. 접근 가능한 실행자는 기존 프로젝트 Git 결과 branch와 백업에 저장하고 실제 readback/ID를 반환한다. PR78은 Draft/open/unmerged로 유지하고 merge하지 않는다.

필수 반환은 PLAN, BASELINE_BEFORE_BUILD, BRIDGE_INTAKE/BUILD_IDENTITY, PROCESS_BEFORE_DISPATCH, canary_process COMMAND/stdout/stderr/RECEIPT, case IDENTITY/TABLE/SEGMENT_ENDPOINTS/PACKED_RAW/NATIVE_EVIDENCE/RESULT 또는FAILURE, native gzip 또는partial, SUMMARY/FAILURE, archive receipt다. source/binary/table/runtime/thread identity를 먼저 읽고 원래 gate로 판독한다. 실제 canary 완료와 원래 reference4/4 재사용을 별도 집계한다. 연속 스펙트럼/전역 온도상한/전체EoR/upstream전체동등성/Bianchi-CMB HOLD는 유지한다.
