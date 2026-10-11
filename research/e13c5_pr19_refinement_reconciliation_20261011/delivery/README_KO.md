# NCP_READY 전달 완료 — E13C5 / PR19 refinement

과학 core는 `f2fefc0c51de41f8ea036a21ba2e0728c3260490`이며, 이 delivery 디렉터리는 그 뒤에 추가한 실제 전달 증명이다. Scientific source·계산 결과·잠금 payload는 바꾸지 않았다.

## 한 개의 전달본

- 파일: `BASS_HE_E13C5_NCP_READY_20261011_sha_e2aac517d708.zip`
- 크기: **3,455,297 bytes**
- SHA-256: `e2aac517d7088c5d5d17f7ee994c6b084a33a9c1df5e5e28eb99d5de6af8634f`
- 내부 scientific ZIP: **3,843,064 bytes**, SHA-256 `291b57399184bb3042ec1b3e0aae4a648b6ba909273d8dbd50752954df639cf3`
- 추가 전달파일: **필요 없음**. Outer ZIP에 실행문·receipt·START와 전체 scientific ZIP을 함께 넣었다.
- 로컬 검증: outer/inner CRC, 모든 manifest payload의 크기·SHA, 중복·위험 member 검사 PASS.
- 별도 전달 경계 정적 대조: PASS. 19개 continuation runtime file과 10개 physics execution file이 모두 포함된다.

## 실제 백업 위치

[Google Drive NCP_READY](https://drive.google.com/file/d/1dYsblmWq0BJaGZ4yY4hmGgpXTOURFrG0/view?usp=drivesdk)

Dropbox: `/BASS_DERIVATION_DOSSIERS_20260912/BASS_HE_E13C5_NCP_READY_20261011_sha_e2aac517d708.zip`

두 위치에 create-only upload가 완료됐으며 파일명·경로·크기를 확인했다. 검증 수준은 **R1 upload ACK + metadata**다. 원격 전체 파일 다운로드·복구 검사는 하지 않았다. 정확한 객체 ID와 응답은 `NCP_READY_BACKUP_ACK.json` 및 `BACKUP_UPLOAD_EVIDENCE.json`을 읽는다.

Detached backup ACK도 두 위치에 저장했다. 그 실제 저장 위치는 `BACKUP_ACK_STORAGE.json`에 있다. ACK는 운영 증명이며 NCP runtime dependency가 아니다.

## NCP 작업과 반환

아카이브의 `00_START_HERE_KO.md`와 `NCP_LOCAL_CODEX_HANDOFF_KO.md`를 읽는다. CPython 3.12.x/Linux에서 검증한 package에 포함된 `code/ncp_continue.py --execute`를 실행한다.

정확한 work unit은 **N512/P60 두 OFF 경로 한 번 → fresh 결과의 exact reduction 한 번**이다. 기존 동일 source/work unit의 실제 성공 NCP 반환이 있으면 검사해 재사용한다. 새 coefficient는 4096, process/thread 1, MPI 0이며 자동 retry·N/P 변경·전체 first2 확대는 하지 않는다.

실제 NCP 과학 실행 상태는 **NOT_RUN**, recipient execution ACK는 **NOT_RECEIVED**다. 성공 기준은 실행 후 `PASS_SCOPED_HOST_PARITY_AND_REDUCTION` 및 1+1회 실행·fresh input SHA·projection 일치다. Verify-only와 업로드 완료를 실제 host 성공으로 해석하지 않는다.

## 연구 상태

두 OFF 경로 refinement와 PR19 mode별 exact replacement에 대한 독립 판정은 PASS_SCOPED다. Full first2는 HOLD_RESOURCE_AUTHORIZATION, physical/production은 HOLD다. 다음 연구 노드는 `E13C5_SELECTED_SUBSET_BUDGET_AND_MISSING_NODE_COMPLEMENT_CONTRACT`다.

현재 PR19에 additive·nonforce로만 기록했으며 merge하지 않았다. Git core는 NCP runtime 전체를 포함하지만 전체 archive payload의 projection이다. 608개 생략 payload도 NCP_READY 안의 scientific ZIP에는 온전히 포함되어 있다.

