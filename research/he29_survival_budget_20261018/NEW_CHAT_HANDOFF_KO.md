# 다음 채팅 인계: BASS_HE HE29 최적화 후속

`$physmath-research-loop`로 BASS_HE HE29 작업을 이어간다. 이번 작업에서는 실행 코드 작성, 새 경량 검증, 실제 Git 게시와 완전 백업 검증까지 끝냈다. 다음 실행자는 먼저 새 native 반환을 확인하고, NCP에서는 준비된 코드의 컴파일·작은 환경 수정·실제 실행을 맡는다. 완료된 연구와 검사를 반복하지 않는다.

## 1. 최신 실제 상태

2026-10-20 intake에서 새 HE29 native 반환은 발견되지 않았다. 원래 네 기준해는 관측상 **0/4**, 선택적 packed canary는 **NOT_RUN**, 이번 NCP 제출·시작은 **0건**이다. 미반환 NCP 프로세스 상태는 미관측이다. Remote Desktop Commander가 반환한 월간 quota에 따른 재시도·재연결 금지를 유지한다.

다음 채팅에서는 최신 GitHub, 관련 Drive·Dropbox, 접근 가능한 NCP 저장 결과와 프로세스부터 읽는다. 새 반환이 있으면 source·binary·table identity를 확인하고 저장된 결과를 먼저 분석한다. 다른 REI 또는 VigilODE 프로젝트의 native 결과를 HE29 완료로 계산하지 않는다. 사용자에게 파일 다운로드·업로드·터미널 입력을 요청하지 않는다.

## 2. 먼저 실제로 읽을 파일

최상위 문서와 기존 게시 영수증:

- `README_KO.md`
- `DAG_STATUS.json`
- `CODEX_HANDOFF_PROMPT_KO.md`
- `NEW_CHAT_HANDOFF_KO.md`
- `results/publication_retry/DELIVERY.json`
- `results/publication_retry/CLOSEOUT_RECEIPT.json`

이번 최적화의 실행·연구·보존 상태:

- `optimization_20261020/README_KO.md`
- `optimization_20261020/NCP_HANDOFF_KO.md`
- `optimization_20261020/RESEARCH_KO.md`
- `optimization_20261020/PERFORMANCE_KO.md`
- `optimization_20261020/DAG_STATUS.json`
- `optimization_20261020/DELIVERY.json`
- `optimization_20261020/evidence/PUBLISHED_BUILD_VALIDATION.json`

현재는 standalone `physmath-research-loop` 1.0.0의 진행 상태를 따른다. 과거 1.3.0으로 생성된 근거는 해당 버전의 기록으로 재사용한다. 새 DAG와 보고서에서 완료 단계를 읽고 그 단계의 연구·검사를 다시 시작하지 않는다.

## 3. 고정 코드와 게시 정체성

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: `research/he29-survival-budget-20261018`
- 최종 ABI2 실행 코드: `a5d4711460c09b310b78c9692aa62534b7a843d3`
- 실행 코드 tree: `681aa556cfffd9cf0ec678b8bf67de66ed6d36d9`
- 실제 Git readback: **82/82 파일 일치, PASS**
- 원래 과학 source·tests: `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`
- HE28 parent: `a41dd37124e34cb22bb9782aaf687a0da91640b7`
- 원본 native owner: `f7830e2f55e7a1938bc3c98f61b60651f8dae474`
- VigilODE dependency: `a21d573980f66fe02891bd216153443b5352f921`

최종 실행 코드 게시와 후속 문서 closeout은 별도다. 후속 문서 closeout의 실제 commit과 readback은 PR78 및 별도 closeout 영수증을 따른다. 최신 문서 HEAD를 실행 code pin으로 대신 사용하지 않는다. `optimization_20261020/DELIVERY.json`의 `implementation_publication.code_commit`과 `PUBLISHED_EXACT_READBACK_PASS` 상태를 확인한다. 해당 코드 값은 위의 `a5d4711…`이다.

이번 시작 HEAD는 `329f838399f24d3952f780d469ad657d8630c4e2`, 첫 최적화 checkpoint는 `8cb0ebb91a78d2f1b751caa1c3ffc5d170ddfe41`이며 당시 19개 파일의 Git readback이 일치했다. 이들은 중간 이력이다. 이전 ABI1 코드 `57642252991b5c453db66eb5a078e6a62cc6f4ea`와 함께 최종 ABI2 실행 pin을 대신하지 않는다. S2 미게시 상태는 이미 해소됐으므로 과거 `ncp/PUBLISH.sh`를 다시 실행하지 않는다.

## 4. 실제 검증된 완전 백업

이번 완전 보존 패키지:

- 파일명: `BASS_HE_HE29_OPTIMIZATION_COMPLETE_20261020_77f1c73e.tar.gz`
- 크기: **4,719,121 bytes**
- SHA256: `77f1c73e8b4239cabcf03983ec9f0852fe334ac732544e410947935c7f4d7ab6`
- Drive ID: `1NBjWqsghFxbujCP6FELTfn7VPU-J8zfz`
- Dropbox ID: `id:BSpOijBcT10AAAAAAD_SLA`
- 검증: **Drive·Dropbox 모두 실제 raw-byte readback 및 검증 대상 91개 내부 파일 SHA 확인 PASS**

이전 `7bf7398b` 완전 archive도 이번에 Drive에서 새로 읽어 내부 229개 파일을 재검증했고 PASS했다. 기존 `c47c5efc`, `798afac1`, `7bf7398b`, `88285fa4` archive는 불변으로 보존한다. 현재 인계의 백업 완료 근거는 위에서 실제 검증한 완전 패키지다. 후속 문서 closeout은 코드 게시 및 이 보존 snapshot과 구분해 기록한다.

## 5. 새 구현과 경량 검증의 범위

새 canonical CSR 조립은 제조 fixture에서 원래 값·구조와 정확히 일치했고, 조립 실험에서 8.35–8.78배의 속도 차이를 측정했다. 새 Rust packed JVP는 동일 상태·시간의 정확한 cache key와 원래 열 누산 순서를 유지한다. 합성 IVP의 순차 packed 경로에서는 1.38–1.53배를 측정했다. 1·2·4 thread의 endpoint 비트와 attempt 수는 같았지만 2·4 thread가 더 느려 NCP는 **1 thread**를 유지한다. 두 배율은 서로 다른 실험이므로 곱하지 않는다. 실제 HE29 native 속도와 전체 process 메모리는 아직 측정하지 않았다. 자세한 사례·source·binary 정체성은 `PERFORMANCE_KO.md`와 연결된 원시 영수증을 읽는다.

게시된 `ncp/build_bridge.py`를 별도의 clean Git worktree에서 실제 실행했고 Cargo compile **146.650초, PASS**였다. 이것은 로컬의 게시 빌더 검증이며 NCP native 실행이 아니다. 이 빌드에서 test·solver·원본 native owner 호출은 모두 0이었다.

두 라이브러리의 정체성은 구분한다.

| 용도 | 크기 | SHA256 |
|---|---:|---|
| 실제 합성 benchmark에 사용한 라이브러리 | 5,450,976 bytes | `8299915d8490e958fbebe54d253d98c98b1b932a50e8640398ad4ec274abf434` |
| 게시된 빌더로 새로 만든 라이브러리 | 5,451,240 bytes | `802190605e7b5e175f36d1d986e2a203c1835fbd6a39571895481b8efe9a92b4` |

두 빌드의 Rust 소스 5개, rustc·Cargo binary SHA, compiler flags는 일치한다. 정적 검사에서 staging 경로와 ELF layout 차이를 관측했고, 기존 benchmark 라이브러리는 그대로 보존했다. 새 바이너리를 같은 바이트로 처리하거나 새 바이너리의 수치 동등성을 검사했다고 주장하지 않는다. 실제 비교 기록은 `evidence/PUBLISHED_BUILD_VALIDATION.json`과 `evidence/published_build_20261020/`에 있다.

## 6. 입력 보정과 다음 native 작업

원본 1569의 입력 manifest에는 `inputs/study/m8_r2_n64/TABLE.json`의 SHA가 62자리로 게시돼 있었다. 전체 SHA가 고정된 원본 a70 archive와 그 내부 manifest를 확인해 누락된 `4b` 두 문자만 복원했다. 22개 DATA의 실제 복원, preflight, 독립 검토는 PASS다. 원본 DATA·물리식·반응률·허용치는 변경하지 않았다.

원래 1569 execution checkout에는 다음 두 패치를 모두 적용한다.

- `ncp/REUSE_SOURCE_VALIDATION_20261019.patch`: 완료된 pytest 실행 한 줄을 제외하고 재사용 근거와 overlay 정체성을 기록한다.
- `ncp/REPAIR_INPUT_MANIFEST_20261020.patch`: 입력 manifest의 누락된 두 문자를 보정한다.

정확한 SHA와 실행 명령은 `CODEX_HANDOFF_PROMPT_KO.md`에 있다. 실행 source는 Git에서 가져오고 archive에서는 검증된 DATA만 사용한다. `START_REFERENCES.sh`가 별도의 원본 입력 archive에서 22개 DATA를 자동 복원하므로 사용자 수동 전달이 필요하지 않다.

다음 우선순위는 원래 네 기준해다. 모두 m8/GL4/q0이며 각 case에 Radau+DOP853을 사용한다.

| 순서 | r | table nodes |
|---:|---:|---:|
| 1 | 2 | 512 |
| 2 | 4 | 512 |
| 3 | 8 | 512 |
| 4 | 4 | 1024 |

부분 반환이 있으면 완료된 case는 재실행하지 않는다. 네 쌍이 모두 admit된 뒤에만 단일 r4/table512 packed canary를 실행한다. `optimization_20261020/NCP_HANDOFF_KO.md`는 clean publication checkout에서 빌드한 다음 DATA를 복원하고, preflight 뒤 canary를 시작하는 절차를 제공한다. runner는 네 case 전체의 source·input·binary·Python·NumPy·SciPy 정체성, 재생성 table SHA, 1 thread 및 process-group 시간 상한을 확인한다. 검증된 22개 입력 DATA 외의 untracked 파일과 tracked 코드 변경은 거절한다.

HE28 pilot과 6개 transport, HE29 finite-donor 90사례·720구간 및 50개 검사, 기존 VigilODE Python 96개·Rust smoke 3개·Schur 합성 검사 23개는 보존 근거를 재사용한다. 새 solver 개발이나 무조건적인 격자 확대를 시작하지 않는다.

## 7. 유지할 과학적 범위와 반환 기준

기존 finite-donor survival 구간의 최대 최종 폭 `2.2487671447191104e-12`는 양의 유한 donor에 대한 조건부 결과다. GL256/512 차이 `2.7755575615628914e-16`은 수치적 안정성 지표다. 둘 다 엄밀한 연속적분 오차나 전역 기체온도 오차상한으로 확대 해석하지 않는다.

기존 pilot의 `3.951006358291365e-14`는 절대 fraction 차이였다. 절대 fraction `1e-11`, method 간 온도차 `1e-9 K`, 원래 number·energy·species 보존 및 양성성 gate를 유지한다. 같은 r/table의 기준해와 저장된 n32/n64 transport를 비교해 시간오차를 분리하고, r2→4·r4→8과 r4의 table512→1024 차이는 각각 strip·table 민감도로 분석한다.

새 결과와 재사용한 결과를 DAG에서 분리한다. 접수 증거가 있을 때만 SUBMITTED로 바꾸고, source·binary·table·runtime·원시 실패·partial endpoint·native JSONL·process 영수증을 보존한다. 새 반환은 별도 results branch/Draft PR와 create-only Drive·Dropbox 백업으로 게시하고, archive SHA/size, provider object ID/content_hash, raw-byte readback을 각각 기록한다.

**연속 스펙트럼, 전체 EoR, 전역 gas-temperature 오차상한, upstream Grackle 전체 동등성, 관측 Bianchi/CMB는 해당 범위의 근거가 생길 때까지 HOLD다.**
