# BASS_HE E13C5 PR19 연결 — 추가 독립 판정

## 판정

**PASS_SCOPED. 최종 열린 blocker는 0건이다.** 판정 대상은 `HE_E13C5_PR19_REFINEMENT_RECONCILIATION01`의 같은 관측량 연결, 저장 incoming의 재사용 적합성, 양의 가중치를 이용한 mode별 선택 부분집합 합산, 그리고 이 결과를 재현하도록 준비한 NCP continuation 계약이다.

기존 `INDEPENDENT_REVIEW.json`의 두 OFF 경로 `PASS_SCOPED`는 그대로 유지한다. 그 문서의 늦게 발견된 외부 계보에 대한 `HOLD_PENDING_RECONCILIATION`은 **이 추가 검토 범위에서 해소**된다. 기존 PR19의 나머지 경로 전체를 이번 reviewer가 새로 물리 검증했다는 뜻은 아니다. 실제 publication·백업·NCP 실행·receiver ACK는 각각 해당 실제 증거가 소유한다.

| 대상 | 판정과 근거 범위 |
|---|---|
| OFF0·OFF700 N512/P60 enclosure | 앞선 독립 `PASS_SCOPED` 유지; 과학 source와 raw 결과 변경 없음 |
| PR19의 N128/P60 선택 12-path | 기록된 선행 scoped 판정 상속; 이번에 전체 물리 재심사하지 않음 |
| 공통 두 OFF 경로 의미·incoming 연결 | 원본 pilot/cover와 현재 저장 자료의 exact 연결 확인 |
| OFF의 두 항만 교체한 네 node 합 | Exact Fraction 직접 합산의 conditional enclosure |
| KF·GM | 각 모드의 기존 네 경로와 published aggregate 보존 |
| NCP continuation 실행 계약 | 준비된 scoped 실행에 적합; 실제 NCP 물리 실행은 NOT_RUN |
| Full first2·full spectrum·physical·production | 기존 HOLD 유지 |

## 독립성과 읽은 범위

Reviewer는 `/root/e13c5_independent_review`다. 후보 enclosure, lineage theory, reducer, acceptance 설계 및 NCP wrapper를 작성하지 않았다. 리뷰 증거용 exact Fraction 감사와 이 판정 파일만 작성했다. GPT-6 Astra 연구/코딩 v4.0.0 하네스의 독립 판정 역할을 그대로 적용했다.

직접 읽은 범위는 원 `cover.py`·`pilot.py`, 선행 계약·보고서·리뷰·START·stderr, 계보 복구 계약과 addendum, 새 이론 및 reducer 전체, 실제 저장 결과의 관련 필드, reducer 실제 실행 기록, 새 NCP wrapper 전체와 수정 diff, lock·계약·최종 handoff·DAG·README·보고서·그림이다. 주요 JSON은 실제 bytes를 파싱하여 필요한 interval과 identity를 읽었다. 선행 나머지 열 경로의 physical local kernel과 변경 없는 E13C4 primitive/suite는 다시 실행하거나 재귀적으로 심사하지 않았다.

선행 `first2/independent_review.md`는 controller가 전달한 독립 Astra 결과의 전사라고 명시한다. 여기서는 이를 **기록된 선행 판정**으로 취급한다. 이번의 직접 재검증으로 바꾸어 부르지 않는다. prior와 current가 같은 captured model과 E13C4 coefficient/interval helper를 공유하므로 두 결과의 일치는 그 물리 모형의 독립 검증이 아니다.

세부 read scope·실제 파일 크기·SHA는 `evidence/lineage_review/READ_FILE_IDENTITIES.json`에 기록했다. SHA는 읽은 자료의 identity이며 과학 타당성의 독립 증거를 대신하지 않는다.

## 1. 실제 계보와 같은 관측량의 연결

추가 판단의 고정 parent는 PR19 `e25039b3a53031ce37800cebefb51200aa5a63a2`, tree `fe861762030cb7b669512fdfa3be8f2c0a188d2c`다. PR18 `48f648cd905cd8c232ae43abe97745ac6a96dec2`의 OFF700 pilot이 그 선행 계보다. 처음 PR17만 읽었던 상태를 현재 전체 연구 frontier로 사용하지 않는다. 검색 결과는 읽은 범위의 기록이며, 모든 다른 branch·파일의 부재를 증명하지 않는다.

PR19에는 OFF/KF/GM × node 0/700/1620/2344의 선택 12개 경로, 36개 segment가 이미 있다. 33개 segment가 새 계산이고 OFF700의 세 segment는 pilot 재사용이다. 실제 기록된 bounded 실행은 exit 0, wall 34.60초, RSS 65,652 KiB다. 출판 receipt의 solver reruns 0은 **출판 단계의 추가 재실행이 0**이라는 뜻이다. 읽은 파일만으로 그 과학 실행 호스트를 NCP라고 인증할 수 없다.

두 OFF 경로는 같은 captured row·stage·mask·source·anchor·initial state·양의 weight·단위를 사용한다. 원 source와 START가 고정한 OFF CSV 및 helper identity와 현재 입력 identity의 일치를 읽었다. 비교에서는 아래 기준을 사용했다.

| Prior | Current | 같은 exact quantity |
|---|---|---|
| Pend | P1 true absolute interval | 절대 photon endpoint |
| DP | P1 true minus captured interval | Native photon 기준 보정 |
| Continuous minus frozen + frozen minus captured | True minus captured interval | 같은 captured segment 기준 보정 |
| Frozen + continuous minus frozen | True absolute interval | 절대 moment |
| Cumulative correction | Cumulative moment correction | 세 captured segment의 실수 합 기준 |
| Energy endpoint minus captured erg / epsilon | P1 energy eV native correction | Native energy stock 기준, 변환 한 번 |
| Weighted reduction | Positive weight × absolute path quantity | 같은 mode와 같은 node의 선택 기여 |

정확 frozen과 native captured를 혼동하지 않았다. Endpoint energy stock의 잔차는 photon discrepancy에 energy를 곱한 항과 별도의 native stock 표현 잔차를 포함한다. Prior의 interval incoming을 운반하는 gain 항에는 incoming uncertainty가 이미 들어 있으므로 또 더하지 않는다. Dedicated total heat와 종별 heat interval의 합도 동일한 enclosure endpoints라고 가정하지 않는다.

## 2. OFF700의 overlap guard 문제는 실제 저장 carry로 판정

원 cover의 `(Ia-oldIa).contains(0)`는 interval overlap만 검사한다. 일반적으로 이것만으로 원 pilot의 incoming 구간이 새 incoming을 모두 포함한다고 할 수 없다.

이 패키지에서는 원 pilot RESULTS와 cover RESULTS의 세 OFF700 record를 직접 읽어 다음을 확인했다.

1. 세 saved incoming interval의 양 endpoint가 pilot과 cover에서 정확히 같다.
2. 원 pilot incoming이 exact rational `previous Pend - captured f0`를 포함한다. 첫 segment는 exact 0이다.
3. 저장된 Pend payload가 그대로 재사용됐다. Contributor의 추가 원본 비교는 DP, gain, J, remainder, frozen, captured, corrected payload도 동일함을 확인했다.

따라서 이 특정 saved reuse의 입력 적합성은 확인됐다. Overlap-only guard를 일반적인 재사용 충분조건으로 채택한 것은 아니다. 전체 endpoint와 exact carry는 reviewer의 `EXACT_LINEAGE_RESULTS.json`에 남겼다.

## 3. 두 항의 교체와 mode별 exact 합

같은 모드에서 각 정확한 관측량이 해당 경로 interval에 포함되고 weight가 고정된 양수라면, weighted interval들의 endpoint 합은 그 선택 부분집합 관측량을 포함한다. 이번 OFF 합은 node 1620·2344의 선행 N128 항과 node 0·700의 새 N512 항을 **개별 항에서 직접 더한 합**이다.

기존 aggregate interval에서 old interval을 빼서 불확실성을 취소하지 않는다. Mode를 섞지 않는다. 나머지 열 path의 weighted term, captured segment moment, captured segment-to-node residual이 보존됐다. KF/GM의 published aggregate payload는 그대로다. 별도로 노출한 exact 재합 결과가 이 두 기존 aggregate 안에 들어가는 것은 bookkeeping 검증이며 새 물리 계산이 아니다.

OFF0·OFF700 각각의 두 step에는 native-node bridge를 남겼다. Moment에는 해당 step의 continuous-minus-segment 보정 합과 원래 segment-minus-node residual을 더한다. Photon과 energy stock은 endpoint residual을 사용하고, U_erg residual은 상속 binary64 epsilon의 정확한 값으로 **한 번** 나누어 eV로 바꾼다. 이 네 bridge는 전체 native weighted aggregate rounding의 인증이 아니다.

Reviewer의 별도 `exact_lineage_audit.py`는 candidate·reducer·interval helper를 import하지 않고 원시 저장 endpoints를 `Fraction`으로 처리했다. **199 checks PASS, 0 failure, actual exit 0**, wall 0.115650042초, child RSS 17,304 KiB였다. 새 coefficient·exp·native·gas·continuous solve는 0이다. 이 감사는 실제 carry, 두 새 weighted absolute term, 열 유지 term, mode 분리, OFF의 14개 직접 합, native bridge를 확인했다. 원 START·stdout·stderr·종료 기록을 모두 보존했다.

Lineage contributor의 최종 실제 run은 **1180 checks, 604 comparisons, disjoint 0**, exit 0, 0.266534940초다. N128/P60 진단 302개와 N512/P60 비교 302개를 구분한다. Source v2는 NCP용 raw projection-file hash와 identity 별칭만 추가했고 원 v1을 보존했다. 같은 검사의 반복을 새 distinct 검증으로 합산하지 않는다.

저장된 OFF의 14개 aggregate quantity는 모두 기존 OFF interval 안에 들어간다. 비교 가능한 모든 개별 diagnostic field가 nested라는 주장은 하지 않는다. 최종 보고서의 폭과 그림을 원 endpoints로 다시 대조한 결과는 다음과 같다.

| OFF 네 node의 quantity | Prior width / refined width |
|---|---:|
| Final photon | 9.405865484 |
| Absorbed count, species sum | 11.037777029 |
| Absorbed energy, species sum | 6.878872645 |
| Heat, species sum | 4.544328017 |
| True signed anchor sum | 12.119895320 |

이는 선택 부분집합의 deterministic enclosure 폭이다. 전체 spectrum, missing node contribution, 새로운 물리 효과 또는 통계적 정확도의 배수로 해석하지 않는다.

## 4. NCP continuation의 source·fresh-result 경계

최종 `code/ncp_continue.py` SHA는 `38957cb24f58b5d36dd4823ce7e642c708f0f4cae725ac2377d3f824b2b41626`이다. `CONTINUATION_LOCK.json` SHA는 `a1ccb4f352a7bd12d97419b09dc41bc2782332ae01c4a7b8173f3cdd3bcdbef7`이고, 잠긴 19개 파일의 실제 크기·SHA가 모두 맞았다.

새 wrapper는 변경 없는 inner runner로 N512/P60 두 경로를 한 번 계산한 뒤, fresh as-run source identity 및 전체 physics numerical projection의 bitwise parity를 확인한다. 그 fresh RESULTS 파일의 실제 SHA를 고정해 reducer에 전달하고 reducer의 `input_identities.current.sha256`과 다시 비교한다. 저장 baseline으로 fresh output을 대체하는 경로는 없다.

Reducer의 host-independent projection은 substantive N512 compatibility·incoming reuse·representation·모드별 term과 aggregate·control을 포함한다. Optional N128 진단, host/경로/시각과 raw fresh producer-file SHA는 제외하지만, raw fresh SHA와 physics parity는 outer wrapper에서 따로 확인한다. N128 진단을 생략한 실제 postprocessing 호출은 **774 checks, 302 comparisons**, exit 0이며 기준 projection 파일과 byte-identical이었다.

| Identity | 값 |
|---|---|
| Physics numerical projection | `f4d0f8c7e37e5c8a013ab133af748173f3ef1a8247f413f4798fdb3518c04a86` |
| Reduction projection 전체 파일, 419815 bytes | `f0681b18032e4de92db2a4d4c867d00895cf761bbdb5a57c571fba6e0e01bb69` |
| Reduction canonical object, 마지막 newline 제외 | `b8d73433d67370176c82f1526907c08e1f5098a741261e92de49c4545c1e0388` |

Physics 한 번은 네 local 신규 평가와 두 인증 local reuse, coefficient 4096회다. Linux CPython 3.12.x, serial scientific process/thread 1, MPI 없음, physics 180초/1 GiB와 후속 exact reduction 60초/1 GiB의 계약이다. 바깥 physics wrapper의 205초에는 intake와 종료 기록이 포함된다. 자동 retry·tolerance/N/P 변경·full first2 확장은 없다.

## 5. 실제 발견한 NCP 문제와 수정 검증

별도 경계 contributor는 과학 child와 payload를 명시적인 `NO_SCIENCE` mock으로 바꾸고 wrapper bytes를 그대로 실행했다. 최초 source `24daad3ca88bbb0d8aa64329376e4ab412cb2cf5a6adbc24feb09b44407db921`에서 11종 중 10종은 예상 동작이었다. **실행 중 CONTINUATION_LOCK.json metadata만 바꾸면 성공으로 남는 한 건**을 찾았다. 당시 마지막 검사는 처음 파싱한 lock만 사용해 실제 lock 파일 변경을 확인하지 않았다.

Owner가 최초 lock SHA를 고정하고 최종 성공 전에 실제 파일 SHA를 다시 비교하도록 수정했다. Reviewer는 전체 기존 소스와 이 작은 diff를 읽고, 변경 후 세 focused case의 실제 자료를 확인했다. Verify-only와 fresh-success mock은 exit 0, lock metadata 변이는 **exit 1, FAILED, `continuation lock metadata changed during run`**으로 거절됐다. 문제는 닫혔다. 최초 실패 source와 raw logs를 보존했다. 11종 전체를 수정 후 다시 실행한 것으로 기록하지 않는다.

별도로 실제 package의 최종 guard-fixed verify-only는 exit 0, 0.215406256초, `VERIFY_ONLY_READY`였고 physics/reduction 실행은 각각 0이다. Process-create transport failure 뒤 output 부재를 확인한 준비검사 재시도도 원 기록에 남아 있다. 모의 fixture의 ACTUALLY_EXECUTED/PASS 문자열이나 verify-only 준비 결과를 실제 NCP 물리 성공으로 세지 않는다. 이번 리뷰가 timeout/resource-exhaustion stress까지 검증한 것은 아니다.

## 6. 문서·그림·마감 범위

최종 `CONTINUATION_REPORT_KO.md` SHA `98efd02c7ed226d1a73d3401fc6121d09468bb5c4a10f84f6a5cd1daa73fc390`을 전체 읽었다. `PR19_REFINEMENT_WIDTHS.png`도 직접 보았다. 보고서 수치와 단위, dedicated heat와 species-sum heat의 구별, 계보·실행 횟수·보호 상태가 저장 증거에 맞는다. 그림의 normalized width·선택 네 OFF node·변경하지 않은 KF/GM 범위가 명확하고 글자 겹침이 없다. Contributor 보고서의 두 LaTeX 표시 오류는 원본을 남긴 후 표시만 수정했고, 수정된 식을 확인했다.

최종 handoff, README, NCP continuation 계약, DAG는 PR19 기준으로 이어진다. 현재 문서가 원 PLAN/REPORT의 계보 복구 전 PR17 intake와 E13C6 제안을 후속 순서에서 대체한다. 과거 실행 기록 자체는 보존됐다. NCP_READY 하나에 필요한 source·선행 결과·입력·리뷰·실행문을 넣는 전달 설계는 코드의 실제 입력 의존성과 맞는다. 실제 외부 저장 성공은 새 delivery/backup receipt를 읽어야 한다.

현재 scientific source, 고정 입력·결과·lock, 최종 continuation 보고서·그림·handoff의 이 snapshot을 판정한다. 마감 후 owner가 `state/RESEARCH_STATE.json`, `state/CLAIM_LEDGER.json`, `CLOSEOUT.json`, manifest, 실제 Git/backup/delivery receipt를 **실제 증거와 이 판정의 포인터로** 갱신하는 것은 허용한다. 이런 파일은 미리 읽은 science의 불변성을 뜻하는 잠금 대상과 구분한다. 새 과학 claim·수치·실행 계약·scope를 바꾸려면 해당 변경 범위의 추가 검토가 필요하다.

## 보존되는 제한과 다음 행동

`baseline_RCT=OFF`, actual atomic photon/heat/recoil `null`, physical/production `HOLD`, HE-F2/F09 `OPEN`, receiver adoption `SEPARATE`, legacy Gamma alias `3.543295 FAIL`, uniform full-path certificate `false`를 유지한다. Full first2는 `HOLD_RESOURCE_AUTHORIZATION`이다.

다음 연구는 `E13C5_SELECTED_SUBSET_BUDGET_AND_MISSING_NODE_COMPLEMENT_CONTRACT`다. 남아 있는 선택 부분집합의 수치 폭과 미포함 spectral node의 signed contribution을 구분해 계약·가정·자원 예산을 정한다. 이번 결과로 missing complement의 상계가 생기지 않는다. 자동 E13C6, 새 gas evolution, 전체 first2 실행 또는 production 승격을 승인하지 않는다. 준비된 NCP work unit의 실제 실행과 반환 판정은 이후 실제 호스트 증거에 따른다.
