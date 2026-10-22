# HE35 유한질량 탄성 pair 압력 교환

두 종의 운동량·열·비등방 압력 교환을 같은 충돌 법칙에서 유도하고 Python/C99로 구현했다. 정의한 등방 pseudo-Maxwell kernel `g dσ/dΩ=κ/(4π)`에서는 첫째·둘째 충돌 모멘트가 정확히 닫힌다. κ는 호출자가 공급하는 m³/s 단위 모델 입력이며 실제 H/He 수송자료를 채택한 값은 없다.

공통 bulk에서 평균압은 `pA'=-2abκ(nB pA−nA pB)`, `pB'=-pA'`이고 각 STF 성분은 THEORY.md 식(4)의2×2 행렬을 따른다. 임의 상대 bulk에는 운동량 교환과 drift heating을 포함한다. 총 운동량과 raw kinetic energy는 보존되며, 동등 온도의 등방 상태는 평형이다. 밀도 역수 가중 STF 이차형은 감소하고, 공통-bulk PSD 압력 cone은 연속시간에 보존된다. 동일 질량/밀도에서 두 relaxation rate는 nκ/2와 nκ이며 heavy stationary-target 극한은 HE34의 nBκ로 연결된다.

독립 각도 oracle은 실제 incoming/outgoing 속도쌍을 구성하여6축 방향의 정확한 이차 angular 평균으로 확인했다. 최초 test의 trace와 half-trace heating 혼동은 원실패를 보존하고 교정했다. 수정된100검사가 최대 정규화 차이1.8670464648487782e−15로5e−13 기준을 통과했다(1.8963s). 이후 정확한 κ=0 branch만 별도 검사했고, C shared-library 이름이 Python import를 가리던 오류도 보존·수정했다.

Fresh 독립 검토는 `b=1−a`의 극단 질량비 cancellation을 발견했다. ma/mb=1e20에서 지워진 작은 질량분율 때문에 잘못된 힘과 에너지 residual이 발생했다. 두 질량분율을 각각 scale하여 계산하고 nonfinite source를 명시 거부하도록 교정했다. 해당 회귀만27.4370s에 수행해 forceA=(-1,0,0), raw trace residual−2.220446049250313e−16, 정규화 에너지 residual1.1102230246251565e−16을 얻었다. 독립 검토 판정은 `PASS_SCOPED_AFTER_CONCRETE_REPAIR`다. 전체100검사의 이전 source pin과 뒤따른 delta 검사의 최종 pin을 별도로 유지하며, 최종 source로100검사 전체를 다시 실행했다고 주장하지 않는다.

새 cosmological IVP0, 과거 cohort 재실행0, NCP0이다. 최초 probe0.6920s, 성공한 baseline1.8963s, zero-κ probe0.2213s, mass-ratio delta27.4370s는 각 receipt에 있다. 초기 import-shadow 실패와 reviewer counterexample의 wall 측정은 별도 완전 계측되지 않았으므로 전체 cumulative wall 값은 확정하지 않는다. 최초30s process 계약은 충족했고, 실행 범위를 새 cohort로 확장하지 않았다.

R1–R3/C1–C2는 HE33/34 convention과 최신 owner contracts를 재사용했다. R4–R5/R9와 C3–C4는 THEORY.md 및 CONTRACT.json의 정확한 event 유도·행렬·정의역·수용기준이다. R6–R8/C5–C9는 code, oracle, 보존/극한 checks, 실제 실패 및 delta 교정, FRESH_INDEPENDENT_REVIEW.json이다. R10/C10은 이 scoped 보고서와 root가 기록하는 실제 publication/backup acknowledgment로 연결한다. 새 strong no-go 주장은 없다.

`READINESS_N2_N5.md`는 REC124의 완료8개 Compton 경로, CR의 별도 완료 CCC H1 n2 finite-core4개 경로, HH136에서 아직 열린 D PI/RR source moments와 HE88 별도 진행 상태를 갱신한다. 이번 HE35는 finite-mass analytic component로 완료되며, 실측/계산된 differential transport 입력, reactive B2, physical B3 closure 및 Einstein feedback은 다음 물리 의무로 남는다.

재개 시 THEORY.md, CONTRACT.json, IMPLEMENTATION.md, FRESH_INDEPENDENT_REVIEW.json을 읽고 final source hash를 확인한다. pair.py는 full drifting tensor source, pair.c/pair.h는 common-bulk thermal/STF 행렬과 안정적인 eigenvalue 계산이다. 모든 실제 실패와 수정 전 source는 additive evidence로 보존된다. standalone kernel은 intake 파일을 runtime import하지 않는다.
