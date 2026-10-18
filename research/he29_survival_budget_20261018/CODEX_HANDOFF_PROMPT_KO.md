# HE29 Codex/NCP 인계: 게시 완료, Git에서 직접 실행

백업/게시 재시도는 완료된 코드를 다시 개발하는 작업이 아니다. 사용자에게 파일 다운로드·업로드·터미널 입력을 요구하지 말고, 허용된 GitHub/클라우드/NCP 접근으로 준비된 실행만 수행한다.

## 고정 출발점
Repository: https://github.com/cosmosapjw-quantum/BASS_HE
Draft PR78: https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
Branch: research/he29-survival-budget-20261018
실행 코드·테스트 revision: 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
이 프롬프트 갱신 직전 확인 publication HEAD: 068bdccc6f991a046300cc0634c9092d72e953d3
Parent HE28 PR77: a41dd37124e34cb22bb9782aaf687a0da91640b7
원본 native owner: rei_bianchi@f7830e2f55e7a1938bc3c98f61b60651f8dae474

먼저 현재 branch/백업에서 새 HE29 native 결과가 있는지 읽는다. 완료됐다면 복원·분석하고 중복 계산하지 않는다. 새 결과가 없다면 별도 checkout을 만든 후 위 실행 revision에 고정한다. 최신 문서·DAG·delivery는 읽되 과학 코드가 달라졌으면 먼저 대조한다. 기존 dirty tree, 실패 기록과 production job을 변경하지 않는다. 현재 PR은 Draft이며 자동 merge하지 않는다. 과거 미게시 복구용 ncp/PUBLISH.sh는 다시 실행하지 않는다.

## 사용자 조작 없이 입력 확보
ncp/START_REFERENCES.sh가 인증된 rclone dbx:/gdrv:로 원본 입력 archive를 가져와 22개 DATA만 전체/개별 SHA 검증 후 복원한다. archive의 옛 코드는 실행하지 않고 기존 불일치 입력을 덮어쓰지 않는다.

입력 파일: BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz
129635 bytes; SHA256 a70d320c7ead5f1fd93170c18f1f80ae5eb58a293a6045a0f728bb7ae2743205
Drive id: 1I31wE6A3laYE6nxMcKNmm5rNMeESIsXi
Dropbox: /BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_HE29_RESUME_COMPLETE_20261018_a70d320c.tar.gz

NCP에 인증된 rclone이 없으면 Codex가 연결된 Drive/Dropbox 또는 Ubuntu의 기존 rclone으로 직접 확보·전송하고 HE29_INPUT_ARCHIVE를 지정한다. 입력 접근이 불가능하면 접근 blocker를 기록한다. 사용자에게 수동 전달을 요구하거나 public 선택 필드 투영을 raw 입력 대신 쓰지 않는다.

## NCP에서 Codex가 실행할 명령
승인된 SSH 연결로 NCP에 들어간다. 이미 NCP 내부면 생략한다. 개인 SSH 정보는 공개 Git에 쓰지 않는다. Git에서 코드를 직접 확보한 새 checkout의 repository root에서:

```sh
git checkout --detach 1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
D="$PWD/research/he29_survival_budget_20261018"
export HE29_WORK_ROOT="$HOME/HE29_REFERENCE_$(date -u +%Y%m%dT%H%M%SZ)"
bash "$D/ncp/START_REFERENCES.sh"
```

BOOTSTRAP_REFERENCES.sh가 원본 Rust lib와 unchanged HE25 owner_server를 컴파일하고 실제 저장된 native 점6개로 대조한다. 이것은 제한된 점 비교이지 upstream Grackle 전체 실행 동등성이 아니다.

작업은 m8/GL4/q0에서 (r2,table512),(r4,512),(r8,512),(r4,1024)의 Radau+DOP853 네 쌍만이다. 기존 HE28 transport6개는 반복하지 않는다. table512는 원본 SHA와 일치해야 비교하고 table1024는 별도 table 민감도로 해석한다.

case3600s, table600s/2GiB, 단일 numerical thread와 첫 실패 STOP을 유지한다. photon3e-15/H,energy3e-12eV/H,절대 fraction1e-11,reference temperature stability1e-9K를 완화하지 않는다. 서로 다른 적분기의 일치를 엄밀한 오차반경으로 부르지 않는다. 로컬50개 테스트를 native PASS로 승계하지 않는다. 입력 archive가 없는 검사 환경에서 포장 검사가 skip되면 전체50 PASS로 기록하지 않는다.

단계별 DAG·실제 case/native calls·실패 원본·source/binary/table SHA를 보존한다. 새 결과는 별도 results branch/Draft PR에 게시하고 기존 PR78과 baseline을 유지한다. 원시 결과와 실행 소스를 불변 아카이브로 만들어 Dropbox/Drive create-only 백업 후 실제 다운로드 SHA/manifest를 확인한다. provider content_hash만 확인한 경우 raw readback과 구분한다.

2026-10-18 최종 패키지 c47c5efc의 Drive 전체 SHA와94파일 및50테스트가 재확인됐다. Dropbox는 업로드와 provider content_hash 일치, raw-byte readback은 아직 미검증이다. 새 native 기준해는0/4 NOT_RUN이다. 연속 스펙트럼·전체 EoR·upstream Grackle 직접 동등성·관측 Bianchi/CMB는 계속 HOLD다.
