# 새 대화 인계: BASS_HE HE29 게시 복구 이후

$physmath-research-loop를 사용해 다음의 실제 상태에서 이어서 작업해줘. 먼저 백업/GitHub에 새 HE29 native 실행 결과가 있는지 확인하고, 완료된 HE28 연구를 재실행하지 마.

## 출발점

Repository https://github.com/cosmosapjw-quantum/BASS_HE
Draft PR78 https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
Branch research/he29-survival-budget-20261018
실행 코드·테스트 revision 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
Parent HE28 PR77 a41dd37124e34cb22bb9782aaf687a0da91640b7
원본 Rust owner f7830e2f55e7a1938bc3c98f61b60651f8dae474

이전의 'S2 미게시' 상태는 해소됐다. 소스·테스트·native bootstrap·입력복원 helper가 실제 push됐다. README_KO.md, DAG_STATUS.json, CODEX_HANDOFF_PROMPT_KO.md와 results/publication_retry/DELIVERY.json을 최신 문서 commit에서 읽어. 실행 코드는 고정 revision과 비교한다. 이 대화의 샌드박스 파일만 존재한다고 가정하지 말고 Git을 주 진입점으로 사용해.

## 데이터 복원

원본 native 입력22개는 129635-byte archive에서 개별 SHA 검증 후 자동 복원한다. wrapper ncp/START_REFERENCES.sh는 인증된 dbx:/gdrv: rclone을 사용한다. 없으면 Codex/연결 도구가 직접 확보해야 하며 사용자 수동 다운로드를 요구하지 않는다.

원본 archive SHA256 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205
Drive id 1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi
Dropbox id id:BSpOijBcT10AAAAAAD_Ncg
경로 /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz
현재 코드를 오래된 archive 코드로 덮어쓰지 않는다. 실행 입력은 그 archive의 DATA만 사용한다. 새 최종 code+prompt archive의 ID/해시는 별도 DELIVERY.json에 기록되어 있다.

## 연구 상태

HE28은 native pilot과6/6 study 완료. HE29는 유한 양의 donor에 Jensen/chord survival bounds를 구현했고90사례/720중첩 구간이 직접 donor survival을 포함했다. 최종 최대폭2.2487671447191104e-12. GL256/512 차이2.7755575615628914e-16은 수치적 안정성이지 엄밀한 연속 적분 오차가 아니다. r8→16의 오차가 다시 커지므로 연속 스펙트럼 수렴 HOLD.

HE28 r2→4 온도차는 n32에서+2.5017143912009487e-10K, n64에서-6.697344900885582e-10K. 시간과 스펙트럼 차이를 분리하려면 같은 model/table의 독립 기준해가 필요하다. 기존 pilot3.951006358291365e-14는 절대 fraction 차이다. 상대차 최대4.198589860958344e-5는 극미량 HeIII가 지배하며 절대1e-11 기준은 변경하지 않았다.

로컬50/50 tests PASS: 기존47개+입력 archive 복원3개. 포장 fixture를 native 과학으로 세지 않는다. 이번 게시 복구의 신규 native 호출0, 새 기준해0/4. 원본 물리·반응률·허용치 불변.

## 다음 선택

새 결과가 있으면 입력·table/source/binary identity를 읽고 분석부터 수행한다. 없다면 준비된 네 기준해만 NCP에 전달한다: m8/GL4/q0, (r2,512),(r4,512),(r8,512),(r4,1024), 각각 Radau+DOP853. 기존 transport6개는 재실행하지 않는다. 큰 구현은 이미 작성됐고 NCP에는 컴파일/작은 환경 수정/실제 실행만 맡긴다.

진행마다 실제 DAG·게시·백업 상태를 기록하고 새 결과와 재사용 결과를 구분한다. backup의 upload/content_hash/full-byte readback 보증을 섞지 않는다. 전체 EoR, upstream Grackle 직접 동등성, 관측 Bianchi/CMB는 계속 HOLD다. 사용자가 단계 범위를 고정하면 그 범위를 넘겨 새 루프를 시작하지 않는다.
