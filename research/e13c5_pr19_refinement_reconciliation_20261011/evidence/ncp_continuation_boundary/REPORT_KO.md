# E13C5 NCP continuation synthetic boundary control

**PASS_SCOPED_SYNTHETIC_BOUNDARY_REPAIR. 실제 과학 계산과 NCP host job은 각각 0회다.**

실제 `ncp_continue.py` bytes를 그대로 fixture package에 복사했다. 두 child executable과 19개 lock payload는 명시적인 NO_SCIENCE mock이다. Fixture wrapper가 출력하는 ACTUALLY_EXECUTED/PASS 문자열은 제어 흐름 시험을 위한 합성 상태이며, 실제 scientific 실행으로 집계하지 않는다.

## 최초 실행과 finding

최초 source SHA256: `24daad3ca88bbb0d8aa64329376e4ab412cb2cf5a6adbc24feb09b44407db921`.

11개 서로 다른 case 중 10개가 예상 동작을 보였다. 기본 verify-only, fresh success, stale current input hash, false fresh parity, failed physics child, wrong projection bytes, pre-run locked payload tamper, wrong producer hash, mid-run locked payload tamper, existing output collision을 포함한다. False parity/failed physics 뒤에는 reduction child가 실행되지 않았다. 기존 output marker도 보존되었다.

추가 lock metadata case에서 최초 failure가 관측되었다. Child가 CONTINUATION_LOCK.json의 metadata만 변경했을 때, 19개 payload의 bytes는 그대로여서 wrapper가 exit 0/PASS와 source_unchanged_during_run=true를 반환했다. 마지막 check_lock은 intake에서 파싱한 object만 사용하고 lock 파일 자체의 SHA를 다시 확인하지 않았다. 최초 harness actual exit는 1이며, 원 source와 모든 case raw evidence를 FIRST_FAILURE.json, FIRST_FAILURE_SOURCE_ncp_continue.py, cases/에 보존했다.

## Owner 수정 후 필요한 범위만 재확인

수정 source SHA256: `38957cb24f58b5d36dd4823ce7e642c708f0f4cae725ac2377d3f824b2b41626`.

Owner가 intake lock SHA를 고정하고 마지막 성공 기록 전에 실제 lock 파일 SHA와 비교하도록 수정했다. Main source는 이 agent가 수정하지 않았다. 변경된 source와 lock identity를 확인한 다음 세 가지 관련 fixture만 새 디렉터리 repair_01/에서 실행했다.

| Case | Actual wrapper exit | 관측 결과 |
|---|---:|---|
| Default verify-only | 0 | VERIFY_ONLY_READY, reduction child 0회 |
| Fresh success | 0 | PASS_SCOPED_HOST_PARITY_AND_REDUCTION |
| Mid-run lock metadata tamper | 1 | FAILED: continuation lock metadata changed during run |

Focused harness actual exit는 0, tool wall time은 0.579502755초다. 세 case 모두 예상 결과였다. 기존 11개 case 전체를 반복하지 않았다.

## 증거와 한계

FINAL_SUMMARY.json이 현재 결론과 최초 failure/수정 후 결과의 포인터를 담는다. Per-case RUN_START.json/RUN_FINISH.json, wrapper stdout/stderr, child invocation records 및 child raw logs가 보존되어 있다. FINAL_FILE_MANIFEST.json은 이 작업 디렉터리의 파일 identity 목록이다.

검사 범위는 프로세스 순서, fresh-input/producer/projection identity, lock 변경 감지, output collision과 실패 전달이다. 두 child는 mock이므로 기존 scientific runner의 수치 동작을 다시 검증한 결과가 아니다. Timeout/resource-exhaustion stress, network/publication, 실제 NCP job은 실행하지 않았다.
