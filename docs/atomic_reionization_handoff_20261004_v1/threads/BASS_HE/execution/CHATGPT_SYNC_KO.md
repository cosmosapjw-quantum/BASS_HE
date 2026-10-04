# Fastest track 재개·연구 스레드 전달 기록

2026-10-04. 사용자 지정 시작 계약은 `271fa2b89cd37b0d07ab0c07ad7ea5ef2a02a58e`의 `threads/BASS_HE/CODEX_START_KO.md`다. 실제 작업 branch는 기존 `research/shared-c64-crossrepo-20260928`이며 이번 supplier 입력 HEAD는 `231a91db0218a09168ee53b009b6603cfa606cff`다. 새 branch를 만들거나 이전 pin으로 reset하지 않았다. 진행 상태는 연구 스레드가 게시한 `../CURRENT_FASTEST_STATE.json`을 우선한다.

연구 스레드: https://chatgpt.com/c/6abfa004-5738-83ee-8b2f-956c60cbdc17

이 URL은 현재 도구에서 로그인 화면을 반환했다. 스레드 본문을 읽거나 메시지를 게시하지 않았으며 자동 양방향 동기화가 확인됐다는 주장을 하지 않는다. 아래 내용을 그 스레드에 전달할 수 있도록 보존한다. 이후 실제 전달 또는 연구 스레드의 새로운 계약 수신은 별도 기록이 필요하다.

## 전달 내용

최신 동기화는 `REPO_SYNC_20261004T141630Z/RETURN.json`이다. 연구 스레드의 HE-F2A/B를 fast-forward로 수신하고, rei의 `67957715cf3336b89c27c1e59c33ca23098f8934`에서 일반 REI-F01 완료 영수증을 확인했다. 영수증에 기록된 6개 산출물 SHA256을 대조했고, provider record 21개의 schema를 확인했다. 이는 소스/구조 검사이며 기존 Rust/원자물리 suite를 다시 실행한 결과가 아니다.

새 manifest는 Grackle 참조율과 Verner 광흡수를 제공한다. HeIII+HI 전하교환 provider record는 없으며, 일반 F01 완료를 선택적 RCT provider 계약으로 승격하지 않는다. F00의 모형·process·lane 파일 3개는 이전 pin과 SHA256이 동일하고 RCT/NRCT는 여전히 제외됐다. 현재 baseline에 BASS_HE rate를 연결할 필요는 없다. RCT owner opt-in/domain/source/energy closure 또는 실제 F09 결과가 생길 때만 공급자 코딩을 다시 연다. 새 wrapper/원자 계산은 추가하지 않았다.

일반 F01 경로의 과거 HTTP404 관측은 이번 완료 영수증으로 대체한다. HE-F2A 후보 제안과 HE-F2B 제외 binding은 연구 스레드의 완료 범위 그대로 수신했다. 현재 RCT 포함의 수락, physical provider admission, scientific promotion은 여전히 미완료다. 형식 검사 로그의 정상적인 빈 파일을 초기 동기화 검사가 거절한 기록은 `REPO_SYNC_20261004T141630Z/VERIFICATION_FAILURE.json`에 보존했고, 남은 조회만 이어서 확인했다.

아래 두 intake는 과거 코딩 기록이며 최신 작업 선택 지침이 아니다.

최신 코딩 루프는 `HE_F2_INTAKE_20261004T131324Z/RETURN.json`이다. rei의 `5f3bfe2fc8fe275ab6a054ca9082f03c5b91427a`에서 REI-F00 완료 영수증과 세 contract artifact, fixture, 명령 로그를 가져왔다. 영수증에 기록된 SHA256과 실제 바이트를 대조하고 model/task/input identity를 확인했다. 새 `consumer_receipts.py`의 거절·재개 상태 검증은 최초 13개를 통과했고, claim ceiling 누락과 충돌하는 기존 완료 기록 보호를 추가한 최종 15개도 통과했다. 이 입력 경계 검증은 기존 과학 suite를 재실행하지 않는다.

이전 intake에서는 REI-F00을 design-lock 범위에서만 완료로 반영했다. 당시 선택 경로에서 REI-F01 영수증과 `atomic_provider.rs`는 HTTP404였다. 이 관측은 위 최신 영수증으로 대체한다. 당시 Codex는 `REACTION_BINDING.json`과 `CONSUMER_LEDGER_ACCEPTANCE.json`을 생성하지 않았으며, 이후 연구 스레드가 게시한 HE-F2A/B 후보/비수락 산출물을 이번에 수신했다. 이전 확인 기록과 게시 초기 상태는 보존한다.

- 최신 게시 커밋에서 HE-F1은 완료됐다. 영수증은 `../runs/HE-F1_20261004/RETURN.json`이다. 기존 GM25 core SHA256과 일치하는지 이번에 확인하며, HE-F1의 57개 검증 결과는 기존 실행 근거로 재사용한다. 같은 suite를 새 PASS로 재표시하지 않는다.
- 게시 당시 `EXECUTION_STATE.json`에는 HE-F1 완료가 반영되지 않아 기본 선택기가 HE-F1을 다시 추천한다. 원본 게시 상태와 전역 DAG를 바꾸지 않고 별도 `RESUME_STATE.json`에 완료 영수증을 연결한다.
- 다음 노드는 HE-F2다. 최초 확인 때 `REI_SCOPE_LOCK=REI-F00`, `REI_PROVIDER_CONTRACT=REI-F01`가 모두 없었고, 이 이력은 `HE_F2_INTAKE_20261004T130100Z/DEPENDENCY_INSPECTION.json`에 보존한다. 최신 확인은 위의 별도 기록을 따른다. 선택 경로의 부재가 다른 private/unpublished 작업의 부재를 증명하지는 않는다.
- 실제 모형/closure 및 provider 계약을 받기 전에는 `REACTION_BINDING.json`과 `CONSUMER_LEDGER_ACCEPTANCE.json`을 완성 처리하지 않는다. 임의 mono-Q closure, null-to-zero, 밀도·opacity 이중 귀속, GM25/KF96 자동 선택·합산을 도입하지 않는다.
- 이 대기는 optional REI-F09 감도만 지연시킨다. REI-F08 baseline 또는 독립 소비자 작업을 막는 전역 gate로 승격하지 않는다. HE-L1/L2/L3, B5C3, 완료된 resume-004를 재개하지 않았다.

## 다음 실행

저장소 루트에서 현재 authoritative 상태를 확인한다. 과거 resume 사본이나 초기 PROGRAM 선택기의 READY만으로 제외된 RCT 작업을 다시 열지 않는다:

```bash
cat docs/atomic_reionization_handoff_20261004_v1/threads/BASS_HE/CURRENT_FASTEST_STATE.json
```

외부 완료 ID를 문서 존재만으로 추가하지 않는다. 일반 F01 완료와 실제 RCT instance는 구별한다. RCT owner 결정·provider/closure·실제 수락 계약이 도착하면 exact commit/content hash를 고정하고 HE-F2의 기존 acceptance에 한정하여 실행한다. 과학 가정 변경은 연구 스레드로 반환한다. Git 게시 확인은 별도 publication receipt를 따르며, Git 수신을 대화 본문의 실제 확인으로 부르지 않는다.
