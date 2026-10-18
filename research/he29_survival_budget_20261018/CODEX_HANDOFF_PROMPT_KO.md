# HE29 Codex/NCP 실행 인계: Git에서 직접 시작

2026-10-18 게시 복구 완료. 사용자에게 파일 다운로드·업로드·터미널 조작을 요청하지 말고, 허용된 GitHub/NCP/클라우드 접근으로 직접 진행한다. 새 알고리즘 개발은 요청하지 않는다. 컴파일, 필요한 작은 환경 수정, 준비된 네 기준해 실행과 반환만 수행한다.

## 고정 출발점

- Repository: https://github.com/cosmosapjw-quantum/BASS_HE
- Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- Branch: research/he29-survival-budget-20261018
- 실행 코드·테스트 revision: 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
- 원본 native owner: rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474
- Parent HE28 완료 native 결과: PR77, a41dd37124e34cb22bb9782aaf687a0da91640b7.

먼저 최신 branch/백업에 같은 HE29 실행의 새 결과가 있는지 확인한다. 완료된 실행은 복원·비교하고 반복하지 않는다. 없다면 신규 checkout에서 위 실행 revision을 pin한다. 이후 문서·delivery 커밋은 읽되 science 코드가 다르면 변경 내용을 먼저 확인한다. 기존 dirty checkout, PR, production job, 실패 결과는 보존한다.

## 입력은 Codex가 확보

현재 모든 실행 코드와 테스트가 Git에 있다. 원본 native 입력22개는 별도 불변 archive에서 코드가 직접 복원한다. public PARENT_SCIENCE.json의 선택 필드 투영을 원본 입력 바이트로 대신하지 않는다.

입력 archive: BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz
129635 bytes; SHA256 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205
Drive: https://drive.google.com/file/d/1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi/view
Dropbox: /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz

NCP에 인증된 rclone dbx: 또는 gdrv:가 있으면 START_REFERENCES.sh가 직접 가져온다. NCP에 rclone이 없다면 Codex가 연결된 Drive/Dropbox 도구 또는 사용자 Ubuntu의 기존 rclone으로 위 파일을 직접 확보하고 NCP에 전송하여 HE29_INPUT_ARCHIVE를 지정한다. 사용자에게 전달을 맡기지 않는다. 권한이 실제로 없으면 우회하지 않고 접근 blocker를 보고한다.

## 실행 명령

원본 repo를 직접 fetch하고 신규 checkout을 만든 뒤, NCP의 기존 승인된 SSH 경로를 사용한다. 이미 NCP 내부면 SSH를 생략한다. 개인 접속정보는 공개 Git에 쓰지 않는다.

```sh
D="$PWD/research/he29_survival_budget_20261018"
export HE29_WORK_ROOT="$HOME/HE29_REFERENCE_$(date -u +%Y%m%dT%H%M%SZ)"
# 자동 복원이 불가능할 때만, Codex가 직접 받은 원본 archive의 경로를 지정한다.
# export HE29_INPUT_ARCHIVE=/absolute/path/to/verified-original-input.tar.gz
bash "$D/ncp/START_REFERENCES.sh"
```

RESTORE_VERIFIED_INPUTS.py는 archive 전체 SHA와22개 개별 입력 SHA를 검사하고 DATA만 추출한다. archive 코드는 실행하지 않는다. 기존 입력이 다르면 덮어쓰지 않는다. 이어서 변경하지 않은 BOOTSTRAP_REFERENCES.sh가 정확한 원본 Rust lib/HE25 owner_server를 컴파일하고 저장된 실제 점6개와 새 binary를 대조한다. 이 점 비교를 upstream Grackle 전체 동등성으로 부르지 않는다.

## 범위·판정

m8/GL4/q0에서 (r2,table512), (r4,512), (r8,512), (r4,1024) 네 model/table의 Radau+DOP853만 실행한다. 이미 완료된 HE28 transport6개는 재실행하지 않는다. table512는 저장된 원본 table SHA와 일치해야 한다. table1024는 별도 table 민감도다.

case<=3600s, table<=600s/2GiB, 단일 numerical thread, 첫 실패 STOP을 유지한다. photon3e-15/H, energy3e-12eV/H, 절대 fraction1e-11, reference temperature stability1e-9K를 완화하지 않는다. Radau/DOP853 일치는 경험적 안정성이고 엄밀한 오차반경이 아니다. native4개는 아직 NOT_RUN이며 기존50개 로컬 테스트를 native PASS로 승계하지 않는다. 그50개는 기존47개+포장3개이며 입력 archive가 없는 환경에서는 포장2개가 명시적으로 skip될 수 있다.

분석기는 같은 model/table의 시간 효과와 strip/table 차이를 구분한다. 첫 실패의 argv/stdout/stderr/input/table identity와 부분 출력은 보존한다. 물리적 재설계가 필요하면 작은 환경 수정으로 위장하지 말고 연구 스레드에 반환한다.

## 게시·백업 및 최종 보고

단계마다 DAG와 실제 case/native 호출 수를 기록한다. 새 결과는 별도 results branch/Draft PR에 게시하고 원본 PR78은 변경하지 않는다. 원시 로그·입력·소스 및 source/binary/table SHA를 아카이브로 만들어 Dropbox·Drive에 create-only 백업한다. 가능한 실제 다운로드 SHA/내부 manifest readback을 실시하고 provider checksum과 구분한다. 과거 ncp/PUBLISH.sh는 초기 미게시 복구 전용이며 현재 branch에 재실행하지 않는다.

한국어로 완료수0~4, 독립 기준해 오차/수지, time/strip/table 구분, commit·PR와 백업 영수증을 보고한다. 연속 스펙트럼·전체 EoR·upstream Grackle 직접 동등성·관측 Bianchi/CMB는 해당 범위 검증 전 HOLD다. 이 인계만으로 실행 권한 밖의 접근·새 비용·무한 재시도는 허용되지 않는다.
