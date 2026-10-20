# HE29 현재 인계: 공유 기준해 budget·부분 반환 분석 — 2026-10-20

## 현재 실행 출처와 완료 범위

현재 후속 단위는 `continuation_20261020T0557Z`다. 새 분석 코드의 고정 commit은 `09929b0a06a833f0c2497e72f074ec8694a264df`이며, 실제 게시·readback 상태는 [continuation_20261020T0557Z/DELIVERY.json](continuation_20261020T0557Z/DELIVERY.json)의 `implementation_publication`과 연결된 PR78 영수증을 읽는다. 실행 전에 `status=PUBLISHED_EXACT_GIT_READBACK_PASS`와 전체 40자리 `code_commit`을 확인한다. 이후 문서 closeout HEAD, 새 분석 code pin, 기존 baseline 과학 pin과 ABI2 실행 pin을 각각 보존한다.

이 분석 commit의 tree는 `f35be906ea4a201849516ee58825b6fa03597a5a`다. 2026-10-20 07:02:52 UTC의 실제 Git fetch/show에서 새·변경 파일 **45/45 bytes 및 SHA 일치, PASS**를 확인했다. 이 이후 문서 commit은 분석 실행 pin을 바꾸지 않는다.

현재 반환 분석의 실행 절차는 [continuation_20261020T0557Z/NCP_HANDOFF_KO.md](continuation_20261020T0557Z/NCP_HANDOFF_KO.md)에 있다. 아래 기존 문서의 **1569 baseline 실행 Bash와 두 overlay는 원문 그대로 유지**했다. 새 분석 checkout은 최신 DELIVERY에서 확인한 분석 code pin을 사용하고, 이미 복원된 baseline DATA를 `--data-root <baseline checkout의 HE29 디렉터리>`로 읽는다. `--study-root`를 생략하면 그 DATA root 아래 `inputs/study`를 사용한다. source·manifest는 분석 Git에서 읽고 원래 DATA SHA를 대조한다. 입력만 복원하려고 `START_REFERENCES.sh`를 다시 호출하지 않는다.

| 역할 | 고정 정체성 |
|---|---|
| 새 read-only budget·부분 반환 분석 | `09929b0a06a833f0c2497e72f074ec8694a264df`; 최종 DELIVERY와 실제 Git readback을 확인 |
| 원래 HE29 science·tests | `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f` |
| HE28 parent | `a41dd37124e34cb22bb9782aaf687a0da91640b7` |
| 원본 native owner | `f7830e2f55e7a1938bc3c98f61b60651f8dae474` |
| 기존 ABI2 packed 실행 코드 | `a5d4711460c09b310b78c9692aa62534b7a843d3` |
| VigilODE dependency | `a21d573980f66fe02891bd216153443b5352f921` |
| 직전 optimization 문서 closeout | `1765522318438e966e61d8a72f12084550da399d` |
| 이번 intake checkpoint | `3b125fc3cf80ce715353be17f640f2d9a5fb9f4a`, 실제 Git 12/12 byte readback PASS |

새 코어 10개, 부분 반환 분류 12개, CLI 통합 6개로 **28개 새 test method가 각각 첫 실행 PASS**다. 독립 제조계 20개와 CAS의 signed closure·공유 기준해 상쇄 0도 보존했다. 실제 로컬의 반환 부재 경로에 새 CLI를 연결한 결과는 **exit 1 / HOLD**, 채택 pair 0/4, reference-dependent 행 0, 기존 DATA 18/18 SHA 일치였다. 이 결과는 로컬 분석 경로의 확인이며 NCP 프로세스 관측이 아니다. 근거는 새 lane의 `evidence/{LINEAR_BUDGET_CHECKS,PARTIAL_RETURN_CHECKS,ANALYZE_BUDGET_CHECKS,LOCAL_NO_RETURN_CHECK}/`와 `THEORY_REVIEW.json`, `WOLFRAM_BUDGET.json`, 독립 코드 검토 영수증에 있다.

이번 분석 연결에서 기존 연구·검사·native·solver·기존 audit 계산의 재실행은 모두 0이다. 초기 intake에 적용한 standalone 1.0.0 이력과 이후 사용자가 명시한 plugin 1.3.0 적용을 구분하며, 버전 전환을 이유로 완료 단계를 다시 실행하지 않는다.

## 다음 실행자의 우선순위

먼저 최신 GitHub의 PR78·관련 branch·반환 artifact, 관련 저장소의 새 source/binary/result identity, Drive·Dropbox의 변경분과 접근 가능한 NCP 저장 결과를 확인한다. 이전 intake 영수증을 재사용하고 이후 변경분을 기록한다. 새 반환이 있으면 저장된 IDENTITY·TABLE·binary/owner·source/input/parent manifest·6점 qualification·thread/runtime을 읽고 분석한다. 다른 REI/VigilODE 모형의 결과는 해당 정체성으로 보존한다.

최종 관측은 **native 기준해 0/4, 선택적 canary NOT_RUN, NCP 제출 0건·시작 0건, 미반환 프로세스 미관측**이다. Remote Desktop Commander의 월간 quota에 따른 재시도·재연결 금지는 유지한다. 접근 가능한 실행자가 실제 프로세스를 확인하기 전에는 중복 실행이 없다고 가정하지 않는다. 사용자에게 파일 다운로드·업로드·터미널 입력을 요구하지 않는다.

새 반환이 없고 실행자가 중복 작업 부재를 확인했다면, 준비된 m8/GL4/q0의 `(r2,512), (r4,512), (r8,512), (r4,1024)` 네 case에 각각 Radau+DOP853만 전달한다. 완료 case를 다시 실행하지 않는다. 네 pair가 모두 원래 admission을 통과한 뒤에만 단일 r4/table512 ABI2 packed canary를 연결한다. canary는 기존 a5 코드, VigilODE a21, 1 thread와 원래 ledger 포함 error norm을 사용한다. NCP의 범위는 컴파일·작은 환경 수정·실제 실행이다.

## 분석의 정확한 의미

`partial_returns.py`는 부분 진행과 완료 admission을 분리한다. method-only·두 method 완료 후 RESULT 미작성·실패·timeout을 기록하고, 다른 유효 case를 보존한다. 원래 `check_result`·`admit_pair`의 물리 gate를 재사용하며 반환 파일 일관성 검사는 별도 필드다. 다른 binary/source/parent/input/thread/Python/NumPy/SciPy cohort를 섞은 대비는 HOLD다. 실제 binary bytes를 제공하지 않았으면 `binary_bytes_readback=NOT_PROVIDED`를 유지한다.

`analyze_budget.py`는 저장 transport `T`와 선택한 기준 후보 `θ`에 대해 signed residual `T−θ`, strip·table 대비와 조립 closure를 출력한다. 공유 θ의 계수를 먼저 합쳐 상쇄한 뒤 `product_hull` 또는 `coherent_hull`을 계산한다. 이 hull은 유한 수치 후보 집합의 범위이며 참 ODE 해의 오차반경이 아니다. method별 시간과 case 전체 시간도 별도로 보존한다.

기존 time/mixed 차이는 SHA `2bcd94edde08854599597ea8b962683a86cb5ca4af1ad0e1c3bec09b9e3c20cc`의 `evidence/reused/NATIVE_RETURN_AUDIT.json` 원문을 재사용한다. 반환 의존 행은 실제 pair가 없으면 HOLD다. 연속 스펙트럼·전역 기체온도 오차상한·전체 EoR·upstream Grackle 전체 동등성·관측 Bianchi/CMB는 해당 범위 검증 전까지 HOLD다.

## 게시와 백업을 읽는 순서

이번 intake 백업은 `BASS_HE_HE29_INTAKE_CHECKPOINT_20261020T0557Z_f6efa95f.tar.gz`, 53,483 bytes, SHA256 `f6efa95f75100e9b8b50cf532e2ca9101725dc99b305e211fe3c70c74d057760`다. Dropbox `id:BSpOijBcT10AAAAAAD_SRw`에서 raw 14/14 파일과 manifest payload 12/12를 검증했다. Drive는 업로드 결과 **UNKNOWN**, 실제 object ID·raw readback 미확인이다. 재시도하지 않으며 dual-provider 완료로 표시하지 않는다. 이 archive의 범위는 intake checkpoint다. [evidence/INTAKE_BACKUP.json](continuation_20261020T0557Z/evidence/INTAKE_BACKUP.json)을 읽는다.

기존 optimization 전체 `77f1c73e…`와 문서 closeout `3380c7c4…`의 양쪽 provider raw PASS는 불변 근거로 재사용한다. **새 구현·최종 문서의 백업 완료 여부는 새 DELIVERY 및 실제 PR/백업 영수증의 archive SHA·size·provider ID·content_hash·raw readback을 읽어 판단한다.** intake 백업이나 이전 archive의 PASS를 새 구현 전체 백업으로 대신 기록하지 않는다.

아래 내용은 직전 optimization 인계 원문이다. 현재 분석 lane 연결과 최신 게시·백업 판정은 이 절 및 새 lane의 DELIVERY/NCP_HANDOFF를 따른다.

---

# HE29 Codex/NCP 현재 인계 — 2026-10-20

## 최신 게시·백업 상태

최종 ABI2 실행 코드는 `a5d4711460c09b310b78c9692aa62534b7a843d3`이며 tree는 `681aa556cfffd9cf0ec678b8bf67de66ed6d36d9`다. 실제 Git readback **82/82 파일 일치, PASS**를 확인했다. 원래 과학 source·tests는 `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`로 유지한다. 아래의 `329f…`와 `8cb0…`는 시작점·중간 checkpoint 이력이다.

후속 문서 closeout의 실제 commit과 readback은 PR78 및 별도 closeout 영수증을 따른다. 후속 문서 HEAD와 실행 code pin을 구분한다. `optimization_20261020/DELIVERY.json`의 `implementation_publication.code_commit`과 `PUBLISHED_EXACT_READBACK_PASS` 상태를 읽으며, 실행 pin은 위 `a5d4711…`을 사용한다.

이번 완전 보존 패키지는 다음과 같다.

- 파일명: `BASS_HE_HE29_OPTIMIZATION_COMPLETE_20261020_77f1c73e.tar.gz`
- 크기: **4,719,121 bytes**
- SHA256: `77f1c73e8b4239cabcf03983ec9f0852fe334ac732544e410947935c7f4d7ab6`
- Drive ID: `1NBjWqsghFxbujCP6FELTfn7VPU-J8zfz`
- Dropbox ID: `id:BSpOijBcT10AAAAAAD_SLA`
- 검증: **양쪽 provider의 실제 raw-byte readback 및 검증 대상 91개 내부 파일 SHA 확인 PASS**

이전 `7bf7398b` 완전 archive도 이번에 Drive에서 다시 읽어 내부 229개 파일을 재검증했고 PASS했다. 실제 확인된 완전 백업을 현재 보존 근거로 사용한다. 기존 archive는 불변으로 유지하고, 후속 문서 closeout은 코드 게시·백업 snapshot과 분리한다.

게시된 builder는 별도의 clean Git worktree에서 실제 Cargo compile **146.650초, PASS**였다. 새 라이브러리 SHA는 `802190605e7b5e175f36d1d986e2a203c1835fbd6a39571895481b8efe9a92b4`이고, 측정에 사용한 `8299915d8490e958fbebe54d253d98c98b1b932a50e8640398ad4ec274abf434`와 구분한다. source·compiler·flags 일치와 경로·ELF layout 차이는 `optimization_20261020/evidence/PUBLISHED_BUILD_VALIDATION.json`에 기록했다. 이 빌드는 로컬 검증이며 HE29 native 실행이나 NCP 제출이 아니다.

최신 관측 상태는 **기준해 0/4, packed canary NOT_RUN, 이번 NCP 제출·시작 0건**이다. 미반환 NCP 프로세스는 미관측이며 Remote Desktop Commander 월간 quota의 재시도·재연결 금지를 유지한다. 다음 실행자는 새 반환을 먼저 분석하고 아래 실행 순서를 따른다. 기존 Bash 실행 블록은 이번 문서 정리에서 변경하지 않았다.

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
