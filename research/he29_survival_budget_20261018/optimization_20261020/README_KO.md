# HE29 최적화 루프 — 2026-10-20

현재 단계: **R1–R5 완료, C5–C8 구현·검증 중. 새 HE29 native 기준해0/4.**

standalone `physmath-research-loop` 1.0.0의 새 최적화 루프다. 2026-10-19의 1.3 연구·코드와 HE28/HE29 완료 근거는 재사용하며, 같은 연구와 source-only suite를 반복하지 않는다.

## 실제 완료한 일

- 최신 BASS_HE PR78 HEAD329f, 원본 rei_bianchi 및 관련 BASS/bass_cr/WU/rec 백업과 VigilODE의 새 실행·source identity를 읽었다. 새 VigilODE/REI 결과는 다른 모델의 결과이고 HE29의 네 기준해를 대체하지 않는다. 백업 관측 범위·실제 raw read·한계는 evidence/BACKUP_INTAKE.json에 있다.
- Git1569 입력 manifest의62자리 SHA 한 항목을 원본 archive SHA와 내부 manifest로 보정했다.22개 DATA 복원/preflight/독립 검토가 PASS다. Archive는 DATA 공급원이며 실행 소스는 Git이다.
- 원래 Jacobian은 gas 유한차분4열과 photon12개 구조 행으로 저장할 수 있다. gas4 + photon K + passive ledger19를 모두 유지한다. 계수는 `16K+92`개, storage는 `8(16K+92)` bytes다. gas 열 뒤 photon 열의 원래 누적 순서를 지킨다.
- 원래 `Model.jac`의 LIL 대입을 canonical CSR 배열 조립으로 바꿨다. explicit zero 제거와 정렬을 유지했고 K512/640/896의 indices/indptr/data가 정확히 같다.
- 조립의 최초 paired 측정(9회, 회당3호출) median ratio는8.3455/8.7024/8.7804다. 이는 원래 photon geometry와 제조된 affine gas RHS로 조립 비용을 분리한 실험이다. HE29 native chemistry·전체 solver 가속률을 뜻하지 않는다.
- exact-time geometry/sigma 캐시는 interval 변경 전후 무효화한다. 기존 HE27 source 캐시는 그대로 재사용하며 새 성과로 세지 않는다.
- 새 모델 검증8개 최초 PASS, trial domain 보정 뒤 관련2개 PASS(현재9개 고유 test methods). 원래 물리/native owner와 허용치, 전체19 ledger error norm은 그대로다.

## 진행 중

`a21d573980f66fe02891bd216153443b5352f921` VigilODE solver를 재사용하는 ABI2 packed JVP와 선택적1/2/4 row workers를 검증 중이다. 최신 upstream의 autonomous identity-mass 단일-step 가속은 이 비자율 adaptive 경로와 직접 같은 계약이 아니므로 native 검증 없이 바꾸지 않는다. Schur/4×4 faer 경로는 분석 대상으로 유지하며 현재 driver의 외부 preconditioner hook이 없어 새 solver를 개발하지 않는다.

## 게시·백업·DAG

이 문서는 R1–R5/C5 체크포인트다. 게시 commit과 새 이중 백업 영수증은 이후 DELIVERY.json에서 기록한다. 현재 패키지/byte readback을 과거 백업 영수증으로 대신 주장하지 않는다. 기존7bf7398b/88285fa4 묶음은 보존한다.

Native 우선순위는 m8/GL4/q0의 `(r2,512),(r4,512),(r8,512),(r4,1024)`, 각 Radau+DOP853뿐이다. 네 쌍이 모두 admit된 뒤 optional r4/table512 VigilODE canary 한 개에 새 kernel을 사용할 수 있다. continuous spectrum/full EoR/global gas-temperature error/upstream Grackle whole runtime/Bianchi/CMB 관측은 HOLD다.
