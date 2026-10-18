# 새 대화 인계: BASS_HE HE29 게시 완료 상태에서 재개

$physmath-research-loop를 사용하되 먼저 최신 GitHub와 백업에서 새 native 결과를 확인하고 완료된 HE28 연구를 반복하지 마.

Repository: https://github.com/cosmosapjw-quantum/BASS_HE
Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
Branch: research/he29-survival-budget-20261018
고정 실행 revision: 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
이번 closeout 시작 때 확인한 publication HEAD: 068bdccc6f991a046300cc0634c9092d72e953d3
Parent HE28 PR77: a41dd37124e34cb22bb9782aaf687a0da91640b7
원본 owner: rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474

이전 'S2 미게시' 상태는 해소됐다. src와 native bootstrap, 자동 입력 복원기, 테스트가 실제 게시돼 있다. 최신 README_KO.md, DAG_STATUS.json, 두 handoff와 results/publication_retry/DELIVERY.json 및 후속 CLOSEOUT_RECEIPT.json을 읽는다. 오래된 387976f branch 상태로 되돌리거나 ncp/PUBLISH.sh를 재실행하지 않는다. 이후 작성된 문서 commit과 실행 코드 revision을 구별한다.

전체 공개 코드+원본 데이터 보존 패키지:
BASS_HE_HE29_PUBLISHED_20261018_v2_c47c5efc.tar.gz
132445bytes; SHA256 c47c5efcfcd668203cbd6082d25e128c7ea8a08291f3a039a4a52674f0530a28
Drive id16z5ApkTBP30elscQJy_LYLdRLIYnS8Le
Dropbox id:BSpOijBcT10AAAAAAD_Ntw
Drive에서 다시 받아94개 내부 hash와50테스트를 확인했다. Dropbox 업로드와 provider hash는 확인됐지만 raw-byte readback은 URL 처리 제한으로 미검증이다. 새 프롬프트·closeout 영수증은 이 불변 패키지와 분리된 후속 문서다.

원본 실행 입력22개는 아래 별도 불변 archive에서 ncp/START_REFERENCES.sh가 자동 복원한다.
SHA256 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205
Drive id1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi
Dropbox /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz
사용자에게 수동 파일 전달을 요구하지 않는다. source는 Git의 고정 revision, archive에서는 DATA만 가져온다.

HE28은 native pilot+6/6 study 완료. HE29는 양의 유한 donor의 Jensen/chord survival bounds를 구현했고90사례/720중첩 구간이 donor survival을 포함했다. 최대 최종 폭2.2487671447191104e-12는 finite-donor 조건부 결과다. GL256/512 차이2.7755575615628914e-16은 엄밀한 연속적분 오차가 아니다. r8→16 오차가 증가해 연속 스펙트럼 수렴은 HOLD.

HE28 r2→4 온도차는 n32에서+2.5017143912009487e-10K, n64에서-6.697344900885582e-10K. 다음에는 같은 model/table 기준해로 시간오차와 strip/table 차이를 분리한다. 기존 pilot3.951006358291365e-14는 절대 fraction 차이이며 절대1e-11 gate는 유지한다.

새 native 결과가 없다면 NCP에는 완성된 코드의 컴파일/작은 환경 수정/실행만 맡긴다. m8/GL4/q0의 (r2,512),(r4,512),(r8,512),(r4,1024), 각 Radau+DOP853 네 쌍이 대상이며 현재0/4 NOT_RUN이다. 기존 transport를 재실행하지 않는다. 50로컬tests는 기존47+입력복원3이며 native 검증이 아니다. 물리·반응률·허용치는 변경하지 않았다.

실제 결과가 있으면 source/binary/table identity부터 확인하고 분석한다. 각 단계 DAG·게시·백업 보증을 구분하고 새 결과와 재사용을 따로 기록한다. full EoR,upstream Grackle 전체 동등성,관측 Bianchi/CMB는 해당 범위의 검증 전 HOLD다. 이 스레드의 backup-closeout 자체는 새 과학실행을 허가하거나 수행한 기록이 아니다.
