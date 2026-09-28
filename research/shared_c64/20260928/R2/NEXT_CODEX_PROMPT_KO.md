# BASS_HE SHARED_C64_R2: 다음 작업을 이어갈 독립 실행 계약

이전 대화 없이 아래 저장소와 평문 evidence를 읽고 진행한다. 사용자는 bass_cr, BASS_HE, WU088_HH 세 작업이 유휴라고 보고했다. 실제 PID와 남은 lease는 아직 관측하지 않았다.

## 1. 목표와 권한

완료된 cloud 계산을 반복하지 않고, CODE-I02 focused independent rereview 및 별도의 common-R-contour 연구 후보를 다음 단계로 연결한다.

허용: 저장소/결과 읽기, 새 격리 scratch와 worktree, 이 연구 namespace의 bounded probe/test, BASS_HE의 owned 연구 branch에 non-force push, 결과 archive의 Google Drive/Dropbox create-only 백업.

금지: main 변경, merge/force push, 기존 디렉터리 삭제/reset/clean, 다른 두 repo의 mutation/native 실행, 기존 scientific kernel/tolerance 변경, service/cgroup/disk/cloud 설정 변경, 새 유료 자원 생성. Live native 계산은 해당 owner의 별도 bounded node 실행 승인이 확인된 경우에만 수행한다.

## 2. Authority와 필독 자료

Repo: cosmosapjw-quantum/BASS_HE.
연구 publication: PR #17, branch research/shared-c64-crossrepo-20260928.
현재 읽는 PR #17의 commit/tree를 fresh read하고 SOURCE_IDENTITY.json에 고정한다. Moving publication checkout과 immutable execution checkout은 분리한다.

원래 CODE-I02 repair:
PR #15 commit af3ed44ce3cc1023aa8a1370ab2981aa76760869
 tree 6fecfde27385d788a7891c4c5022b633eba74b83.

원래 cloud 실행 basis:
commit 6ddc4ff821ab5d1397fbd08493dd3954a89750f1
 tree e80a9218d9d275546132110605da35160a878bb0.

이미 완료된 PR #16 evidence:
commit 2c3812e390b91b89da1de30988b3933646b79f30
 tree e96885f705dcaa43861107672fbf6d597051da6d.
파일: evidence/cloud/ncp-c64g3/20260928/resume-004/RUN_RETURN.json.
이 기록은 full216/cloud75/fault52, stale negatives7, endpoints7/actions56/panel-pairs28, imported0, committed65를 보고한다. 직접 identity와 evidence 범위를 확인한다. 같은 closure에서 resume-004 또는 15-arm sweep을 다시 시작하지 않는다. CODE-I02 독립 과학 재검수는 이 보고와 별개로 남아 있다.

다른 repo의 읽기 기준:
- cosmosapjw-quantum/bass_cr PR #4 head 820b3e0a6da9f7a8c8ece8fcbd3afcf3fa9a6dc3.
  research/foundation_rebuild/ncloud_c64g3_20260928/execution_evidence/F1_R2/20260928T101921Z/RETURN_REPORT.json.
  F1_ENGINE_ADMISSION_PASS가 기록돼 있고 exactly-once 실행은 이미 소비됐다. F1 재실행, F2/F3 또는 새 capture는 승인되지 않았다.
- cosmosapjw-quantum/WU088_HH PR #12 head a49a704bf84fa86c34c16cd26a631dfabfbbc5ab.
  M3A 완료, M3B는 경쟁 부하로 유효 측정이 없다.
  R31U commit ff3db87dfbadd5f1eed89b413e5b785baf63a429의 research/r31u_shared_host/RESEARCH_AND_DESIGN_KO.md와 RESULT.json도 읽는다.

root와 해당 하위 AGENTS.md를 읽고, research/shared_c64/20260928/R1/ 및 R2/의 SOURCE_PINS.json, REPORT_KO.md, RESULT_SUMMARY.json, RUN_RETURN.json을 따른다. 다른 모델의 행렬·channel·rate·tolerance를 HE에 이식하지 않는다.

현재 cwd가 old main이라면 그곳에서 계산하지 않는다. fetch로 필요한 객체를 확보하고 새 detached worktree를 만든 뒤 exact commit/tree를 검증한다. 기존 경로가 있으면 identity를 검사하거나 고유 경로를 새로 사용한다. rm -rf, git reset --hard, git clean은 금지한다.

## 3. 첫 미완료 gate: 독립 과학 재검수

PR #15 CODE-I02 focused independent review가 아직 없으면 이를 최우선으로 둔다. 새 독립 context의 read-only reviewer에게 exact repair, previous finding, 정상 cloud return을 제공한다. 본 작업자가 구현에 관여했다면 이름만 바꿔 reviewer가 되지 않는다.

state_a/state_b, R, p, lambda, depth, Z1/Z2, policy 및 missing/stale certificate 경계를 검사한다. 구조 hash는 인증 서명이나 cryptographic authenticity가 아니다. Important/Critical finding이 나오면 해당 범위를 HOLD로 두고 최소 재현과 수정 방향을 반환한다.

기존의 정상 grid 전부를 무조건 반복하지 말고 변경 의존성과 독립 검수 계약이 실제로 요구하는 focused test를 선택한다. 기존 결과 재집계와 새 독립 실행을 구분한다. Desired verdict를 주입하지 않는다. 이 프롬프트는 Eq. (55) 실행 승인이 아니다.

## 4. Common-contour 후보의 별도 검수

원본 R1 archive:
BASS_HE_SHARED_C64_RESEARCH_20260928_v1.zip
668774 bytes
SHA256 b70fbd51736d6e3004c27793cb1c47e50878fc72bad090de83e2a57aa94522a2.
Drive object 1BYwBr102UtC8vHuvuS6BHOlkS74wlkCS.
Dropbox object id:BSpOijBcT10AAAAAADukRg.
R2 package에도 이 원본 ZIP이 그대로 포함된다. Manifest를 먼저 확인한다.

원래 CF/Sturm 함수는 고정하고, common contour의 rho<ReRc 및 실제 same-sheet homotopy를 검수한다. 작은 nodal residual이나 32/64 agreement만으로 singularity-free 영역을 증명했다고 하지 않는다. 확인되지 않은 영역은 UNRESOLVED로 남기고 기존 method에 명시적으로 fallback하거나 거절한다.

R2의 analytic rho jet과 interpolation bound는 실제 finite-trace evaluator에 관한 식이다. 복소 A를 보간한 뒤 abs(Im A)를 취한다. Delta 자체를 보간해 cusp를 숨기지 않는다. 이산 bound에 CF/quadrature/homotopy/roundoff를 포함했다고 하지 않는다. 실험의 1e-5 Eh*a0는 새로운 production tolerance가 아니다.

Hybrid telescope는 actual downstream과 approximate upstream을 쓰는 exact identity다. Atomic probability 계산이나 사전 branch 생략 권한을 얻은 것이 아니다.

Production integration은 별도 승인/독립 검수 이후 새 scientific_source_id로 진행한다. 지금 수정할 수 있는 것은 research namespace뿐이다. 새 probe가 필요하면 TDD와 명시적 계산 예산을 쓰고 이미 유효한 spectral trace는 불필요하게 재계산하지 않는다.

## 5. Idle 상태에서 공유 VM 조정

Coordinator는 한 명만 지정한다. 각 owner의 repo/worktree, PID+birthtime/boot-id, leaf cgroup, 실제 thread team, ready task, memory 사용량을 읽기 전용으로 등록한다. 다른 owner의 작업을 kill/이동/재시작하지 않는다.

CR F1-R2는 완료됐으므로 idle을 재실행 허가로 해석하지 않는다. HH M3B에는 그 owner가 요청하는 짧은 BENCHMARK_EXCLUSIVE 창을 먼저 조정한다. 그 창에는 다른 native/압축/빌드를 겹치지 않는다. 이 thread가 HH 실행 계약을 고치거나 실행하지 않는다.

16/16/16을 하드코딩하지 않는다. HE의 이전 16-worker와 새 32-worker 선택은 각각 다른 측정 receipt에 묶여 있다. HH의 132-task 동일 mix 제안 역시 owner의 amendment 승인이 필요하다.

공통 ancestor memory.current를 한 번만 세고, 아직 반영되지 않은 pending reservation만 더한다. TTL 만료로 live worker의 할당을 재발급하지 않는다. Exclusive benchmark, shared workload, scientific cache hit은 서로 다른 실행 조건이다. 새로운 live 자원 설정은 RESOURCE_PLAN.json으로 먼저 제안하고 해당 권한을 확인한다.

## 6. Durable 산출물과 GitHub 게시

Repository 밖의 고유 state에 command, cwd, UTC, exit code, raw log SHA, source/dependency identity를 남긴다. Source/numerics/runtime/provenance/permission 문제를 구분한다. 완료 node를 근거 없이 다시 돌리지 않는다.

새 평문 output:
research/shared_c64/20260928/R2_followup/<UTC-run-id>/

REVIEW_RETURN.json, RESOURCE_PLAN.json, METHOD_ADMISSION.json, NUMERICAL_CHECKS.json, COMMAND_LOG.txt, RUN_RETURN.json, MANIFEST.json을 게시한다. 독립 review를 못 했으면 NOT_RUN이지 PASS가 아니다.

Publication branch가 evidence-only commit으로 이동해도 계산 basis를 자동 변경하지 않는다. 동시 remote 변경은 먼저 읽고 append-only reconcile하며 non-force push만 한다.

새 archive와 sidecar는 기존 Drive folder 1pkohlay5eIfFJsBwPZ_yn2jIZONZjesI 및 Dropbox /BASS_DERIVATION_DOSSIERS_20260912/에 create-only 백업한다. 실제 ACK/object-id/size/checksum을 기록하고 upload verification과 restore verification을 구분한다. 이미 같은 객체가 검증됐다면 중복 upload/restore를 반복하지 않는다. Credential과 원 논문 PDF를 공개하지 않는다.

## 7. 종료와 반환

Source identity 실패, wrong-pair admission, numerical gate 실패, 미승인 kernel 변경 필요, unverified homotopy domain은 그 범위를 HOLD로 반환한다. 독립적으로 계속할 수 있는 research lane까지 자동 취소할 필요는 없으나 결과를 섞지 않는다.

최종 반환에는 reviewed/execution/publication commit과 tree를 각각 기록한다. 신규 계산수, 재사용 근거, 각 gate, PR URL, backup object, 남은 최소 node를 제시한다.

scientific_PROMOTE=HOLD, Eq55=NOT_RUN, full_Nmax4=NOT_ESTABLISHED, continuum=NOT_ADMITTED를 유지한다. 새 독립 판정이 나와도 그 범위만 기록하며 자동 production 실행이나 merge를 하지 않는다.
