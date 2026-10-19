# HE29 Codex/NCP 인계: 고정 과학 소스와 네 기준해 실행

2026-10-19 현재 GitHub와 백업에서 새 HE29 반환을 찾지 못했다. 마지막 관측 상태는 0/4 NOT_RUN이다. 이 대화의 NCP 제출은 Remote Desktop Commander의 월간 사용량 한도로 막혔으며 접수·시작·완료를 기록하지 않는다. 원격 도구가 반환한 재시도/재연결 금지를 유지한다. NCP에 실제 접근할 수 있는 실행자는 현재 프로세스와 저장 결과를 먼저 읽고 중복이 없을 때 아래 작업을 수행한다. 사용자에게 파일 다운로드·업로드·터미널 입력을 요구하지 않는다.

## 고정 출발점과 재사용

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: research/he29-survival-budget-20261018
- 이번 intake publication HEAD: 3f16fe525d726aaebbe9262e0e869540321209eb
- 과학 코드·테스트 execution revision: 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
- Parent HE28 PR77: a41dd37124e34cb22bb9782aaf687a0da91640b7
- 원본 Rust owner: rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474

HE28 pilot/6개 transport, HE29 90사례/720구간과 50/50 source-only 검증은 기존 근거를 재사용한다. source-only PASS를 새로운 native 실행 근거로 쓰지 않는다. 과거 ncp/PUBLISH.sh를 실행하지 않는다. 기존 dirty tree·production job과 실패 기록을 보존한다. 현재 PR78은 Draft/unmerged로 유지하고 새 native 결과는 별도 results branch/Draft PR에 게시한다.

원본 1569 bootstrap에는 pytest 전체 재실행 한 줄이 있다. 현재 사용자의 반복 금지 지시를 적용하는 `ncp/REUSE_SOURCE_VALIDATION_20261019.patch`를 별도 실행 경계 identity로 사용한다. Git의 원본 bootstrap·과학 코드·테스트는 수정하지 않았고, 새 isolated execution checkout의 bootstrap에만 overlay를 적용한다. 제거되는 실행문은 pytest 한 줄뿐이다. 나머지 컴파일·입력 preflight·native qualification·campaign·실패 보존은 유지한다. 패치는 재사용 근거, 실제 bootstrap SHA, overlay diff, 실행 HEAD를 WORK/logs에 기록한다.

## 실행자가 NCP에서 수행할 명령

승인된 NCP 세션에서 실행한다. 개인 접속 정보는 공개 Git에 기록하지 않는다. 입력 archive를 먼저 사용자에게 요청할 필요가 없다. 다음 명령은 새로운 checkout을 만들며 기존 작업 폴더를 바꾸지 않는다.

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
git checkout --detach 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
[[ "$(git rev-parse HEAD)" == 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f ]]
[[ -z "$(git status --porcelain)" ]]
[[ "$(git hash-object "$HE29_REL/ncp/BOOTSTRAP_REFERENCES.sh")" == ed227e2937f554bd5ecda4bf24dd5597b73a77a4 ]]
git apply --check "$HE29_PATCH"
git apply "$HE29_PATCH"
export HE29_WORK_ROOT="$HOME/HE29_REFERENCE_$(date -u +%Y%m%dT%H%M%SZ)"
bash "$HE29_REL/ncp/START_REFERENCES.sh"

```

patch SHA256은 `cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e`, 원본 bootstrap Git blob은 `ed227e2937f554bd5ecda4bf24dd5597b73a77a4`, 적용 후 bootstrap SHA256은 `11d0ad0125f40a2890dac82e5103f13d17e6066f41440eabb06c7a8b1f319bc2`다. 위 identity가 달라지면 해당 변경을 먼저 분석한다.

## 네 기준해와 유지할 조건

모두 m8/GL4/q0이며 각 case에서 Radau 다음 DOP853을 실행한다.

| 순서 | strips r | table nodes | 출력 |
|---|---:|---:|---|
| 1 | 2 | 512 | references/m8_r2_table512 |
| 2 | 4 | 512 | references/m8_r4_table512 |
| 3 | 8 | 512 | references/m8_r8_table512 |
| 4 | 4 | 1024 | references/m8_r4_table1024 |

case3600s는 table 생성과 두 적분기를 합한 process-group 시간 상한이다. table600s와 예상 table allocation2GiB를 유지한다. 2GiB는 전체 프로세스 RSS 강제 상한으로 해석하지 않는다. 수치 thread는 각각1이고 첫 실패에서 campaign은 멈춘다. numpy/scipy 등 실제 dependency와 rustc 버전은 실행 로그에 보존한다.

photon number defect3e-15/H, energy defect3e-12eV/H, species defect3e-12, 양성성, solver pair 절대 fraction1e-11 및 temperature stability1e-9K를 유지한다. table512는 같은 r의 저장 SHA와 맞아야 하고 table1024는 별도 table 민감도다. 두 적분기의 일치는 경험적 안정성 지표다. 원본 물리식·반응률·허용치를 바꾸지 않는다.

## 자동 입력 복원

START_REFERENCES.sh는 인증된 rclone dbx:/gdrv:에서 원본 입력 archive를 확보하고 22개 DATA를 전체/개별 SHA로 검증하여 복원한다. archive의 옛 소스를 실행하지 않으며 기존 불일치 DATA를 overwrite하지 않는다.

- BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz, 129635 bytes
- SHA256 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205
- Drive id 1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi
- Dropbox /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz

NCP에 인증된 rclone이 없다면 연결된 Drive/Dropbox 또는 기존 허용된 전송 경로로 실행자가 확보하여 HE29_INPUT_ARCHIVE를 설정한다. 접근이 없으면 정확한 환경·입력 blocker를 기록한다. 사용자 수동 전달이나 public 선택필드 투영으로 원본 바이트를 대체하지 않는다.

## 반환과 바로 이어질 분석

성공·실패 모두 생성되는 WORK.tar.gz와 SHA256, source/adapter/build identity 및 모든 로그를 보존한다. WORK archive 자체는 BASS Git source 전체를 포함하지 않으므로 Git execution revision과 위 adapter identity도 함께 반환한다. `build/RECEIPT.json`의 native_run:false는 빌드 시점 필드다. 실제 실행/호출은 case RESULT, method JSON, process receipt와 native JSONL로 판정한다.

반환 파일: build/RECEIPT.json, logs/ENVIRONMENT.txt와 PYTHON_FREEZE.txt, 로그/EXIT_CODE.txt, 새 REUSED 로그와 실행 overlay/SHA/HEAD, preflight/PREFLIGHT.json, references/DESIGN.json과 SUMMARY.json, 각 case IDENTITY.json/SAVED_POINT_PARITY.json/TABLE.json/Radau.json/DOP853.json/RESULT.json 및 실패·partial/native JSONL/process 영수증. compiler flags는 edition2021 opt-level2이며 fast-math를 추가하지 않는다.

campaign 실패 때문에 자동 analyzer가 생략되면 저장된 성공 결과부터 별도 새 출력으로 `analyze_references.py --root <WORK>/references --out <NEW_ANALYSIS.json>`를 실행한다. incomplete JSON 저장 뒤 exit1은 부분 결과 판정이다. 완료 case가 있으면 campaign 전체를 다시 실행하지 않는다. case 직접 호출의 --case-wall-s는 자체 timeout을 집행하지 않으므로 남은 작업에는 기존 run_process와 동일한 process-group 시간 제한을 유지한다.

같은 r/table의 저장 n32/n64 transport와 새 reference 차이로 시간 적분 효과를 분리한다. r2→4, r4→8 기준해 차이는 strip 민감도, r4의512→1024는 table 민감도다. 상세 반환·부분 분석 계약은 results/continuation_20261019/INDEPENDENT_REVIEW_KO.md에 있다.

단계별 DAG·실제 case/native calls·실패 원본을 기록한다. 새 결과를 별도 results branch/Draft PR와 Drive/Dropbox create-only 백업에 반환하며 provider content_hash와 raw-byte readback을 구분한다. 현재의 과학 범위와 HOLD는 유지한다. 기존 백업 c47c5efc/798afac1은 불변으로 보존하며, 이번 overlay·조회 기록은 별도 후속 묶음이다.
