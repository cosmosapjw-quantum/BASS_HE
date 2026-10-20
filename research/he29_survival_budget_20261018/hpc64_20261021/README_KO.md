# HE29:64코어/128GB 최적화 후속 연구

이번 단위는 **고정 solver를 유지한 source-table 병렬 구성/cache, native 기록 묶음 쓰기, 자원·중복 실행 제어**를 구현한다. 기준 publication `a02ae998570d5a0a4fffdf46299ee77b1c738759`에서 완료된 네 기준해4/4와 저장된09929 분석을 재사용했다. 준비된 미완료 HE29 과학 실행은 **r4/table512 packed canary 한 개**다. 아직 NCP 제출/시작0, native/physical solver0, 실제 HE29 속도 미측정이다.

## 최신 intake

연구 전에 BASS_HE85 branch와 PR78/79/80, 관련 저장소의 정해진 branch/PR/Actions 범위, 백업 변경분, 다른 대화를 확인했다. 새 HE29 반환은 관측 범위에서 없었다. 다른 대화는 실제 서비스 오류, Dropbox의 대규모 folder 조회는 partial pagination이다. 모든 대화나 미게시 원격 실행의 부재를 주장하지 않는다. `evidence/*DELTA*`, `PENDING_INVENTORY.json`, `PERSONAL_CONTEXT_RAW.json`에 범위·실패·후속 판단을 보존한다.

## 코드와 검증

| 경로 | 역할 | 새 검증 |
|---|---|---|
| src/parallel_source.py | 원래 행 산술과 canonical digest를 유지한 spawn pool 및 exact immutable cache |11개 첫PASS, 실제256×640 row bytes 일치1회 |
| src/batched_native.py | 원래 stdio 호출·수치·순서를 유지한 batch flush/fsync |11개 첫PASS, 제조 I/O9sample |
| src/hpc_canary.py | a5 source/manifest, 외부 DATA22, baseline4/4 및 raw/gzip/admission 연결 |10개 첫PASS |
| src/host_plan.py | affinity/cgroup ancestor/memory/process/CPU55/공유lease |12개 첫PASS+cwd2개+root4개 신규 표적PASS |
| src/build_parallel.py,src/batch_entry.py | 기존 bridge 재사용 또는 jobs≤8 compile, table≤48, thread1 canary 한 번 |12개 첫PASS |

총62개 **distinct test methods**이며 기존 suite를 다시 실행하지 않았다. NCP shell2블록 syntax PASS, 제조 return package payload2/2/member3 readback PASS는 별도 근거다. 단일 독립 검토에서 발견한 실제 cgroup 최상위 파일 처리 문제는 좁은 signature 조건으로 수정했다. 현재 검토·게시 상태는 DAG/DELIVERY를 읽는다.

Source-row subset은 직렬0.7128초, spawn2 병렬1.1771초로 작은 입력에서 병렬 쪽이 느렸다. 제조 trace I/O는 원본 중앙값1.9774초, B256 0.6100초, 해당 범위3.242배였다. 이 숫자들은 NCP64 또는 HE29 solver 배율이 아니다. 이전 pair에서 table이3.79%였으므로 그 구간만 없애는 이상적 전체 가속 상한은1.0394배다. 이전 assembly/IVP 배율과 곱하지 않는다.

B256은 hardkill 때 마지막 완료 fsync 이후 성공 반환 point 최대255개의 trace가 durable하지 않을 수 있는 변경된 계약이다. 정상/제어된 실패·segment·RAW·close 경계를 확정하고, complete gzip readback 및 count 일치 후에만 RESULT를 쓴다. 자세한 유도·출처·실제 결과는 `RESEARCH_KO.md`, `evidence/EXTERNAL_RESEARCH.json`, `evidence/TRACE_POLICY_KO.md`와 각 DELIVERY에 있다.

## 실행/게시/백업

Intake는 `cbbed9c3da6b41914527e322d2cb9bea9dc7b1f3`로 게시, 실제8/8 Git readback PASS다. Stage1 Dropbox는 raw payload9/9 및 regular member10/10 PASS이며 Drive와 후속 보존 상태는 `evidence/INTAKE_BACKUP_RECEIPT.json`의 실제 기록을 따른다. 고정 실행 code pin은 후속 `DELIVERY.json.code_commit`, 후속 문서 HEAD는 별도다. PR78은 Draft/open/unmerged를 유지한다.

실행자는 `NCP_HANDOFF_KO.md`를 따라 Git pin을 읽고 `ncp/RUN_READY.sh`를 한 번 사용한다. 실제 host·process·저장 결과를 관측한 뒤 기존 bridge를 재사용하고 필요한 구간만 계산한다. 사용자에게 파일 전송/터미널 작업을 넘기지 않는다. RDC 호출0이며 별도 접근 가능한 NCP 실행자는 현재 발견되지 않았다.

원래 physics·반응률·적분 허용치·gate와 full-state19ledger norm을 유지한다. 연속 스펙트럼, 전역온도상한, 전체EoR, wholeGrackle 동등성, 관측Bianchi/CMB는 HOLD다. 초기 standalone skill1.0.0과 이번 통합 plugin1.3.0 이력을 구분하며 버전 때문에 완료 단계를 반복하지 않는다.
