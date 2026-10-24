# HE-ANG-TDCS54-ANCHORS 과학 인계 — C10 실제 전달 대기

Root PASS_SCOPED, 독립 R6 PASS, C9 PASS_AFTER_FIGURE_CORRECTION이다.
R1–R10/C1–C9의19단계를 확보했고 C10은 실제 publication/delivery 대기다.
Science S, 새 PR, delivery D와 central C/E는 아직 실제 SHA/receipt가 없으므로
이 파일에 미래 identity를 만들어 넣지 않는다.

## 기준과 source

Baseline은 BASS_HE `2cb9f9176c2a1764bb8ceaf2392531a100eb6820`이며 새 경로는
`research/he_ang_tdcs54_anchors_20261024/`다. Target branch는
`research/he-ang-tdcs54-anchors-20261024`, PR base는
`research/he-ang-ccc-exchange-20261024`다. No merge/activation을 유지한다.

Jones–Madison, PRA62,042701(2000), DOI10.1103/PhysRevA.62.042701의
Table IV 및 article p8/Fig.10에서 두 located H1s TDCS 점을 확보했다.
입사54.4eV, slow5eV, slow210도 CW, fast4/10도 CCW다. Source atomic units에서
(CDW-EIS,CCC99,experiment)는 fast4에서(1.83,2.58,1.52), fast10에서
(0.99,1.51,1.24)다. 전체8개 peak-height 특징량의24개 source cell과16개
printed ratio를 보존하지만, 위치가 알려진 점은 두 개뿐이다.

원전의 무한 핵질량, CDW의 exchange neglect, CCC99의 unpublished Bray
제공 provenance와 재수록 실험값의 한계를 유지한다. Already-reported TDCS에
spin/count/equal-sharing 인자를 추가하지 않는다. Fast energy를 평가하거나
unknown peak angle을 만들지 않으며, full joint law를 보간·적분하지 않는다.

## 확보한 exact 진단

공통 scale는 model=A*u*experiment의 방향이다. Fraction 계산으로 공통
scale의 필요충분 교집합과 witness, 자유/clipped minimax, scale-free pair
contrast와 조건부 printing compatibility를 구현했다.

- Located CDW: Q=1891/1254, A*=9435/9424, delta*=637/3145.
- Located CCC99: Q=3999/2869, A*=1717/1178, delta*=565/3434.
- A∈[13/20,27/20]의 CCC99: Ac=27/20, q(Ac)=44/171.
- All-feature CDW delta*=1593/5849, 약27.235425%. Source summary26%와
  정확히 같게 만들지 않고 둘을 보존했다.
- δ=.10에서 두 producer의 located common-scale 집합은 absolute scale
  상자를 씌우기 전에도 공집합이다. 지정한 결정론적 모형의 비교 결과이며
  통계적 기각이나 보정 factor 제안이 아니다.
- Source signs로 계산한 작은 전자 사이각은146/140도이고 slow polar150도다.
- 별도 nearest0.01 printing model에서16개 ratio control이 compatible이다.

실제 analysis JSON의 당시 status는 PENDING_C9로 보존한다. 현재 최종
과학 수용은 `CLAIM_GATE.json`, `SCIENCE_DECISION_KO.md`, `reviews/C9_REPORT.json`
으로 연결한다. 과거 raw status를 최종 판정으로 덮어쓰지 않는다.

## 실제 검증·비용·교정

14개 test method와 source analysis가 PASS했다. 계획된 tests/analysis/plot
세 child 뒤 독립 C9가 유일하게 발견한 C9-FIG-01은 annotation이 marker를
가리는 표시 문제다. 원래 code/runner/PNG/SVG를 보존하고 x=.03→.40 한 줄만
바꾸어 plot-only reserve를 한 번 실행했다. 새 그림을 실제 열어 확인했고
독립 C9가 닫았다. Tests/analysis/core/source는 변경하거나 재실행하지 않았다.

4개 child와 runner 구간의 측정 누적은 CPU1.887889초,
wall1.9431963300012285초, reserve1회다. 새 CPU8/wall30 안의 측정 구간이지만
host orchestration/일부 준비·문서 I/O/remote 전체 CPU는 UNKNOWN_NOT_ZERO라
end_to_end_cpu_cap_established=false다. 실패·측정 overshoot·old suite replay·
new IVP·provider solve는0이다. 이전 allowance, 실패와 unknown은 그대로다.

재현 command와 정확한 argv는 README와 immutable START/FINISH에 있다.
이것은 완료 과학의 자동 replay 승인이 아니다. Recovery는 저장 결과를 쓴다.
Wolfram evaluator1/context1을 구별하며 unused context documentation은 public
Git에서 제외한다. SHA/bytes와 B1 receipt reference를 남기고 원본 및 실제
B1 archive는 유지한다. Evaluator R7_CODE/R7_RAW/ASSESSMENT는 그대로다.
SciSpace query와10개 citation metadata만 연결하고 abstract/fulltext는 제외했다.

## 실제 backup과 다음 전달

B1 archive는178668 bytes/54members, SHA256
`5c166c53609fd1c8b6b0af6059ea3e205bd50e5a69de613d845bec3b98d7cdcd`다.
Drive `10bExiGPtKflSI2cJy2vb06d5eaYhN2T3`, Dropbox
`id:BSpOijBcT10AAAAAAD_9RQ`의 실제 완료 ACK와 metadata size readback 뒤
root GO로 실행했다. B1은 재생성하지 않았다. 실제 receipt는
`delivery/B1_BACKUP_ACK.json`이다. S/C 뒤 B2, D/E 뒤 B3는 미래 실제 ACK로
기록한다. 현재 C10 pending을 최종20/20 완료로 선취하지 않는다.

## 다음 물리 입력

HE-ANG-SOURCE-PAYLOAD와 부모 HE-ANG은 SOURCE_INPUT_PENDING이다.
Physical provider/full joint law/event sigma/ion recoil law는 admit하지 않았다.
새 sparse points는 미래 source의 located control로 쓸 수 있지만 full support,
spin/amplitude/count/exchange/frame/recoil와 calibrated uncertainty를 대체하지 않는다.
C9-NB-01, C23E, 다른 owner의 scoped 결과·OPEN·historical reservation과 이전
HE-X1/HE38/contract/Hex/DDCS20/CCC 비용·실패·unknown을 보존한다.
