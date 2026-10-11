# BASS_HE E13C5 — NCP 시작 안내

이 NCP_READY 압축파일 **한 개**에 실행문, 입력, 결과, 소스, 두 실행 잠금 파일과 독립 검토 기록을 넣었다. 추가 E13C4 전달파일이나 과거 임시 디렉터리는 필요 없다.

## 현재 완료 상태

- 연구 노드: `HE_E13C5_PR19_REFINEMENT_RECONCILIATION01`.
- 실제 scientific core commit: `f2fefc0c51de41f8ea036a21ba2e0728c3260490`.
- 실제 scientific core tree: `7991cff42f09861366311f4cdfba0edcaa99af1e`.
- 현재 계보: BASS_HE draft PR19, `research/e13c5-first2-branch-cover-20261011`.
- PR19의 기존 12개 선택 경로 중 OFF0·OFF700을 N512로 정밀화하고 mode별로 합산했다. 독립 판정은 `PASS_SCOPED`, 열린 blocker는 0건이다.
- **실제 NCP 과학 실행은 아직 `NOT_RUN`이다.** 업로드 ACK와 준비 확인은 NCP 실행 ACK가 아니다.

## 파일을 여는 순서

1. 전달 메시지 또는 별도 실제 backup ACK에서 **바깥 ZIP의 전체 SHA-256와 크기**를 확인한다. ZIP을 새 경로에 안전하게 풀고 `NCP_READY_MANIFEST.json`의 각 파일 크기·SHA를 확인한다.
2. `DELIVERY_RECEIPT.json`의 `scientific_archive`에서 내부 ZIP의 정확한 이름·크기·SHA 및 package root를 읽는다. 내부 ZIP을 새 경로에 안전하게 풀고 root `FILE_MANIFEST.json`의 모든 payload를 확인한다.
3. 두 ZIP 모두 absolute path, `..`, symlink와 중복 member를 거부한다. 기존 checkout이나 return directory를 덮어쓰지 않는다.
4. `NCP_LOCAL_CODEX_HANDOFF_KO.md` 전체를 읽고 그대로 진행한다. 실행에 필요한 모든 파일은 내부 package에 있다.
5. 내부 package의 `CONTINUATION_REPORT_KO.md`, `INDEPENDENT_REVIEW.json`, `INDEPENDENT_LINEAGE_REVIEW.json`, `NCP_CONTINUATION_CONTRACT.json`, `CONTINUATION_LOCK.json`, `NEXT_DAG.json`을 먼저 읽는다.

동일 source와 동일 work unit에 대한 실제 성공 NCP return이 이미 있으면 검증하여 재사용한다. 준비 확인이나 Chat의 결과를 그러한 return으로 간주하지 않는다.

## 이번 NCP 실행

검증한 package에서 CPython 3.12.x / Linux / 표준 라이브러리로 실행한다. 정확한 명령과 자동 고유 output 경로를 만드는 Python block은 handoff에 포함되어 있다.

```text
python3 code/ncp_continue.py --package <검증한 package 절대경로> --out <아직 존재하지 않는 새 output 절대경로> --execute
```

`--execute` 없이 실행하면 verify-only다. 과학 work unit은 N512/P60 두 OFF 경로 한 번, 이어서 fresh 결과에 대한 exact reduction 한 번이다. Process 1 / thread 1 / MPI 0, 새 coefficient 4096, physics child 180초·wrapper 205초·reduction 60초, 각 1 GiB 제한을 지킨다. 동일 job을 자동 재시도하거나 N/P·tolerance를 바꾸지 않는다.

성공 status는 `PASS_SCOPED_HOST_PARITY_AND_REDUCTION`이다. 상세 parity hash, fresh input identity와 return manifest 조건은 handoff가 소유한다. 첫 실패의 stdout/stderr·checkpoint·실제 exit를 보존하고 실패를 성공으로 바꾸기 위해 baseline을 수정하지 않는다.

## 이번 인증의 한계와 다음 연구

고정된 captured model의 선택 부분집합에 대한 interval enclosure다. Full first2는 `HOLD_RESOURCE_AUTHORIZATION`, physical/production은 `HOLD`, baseline RCT는 `OFF`이며 실제 atomic photon/heat/recoil은 `null`이다. 세 gas history OFF/KF/GM을 하나의 물리량으로 합하지 않는다.

다음 연구 노드는 `E13C5_SELECTED_SUBSET_BUDGET_AND_MISSING_NODE_COMPLEMENT_CONTRACT`다. 선택 부분집합의 interval 폭과 누락된 spectral node의 signed contribution을 분리해 조건·상계·자원 계약을 정한다.

별도 `NCP_READY_BACKUP_ACK.json`은 업로드 후 생성되는 운영 증명이다. 이 파일이나 추가 전달파일 없이도 이 압축파일 하나로 NCP 실행을 준비할 수 있다. 원격 복구 검사를 했다고 가정하지 않는다.
