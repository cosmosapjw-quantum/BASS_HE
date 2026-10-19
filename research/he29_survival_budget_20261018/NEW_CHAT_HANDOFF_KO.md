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
