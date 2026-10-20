# HE29 Codex/NCP 현재 인계 — 2026-10-20

## 현재 실행 순서

먼저 최신 GitHub·백업·접근 가능한 NCP 저장 결과와 프로세스를 읽는다. 이 턴의 전체 intake에서 새 HE29 native 반환은0건, 네 기준해는관측상0/4다. 다른 REI/VigilODE native 결과는 source/binary/table 계약이 달라 HE29 완료로 계산하지 않는다. Remote Desktop Commander 월간 quota에 따른 재시도·재연결 금지를 유지하며 이 턴은 NCP 작업을 제출하거나 시작하지 않았다.

새 HE29 반환이 있으면 source·binary·table identity를 읽고 저장 결과부터 분석한다. 없고 중복 실행 프로세스도 없을 때 아래 원래 네 기준해만 실행한다. HE28 pilot/6-case transport, HE29 90/720과50 tests, 기존 VigilODE96/3/Schur23은 반복하지 않는다. 사용자에게 파일 다운로드·업로드·터미널 실행을 요청하지 않는다.

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: `research/he29-survival-budget-20261018`
- 이번 시작 publication: `329f838399f24d3952f780d469ad657d8630c4e2`
- 첫 최적화 checkpoint: `8cb0ebb91a78d2f1b751caa1c3ffc5d170ddfe41`,19파일 actual Git readback MATCH
- 원래 과학 source·tests: `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`
- HE28 parent: `a41dd37124e34cb22bb9782aaf687a0da91640b7`
- 원본 native owner: `rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474`

## 고정1569 실행 checkout과 두 overlay

원본 bootstrap의 완료 pytest 재실행 한 줄은 별도 재사용 overlay로 제외한다. 새로 발견한 입력 manifest 결함도 별도 patch로 고친다. `inputs/study/m8_r2_n64/TABLE.json`의 Git 게시 SHA는62자리였고, 전체SHA가맞는a70 archive의 실제 파일 및 내부 manifest는64자리였다. 누락된 `4b` 두 문자만 복원했다.22개 DATA 실제 복원·preflight·독립 검토가 PASS다. 원본 DATA/물리식/반응률/허용치는 바꾸지 않았다.

아래 명령은 새 isolated checkout을 사용하고 기존 dirty tree와 production job을 보존한다. `ncp/PUBLISH.sh`나 과거 미게시 복구 절차는 실행하지 않는다.

```bash
set -euo pipefail
HE29_STAGE="$(mktemp -d "${TMPDIR:-/tmp}/he29-resume.XXXXXXXX")"
git clone --branch research/he29-survival-budget-20261018 --single-branch \
  https://github.com/cosmosapjw-quantum/BASS_HE.git "$HE29_STAGE/BASS_HE"
cd "$HE29_STAGE/BASS_HE"
HE29_PUBLICATION_REV="$(git rev-parse HEAD)"
HE29_REL=research/he29_survival_budget_20261018
HE29_PATCH="$HE29_STAGE/REUSE_SOURCE_VALIDATION_20261019.patch"
git show "$HE29_PUBLICATION_REV:$HE29_REL/ncp/REUSE_SOURCE_VALIDATION_20261019.patch" > "$HE29_PATCH"
printf '%s  %s\n' cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e "$HE29_PATCH" | sha256sum -c -
HE29_INPUT_PATCH="$HE29_STAGE/REPAIR_INPUT_MANIFEST_20261020.patch"
git show "$HE29_PUBLICATION_REV:$HE29_REL/ncp/REPAIR_INPUT_MANIFEST_20261020.patch" > "$HE29_INPUT_PATCH"
printf '%s  %s\n' 71f16bc8bc946bdd9107c476662fb83b9812cb4078045b933066fca300eb1e85 "$HE29_INPUT_PATCH" | sha256sum -c -
git checkout --detach 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
[[ "$(git rev-parse HEAD)" == 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f ]]
[[ -z "$(git status --porcelain)" ]]
[[ "$(git hash-object "$HE29_REL/ncp/BOOTSTRAP_REFERENCES.sh")" == ed227e2937f554bd5ecda4bf24dd5597b73a77a4 ]]
git apply --check "$HE29_PATCH"
git apply "$HE29_PATCH"
git apply --check "$HE29_INPUT_PATCH"
git apply "$HE29_INPUT_PATCH"
export HE29_WORK_ROOT="$HOME/HE29_REFERENCE_$(date -u +%Y%m%dT%H%M%SZ)"
bash "$HE29_REL/ncp/START_REFERENCES.sh"

```

| patch | SHA256 |
|---|---|
| 재사용 source 검증 overlay | `cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e` |
| 입력 manifest repair | `71f16bc8bc946bdd9107c476662fb83b9812cb4078045b933066fca300eb1e85` |

원본 bootstrap blob은 `ed227e2937f554bd5ecda4bf24dd5597b73a77a4`, overlay 적용 후 bootstrap SHA는 `11d0ad0125f40a2890dac82e5103f13d17e6066f41440eabb06c7a8b1f319bc2`다. 보정 manifest SHA는 `28917c4c292988a72dd4154443555437ed1de06158ff91a2104c0b189aacaca7`다. 실제 source·overlay·입력 identity를 반환에 포함한다.

`START_REFERENCES.sh`가 인증된 기존 rclone dbx:/gdrv:에서 원본 입력 archive를 받아22 DATA만 복원한다. 실행 source는 Git이며 archive에서 코드를 실행하지 않는다. 기존 불일치 DATA는 덮어쓰지 않는다.

원본 입력 archive: `BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz`,129635bytes, SHA256 `a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205`. Drive `1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi`, Dropbox `id:BSpOijBcT10AAAAAAD_Ncg`. 접근이 없으면 실행자가 허용된 연결로 확보하거나 정확한 blocker를 기록한다.

## 네 기준해와 원래 gate

모두 m8/GL4/q0이며 각 case에서 Radau 다음 DOP853이다.

| 순서 | r | table nodes | 출력 |
|---:|---:|---:|---|
|1|2|512|references/m8_r2_table512|
|2|4|512|references/m8_r4_table512|
|3|8|512|references/m8_r8_table512|
|4|4|1024|references/m8_r4_table1024|

case3600초는 table과 두 적분기를 합한 process-group 상한이다. table600초와 예상 allocation2GiB를 유지한다. 2GiB는 전체RSS강제상한이 아니다. numerical thread1, 첫 실패 중단, 실제 dependency/compiler identity와 stdout/stderr/partial output을 보존한다.

number defect3e-15/H, energy defect3e-12eV/H, species defect3e-12, 원래 양성성, method pair 절대fraction1e-11 및 temperature difference1e-9K를 유지한다. table512는 같은 r의 저장 SHA와 같아야 하며 table1024는 별도 민감도다. 기존3.951006358291365e-14는 절대fraction 차이였다. 허용치를 바꾸지 않는다.

## 결과 분석과 선택적 새 최적화

성공·실패 모두 WORK.tar.gz와 전체SHA, build/RECEIPT, environment/dependency, execution overlay, preflight, DESIGN/SUMMARY, 각 case IDENTITY/TABLE/SAVED_POINT_PARITY/Radau/DOP853/RESULT 및 실패·partial/native JSONL/process 영수증을 반환한다. build의 native_run:false는 빌드 시점 필드다. 실제 호출과 완료는 case와native로그로 판정한다.

campaign이 실패하면 저장된 성공 case부터 `analyze_references.py --root <WORK>/references --out <새파일>`로 분석한다. 완료 case는 재실행하지 않는다. 남은 case에도 기존 process-group 시간 상한을 적용한다. 같은 r/table의 n32/n64 transport 차이로 시간오차를, r2→4/r4→8 기준해 차이로 strip 민감도를, r4의512→1024로 table 민감도를 분리한다.

네 baseline 쌍이 **모두 admit된 뒤** 단일 r4/table512 optional VigilODE canary를 사용할 수 있다. 이번에는 [optimization_20261020/NCP_HANDOFF_KO.md](optimization_20261020/NCP_HANDOFF_KO.md)의 ABI2 packed 경로가 준비됐다. 고정VigilODE a21d의 같은 RODAS5P–GMRES, 원래RHS/FD/partial-time, 전체ledger error norm을 유지하고 JVP 연결부만 가속한다. 새 solver·전체격자확장·추가transport가 아니다.

최종 ABI2 source pin은 `optimization_20261020/DELIVERY.json`의 `implementation_publication.code_commit`이다. status가 `PUBLISHED_EXACT_READBACK_PASS`인지 확인한다. 후속 문서 publication과 실행 code pin을 구분하며 과거5764225나첫8cb checkpoint를최종ABI2코드로대신쓰지않는다. NCP는 해당cleanGit에서컴파일·작은환경수정·실제실행만수행한다. 기본thread1이며2/4는합성실측에서느려확대하지않는다.

## 게시·백업·DAG

이번 정확한 게시/백업은 `optimization_20261020/{DAG_STATUS.json,DELIVERY.json}`과evidence영수증을 읽는다. 이전7bf7398b complete/88285fa4 closeout, c47c5efc/798afac1은불변이다. 새native반환은별도resultsbranch/DraftPR와Drive/Dropbox create-only백업으로보존하며providercontent_hash와실제raw-byte검증을각각기록한다. PR78은Draft/unmerged를유지한다.

finite-donor conditional survival과수치안정성의기존범위를유지한다. 연속spectrum/전역gas-temperature오차상한/전체EoR/wholeupstreamGrackle/관측Bianchi+CMB는HOLD다.
