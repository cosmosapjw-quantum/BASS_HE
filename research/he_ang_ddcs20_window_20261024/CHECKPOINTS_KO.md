# 단계별 evidence 및 checkpoint 연결

20개 R1–R10/C1–C10 각 행은 `LOOP_PROGRESS.json`에 자체 predecessors/status/evidence/checkpoint/Dropbox·Drive backup 상태를 가진다. 여러 닫힌 단계가 하나의 실제 archive/업로드 ACK를 공유할 수 있다. 단계별 표기는 서로 다른 20개 압축본 생성을 뜻하지 않는다.

첫 checkpoint `HEANG_DDCS20_R1_R10_C1_C5_20261024.tar.gz`는 theory loop 완료 및 implementation preparation C1–C5만 포함한다. C6–C10의 실제 run/review/admission은 이 checkpoint에서 완료가 아니다. Git publication은 `PENDING_C9`, 원격 backup은 실제 provider ACK 전 `PENDING_PROVIDER`다. Root가 업로드를 마치면 해당 닫힌 stage 행에 같은 실제 ACK identity를 연결한다.

Archive는 공개 가능한 전사 수치/독립 유도/코드/범위화한 survey만 포함하며 원문 논문 PDF·이미지·전체 추출·full personal search는 포함하지 않는다. RAW_OBSERVATIONS는 원위치와 hash reference만 들어간다. Archive 자체를 자신 안에 넣지 않으며 archive 외부 receipt가 SHA256/bytes/member list를 기록한다.

두 번째 이후 checkpoint는 C6–C8 raw outcomes와 C9 결정이 생긴 뒤 root 승인된 범위로 닫는다. 실패·pending을 complete로 바꾸거나 과거 Hex ledger를 초기화하지 않는다. Scientific admission과 게시/backup 성공은 별도 상태다.
