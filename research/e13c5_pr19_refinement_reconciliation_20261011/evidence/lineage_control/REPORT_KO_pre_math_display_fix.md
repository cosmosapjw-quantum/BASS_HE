# E13C5 PR19 lineage 연결과 N512 부분집합 reduction

## 결과

**`HE_E13C5_PR19_REFINEMENT_RECONCILIATION01`의 독립 산술 작업은 `PASS_SCOPED_POSTPROCESSING`이다.** 기존 PR19의 N128/P60 12-path 결과와 이번 두 OFF path의 결과를 같은 기준으로 연결하고, OFF0·OFF700만 N512로 교체한 새 selected-subset enclosure를 계산했다. 물리 solver나 coefficient 평가를 다시 실행하지 않았다.

기존 PR19 `e25039b3a53031ce37800cebefb51200aa5a63a2`에는 이미 OFF/KF/GM × node 0/700/1620/2344의 12개 path, 36개 segment가 존재한다. 이번 두 OFF path 계산은 **기존 E13C5의 refinement**다. 기존 연구가 없었던 것으로 다시 시작한 결과로 서술하면 안 된다.

Full diagnostic run에서 1,180개 체크가 통과했고, 비교 가능한 같은 양의 interval 비교는 N128 302개 + N512 302개 = 604개였다. **서로 만나지 않는 interval은 0개**다. N512 비교 302개 중 prior가 current를 포함한 것은 288개, current가 prior를 포함한 것은 147개다. 양쪽 포함에 해당하는 exact-zero 또는 동일 interval은 두 집계에 모두 들어간다. 비교는 overlap, 양쪽 containment, exact width ratio를 각각 보존한다. 단순 overlap을 더 높은 정밀도의 독립 증명으로 바꾸지 않았다.

최종 reviewer는 별도 담당자다. 이 문서는 schema·baseline 연결과 exact reduction의 독립 산술 기여이며, 최종 scientific admission이나 promotion 판정이 아니다.

## 기준을 일치시킨 비교

Prior와 current는 같은 C4 coefficient/interval helper를 사용한다. 두 helper hash와 OFF SEGMENTS/STAGES의 원본 hash, 선택 key, source/mask/anchor 상태, 양의 캡처 weight를 연결했다. Prior의 `cover.py`, 계약, 보고서, review, START와 원 pilot RESULTS를 실제로 읽고 결과 구조를 확인했다. `cover.py`와 physical candidate 코드를 실행하거나 import하지 않았다.

| Prior quantity | Current quantity | 비교 기준 |
|---|---|---|
| `Pend` | `P1.true_absolute_interval` | 절대 photon |
| `DP` | `P1.true_minus_captured_interval` | continuous−captured photon |
| `continuous_minus_frozen + frozen_minus_captured` | 관측량의 `true_minus_captured_interval` | 같은 captured segment 기준 보정 |
| `frozen + continuous_minus_frozen` | 관측량의 `true_absolute_interval` | 절대 moment |
| `cumulative_correction` | 누적 correction interval | 세 segment의 captured moment 정확한 실수 합 기준 |
| `energy_endpoint_minus_captured_erg / epsilon` | `P1_energy_eV.true_minus_captured_interval` | 같은 native energy stock 기준, eV |
| `weighted_reduction` | positive captured weight × 새 절대값 | 같은 selected path의 weighted observable |

`epsilon`은 상속된 binary64 `1.602176634e−12`의 정확한 값이다. Ergs를 eV로 바꾸는 나눗셈은 `Fraction`으로 정확히 수행하며 중복 적용하지 않는다. Prior의 continuous-minus-frozen을 current의 continuous-minus-captured와 곧바로 비교하지 않았다. Node reduction도 이 차이와 구분했다.

N128 비교는 동일 해상도에서 두 표현·전파 방식의 호환성을 확인하는 진단이다. N512 비교는 교체할 새 enclosure와 prior의 호환성을 확인한다. 기존 출력에 대한 reference solver 또는 새로운 physical tolerance는 사용하지 않았다.

## OFF700 재사용 입력 검증

기존 cover의 `(Ia−oldIa).contains(0)`는 overlap만 보장한다. 이를 original pilot 입력의 충분한 enclosure로 간주하지 않고, 실제 원본 pilot RESULTS SHA-256 `75648e29291c3c364c2d8a0c859710d95074f1c12c5d910c61a4856465034b96`를 별도로 읽었다.

세 재사용 segment 모두에서 다음을 실제 exact Fraction 비교로 확인했다.

1. Cover에 저장된 Ia와 원 pilot Ia의 양 endpoint가 정확히 같다.
2. 원 pilot Ia가 `previous Pend−captured f0`의 exact rational interval을 포함한다. 첫 segment는 정확한 0이다.
3. Pend endpoints와 DP, g, J, remainder, frozen, captured 및 corrected payload가 원 pilot record와 같다.

따라서 이번 실제 저장 데이터의 재사용 입력은 원래 overlap guard만으로 추정하지 않았다. 이 확인은 동일 bytes의 재사용과 입력 interval 관계를 입증하며, 그 원 coefficient 모형의 별도 검증을 뜻하지 않는다.

## Hybrid reduction의 정의

각 mode는 서로 다른 고정 gas history이므로 세 mode aggregate를 따로 유지한다. 모든 12개 path를 한 물리적 합으로 더하지 않는다.

[
I^{
m hybrid}_{m,X}=sum_{nin{0,700,1620,2344}}omega_{m,n}I_{m,n,X},qquad omega_{m,n}>0.
]

여기서 OFF의 node0·700 interval만 이번 N512 결과를 사용한다. OFF1620·2344와 KF/GM의 여덟 path는 prior N128 path term을 그대로 사용한다. 같은 모드에서 네 node의 positive-weight interval을 정확한 유리수로 다시 합했다. 기존 aggregate interval에서 old interval을 빼고 new interval을 넣는 방식은 사용하지 않았다. 그 연산은 같은 불확실성을 제거하지 못하고 불필요한 폭을 만들 수 있다.

결과는 `hybrid.path_terms`에 12개 항을 모두 보존한다. 각 항에는 weight, 어느 입력을 사용했는지, weighted reduction, 기존 captured segment moments와 captured segment-to-node residual이 들어 있다. `exact_fraction_term_sums_by_mode`는 실제 exact sum이며, `selected_subset_weighted_reductions`는 OFF의 새 sum과 **그대로 보존한** KF/GM의 기존 published interval이다. KF/GM published interval이 그대로인 동안 exact 재합 결과가 그 안에 들어가는 것도 확인했다.

Captured node의 native reduction은 따로 남긴다. OFF0/700의 두 step 각각에 대해

[
Delta X_{
m continuous-node}in
sum_{	ext{step segments}}Delta X_{
m continuous-segment}
+igl(X_{
m captured,segments}-X_{
m captured,node}igr)
]

를 계산했다. Endpoint photon은 기존 P residual, endpoint energy는 기존 U_erg residual을 정확히 eV로 바꾸어 더한다. 새 node 기준 보정은 `hybrid.captured_node_bridges` 네 항에 기록했다. 이 식은 같은 캡처 node와 segment의 연결이며, native full aggregate reduction 또는 다른 gas path를 새로 인증하지 않는다.

## 수치적으로 달라진 폭

다음 비율은 `prior interval 전체 폭 / 새 interval 전체 폭`이며, acceptance tolerance나 물리 효과의 크기가 아니다. 모든 판단은 전체 exact endpoints를 사용했다. 표의 비율만 표시용으로 반올림했다.

| 대상 | prior/new 폭 비율 |
|---|---:|
| OFF0 final photon | 13.1901324 |
| OFF700 final photon | 14.6233621 |
| OFF0 세 segment total-heat native correction | 21.4009023 |
| OFF700 세 segment total-heat native correction | 14.7289928 |
| OFF 네 node selected-subset final photon | 9.4058655 |
| OFF selected-subset count의 종별 합 | 11.0377770 |
| OFF selected-subset absorbed energy의 종별 합 | 6.8788726 |
| OFF selected-subset heat의 종별 합 | 4.5443280 |
| OFF selected-subset true anchor 합 | 12.1198953 |

OFF selected-subset total heat의 전체 interval 폭은 약 `5.31211137771e−22`에서 `1.16895421230e−22` eV로 줄었다. 결과의 exact endpoints는 JSON에 있다. 교체하지 않은 두 OFF node도 합에 남으므로 두 개선 path의 폭 비율과 전체 subset의 폭 비율이 같을 이유는 없다. KF/GM의 published aggregate와 그 종별 합은 이번 교체로 바뀌지 않았다.

OFF hybrid의 모든 저장 aggregate quantity가 기존 OFF aggregate interval 안에 들어갔다. 이는 여기서 계산한 exact 합에 대한 사실이다. 모든 후속 refinement에서 containment가 자동 성립한다는 일반 주장으로 확대하지 않는다.

## Exact controls와 실제 실행

8개 synthetic exact controls는 서로 다른 positive weight와 node value를 사용한다. Weighted OFF=19를 기준으로 weight 누락, node 교환, 서로 다른 mode의 혼합을 거부했다. Frozen=10, captured=12, continuous-minus-frozen=3인 예에서는 native correction=1, true absolute=13이 되며 기준을 혼동해 native+3을 쓰면 15가 되어 실패한다. Direct replacement sum과 old-aggregate minus old-interval plus new-interval의 폭 차이도 exact rational로 확인했다.

최종 scientific postprocessing source는 `lineage_reduction.py`, SHA-256 `dd8796ae232d3d72384df14263658d1e48e87a8fad6982f64a6ab811ce2eb985`, 28,050 bytes다. Standard-library Fraction만으로 endpoints, 비교, weight product와 누적합을 계산했다. 새 coefficient/native/gas/continuous solve는 0회다.

`run_v2`의 실제 exit는 0, wall time은 0.266534940초, CPython은 3.12.14다. 최초 `run_v1`도 성공했으며 v2는 NCP wrapper가 쉽게 읽도록 exact projection-file byte hash와 `input_identities` 별칭을 추가한 interface 변경만 포함한다. 물리 내용·baseline·acceptance를 바꾸지 않았다. 실패는 없고, 같은 체크의 재실행을 새 distinct check로 세지 않았다. 원 run/source/results를 보존했다.

## NCP 실행 연결

CLI는 이전 절대 archive 위치를 사용하지 않는다. 포함된 파일을 지정하고, fresh producer의 N512 결과를 `--current`로 전달한다.

```text
python3 lineage_reduction.py \
  --prior <prior_first2/RESULTS.json> \
  --prior-start <prior_first2/START.json> \
  --pilot <prior_pilot/RESULTS.json> \
  --current <fresh_N512_RESULTS.json> \
  --controls <PATH_CONTROLS.json> \
  --out <fresh_output_directory>
```

`cover.py`는 기본적으로 prior RESULTS와 같은 디렉터리에서 identity 확인만 한다. 위치가 다르면 `--prior-code`를 사용한다. N128 진단을 포함하려면 `--diagnostic <N128_RESULTS.json>`를 지정한다. NCP에서는 진단 없이 실행해도 된다.

출력 `RESULTS.json`은 `status`, `failed_count`, `input_identities.current.sha256`와 모든 과학적 결과를 포함한다. 실패 체크가 있으면 process exit가 1이고, 호환성 gate 실패 시 hybrid는 계산하지 않는다. `NUMERICAL_PROJECTION.json`은 N512 compatibility·representation·original reuse·hybrid와 체크 전체를 포함하며 host/경로/시각/raw fresh-file hash와 선택적인 N128 진단은 제외한다. Fresh producer의 identity와 scientific parity는 바깥 NCP runner가 별도로 확인해야 한다.

검토 기준 projection은 `output_v2/NUMERICAL_PROJECTION.json`이다. **파일 bytes 자체의 SHA-256**은 `f0681b18032e4de92db2a4d4c867d00895cf761bbdb5a57c571fba6e0e01bb69`, 크기는 419,815 bytes다. `NUMERICAL_IDENTITY.json.sha256`이 이 hash다. 별도 `numerical_projection_sha256`은 마지막 newline을 제외한 canonical object hash로 두 hash의 정의가 다르다.

N128 진단을 생략한 실제 CLI 호출도 수행했다. Exit0, 0.215819080초였고, projection 파일이 진단을 포함한 기준 파일과 byte-identical이었다. 이 호출은 같은 저장 N512 입력을 재처리한 protocol 확인이며 실제 NCP physical execution은 아니다. NCP-form 결과는 774 checks, 302 comparisons이고, 추가한 진단까지 포함한 chat 결과는 1,180 checks, 604 comparisons다.

## 보존하는 한계

근거는 직접 유도한 baseline 연결과 실제 exact arithmetic postprocessing이다. Prior와 current가 같은 C4 coefficient와 interval helper를 공유하므로 둘의 일치를 독립 physical-model validation으로 쓰지 않는다. 결과는 constituent certificate의 유효성에 조건부인 selected-subset enclosure다. Full first2, 새 gas evolution, 실제 atomic photon/heat/recoil, physical/production admission, receiver adoption과 자동 E13C6 진행은 열지 않는다.
