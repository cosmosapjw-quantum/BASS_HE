# BASS_HE: 최신 반환 통합과 시작되지 않은 HE29 기준해의 안전한 연결

2026-10-20 intake 기준. 최근 구간은 2026-10-17T09:55:50Z 이후이며 GitHub의 83개 branch, 82개 고유 tip의 commit metadata를 읽었다. 이 범위에 속한 tip은 네 개였다. 현재 PR78의 head는 `d63135807c80dc2ada7f85214b5087b9e3dff375`, branch는 `research/he29-survival-budget-20261018`이며 Draft/open/unmerged다. 아래 완료 상태는 읽은 실제 반환과 영수증의 범위다. 이번 작업에서 NCP에 제출하거나 원격 프로세스에 연결하지 않았다.

## 새 근거와 재사용한 완료 결과

| 항목 | 확인한 근거 | 현재 과학적 의미 |
|---|---|---|
| HE27 native A/B | 최근 문서 tip `2a9e27ade27fb2762bc955882799b736970bb786` | 저장 ΔT=+9.426948111e-9 K, 같은 table Radau–DOP853 차이 7.1054e-14 K. 기존 실행 재사용 |
| HE28 source | `d496e0e8b7c9d5a708bf07c4c6eaa4900c6d489c` | strip refinement 실행 계약 |
| HE28 실제 NCP 반환 | `a41dd37124e34cb22bb9782aaf687a0da91640b7`; 실행 source `bcd3ac4c58760bcfb1f03ee30bd82fd3d77ff7a4` | m8/r2,4,8/n32,64의 transport 6/6 완료. 약 475초, native call 7,178. 독립 adaptive reference 6개를 뜻하지 않음 |
| HE29 exact budget / partial classifier | 실행 code `09929b0a06a833f0c2497e72f074ec8694a264df` | 공유 reference 변수를 보존하는 정확 선형 후처리와 부분 반환 분류 완료 |
| ABI2 packed JVP | `a5d4711460c09b310b78c9692aa62534b7a843d3`; VigilODE `a21d573980f66fe02891bd216153443b5352f921` | 제조계 측정과 구현은 완료. HE29 native speedup은 미측정 |
| HE29 필요한 네 pair | 최신 공개 반환에서 채택 0/4 | 실제 NCP 현지 상태는 현지 실행자가 먼저 확인. 공개 기록 부재를 프로세스 부재로 해석하지 않음 |

HE28 pilot은 transport 8.239220060821102 K, Radau 8.239220062970691 K, DOP853 8.239220062970656 K다. transport–Radau 절대 차이는 2.1495889512834765e-9 K, Radau–DOP853은 3.552713678800501e-14 K다. 기존 3.951006358291365e-14는 **절대 fraction 차이**이며 상대 오차가 아니다. 최대 상대 차이는 4.198589860958344e-5다. 허용치 자체는 수정하지 않는다.

HE28 여섯 반환에서 최대 number defect는 2.964615315390051e-21/H, energy defect는 1.9147010366094008e-16 eV/H다. n64−n32 온도 차이는 r2/4/8 각각 1.1746656980449188e-9, 2.547597688362657e-10, 2.92054380679474e-10 K다. r2→4 contrast는 n32에서 +2.5017143912009487e-10 K, n64에서 −6.697344900885582e-10 K이며 mixed difference는 −9.199059292086531e-10 K다. 따라서 현재 자료만으로 strip 효과와 시간 이산화 효과를 분리하지 않는다. PR77의 이전 '실행 중' 본문보다 후속 실제 6/6 반환이 최신 근거다.

## 이론적으로 필요한 다음 값

고정 finite model/table key를 i=(r,N), 저장 transport를 T(i,n), 같은 key의 수치 기준 후보를 θ(i,m)으로 둔다. m은 Radau 또는 DOP853이다. 기존 정확 budget이 사용하는 항등식은

\[
T(b,n)-T(a,n)=[\theta(b,m)-\theta(a,m)]+[T(b,n)-\theta(b,m)]-[T(a,n)-\theta(a,m)].
\]

공유 θ의 계수는 전개하면 정확히 소거된다. 따라서 추가 계산은 저장 transport의 재실행이 아니라 `(r,N)=(2,512),(4,512),(8,512),(4,1024)`의 네 pair다. 같은 i의 n32/n64 차이를 이 식에 넣으면 기준 후보가 상쇄된다. 이 계산 경로는 기존 `continuation_20261020T0557Z/src/analyze_budget.py`가 구현했으므로 재구현하지 않는다.

두 방법의 일치는 두 수치 오차의 차이를 제한한다. 공통 오차 성분 또는 참 finite ODE 해를 둘러싸는 구간을 보증하지 않는다. `product_hull`과 `coherent_hull`은 저장된 유한 후보 집합의 범위다. table512→1024는 r4에서 별도의 민감도이며, 없는 table1024 transport를 만들어 넣지 않는다. 연속 스펙트럼·전역 온도 오차상한·전체 EoR·upstream Grackle 전체 동등성은 계속 HOLD다.

## 새로 메운 실행 공백

기존 `START_REFERENCES.sh`는 입력 복원 뒤 `BOOTSTRAP_REFERENCES.sh`를 호출하고, bootstrap은 새 WORK에서 네 case를 모두 실행한다. 반면 최신 인계는 '반환된 case를 재사용하고 누락 case만 실행'하도록 요구했다. 부분 반환 뒤 START를 다시 호출하면 소비한 case 예산을 새 이름으로 다시 배정할 수 있다. 개별 `reference_runner.py case`는 자체 watchdog을 제공하지 않으므로 단순 shell loop로 대신할 수도 없다.

새 `src/continue_missing_references.py`는 다음 집합만 실행한다. Fresh START도 발견된 watchdog 결함을 재사용하지 않도록 별도 세 번째 bootstrap overlay와 `launch_fresh_references.py`를 제공한다. 이 경로는 원래 DESIGN을 absent root에만 생성하고 같은 controller를 호출한다.

\[
J_{new}=\{j\in J:\;\text{case path와 process path가 모두 부재하고 원래 classifier가 ABSENT로 판정}\}.
\]

정상 완료, 한 method만 완료, 실패, malformed 파일, 깨진 symlink를 포함해 하나라도 점유된 path는 보존한다. 기존 case를 재시작하지 않으므로 그 case의 소비 예산도 초기화하지 않는다. 원래 DESIGN의 per-case 예산을 그대로 읽고 새 옵션은 이를 낮출 수만 있다. 원래 계약에 없는 aggregate deadline을 새로 만들거나 갱신하지 않는다. 별도의 상위 실행 예산이 실제 현지에 존재한다면 그 원래 deadline도 유지해야 한다.

실행은 같은 process-group 계약의 수정 wrapper에 unchanged `reference_runner.py case`를 전달한다. 독립 검토가 원래 watchdog에서 leader가 SIGTERM으로 먼저 종료하면 TERM-resistant descendant가 남는 결함을 제조 child로 재현했다. 새 wrapper는 timeout 뒤 leader 종료 여부와 무관하게 잔여 group에 SIGKILL을 보내고 이 신호 여부를 영수증에 기록한다. 원래 execution.py와 science source는 수정하지 않는다. 순차 실행과 새 실패 시 중단을 유지한다. 새 wrapper는 timeout 이후 leader의 SIGTERM 반응을 최대 3초 기다린 뒤 잔여 group에 SIGKILL하므로 per-case 값은 wait budget이며 엄격한 전체 wall-time 인증값이 아니다. 모든 기존 source/input/binary/table 및 physical admission은 원래 구현을 사용한다. 다른 source/binary/runtime cohort와 새 결과를 혼합하지 않는다.

controller는 기본적으로 plan만 만든다. Linux `/proc`에서 같은 references 아래의 원래 runner 실행을 확인하고, 새 controller끼리의 경합은 advisory lock과 create-only process directory로 막는다. 원래 legacy runner가 이 lock을 사용하지 않는다는 한계가 있으므로 현지 intake에서 진행 중 작업을 먼저 확인해야 한다. 새 controller는 기존 프로세스에 신호를 보내지 않는다.

## 실제 경량 검증과 재사용 경계

최초 11개 focused test method가 PASS했고, 독립 검토의 실제 watchdog 결함 교정 후 영향받은 wrapper와 기존 controller 연결을 포함한 12개 focused test method가 0.370초에 PASS했다. 점유 path 보존, cohort 불일치, 예산 증가 거절, 완료·partial skip, fake child 실패, 원래 watchdog timeout, 계획 이후 path 점유, controller lock, 관측 가능한 기존 runner 감지, source drift 거절을 검증했다. 추가 검사는 leader가 종료된 뒤에도 SIGTERM을 무시하는 descendant의 종료를 확인했다. Fresh launcher의 원래 DESIGN/기존 root 보존 및 예산 도메인 검사 2개도 별도로 PASS했다. 이번 고유 test method는 총 14개다. 세 번째 bootstrap overlay는 정확한 원본 hash에서 zero-fuzz 적용과 bash -n을 통과했다. fake child만 실행했으며 native RHS 또는 reference 적분은 호출하지 않았다.

추가 production import/plan 검증은 고정 source closure와 원본 a70 archive를 사용했다. archive 129,635 bytes 및 전체 SHA를 실제 확인하고, 22개 DATA와 20개 parent source hash를 검사했다. 실제 생산 모듈을 import하고 네 부재 case의 계획을 만드는 CLI가 1.024802초에 exit 0이었다. binary는 실행 권한이 없는 명시적 제조 fixture였으며 실행되지 않았다. 이것은 CLI/import/provenance 연결 검증이고 native qualification이나 물리 계산이 아니다. 상세 근거는 `evidence/PRODUCTION_PLAN_TEST.json` 및 test stderr다.

기존 owner가 보고한 HE29 90개 finite-donor 사례/720개 bound, 기존 50개 검사, exact budget의 28개 새 test method와 20개 제조계, Wolfram closure 0, ABI2/VigilODE 측정은 원래 evidence를 재사용한다. 이번 실행 횟수에 합산하지 않는다. 새로운 tensor geometry가 없으므로 xAct 계산을 별도로 수행하지 않았다. 이번 lane은 기존 물리 유도·CAS를 재사용하고 실행 공백과 실제 확인된 watchdog 결함에 새 구현을 집중했다.

## Backup intake와 접근 범위

| artifact | 실제 이번 확인 | 원래 receipt의 검증 |
|---|---|---|
| `BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz` | Drive/Dropbox metadata, Drive 실제 bytes SHA 및 22 input hashes | 원래 보존 자료 |
| `BASS_HE_HE29_REFERENCE_BUDGET_COMPLETE_20261020_7a86d5bb.tar.gz` | Dropbox ID·size·mtime metadata | 기존 raw/payload PASS 재사용; Drive 업로드 UNKNOWN 유지 |
| `HE29_REFERENCE_BUDGET_HANDOFF_CLOSEOUT_20261020_d0a76860.tar.gz` | Dropbox ID·size·mtime metadata | 기존 raw/payload PASS 재사용 |
| `BASS_HE_HE29_OPTIMIZATION_COMPLETE_20261020_77f1c73e.tar.gz` | Drive metadata | 기존 양 provider raw/91 payload PASS 재사용 |

Dropbox HE29 exact-title 검색은 12개이며 has_more=false였다. 날짜 filter를 넣은 넓은 검색은 오래된 결과도 반환하여 날짜 completeness 근거로 쓰지 않는다. Drive title 검색은 알려진 ID의 직접 metadata 조회와 달리 빈 결과를 돌려주었다. 따라서 검색 index의 누락을 파일 부재로 해석하지 않는다. 현재 대화의 인용문과 접근 가능한 저장 자료를 연결했으며 모든 비공개 대화가 열람되었다고 주장하지 않는다.

현재 AGENTS에는 모델별 routing 강제 규칙이 없다. 정확한 Fortran/OpenMP/SIMD/MPI, 실측 비용, 완료 계산 재사용, 과학적 claim 범위 분리를 유지한다. 이번 구현은 orchestration과 증거 보존만 바꾸며 과학 runner와 물리 허용치는 그대로다.

## DAG

`최신 intake → HE28 실제 반환 재사용 → HE29 exact reducer 재사용 → absent-only controller/경량 검증 → 독립 검토 → Git 게시·백업 → 현지 새 반환 intake → 필요한 네 pair → exact budget → optional ABI2 canary`

독립 검토는 `REVIEW_HE_CONTROLLER.json`의 PASS_SCOPED이며 실제 watchdog 지적은 교정 및 focused 검증으로 닫혔다. 이번 Git/backup 완료 여부는 이후 실제 delivery receipt에 기록한다. 네 기준해와 canary의 완료 상태를 문서 준비나 controller test PASS로 승격하지 않는다.
