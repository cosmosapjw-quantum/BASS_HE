# HE29 현재 Codex / NCP 인계 — 기준해 4/4 이후의 단일 packed canary

## 현재 결론

2026-10-20의 새 PR80 native 반환을 실제 raw archive와 binary, method/RESULT, source/input/parent/table/cohort identity로 읽었다. m8/GL4/q0의 `(r2,512), (r4,512), (r8,512), (r4,1024)` Radau+DOP853 pair는 **4/4 admitted**다. 이 네 pair와 기존 transport를 다시 실행하지 않는다. 저장된 `09929` 분석도 이미 exit0로 완료돼 다시 실행하지 않는다.

현재 authoritative lane은 `native_intake_20261020T1315Z/`다. 먼저 그 `README_KO.md`, `RESEARCH_KO.md`, `DAG_STATUS.json`, `DELIVERY.json`, `NCP_HANDOFF_KO.md`, `LOOP_STATUS.json`과 `evidence` 영수증을 읽는다. 원래 기준해 실행용 이전 프롬프트는 Git `d63135807c80dc2ada7f85214b5087b9e3dff375`에서 보존된다. 그 당시 0/4·실행 명령을 현재 작업으로 재사용하지 않는다.

## 실행 source와 publication을 구분

| 역할 | 고정 Git identity |
|---|---|
| original science / tests | `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f` |
| owner | `f7830e2f55e7a1938bc3c98f61b60651f8dae474` |
| 저장된 budget 분석 | `09929b0a06a833f0c2497e72f074ec8694a264df` |
| packed science / bridge / runner | `a5d4711460c09b310b78c9692aa62534b7a843d3` |
| 재사용 watchdog | `ed5adca43f474553a9bce7f5de45d464be5905cb` |
| VigilODE | `a21d573980f66fe02891bd216153443b5352f921` |

새 외부 wrapper의 실행 commit은 현재 lane `DELIVERY.json`의 `implementation_publication.code_commit`이다. `status=PUBLISHED_EXACT_READBACK_PASS`일 때만 그 pin을 사용한다. 이후의 문서/영수증 HEAD를 a5·ed5 또는 wrapper code pin 대신 사용하지 않는다. wrapper는 원래 target의 `run_process` alias만 PR79의 검증된 process-group helper로 연결한다.

## 다음 실제 작업

접근 가능한 NCP 실행자가 현재 프로세스와 저장된 canary/build 결과를 먼저 확인한다. 현재 이 대화는 원격 프로세스를 관측하지 못했고, 제출·시작·native 실행은 0이다. Remote Desktop Commander의 기존 월간 quota에 따른 호출·재시도·재연결 금지는 유지한다. 사용자에게 파일 이동이나 터미널 작업을 요구하지 않는다.

새 lane의 `NCP_HANDOFF_KO.md`에 실행 가능한 source 확보·artifact reuse·preflight·단일 canary 명령이 있다. 확인된 기존 실행 root는 `/root/HE29_REFERENCE_20261020T120000Z`, references는 그 아래 `references/`, Python은 `venv/bin/python`, binary는 `build/he29_owner_server`다. 저장된 이 경로가 현재에도 존재한다고 추정하지 말고 실행자가 실제 관측한다.

필수 runtime은 Python `3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]`, NumPy2.3.5, SciPy1.17.0, thread1이다. 실제 baseline binary SHA256은 `a82e540797322027deaab6e6bcb2bde746de737adeedbf144313598c65f5b7e9`이다. r4/table512의 재생성 source-table hash는 `919ca6f42028bffc37cb208916ee5a9927356eb99344fe467f9b98e30e9fddcd`여야 한다. 기존 library/BUILD_IDENTITY가 계약에 맞으면 재사용하고, 필요한 경우에만 깨끗한 Git a5 checkout에서 빌드한다. Source validation용 old tests/benchmark를 다시 실행하지 않는다.

허용 실행은 **단일 r4/table512 packed canary, 기본 wall900초, thread1**다. 원래 full state의 gas4/photonK/**ledger19 전체 norm**과 원래 solver/반응률/적분 tolerance/gate를 유지한다. 새 solver 개발·transport 재실행·자동 grid 확대는 없다. 기존 결과/partial/failure 디렉터리를 덮어쓰거나 자동 재시도하지 않는다.

## DATA 복원 경계

실행 source는 Git이다. Archive는 SHA 확인한 DATA와 provenance만 공급한다. 기존 baseline DATA가 있으면 그대로 재사용한다. 없을 때만 준비된 복원기로 원본22개 DATA를 복원하고, 입력 복원만을 위해 `START_REFERENCES.sh`를 호출하지 않는다. `ncp/PUBLISH.sh` 및 387976f 복귀도 하지 않는다.

원본 DATA archive: `BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz`, 129635 bytes, SHA256 `a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205`, Drive `1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi`, Dropbox `id:BSpOijBcT10AAAAAAD_Ncg`.

기존 baseline1569 실행 provenance에는 다음 두 patch가 모두 적용돼 있다. 이들은 현재 baseline 재실행 지시가 아니다.

- `REUSE_SOURCE_VALIDATION_20261019.patch`: `cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e`
- `REPAIR_INPUT_MANIFEST_20261020.patch`: `71f16bc8bc946bdd9107c476662fb83b9812cb4078045b933066fca300eb1e85`

## 반환과 과학 범위

원래 gate: abs fraction1e-11, method ΔT1e-9K, number3e-15/H, energy3e-12eV/H, species3e-12, 원래 양성성. 적분 rtol1e-10, scaled atol1e-12를 유지한다. 두 solver의 일치와 finite-candidate hull을 참 ODE 해의 오차반경으로 해석하지 않는다.

Native 원본 archive는 `BASS_HE_HE29_NATIVE_RETURN_20261020_c1c4c061.tar.gz`, 276206340 bytes, SHA256 `c1c4c06149bf9561141bc0f6b6f39c280bd554a5e1252ed0825f0e950f1c10c6`, Dropbox `id:BSpOijBcT10AAAAAAD_Z-w`, Drive parts folder `1pkohlay5eIfFJsBwPZ_yn2jIZONZjesI`다. 실제 Dropbox full bytes와292 payload·293 regular member를 확인했다. Drive는 producer dual-raw 영수증을 재사용하며 이번 intake는 parts manifest raw와3part metadata만 새로 읽었다. 원본trace/binary 전체를 새 소규모 admission archive에 포함했다고 주장하지 않는다.

새 실행 결과가 생기면 성공·실패·timeout·partial을 모두 보존하고 source/owner binary/bridge library/table/input/parent/runtime/thread/wall/trace identity를 포함해 Git 결과 요약과 immutable backups로 반환한다. 원래 분석 출력의 상태와 새 canary admission을 별도로 기록한다. 전체 EoR·연속 스펙트럼·전역 gas-temperature 오차상한·whole Grackle 동등성·관측 Bianchi/CMB는 HOLD다. 실제 HE29 packed speedup은 아직 미측정이며 이전 조립/제조IVP 가속을 곱하지 않는다.

PR78은 branch `research/he29-survival-budget-20261018`에서 Draft/open/unmerged를 유지한다. PR79/80을 병합하지 않고 고정 source와 실제 evidence를 재사용한다. 모든 완료 연구·검증 재실행은 금지한다.
