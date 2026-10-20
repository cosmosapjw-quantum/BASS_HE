# HE29 후속 분석: 공유 기준해와 부분 반환

2026-10-20 05:57 UTC 재개 단위다. 최신 GitHub·관련 저장소·백업·로컬 반환을 먼저 읽은 뒤, 공유 기준해를 보존하는 정확한 signed 분해와 부분 반환 분석기를 구현했다. **새 테스트 28개 첫 PASS, 분담 독립 검토 PASS, 실제 로컬 분석은 기준해 0/4·HOLD**다. 이번 작업은 원래 solver·물리식·반응률·허용치를 변경하지 않는다.

## 실제 상태

| 축 | 상태와 근거 |
|---|---|
| DAG | R1–R9 및 새 분석기의 C1–C9 완료. R10/C10 게시·보존·인계 진행. 조건부 산술 검증과 실제 native 미완료를 분리한 `DAG_STATUS.json` 참고 |
| 게시 | intake `3b125fc3cf80ce715353be17f640f2d9a5fb9f4a`, 실제 12/12 Git readback PASS. 새 구현 및 후속 인계의 실제 commit은 `DELIVERY.json`과 publication receipt에 기록 |
| 백업 | intake `f6efa95f…`: Dropbox raw bytes·내부 검증 PASS, Drive 단일 업로드 UNKNOWN·재시도 없음. 기존 COMPLETE `77f1c73e…`와 CLOSEOUT `3380c7c4…`의 dual raw PASS 재사용. 최종 새 묶음은 실제 provider receipt로 판정 |
| 새 실행 | HE29 native 0, NCP 제출/시작 0, HE28 transport 0, 기존 science·source·최적화 검사 재실행 0 |

Remote Desktop Commander의 기존 월간 quota 및 재시도·재연결 금지 상태를 유지한다. 미게시 NCP 프로세스는 관측하지 못했다. 로컬 경로가 없다는 사실을 원격 프로세스 부재로 확대하지 않는다.

## 새 구현

`src/linear_budget.py`는 입력 binary64를 각각 정확한 유리수로 변환하고, 반복 사용된 기준해의 계수를 먼저 합쳐 소거한다. key별 독립 Radau/DOP853 선택의 `product_hull`과 모든 key의 동일 method 선택인 `coherent_hull`을 따로 계산한다. exact width와 표시용 binary64 outward width를 구분한다.

`src/partial_returns.py`는 준비됨·method-only·실패·timeout·완성 상태를 구분하고 원래 admission contract를 재사용한다. method JSON, RESULT, source/binary/table identity와 실행 cohort를 연결하며, method 적분 시간과 전체 process 시간을 분리한다. 일부 잘못된 반환 때문에 다른 유효 부분을 폐기하지 않는다.

`src/analyze_budget.py`는 기존 transport DATA 18개를 고정 SHA와 model/table/owner/thread/source 계약에 대조해 읽는다. admit된 기준해에 대해서만 signed residual과 strip/table 대비를 만든다. 기존 `NATIVE_RETURN_AUDIT.json`은 원래 SHA를 확인한 bytes와 값을 그대로 포함하며 기존 time/mixed/sign 계산을 반복하지 않는다. 입력은 baseline checkout의 `--data-root`에서 재사용할 수 있고, code/manifest는 분석 Git revision에 고정된다. 출력은 create-only·atomic·fsync다.

finite-candidate hull은 저장된 두 수치 후보가 만드는 범위다. 참 ODE 해의 오차반경이나 연속 스펙트럼 인증을 뜻하지 않는다. 수식·전제·구성적 증명·원전 채택 위치는 `RESEARCH_KO.md`와 `THEORY_REVIEW_KO.md`에 있다.

## 이번 검증과 기존 근거 재사용

| 범위 | 이번 결과 | 근거 |
|---|---|---|
| 선형식 코어 | 새 10개 test method 첫 PASS | `evidence/LINEAR_BUDGET_CHECKS/` |
| 부분 반환 분류기 | 새 12개 test method 첫 PASS | `evidence/PARTIAL_RETURN_CHECKS/` |
| CLI·외부 DATA 연결 | 새 6개 test method 첫 PASS | `evidence/ANALYZE_BUDGET_CHECKS/` |
| 독립 제조 이론 | 20개 사례 PASS, 새 native 0 | `evidence/THEORY_REVIEW.json` |
| Wolfram | signed closure 0, 공유 reference 소거 0, 제조 product [9,11]/coherent [10,10] | `evidence/WOLFRAM_BUDGET.json` |
| 한 번의 분담 C9 | core/classifier와 CLI 연결 PASS, 중대 finding 0 | `evidence/CODE_REVIEW.json`, `evidence/CLI_CODE_REVIEW.json` |
| 실제 로컬 분석 | 18 DATA SHA 일치, admitted 0/4, reference-dependent rows 0, exit 1/HOLD, 오류 없음 | `evidence/LOCAL_NO_RETURN_BUDGET.json`, `evidence/LOCAL_NO_RETURN_CHECK/` |
| 새 인계 Bash | 구문 PASS, 실제 명령 미실행 | `evidence/NCP_HANDOFF_SYNTAX/` |

원래 HE29 science/test revision은 `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`, native owner는 `f7830e2f55e7a1938bc3c98f61b60651f8dae474`다. 완성된 ABI2 최적화 코드는 `a5d4711460c09b310b78c9692aa62534b7a843d3`, VigilODE는 `a21d573980f66fe02891bd216153443b5352f921`을 유지한다. 이전 검증·가속 측정·clean build는 완료 근거로 재사용하고 다시 실행하지 않았다. 이번 새 분석기는 Python 표준 라이브러리를 사용하며 새 Rust 의존성을 추가하지 않았다.

## intake 근거와 한계

- `evidence/BASS_GITHUB_DELTA.json`: 83개 BASS_HE branch의 변경 대조, PR78 및 반환 채널.
- `evidence/RELATED_GITHUB_DELTA.json`: VigilODE·REI·REC·HH·BASS·bass_cr의 새 source/binary/result identity.
- `evidence/BACKUP_DELTA_INTAKE.json`: 이전 전체 census를 재사용한 최신 provider 변경분 및 실제 읽기 범위.
- `evidence/PERSONAL_CONTEXT_INTAKE.json`: 다른 대화 검색 오류 및 이전 파일 결과를 새 실행 완료로 사용하지 않은 근거.
- `evidence/LOCAL_INTAKE_AND_GAPS.json`: 로컬 native 부재 관측과 기존 분석 연결의 공백.

관련 프로젝트에는 새 실행 결과가 있지만 HE29 네 pair의 계약과 다르다. 다른 대화 검색은 실제 오류를 반환했고, provider 색인은 누락·날짜 필터의 한계가 있었다. 확인된 범위에서 새 HE29 기준해는 0/4이며 모든 대화·미게시 원격 실행의 완전한 부재를 증명하지 않는다.

## 다음 실제 실행과 인계

원래 m8/GL4/q0의 `(r2,512)`, `(r4,512)`, `(r8,512)`, `(r4,1024)`에서 각각 Radau+DOP853를 수행한다. 새 반환이 있으면 identity를 읽고 분석부터 하며, 완료 case는 다시 실행하지 않는다. 네 pair가 모두 admit된 뒤에만 단일 r4/table512 packed canary가 선택 가능하다. `NCP_HANDOFF_KO.md`의 분석 명령은 적분기를 호출하지 않는다.

실행 source는 Git의 고정 revision에서 가져오고 archive에서는 검증 DATA만 사용한다. 원래 baseline 인계의 두 overlay patch를 유지한다. 사용자에게 파일 다운로드·업로드·터미널 작업을 요구하지 않는다. 새 대화에서는 canonical `../NEW_CHAT_HANDOFF_KO.md`, 현재 `DELIVERY.json`, DAG 및 PR78의 실제 최신 상태를 먼저 읽는다.

연속 스펙트럼, 전역 gas-temperature 오차상한, 전체 EoR, upstream Grackle 전체 동등성, 관측 Bianchi/CMB는 해당 범위 검증 전까지 HOLD다.
