# BASS_HE CODE-I02 focused independent rereview handoff

이 문서는 별도 독립 reviewer 또는 Work thread에서 사용한다. 이전 대화 없이 시작하고, 이 문서를 작성한 연구 스레드나 구현자/실행자의 판단을 독립 판정으로 재사용하지 않는다.

## 1. Exact target

Repository: cosmosapjw-quantum/BASS_HE

Review PR: #15, DR11H: bind pair-membership certificate to endpoint identity

Exact implementation head:
af3ed44ce3cc1023aa8a1370ab2981aa76760869

Canonical durable-record tree expected:
6fecfde27385d788a7891c4c5022b633eba74b83

Base:
ac09160bae74f051e5e2e17d8a1cde4084576c16

Changed files only:
- src/bass_he/spectral.py
- src/bass_he/sturm_geometry.py
- tests/test_dr11h_certificate_binding.py

Supporting runtime evidence, not independent decision evidence:
PR #16 head 2c3812e390b91b89da1de30988b3933646b79f30
evidence/cloud/ncp-c64g3/20260928/resume-004/RUN_RETURN.json
execution commit/tree:
6ddc4ff821ab5d1397fbd08493dd3954a89750f1
e80a9218d9d275546132110605da35160a878bb0

검토 전에 모든 ref를 fresh-read한다. PR #15 head가 달라졌으면 guessed revision을 검토하지 말고 중지 후 reconcile한다.

## 2. Original finding

CODE-I02의 원래 문제는 valid pair-membership certificate가 endpoint dict identity에 묶이지 않았다는 것이다. 따라서 certificate를 복사한 뒤 state_b, R, p, lambda, depth, Z1, Z2 등의 endpoint field를 바꾸어도 downstream geometry가 stale membership evidence를 소비할 수 있었다.

수정본은 policy FINITE_CF_ADVERTISED_ORDINAL_PAIR_MEMBERSHIP_V2, canonical float/complex hex identity, canonical JSON SHA256 binding, 그리고 contour geometry 시작 전 validate_pair_membership_certificate(ep)를 도입한다.

판정 범위를 Eq.(55), physical probability, Nmax convergence, continuum ionization, common-contour optimization으로 넓히지 않는다.

## 3. Required review questions

A. Binding coverage

현재 geometry가 사용하는 endpoint identity가 실제로 다음 모두에 bind되는지 코드로 확인한다.
- state_a
- state_b
- R
- p
- lambda
- CF depth
- Z1, Z2
- membership tolerance
- probe scale
- policy id

B. Call order

sturm_geometry.contour_geometry()의 call order를 추적하여 stale certificate가 spectral/geometry continuation 전에 fail closed 되는지 확인한다.

C. Missing attack cases

기존 focused tests는 state_b, R, p, lambda, depth, Z1, Z2 및 stale policy를 다룬다. 독립 검토에서는 최소한 다음을 추가하거나 동등하게 직접 검증한다.
- state_a mutation
- tolerance-only mutation
- probe_scale-only mutation
- malformed 또는 missing binding hash
- malformed permutation

테스트 부재 자체를 실패 증거로 취급하지 않는다. 구현을 먼저 읽고, 빠진 high-value case를 실제로 공격한다.

D. Binding versus authenticity

현재 SHA256은 unkeyed self-consistency checksum이다. certificate payload와 current endpoint의 canonical consistency를 확인하지만, 그 payload가 membership solver에서 생성되었다는 provenance authenticity를 증명하지 않는다.

따라서 CODE-I02 intended claim이 stale-copy prevention인지, 아니면 jointly fabricated endpoint + certificate + recomputed hash까지 막아야 하는지 명시적으로 판정한다. 전자가 scope라면 그 claim ceiling을 적고, 후자를 암묵적으로 주장했다면 gap을 finding으로 분류한다.

E. Diagnostic fields

probe_radius, probe_R, scaled_distance_matrix, sum_scaled_matching_error, local_sheet_gap 등 일부 diagnostic field는 모두 재-bind/revalidate되지 않는다. downstream path가 이 값에 의존하는지 추적한다. 의존하지 않으면 명시하고, 의존한다면 영향과 severity를 분류한다.

F. Intact geometry

PR #16 resume-004는 cross-platform supporting evidence로만 사용한다. 해당 기록은 stale negative cases 7개가 geometry 전에 거절되었고, normal certificate PASS, endpoints 7, geometry actions 56, independent 32/64 pairs 28, full tests 216 PASS, imported evidence 0을 보고한다.

resume-004나 15-arm worker sweep는 반복하지 않는다. 독립 판정에 필요한 focused attack tests만 새로 실행한다.

## 4. Decision contract

다음을 분리해서 반환한다.

- Critical findings: integer + details
- Important findings: integer + details
- Minor or claim-scope notes: details
- CODE_I02_CLOSED: true/false
- stale_certificate_reuse_blocked: true/false
- intact_7_branch_geometry_supported: true/false
- PROMOTE: PASS/HOLD
- Eq55_next_node_authorized: true/false

Eq55 next node는 아래가 모두 참일 때만 authorize한다.
- Critical findings = 0
- Important findings = 0
- PROMOTE = PASS
- Eq55_next_node_authorized = true

finding이 physics assumption, numerical tolerance, certificate policy, 또는 structural redesign을 요구하면 evidence를 보존하고 연구 스레드로 반환한다. 독립 검토 context 안에서 substantive redesign을 구현하지 않는다.

## 5. Claim ceiling

PASS가 나오더라도 닫히는 것은 CODE-I02 independent rereview gate뿐이다. 다음은 별도 OPEN 또는 NOT_RUN 상태다.
- Eq.(52)/(55) exponent convention
- physical P_rot
- new production Eq.(50)/(54)
- Nmax convergence
- continuum ionization
- common-contour lifted homotopy
