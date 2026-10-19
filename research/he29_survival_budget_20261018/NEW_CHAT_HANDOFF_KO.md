# HE29 현재 재개점: VigilODE 확장 게시, 네 기준해 대기

physmath-research-loop 1.3.0으로 이어간다. 먼저 현재 PR78와 관련 GitHub·백업의 새 반환부터 확인한다. 상위 README/DAG/Codex prompt와 `vigilode_20261019/{README_KO.md,DAG_STATUS.json,DELIVERY.json,NCP_HANDOFF_KO.md}`를 실제로 읽는다. 관련 intake·build·smoke·source addendum은 그 아래 evidence에 있다.

## 고정 정체성과 게시

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: research/he29-survival-budget-20261018
- 기존 과학 코드·테스트: 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
- 원본 Rust owner: rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474
- 새 VigilODE 연결 코드: 57642252991b5c453db66eb5a078e6a62cc6f4ea, 54/54 GitHub readback MATCH
- 재사용 VigilODE source: a21d573980f66fe02891bd216153443b5352f921
- 위 source commit 뒤의 closeout은 문서·DAG·백업 영수증이며 새로운 과학 실행 revision이 아니다.

## 이미 끝난 일과 이번 새 결과

HE28 pilot/6개 study, HE29 finite-donor 90사례/720구간과 50개 source-only tests는 반복하지 않았다. 새 Schur 대수는 Wolfram 잔차 8개가 0이며 23개 합성 선형계가 통과했다. 전용 Schur preconditioner를 production에 넣었다고 주장하지 않는다.

VigilODE a21d의 실제 RODAS5P/GMRES/faer를 연결했고, Rust 1.94.1 bridge compile과 작은 실제 FFI 3개, 새 Python 검사 96개가 통과했다. callback overflow와 build 전후 source identity 경계를 수정했다. 새 Rust library SHA256은 8d2f1271726781d2b000f0cd5eaadb0adac8029eb9357f786bfd647cea390460이다. NCP 재빌드의 binary bytes가 같다고 가정하지 않는다.

GitHub와 백업의 관측된 새 HE29 native 기준해는 **0/4**다. 추가로 백업 하위 폴더 40개/직접 항목 881개와 shared scratch 파일명 검색을 끝냈다. 상세 조회 범위·더 깊은 미관측 하위 경로는 두 census에 명시했다. NCP 내부 미게시 실행은 관측하지 못했다.

VigilODE PR71 run39255702592는 별도 source bab3902에서 build/small native 확인 후 JSON int32 직렬화 때문에 accuracy/timing BLOCKED다. 실제 읽은 VODE/Diffsol 비교 ZIP은 11개 member, manifest 10/10 MATCH다. 그 안의 저장 VODE 관측과 과거 Rust 수치는 HE29 source/owner/table identity가 없어 새 HE29 결과로 사용하지 않는다.

## 다음 실행

먼저 네 원래 기준해 (r2,512),(r4,512),(r8,512),(r4,1024), 각 Radau+DOP853을 완료·분석한다. m8/GL4/q0, 물리식·반응률·허용치와 absolute fraction 1e-11 gate를 유지한다. 4/4 identity·admission 통과 후에만 같은 r4/table512의 선택적 VigilODE 한 건이 가능하다. 이 canary로 기준해 완료 수를 늘리지 않는다.

NCP는 이 대화에서 원격 도구의 월간 quota로 미제출·미시작이며 내부 workspace는 미관측이다. 해당 응답의 재시도·재연결 금지를 유지한다. 접근 가능한 실행자는 현재 프로세스와 저장 결과를 먼저 확인한다. Git의 고정 source와 원래 자동 입력복원기로 22개 DATA만 확보한다. 사용자에게 수동 파일 전달을 요구하지 않는다. 옛 PUBLISH.sh를 실행하지 않는다.

## 백업

- 전체 새 보존 묶음: BASS_HE_HE29_VIGILODE_COMPLETE_20261019_7bf7398b.tar.gz
- 2,958,755 bytes; SHA256 7bf7398b77b2bf04a6917bef4241fc216764c7658ebf25c85e5df7377fb6147a
- Drive: 1RypR402ikbM_nF42R6NUzExWQfa0Xp6G
- Dropbox: id:BSpOijBcT10AAAAAAD_Q4A
- 양쪽 실제 raw bytes와 229개 payload 해시 MATCH. R2 archive78356130도 양쪽 raw SHA MATCH.
- 기존 c47c5efc/a70d320c 원본 archive를 그대로 함께 보존했고, 798afac1과 이전 242201a1도 불변이다. 외부 Rust toolchain/vendor 전체를 새 archive에 넣었다고 주장하지 않는다.

후속 handoff/closeout 문서는 위 불변 코드 archive와 분리된다. 실제 DAG·게시·백업 receipt를 읽고 재사용 자료와 새 실행을 구분한다. 연속 스펙트럼·전체 EoR·전역 gasT bound·upstream Grackle 전체 동등성·관측 Bianchi/CMB는 HOLD다. 아래는 이전 관측 시점의 보존 기록이다.

---

# 새 대화 인계: BASS_HE HE29 네 기준해 대기

$physmath-research-loop로 HE29를 이어간다. 현재 게시된 README_KO.md, DAG_STATUS.json, CODEX_HANDOFF_PROMPT_KO.md 및 results/continuation_20261019/의 INTAKE_AND_DISPATCH.json, BACKUP_CENSUS_SUMMARY.json, OVERLAY_CHECKS.json, DELIVERY.json을 읽는다. publication_retry/의 기존 두 receipt는 보존·재사용한다.

Repository https://github.com/cosmosapjw-quantum/BASS_HE
Draft PR78 https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
Branch research/he29-survival-budget-20261018
intake HEAD 3f16fe525d726aaebbe9262e0e869540321209eb
과학·테스트 revision 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
Parent HE28 a41dd37124e34cb22bb9782aaf687a0da91640b7
원본 Rust owner rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474

2026-10-19 실제 조회: PR78 HEAD 동일,83개 branch 이름/최신20개 PR/6897개 비절단 tree, Drive 최신1000개(게시 이후 구간 포함), Dropbox 원본 폴더3237개(6페이지 완료). 새 기준해 반환은0/4 관측이다. 미게시 NCP 작업은 원격 도구의 월간 사용량 한도로 확인하지 못했다. 실제 제출·시작은 하지 않았다. quota 응답이 재시도/재연결을 금지하므로 동일 원격 도구를 재시도하지 않는다. 접근 가능한 실행자가 있으면 프로세스/결과부터 확인하고 중복 없이 이어간다.

S2 게시 복구는 완료돼 있다. 387976f로 돌아가거나 PUBLISH.sh를 재실행하지 않는다. HE28 pilot/6case, HE29 finite-donor90case/720bounds,50개 source-only tests를 반복하지 않는다. source와 test revision은 그대로다.

원본 bootstrap의 pytest 전체 실행 한 줄만 대체하는 ncp/REUSE_SOURCE_VALIDATION_20261019.patch를 새로 준비했다. SHA256 cd0b7ab40688b3c60ab689876690b2edd71aea5268b4e7ff285a637ca094a33e. 원본 bootstrap Git blob ed227e2937f554bd5ecda4bf24dd5597b73a77a4. 갱신된 Codex handoff의 명령으로 원본1569를 clean checkout한 뒤 patch를 적용한다. source-only 근거 REUSED/새 tests0과 실제 adapter SHA·diff·HEAD를 기록하며 compiler/native점 qualification/4case/실패보존은 유지한다. 이 패치에 대한 적용·중복·target변경 거절과 Bash 구문만 새로 확인했다.

새 반환이 있으면 source/binary/table identity 및 완료된 쌍부터 분석한다. 없으면 NCP에는 m8/GL4/q0의 (r2,512),(r4,512),(r8,512),(r4,1024),각 Radau+DOP853 네 쌍만 전달한다. 첫 실패 STOP,case3600s,table600s/예상2GiB,단일 수치thread 및 기존 물리·반응률·허용치를 유지한다. 절대 fraction gate1e-11과 기존 pilot3.951006358291365e-14의 절대차 의미도 유지한다. bootstrap 실패 후 저장된 partial 분석을 생략하지 않는다.

입력22개는 START_REFERENCES.sh가 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205 archive에서 DATA만 자동 복원한다. Drive1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi; Dropbox /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz. 사용자에게 수동 파일 전달을 요구하지 않는다.

기존 완전 코드·입력 package: c47c5efcfcd668203cbd6082d25e128c7ea8a08291f3a039a4a52674f0530a28,132445bytes,Drive16z5ApkTBP30elscQJy_LYLdRLIYnS8Le,Dropbox id:BSpOijBcT10AAAAAAD_Ntw. 기존 handoff overlay:798afac15d04bf53f5a95ecb3a41782973ff023dce2ca5d371a501ff57fcfa38,4929bytes,Drive1_dqACrV1XnvGGRUmCOhe0b2IrKXUY4mH,Dropbox id:BSpOijBcT10AAAAAAD_N6Q. Drive 원시 readback·manifest 검증과 Dropbox upload/provider hash 근거를 재사용했다. 기존 Dropbox raw readback 상태는 미검증 그대로다. 이번 후속 묶음의 실제 게시·보존은 continuation_20261019/DELIVERY.json에 별도로 기록한다.

유한 donor survival 결과의 범위를 유지한다. n32에서 r2→4 +2.5017143912009487e-10K,n64에서 -6.697344900885582e-10K이므로 같은 model/table 기준해로 시간오차를 분리한다. 연속 스펙트럼·전체 EoR·nonlinear gas-temperature 상한·upstream Grackle 전체 동등성·관측 Bianchi/CMB는 해당 검증 전 HOLD다. 단계별 실제 DAG/게시/백업과 재사용/새 결과를 구별한다.
