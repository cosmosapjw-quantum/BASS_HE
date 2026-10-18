# HE28 NCP 실행 인계

사용자에게 추가 다운로드나 명령 입력을 요청하지 말고 GitHub에서 직접 코드를 가져와 실행하라. BASS_HE branch `research/he28-strip-refinement-20261018`, science commit `62acea9141324ef176110314226cb5c40a05bf82`가 기준이다. 이후 delivery-only commit은 허용하되 scientific source diff가 있으면 먼저 확인한다. 본 단계의 새 RefinedSourceModel/native runner는 이미 작성되어 있으므로 재설계하지 말고 컴파일, 작은 환경 수정, 실제 검증에 집중한다.

먼저 HE27 PR75와 HE28 README/DAG를 읽어라. HE27 native A/B가 이미 끝났으므로 반복하지 않는다. 원본 owner는 `cosmosapjw-quantum/rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474`. 새 runtime과 raw results는 새 브랜치/새 work directory에만 저장하고 원래 dirty checkout/production/PR73-75를 수정하지 않는다.

승인된 Ubuntu/NCP 연결을 사용하라. NCP 내부이면 바로 작업하고 Ubuntu이면 기존 승인된 SSH key/config를 이용한다. 인증자료를 공개 로그에 쓰지 않는다. NCP 접근이 막히면 실제 가능한 작업과 미수행을 분리하고 접속을 우회하지 않는다.

D=research/he28_strip_refinement_20261018
새 고유 HE28_WORK_ROOT를 정하고 다음을 직접 실행한다:
`HE28_WORK_ROOT="$WORK" bash "$D/ncp/BOOTSTRAP.sh"`
필요하면 실제 존재/검증한 HE28_OWNER_REPO와 HE28_PYTHON을 제공한다. 기본 스크립트는 original Rust clone 및 unchanged HE25 owner_server.rs를 컴파일하고17개 parent SHA,27개 tests,preflight,native pilot을 실행한다. Python dependencies는 requirements.txt로 고정되어 있다. first failure와 모든 stdout/stderr는 보존한다.

pilot은 q0,m4,r2,n16,GL4,table512에서 transport와 동일 table/RHS의 Radau 및 DOP853를 비교한다. process exit와 `pilot/SUMMARY.json`의 `all_processes_pass`, `pilot_accuracy_pass`를 모두 확인한다. 기존 source3e-13, photon3e-15/H, energy3e-12eV/H, density1e-9 등 불변. pilot T1e-8K,gas fraction1e-11,reference stability1e-9K. 불충족 시 허용치 변경 없이 HOLD.

통과 시 동일 Python으로:
`"$WORK/venv/bin/python" "$D/src/he28_run.py" campaign --stage study --binary "$WORK/build/he28_owner_server" --build-receipt "$WORK/build/RECEIPT.json" --pilot-result "$WORK/pilot/m4_r2_n16/RESULT.json" --out "$WORK/study"`
외부 HE28_PYTHON을 썼다면 위 실행파일만 같은 환경의 실제 Python으로 바꾼다. study는 q0,m8,r2/4/8,n32/64의6개이며 자동 전체 Cartesian sweep은 하지 않는다. Table2GiB/wall600s,case3600s가 기본이다. cap 실패는 먼저 실제 자원/원인을 기록한다. 임의 해상도 축소나 scientific gate 완화는 금지한다.

270개 source-only 결과에서 r8 오차는 r1보다 약26배 작았지만 r16은 비단조적이다. 이는 고정 기체에서 exp(-tau(E))의 미래 kernel 진단이지 coupled temperature/EoR 오차가 아니다. 8개 순간 모멘트 일치와 연속 스펙트럼 수렴을 혼동하지 않는다. 실제 새 native 실행은 현재0회다.

각 완료 단계마다 새 raw/source/table/binary SHA 및 DAG를 기록하고 Draft PR로 게시한다. Code/source/model/table가 변한 뒤 과거 pilot을 재사용하지 않는다. 모든 단계와 실패를 복원 아카이브/Git bundle로 묶어 Drive/Dropbox create-only 업로드하고 각각 실제 다운로드 SHA를 검증한다. HE28 source package Drive id `1GWJUJuBO0N0Sq8d6FGzdrsJgJQdUfO6A`,SHA256 `b50eced554dcdd7a210ef5ec0346e2b5cf9be5c1b8cdb018e200a5e718f527b1`; Dropbox id `id:BSpOijBcT10AAAAAAD-8Tw`는 upload/content-hash까지 검증됐으나 raw readback이 미완료다. 기존 파일을 덮어쓰지 말고 이를 가능한 경우 완결한다.

한국어 최종 보고에는 실제 native run 수와 T/fraction/reference 차이,수지,원인별 실패,commit/PR,두 provider readback을 적는다. Native Grackle-rate Rust port를 upstream Grackle 직접 실행으로 부르지 않는다. 연속 스펙트럼/전체 EoR/관측 Bianchi/CMB는 해당 증거 없으면 HOLD. 소스 재설계나 반복 계획 대신 제공된 구현을 실행해라.
