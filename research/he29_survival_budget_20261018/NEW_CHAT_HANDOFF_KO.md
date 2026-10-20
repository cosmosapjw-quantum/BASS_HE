# 다음 채팅 인계: BASS_HE HE29 공유 기준해·부분 반환 분석

현재 최종 통합 보존본은 `BASS_HE_HE29_REFERENCE_BUDGET_COMPLETE_20261020_7a86d5bb.tar.gz`(6,621,294 bytes, SHA256 `7a86d5bbe27da9da52584edb27145b626c6954455729c9af3365147fc4802c08`)다. Dropbox `id:BSpOijBcT10AAAAAAD_SUQ`의 실제 raw GET과 outer70/70·manifest 포함71/71 검증이 PASS다. 문서 snapshot은 `a143b08eeeb37e7f8cdbc78d84f750c321a220be`, 실행 분석 pin은09929b0이다. Drive 단일 업로드는43초 동안 접수 ID/완료 응답이 없어 UNKNOWN이고, 한 번의 조회에서 exact name을 찾지 못했으며 재시도·우회는0이다. 기존 f6·567의 standalone UNKNOWN도 바꾸지 않는다. 최신 인계 metadata는 후속 작은 handoff 묶음/PR78의 실제 영수증에 따로 보존한다. 상세 실제 상태는 `continuation_20261020T0557Z/evidence/FINAL_BACKUP_RECEIPT.json`과 DELIVERY를 읽는다.

`$physmath-research-loop`를 사용해 BASS_HE HE29 작업을 이어서 진행해 줘. **먼저 최신 GitHub, 관련 branch와 반환 artifact, 관련 저장소, Drive·Dropbox 변경분에서 새 HE29 native 반환이 있는지 확인해 줘.** 기존 intake와 완료 근거를 읽고 그 이후 변경분만 확인해. 새 결과가 있으면 source·binary·table identity를 읽고 저장된 반환부터 분석해. 완료된 HE28 연구, HE29 source 검증, VigilODE 최적화, 이번 budget 검증을 반복하지 마.

## 1. 현재 실제 상태와 다음 판단

2026-10-20 05:57 UTC부터 진행한 후속 단위는 `continuation_20261020T0557Z`다. 마지막 관측에서 새 HE29 기준해는 **0/4**, 선택적 packed canary는 **NOT_RUN**이다. 이번 NCP 제출은 **0건**, 시작은 **0건**이며 미반환 프로세스는 **미관측**이다. Remote Desktop Commander의 월간 quota에 따른 **재시도·재연결 금지**를 유지한다. 작업이 제출됐거나 원격 프로세스가 없다고 추정해 상태를 바꾸지 마.

최신 저장 결과를 읽을 수 있으면 먼저 분석해. 접근 가능한 실행자가 현지 프로세스와 저장 결과를 확인하고 중복 작업이 없음을 확인한 뒤에만 필요한 미완료 case를 시작해. 다른 REI/VigilODE 프로젝트에는 새 native·합성 결과가 있지만 HE29의 네 reference pair와 source/binary/model 계약이 다르다. 이들의 실제 정체성과 적용 범위를 보존하고 HE29 완료 수에 넣지 마.

사용자에게 다운로드·업로드·터미널 입력을 요구하지 마. 실행 시작점은 Git이며 archive는 검증한 DATA만 공급한다. NCP에는 준비된 코드의 컴파일·작은 환경 수정·실제 실행만 맡겨. 새 solver 개발, 기존 transport 재실행, 무조건적인 전체 격자 확대를 시작하지 마.

## 2. 먼저 실제로 읽을 문서와 영수증

아래 모든 경로의 기준은 `research/he29_survival_budget_20261018/`다. repository의 `AGENTS.md`와 현재 적용할 skill의 실제 지시를 함께 읽어.

| 구분 | 읽을 파일 |
|---|---|
| canonical 인계 | `README_KO.md`, `DAG_STATUS.json`, `CODEX_HANDOFF_PROMPT_KO.md`, `NEW_CHAT_HANDOFF_KO.md` |
| 기존 게시 마감 | `results/publication_retry/DELIVERY.json`, `results/publication_retry/CLOSEOUT_RECEIPT.json` |
| 이번 분석 단위 | `continuation_20261020T0557Z/README_KO.md`, `RESEARCH_KO.md`, `DAG_STATUS.json`, `DELIVERY.json`, `NCP_HANDOFF_KO.md` |
| 최신 intake | 같은 lane의 `evidence/INTAKE_PUBLICATION.json`, `INTAKE_BACKUP.json`, `BASS_GITHUB_DELTA.json`, `RELATED_GITHUB_DELTA.json`, `BACKUP_DELTA_INTAKE.json`, `LOCAL_INTAKE_AND_GAPS.json` |
| 새 분석 검증 | 같은 lane의 `evidence/LINEAR_BUDGET_CHECKS/`, `PARTIAL_RETURN_CHECKS/`, `ANALYZE_BUDGET_CHECKS/`, `LOCAL_NO_RETURN_CHECK/`, `THEORY_REVIEW.json`, `WOLFRAM_BUDGET.json`, `CODE_REVIEW.json`, `CLI_CODE_REVIEW.json` |
| 기존 optional 최적화 | `optimization_20261020/DELIVERY.json`, `DAG_STATUS.json`, `NCP_HANDOFF_KO.md`, `PERFORMANCE_KO.md`, `evidence/PUBLISHED_BUILD_VALIDATION.json` |

위 표에서 “같은 lane”은 `continuation_20261020T0557Z/`를 뜻한다. 새 DELIVERY가 연결하는 최종 Git/PR/backup 영수증도 실제로 읽어. 문서 작성 시점과 code pin, provider upload 접수와 raw-byte 검증을 구분해.

초기 intake는 당시 읽은 standalone 1.0.0 규약을 사용했고, 이후 사용자가 명시한 plugin 1.3.0을 실제로 읽어 통합·검증·보존에 적용했다. 버전 전환 때문에 완료한 단계의 근거를 다시 만들거나 검사를 반복하지 마. 다음 작업은 현재 DAG에서 실제로 남은 실행·반환 분석에 연결해.

## 3. Git과 고정 정체성

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: `research/he29-survival-budget-20261018`
- PR78은 Draft/open/unmerged로 유지한다.

| 역할 | 정체성 |
|---|---|
| 새 budget·부분 반환 분석 code pin | `09929b0a06a833f0c2497e72f074ec8694a264df` |
| 분석 tree·실제 게시 검증 | `f35be906ea4a201849516ee58825b6fa03597a5a`; 2026-10-20 07:02:52 UTC 실제 Git fetch/show 45/45 bytes·SHA PASS |
| 새 분석 publication gate | `continuation_20261020T0557Z/DELIVERY.json`의 `implementation_publication.status=PUBLISHED_EXACT_GIT_READBACK_PASS` 및 전체 `code_commit` |
| 이번 intake checkpoint | `3b125fc3cf80ce715353be17f640f2d9a5fb9f4a`; tree `c7ccb7b1154f41bd8e506e47f2ecbf909452c427`; 실제 Git 12/12 byte readback PASS |
| 직전 optimization 문서 closeout | `1765522318438e966e61d8a72f12084550da399d`; 실제 문서 39개 readback PASS |
| 기존 ABI2 packed 실행 code pin | `a5d4711460c09b310b78c9692aa62534b7a843d3` |
| ABI2 tree·게시 검증 | `681aa556cfffd9cf0ec678b8bf67de66ed6d36d9`; 실제 Git 82/82 readback PASS |
| 원래 HE29 science·tests | `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f` |
| HE28 parent PR77 | `a41dd37124e34cb22bb9782aaf687a0da91640b7` |
| 원본 Rust owner | `f7830e2f55e7a1938bc3c98f61b60651f8dae474` |
| VigilODE dependency | `a21d573980f66fe02891bd216153443b5352f921` |

새 분석 코드, 원래 baseline 실행, 기존 packed canary는 각각 위 pin을 사용한다. 이후 문서 closeout HEAD를 이들 code pin으로 바꾸지 마. 최신 실행 코드를 과거 `387976f` 미게시 상태나 ABI1 `57642252991b5c453db66eb5a078e6a62cc6f4ea`, 중간 `8cb0ebb91a78d2f1b751caa1c3ffc5d170ddfe41`로 되돌리지 마. HE29 S2 미게시 문제는 이미 해결됐으므로 `ncp/PUBLISH.sh` 또는 미게시 복구 절차를 실행하지 마.

## 4. 이번에 완료한 분석 구현과 검증

새 분석은 저장 endpoint의 후처리다. 원래 물리식·반응률·허용치·적분 경로는 변경하지 않았다.

`partial_returns.py`는 absent, identity/table-only, method-only, 두 method가 있지만 RESULT가 없는 상태, failure/timeout, 완성·유효 또는 invalid 상태를 구분한다. 물리적 pair admission은 기존 `check_result`·`admit_pair`를 재사용한다. 원래 source/input/parent maps, owner, binary build receipt, 6점 native qualification, table SHA, thread와 runtime을 확인하며 반환 파일 간 내용 일관성은 별도 분석 계약으로 기록한다. process timeout/실패 관측과 완료 결과의 채택 여부도 분리한다. 한 case가 invalid여도 다른 valid case는 보존한다.

`linear_budget.py`와 `analyze_budget.py`는 같은 model/table의 기준 후보 `θ`와 저장 transport `T`를 연결한다. 개별 `T−θ`와 strip·table 대비를 부호를 유지해 출력한다. strip 대비의 식은 다음과 같다.

`T_b−T_a = (θ_b−θ_a) + (T_b−θ_b) − (T_a−θ_a)`

공유된 θ key의 계수를 먼저 합친 뒤 정확한 유리수 산술로 projection을 수행하므로 assembled closure는 정확히 0이다. `product_hull`은 각 key의 두 후보를 독립적으로 선택하고, `coherent_hull`은 모든 key에서 같은 method label을 선택한다. exact hull 폭과 binary64 표시 폭을 구분한다. 서로 다른 provenance cohort 사이의 대비는 HOLD다.

현재 근거는 다음과 같다.

| 새 검증 | 실제 결과 |
|---|---|
| 선형식 코어 | 10개 test method, 첫 실행 PASS |
| 부분 반환 분류기 | 12개 test method, 첫 실행 PASS |
| CLI·DATA 연결 통합 | 6개 test method, 첫 실행 PASS |
| 위 새 구현 검사 합계 | **28개**; 완료 suite 재실행 없음 |
| 독립 이론 제조계 | 20개 고유 사례 |
| CAS | signed closure 0, 공유 reference cancellation 0 |
| 실제 반환 부재 경로의 새 CLI | exit **1**, **HOLD**, admitted 0/4, reference-dependent 행 0, 원래 DATA **18/18 SHA PASS** |
| 이번 단위의 이전 결과·검사·native·solver·기존 audit 계산 재실행 | **0** |

실제 CLI의 로컬 HOLD는 원격 NCP 프로세스 관측이 아니다. 위 제조계와 대수 검증도 새 HE29 reference pair를 대신하지 않는다. 기준해에 의존하는 물리적 분해 값은 여전히 HOLD다.

기존 `src/analyze_return.py`가 계산한 time difference·mixed difference·sign change는 다시 계산하지 않았다. 원본 archive member의 `NATIVE_RETURN_AUDIT.json` 1,934 bytes를 그대로 복원해 재사용했다. SHA256은 `2bcd94edde08854599597ea8b962683a86cb5ca4af1ad0e1c3bec09b9e3c20cc`이며 `continuation_20261020T0557Z/evidence/reused/PROVENANCE.json`에 archive/member 정체성이 있다.

## 5. 원래 1569 실행과 자동 DATA 복원

`CODEX_HANDOFF_PROMPT_KO.md`에 보존된 baseline Bash를 사용한다. 새 isolated Git checkout에서 `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`로 detach하고 아래 두 overlay를 모두 적용한다.

| 대상 | SHA256 또는 Git blob |
|---|---|
| `ncp/REUSE_SOURCE_VALIDATION_20261019.patch` | `cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e` |
| `ncp/REPAIR_INPUT_MANIFEST_20261020.patch` | `71f16bc8bc946bdd9107c476662fb83b9812cb4078045b933066fca300eb1e85` |
| 원본 bootstrap Git blob | `ed227e2937f554bd5ecda4bf24dd5597b73a77a4` |
| 재사용 overlay 적용 bootstrap SHA256 | `11d0ad0125f40a2890dac82e5103f13d17e6066f41440eabb06c7a8b1f319bc2` |
| 보정된 INPUT manifest SHA256 | `28917c4c292988a72dd4154443555437ed1de06158ff91a2104c0b189aacaca7` |
| PARENT manifest SHA256 | `7c3262d58a28d4d272a9bb90e0a018be9d35306312f45787a5569698654e9f82` |

첫 overlay는 완료 pytest 실행 한 줄을 제외하고 재사용 근거를 기록한다. 둘째 overlay는 `inputs/study/m8_r2_n64/TABLE.json`의 SHA에서 누락된 `4b` 두 문자를 복원한다. 원본 archive 및 내부 manifest와 대조한 정확한 DATA SHA는 `b31a862f59c96492be7e6b218b9cc5e78de9e5c2dd72433b6b4b4b8b7743e0d5`다. DATA·모형·허용치는 그대로다. 기존 복원 22개와 preflight의 완료 근거를 재사용한다.

원본 입력 archive는 `BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz`, **129,635 bytes**, SHA256 `a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205`다. Drive ID는 `1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi`, Dropbox ID는 `id:BSpOijBcT10AAAAAAD_Ncg`다. `START_REFERENCES.sh`의 자동 복원기가 이 archive에서 SHA 검증한 **22개 DATA만** 복원한다. archive의 코드나 binary를 실행 출처로 사용하지 않는다. 기존 불일치 DATA는 덮어쓰지 않는다.

이미 baseline DATA가 복원돼 있으면 새 분석 checkout에서 이를 `--data-root`로 공유한다. 그 경로는 `inputs`가 아닌 **baseline checkout의 `research/he29_survival_budget_20261018` 디렉터리**다. source·manifest는 새 분석 Git pin에서 읽는다. `--study-root`를 생략하면 이 root 아래 `inputs/study`를 사용한다. DATA가 사라졌을 때는 기존 `ncp/RESTORE_VERIFIED_INPUTS.py`로 검증 복원하며 입력 복원을 위해 기준해 실행 starter를 다시 호출하지 않는다.

## 6. 다음 네 기준해와 그 이후 한 canary

새 반환을 확인하고 중복 실행이 없을 때 필요한 미완료 case만 실행한다. 전부 **m8/GL4/q0**이며 case마다 **Radau+DOP853**이다.

| 순서 | r | table nodes | 반환 디렉터리 |
|---:|---:|---:|---|
| 1 | 2 | 512 | `references/m8_r2_table512` |
| 2 | 4 | 512 | `references/m8_r4_table512` |
| 3 | 8 | 512 | `references/m8_r8_table512` |
| 4 | 4 | 1024 | `references/m8_r4_table1024` |

case당 **3,600초**는 table과 두 적분기를 합한 process-group 상한이다. table **600초**, 예상 allocation **2 GiB**, numerical **1 thread**, 첫 실패 중단과 원시 실패·partial output 보존을 유지한다. 2 GiB는 전체 RSS의 강제 상한이 아니다.

원래 상대/절대 적분 허용치 `1e-10/1e-12`, pair 절대 fraction `1e-11`, method 간 온도차 `1e-9 K`, number defect `3e-15/H`, energy defect `3e-12 eV/H`, species defect `3e-12` 및 양성성 gate를 유지한다. table512는 같은 r의 저장 table SHA와 같아야 한다. table1024는 별도 민감도이며 해당 transport를 만들어 넣지 않는다.

네 pair가 모두 admit된 뒤에만 **단일 r4/table512 packed canary**가 선택 가능하다. `optimization_20261020/NCP_HANDOFF_KO.md`에 따라 clean a5 Git에서 빌드하고 실제 binary/source/table/runtime gate를 통과한다. VigilODE a21의 기존 RODAS5P–GMRES, 원래 RHS·FD·partial-time과 ledger를 포함한 전체 state error norm을 유지한다. 기본 thread는 **1**이다. 합성 측정에서 2·4 thread가 느렸으므로 확대하지 않는다.

기존 합성 packed 속도 1.38–1.53배와 CSR 조립 8.35–8.78배는 서로 다른 측정의 재사용 근거다. 두 값을 곱하거나 실제 HE29 native 속도라고 주장하지 않는다. 실제 HE29 속도와 전체 process 메모리는 아직 미측정이다.

기존 합성 benchmark library SHA는 `8299915d8490e958fbebe54d253d98c98b1b932a50e8640398ad4ec274abf434`다. 게시 builder의 compile-only 결과는 `802190605e7b5e175f36d1d986e2a203c1835fbd6a39571895481b8efe9a92b4`이며 compile **146.650초 PASS**였다. 후자의 별도 수치 동등성 실행을 주장하지 않는다. 두 binary와 해당 source/compiler/flags 영수증을 각각 보존한다.

## 7. 반환 분석과 결과 보존

새 분석 실행 Bash는 `continuation_20261020T0557Z/NCP_HANDOFF_KO.md`에 있다. 최신 DELIVERY가 가리키는 고정 analysis commit의 clean Git checkout에서 다음 기존 경로를 연결한다.

- `--root`: 원래 baseline WORK의 `references`.
- `--data-root`: 원래 22개 DATA가 복원된 baseline checkout의 HE29 root.
- `--binary`: 실제 원본 owner binary가 보존돼 있을 때 해당 파일.
- `--out`: 새 분석 디렉터리의 아직 존재하지 않는 JSON.

결과는 create-only·atomic·fsync로 저장한다. exit 0은 네 pair와 필요한 대비·입력이 모두 유효함을, exit 1은 누락·부분 반환·cohort 불일치에 따른 HOLD를, exit 2는 invalid 입력·반환 또는 CLI 오류를 뜻한다. JSON이 생성되지 않았으면 실행 로그에서 CLI 자체 오류를 구분한다. 반환 snapshot을 바꾸면 새 output 경로를 사용한다.

각 case의 IDENTITY, TABLE, SAVED_POINT_PARITY, Radau, DOP853, RESULT 또는 FAILURE, native JSONL, build와 process COMMAND/RECEIPT, stdout/stderr·부분 endpoint를 보존한다. source/binary/owner·input/parent maps·6점 qualification·thread와 Python/NumPy/SciPy 정체성을 함께 보존한다. 실제 binary bytes를 읽지 않았다면 `binary_bytes_readback=NOT_PROVIDED`를 남긴다. method별 시간과 case 전체 시간은 별도 범위이며 이를 섞은 speedup을 만들지 않는다.

한 case가 실패하거나 잘못돼도 다른 유효 case와 독립 대비는 분석한다. source/binary/parent/input/thread/runtime cohort가 다른 pair 사이의 대비는 HOLD로 둔다. 새 분석의 code pin·DATA provenance·publication DELIVERY snapshot·exit code도 반환에 포함한다.

## 8. 게시·백업의 실제 상태

이번 intake checkpoint는 다음 패키지로 보존됐다.

- 파일: `BASS_HE_HE29_INTAKE_CHECKPOINT_20261020T0557Z_f6efa95f.tar.gz`
- 크기: **53,483 bytes**
- SHA256: `f6efa95f75100e9b8b50cf532e2ca9101725dc99b305e211fe3c70c74d057760`
- Dropbox: `id:BSpOijBcT10AAAAAAD_SRw`
- Dropbox 검증: provider content_hash 일치, **전체 raw bytes 및 내부 14/14 파일·manifest payload 12/12 PASS**.
- Drive: **UNKNOWN**. provider ack·object ID를 받지 못했고 raw readback은 미실행이다. 재시도하지 않는다.
- 범위: intake 12개 Git 파일과 metadata 2개. 새 구현 전체의 백업을 뜻하지 않는다.

기존에 완료한 다음 두 archive의 검증은 재사용한다.

| 패키지 | 크기·SHA256 | 실제 provider와 검증 |
|---|---|---|
| `BASS_HE_HE29_OPTIMIZATION_COMPLETE_20261020_77f1c73e.tar.gz` | 4,719,121 bytes; `77f1c73e8b4239cabcf03983ec9f0852fe334ac732544e410947935c7f4d7ab6` | Drive `1NBjWqsghFxbujCP6FELTfn7VPU-J8zfz`; Dropbox `id:BSpOijBcT10AAAAAAD_SLA`; 양쪽 raw·91개 payload SHA PASS |
| `HE29_OPTIMIZATION_HANDOFF_CLOSEOUT_20261020_3380c7c4.tar.gz` | 1,714,101 bytes; `3380c7c432d6c05840b215b5ff129e8209e7ce5908221ed75d9a3e4a6f6e19aa` | Drive `12l06rbWAjxbsnJaLlsvRBTiXXBUYAhsd`; Dropbox `id:BSpOijBcT10AAAAAAD_SMA`; 양쪽 raw·47개 payload 및 내부 checkpoint 21개 SHA PASS |

새 분석 구현과 이 최종 인계의 백업 상태는 `continuation_20261020T0557Z/DELIVERY.json` 및 연결된 실제 PR/backup receipt에서 읽어. 해당 archive SHA·size, provider ID·content_hash, 실제 raw-byte 검증과 내부 파일 수를 각각 확인해. 문서가 아직 실제 값을 담지 않았다면 그 provider의 완료를 추정하지 마. 기존 archive는 불변으로 유지한다.

새 native 결과는 별도 results branch/Draft PR와 create-only Drive·Dropbox 백업으로 보존한다. 결과 유효성, source provenance, Git 게시, archive 보존 상태를 DAG에서 각각 기록하고 실제 접수 근거가 있을 때만 SUBMITTED/STARTED로 표시한다.

## 9. 완료 연구의 재사용과 과학적 HOLD

HE28 native pilot과 6/6 transport, HE29 positive finite-donor 90사례·720구간, 기존 50개 source/input 검사, VigilODE·Schur·ABI2의 완료 구현·검사와 이번 28개 검사를 재사용한다. 완료했다는 이유를 확인하려고 같은 연구를 다시 실행하지 마.

기존 survival 구간의 최대 최종 폭 `2.2487671447191104e-12`는 양의 유한 donor에 조건부인 결과다. GL256/512 차이 `2.7755575615628914e-16`은 수치적 안정성 지표이며 연속적분의 엄밀한 오차 증명이 아니다. 기존 pilot `3.951006358291365e-14`는 절대 fraction 차이였고 절대 `1e-11` gate는 그대로다.

HE28의 r2→4 온도차는 저장 audit에서 n32 **+2.5017143912009487e-10 K**, n64 **−6.697344900885582e-10 K**로 읽는다. 이번 분석은 동일 model/table의 공유 기준 후보를 붙여 signed reference-conditioned 분해를 제공한다. 이 잔차는 선택한 수치 기준과의 차이이며 참 시간 오차의 인증값이 아니다. 두 solver의 합의나 finite-candidate hull을 참 해가 포함된다는 증명으로 사용하지 마.

**연속 스펙트럼, 전역 기체온도 오차상한, 전체 EoR, upstream Grackle 전체 동등성, 관측 Bianchi/CMB는 해당 범위의 근거가 생길 때까지 HOLD다.** 지금 남은 우선순위는 새 반환의 identity 판독과 부분 분석, 그 다음 준비된 네 기준해의 필요한 실행, 마지막으로 조건을 만족한 단일 canary다.
