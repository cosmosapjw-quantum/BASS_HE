# E13C5 선행 계보와 이번 refinement의 관계

## 현재 기준

이번 이어하기의 외부 기준은 BASS_HE **PR19**의 `e25039b3a53031ce37800cebefb51200aa5a63a2`다. PR17만 확인한 최초 intake는 더 진행된 별도 branch를 놓쳤다. Dropbox 복구 폴더의 publication receipt를 계기로 PR18과 PR19의 실제 head, 계약, 결과, 코드와 판정 기록을 읽고 관계를 바로잡았다. 원래 계산의 PLAN·실행 결과·최초 실패·리뷰는 보존한다.

| 단계 | 실제 확인한 commit | 완료 범위 |
|---|---|---|
| PR17 / E13C4 | `8fc3fb14dd33da10efa86c97c4beb9b0d12eeaad` | E13C4 전달 기준; scientific core는 `d1bb3ff33b7a448e3c08fc7b41467e2a7f94a146` |
| PR18 / OFF700 pilot | `48f648cd905cd8c232ae43abe97745ac6a96dec2` | OFF700 세 segment의 incoming·anchor pilot, source binding 및 출판 |
| PR19 / selected first2 cover | `e25039b3a53031ce37800cebefb51200aa5a63a2` | OFF/KF/GM × node 0/700/1620/2344, 12개 경로·36개 segment, N128/P60, 기록된 독립 PASS_SCOPED |

PR19의 당시 다음 노드 `scoped_publication`은 이후 publication receipt에서 완료되었다. 그 DAG에는 E13C6가 없다. `full_first2=HOLD_RESOURCE_AUTHORIZATION`도 남아 있다. 이 기록을 근거로 E13C6를 이미 지정된 다음 노드로 취급하거나 전체 first2를 완료로 올리지 않는다.

## 이번에 새로 수행한 범위

이번 네 번의 실행은 OFF node 0과 700의 세 segment씩에 대한 N32/N128/N512/P60 및 N32/P80 refinement다. 이전 12-path cover와 공통인 두 경로를 더 높은 분할수로 다룬 후속 계산으로 해석한다. 이번 계산을 최초 E13C5 실행으로 세지 않는다. 구현은 incoming 중심·반경을 나누어 전파하며, prior code는 incoming interval을 직접 전파한다. 같은 E13C4 coefficient·interval helper와 같은 captured gas를 공유한다는 의존성을 명시한다.

추가 노드 `HE_E13C5_PR19_REFINEMENT_RECONCILIATION01`은 공통 경로의 의미를 맞춰 정확 유리수로 대조하고, OFF 선택 부분집합의 양의 가중 합에 두 N512 경로를 적용한다. OFF의 나머지 두 경로와 KF/GM의 여덟 경로는 선행 결과를 유지한다. OFF, KF, GM은 서로 다른 gas history이므로 세 mode의 합산 결과도 각각 유지한다.

이 exact postprocessing은 새 coefficient 계산, 새로운 gas 진화, native 실행이나 전체 first2 계산을 요구하지 않는다. 구체적인 검산·판정 결과와 현재 다음 노드는 `CONTINUATION_REPORT_KO.md`, `INDEPENDENT_LINEAGE_REVIEW.json`, `NEXT_DAG.json`이 소유한다. 아직 생기지 않은 판정 파일의 존재를 이 문서 자체가 대신 보증하지 않는다.

## 과거 문서와 현재 실행문

`REPORT_KO.md`, `PLAN.json`, `INDEPENDENT_REVIEW.json`은 선행 계보를 복구하기 전 완료된 두-track 계산의 과학 기록이다. 원래 문서에서 PR17을 intake 기준으로 삼거나 E13C6 aggregate를 제안한 부분은 당시 문맥이다. 현재 실행 순서는 **이 addendum, CONTINUATION_REPORT_KO.md, NEXT_DAG.json, 새 NCP_LOCAL_CODEX_HANDOFF_KO.md**를 따른다. 교체한 초기 README·DAG·handoff·state 사본은 `evidence/pre_reconciliation/`에 보존했다.

## 증거와 한계

`inputs/pr19_lineage/first2/RESULTS.json`의 SHA-256은 `418dcac9280947abc227c69f9178c0163bbdb00fa34bff1f9e34ab9eea35ece4`, `cover.py`는 `aaae27a0d053d42ce6727593df676352697dd042486aa448d1e9104b16f979f6`이다. PR18 pilot과 결과도 선행 START가 고정한 SHA에 맞춰 복구했다. Git에서 읽은 코드·결과의 byte identity를 확인했으며, Dropbox receipt는 connector가 반환한 추출 텍스트로 보존했다. 이 텍스트 복사에 원격 raw-byte 동일성까지 주장하지 않는다.

PR19의 실행 기록은 한 번의 serial N128/P60 실행, exit 0, wall 34.60초, 최대 RSS 65,652 KiB다. Publication receipt의 `publication_solver_reruns=0`은 **출판하면서 다시 풀지 않았다는 뜻**이다. 앞선 과학 실행이 없었다는 뜻이 아니다. 읽은 증거만으로 선행 host를 NCP라고 단정하지 않는다. Recipient execution ACK 역시 별도·미관측 상태다.

출처: [PR18](https://github.com/cosmosapjw-quantum/BASS_HE/pull/18), [PR19](https://github.com/cosmosapjw-quantum/BASS_HE/pull/19), 그리고 이 패키지의 `evidence/lineage_intake/`와 `inputs/pr19_lineage/` 원문. 정확한 검색 범위와 반환 identity는 `RECONNAISSANCE.json`, `FETCH_METADATA_AND_IDENTITIES.json`, `OPEN_PR_INVENTORY.json`에 기록했다.
