# HE27 source-cut native 연구

HE25 PR72 eb4952af와 HE26 PR73 98b31fbd를 불변 기준으로 사용한다. 새 source injection만 opt-in 구현하며 기존 HE25 physics/transport/reference, HE23 per-total-H density 및 원본 Rust f7830e2f를 변경하지 않는다. fixed-K 노드의 신규 photon counts만 구성하고, 이미 태어난 광자는 remap하지 않는다.

## 이론·실행 범위

HE26의 양의 true child N/U/세 종 sigma/heat를 각 방향과 같은 활성 threshold band의 고정 노드에 양의 cubature로 투사한다. source law H*dN/dln(a), BB50000K, source total, 실제 birth proper time, physical binding과 fit cutoff 구분을 유지한다. 개별 child spectrum은 투사 후 보존되지 않으므로 순간8모멘트 일치는 미래흡수 정확도를 뜻하지 않는다. C5 source gate108/108, 새 테스트14/14 통과한 원본 투사470ab942는 native n16 pilot을 통과했으나 adaptive reference가 source 시간 잡음으로 정체했다. 첫 raw/실패 기록을 보존하고 새로운 opt-in conditioning 경로를 연구 중이다. DAG_STATUS.json을 실제 stage 판정 기준으로 사용한다.

## 소유권과 판정

Rust igm_point_rhs가 CI/RR/DR/thermal/Case-A escape/CMB를 소유한다. 외부 HE25가 photon redshift/shear와 gas2Hu work를 각각 한 번 계산한다. 모든 photon/event/energy는 total-H 기준이다. density1e-9, point event2e-10, microledger2e-9, total number3e-15/H, total energy3e-12eV/H, Newton3e-15 계약을 유지한다. 실제 차가운8K native 상태에서 DR/일부CI가0인 것은 소유권 부재가 아니다. upstream Grackle 라이브러리를 직접 실행했다는 주장은 하지 않는다.

시간·source-time 보간·각도·에너지 오차를 각각 검증해야 한다. 완전한 EoR, 관측 Bianchi와 CMB는 HOLD다. 원래 manufactured shell GL32 오차는 실제 stellar spectrum 또는 EoR 관측 오차가 아니다.

## 재실행

기존 환경 /root/HE25_NCP_BIRTH_20261016/venv와 SHA22d11447 원본 rlib 기반 서버를 사용한다. analysis/run_native.py는 새 디렉터리만 생성한다. source gate는 analysis/source_acceptance.py, 전체 새 테스트는 tests/, 실제 native 원본은 results/에 보존한다. 첫 정체한 reference는 결과가 아닌 first_reference_failure/로 구분한다. source_manifest, commands, backup receipts와 최종 결과를 함께 사용한다.
