# E13C5 독립 recurrence 산술 검산

## 판정과 검산 범위

**`PASS_SCOPED_ARITHMETIC`**. 독립 exact toy 76개와 저장된 N512/P60 결과의 검산 3,867개가 실제 실행에서 통과했다. 저장 결과 검산 중 1,626개는 interval endpoint 순서 확인, 2,241개는 incoming·계수·representation·anchor·누적·ledger 산술 확인이다. 이를 합치면 서로 다른 성공 TestID는 3,943개이며, endpoint 순서 확인을 제외하면 2,317개다. 실패한 첫 시도 또는 같은 control의 재실행을 추가 성공 항목으로 세지 않았다.

담당자는 `/root/e13c5_recurrence_control`이다. 이 산출물은 독립 산술 기여이며 최종 decision review가 아니다. Production 모듈을 import하지 않은 별도 `Fraction` interval 연산으로 저장 Decimal 문자열을 정확한 유리수로 읽었다. Production `path_enclosure.py`의 앞부분은 output schema와 정의를 확인하기 위해 읽었다. 검산 대상 local coefficient·first variation integral·remainder interval과 원래 캡처 입력은 공유한다. 따라서 이 검산은 그 저장 interval들이 주장한 local 함수를 감싼다는 조건에서 recurrence의 산술 및 연결을 확인한다. Local coefficient enclosure, 원자 모형, gas history 또는 정확한 continuous reference를 새로 증명한 것은 아니다.

새 coefficient 평가, native 계산, gas advance, continuous solver 실행은 모두 0회다. 저장 continuous reference 값이나 order gap을 정확한 해의 보증으로 사용하지 않았다.

## 실제 실행 기록

| 실행 | 실제 결과 | 시간 | 주요 source SHA-256 |
|---|---|---:|---|
| `toy_run_v2` | exit 0, 76 PASS | 0.064800257 s | `bba710d94b751a78dde186956ca668a95a4219d5ed0ee73bcbe652b4334590ec` |
| `saved_audit_run_v2` | exit 0, 3,867 PASS | 0.164411482 s | `93924165bc95a484ad4a6cd520d6264d180f8ccf86c7c04fec0105ef2c811ca9` |

실행 runtime은 CPython 3.12.14다. 각 run의 `START.json`, `FINISH.json`, 실제 argv, timeout, source identity, stdout/stderr와 process exit를 보존했다. 시간은 단일 host의 실제 wall time이며 다른 방법이나 실행 환경과의 성능 비교가 아니다.

검산한 N512/P60 결과는 417,016 bytes, SHA-256 `5a3b9f17c6d250afed0e4270e4cce71d22d930a482084bc12c3e7dcc66cb68d7`이다. 입력 `PATH_CONTROLS.json`은 24,911 bytes, SHA-256 `41891a30f61976d2c19165ee48a077bccbd41b17011939e1ed4dd80eb49cfd63`이다.

재현 명령은 각 `FINISH.json`에 절대 경로로 기록했다. 새 경로에서 재현할 때는 `audit_saved_path.py --results <N512_P60.json> --inputs <PATH_CONTROLS.json> --out <fresh-json>` 또는 `exact_recurrence_toys.py --out <fresh-json>`를 사용한다. 결과 경로는 이미 존재하면 거부한다. 재현 실행도 별도 결과로 보존하고 원 결과를 덮어쓰지 않는다.

## 직접 확인한 물리·산술 관계

### Incoming center와 uncertainty

기존 local0 적분에 현재 들어오는 photon correction의 center를 frozen homogeneous gain으로 더하고, 그 uncertainty를 별도 radius로 전달했는지 확인했다. 모든 output에 대해

\[
S_*\ge |c_{\rm in}|+\eta_{\rm in}+B_{r,+},\qquad
R_X\ge |g_X|_+\eta_{\rm in}+S_* T_{X,+}
\]

를 exact rational 비교로 검사했다. Signed local interval, gain × incoming center, exact-frozen minus captured representation을 합친 interval과 저장 center 사이의 최대 거리도 radius에 포함되는지 확인했다. 첫 구간 두 곳만 exact incoming0이고, 네 후속 구간의 center와 radius는 이전 출력에서 그대로 전달된다.

적분 count의 homogeneous gain은 `1−W`, photon endpoint의 gain은 `W`다. 실제 OFF/node0의 두 번째 짧은 구간에서 두 gain은 각각 약 0.0685800432367, 0.931419956763이다. 두 가지를 바꾸면 incoming uncertainty의 모양을 잃는다. 독립 toy에서는 `h=ln2`, `L=2`로 정하여 `W=1/4`, count gain `3/4`를 정확히 얻었다. 잘못된 `1/4` count uncertainty bound는 선택한 exact endpoint를 포함하지 못했다.

### Native representation과 energy stock

CSV를 binary64로 읽고 그 값의 정확한 유리수를 만드는 계약을 독립 구현했다. 캡처된 erg 필드는 상속된 binary64 `1.602176634e−12`의 exact lift로 나누어 eV로 변환한다. 이 변환에서 생기는 비유한 소수도 Fraction으로 정확히 계산했다. 종별 heat는 캡처된 `B_i−χ_i A_i`, 총량은 종별 값의 정확한 실수 합으로 확인했다.

각 output의 signed representation `exact_frozen−captured`가 first variation과 같은 부호로 candidate interval에 들어감을 확인했다. 특히 저장 native energy `u/eps`는 `E_h n`과 동일하다고 가정하지 않는다. 저장된 `u/eps−E_h n` residual과 photon representation을 함께 넣었을 때 energy representation identity가 0을 포함했다. Exact toy의 native stock 항을 일부러 빼면 세 구간 모두 energy ledger가 0이 아닌 값을 남겼다.

### 네 개의 실제 energy anchor

각 seam은 `ΔE=E_next,0−E_prev,h`로 정의한다. 그 부호를 유지한 채 correction interval의 양 endpoint와 곱한 네 corner를 모두 exact rational로 계산했다. 저장 corner interval과 최종 anchor interval은 해당 값을 모두 포함했다. `ΔE×(captured photon+correction)`의 직접 interval과 native/correction 분할도 별도로 확인했다.

아래 값은 읽기 편하게 반올림한 표시값이며, 검산에는 JSON의 전체 exact decimal endpoints를 썼다.

| track / 연결 | ΔE, eV | correction anchor, eV |
|---|---:|---:|
| node0, step1→step2/segment0 | −1.11006097832e−15 | [−6.74553857443e−28, −6.74548392634e−28] |
| node0, step2/segment0→1 | +7.41696612540e−16 | [+4.21400350791e−28, +4.21403767075e−28] |
| node700, step1→step2/segment0 | +2.65072444723e−15 | [+2.21378734188e−28, +2.21380466440e−28] |
| node700, step2/segment0→1 | −2.11702523255e−16 | [−1.74781328900e−29, −1.74779961083e−29] |

작은 anchor 크기는 이를 생략할 근거로 쓰지 않았다. 독립 toy에는 negative/positive/crossing ΔE 및 signed correction이 포함되며, 절댓값으로 바꾸는 shortcut은 exact counterexample에서 거부되었다.

### 누적과 number/energy ledger

종별 및 총 source/count/energy/heat/redshift의 각 누적 center는 모든 선행 구간을 포함한다. 누적 radius에는 이전 radius, 새 radius, 저장 center를 표현할 때의 차이가 들어간다. 캡처 moment 누적은 원래 row 값의 정확한 실수 합을 포함하며, native weighted aggregate reduction을 새로 인증하지 않는다.

각 구간의 frozen number/energy, first variation number/energy/heat 식과, 두 track의 최종 number/energy/heat ledger를 저장 endpoint에서 다시 조합했다. 원래 저장 ledger interval은 이 exact rational 조합을 포함하고, 각 조합은 0을 포함했다. 최종 energy 식에서는 네 seam 중 해당 track의 signed true anchor 두 개를 차감한다. 종별 cumulative 값과 별도 total 값의 일관성도 확인했다.

Ledger inclusion은 공유된 입력에 대한 보존식 consistency 검산이다. 각 output이 true continuous solution을 감싼다는 논증을 ledger 일치만으로 대체하지 않는다.

## 처음 발생한 실패와 수정

`toy_run_v1`에서는 음수 representation을 빼거나 뒤집은 두 mutation control의 잘못된 interval이 우연히 선택된 **상단** truth endpoint를 포함했다. 두 TestID는 FAIL로 보존했다. 동일한 허용 incoming interval의 **하단** endpoint를 쓰면 interval의 잘못된 상향 이동을 판별할 수 있으므로 fixture만 수정했다. Bound·tolerance·production source는 변경하지 않았다. 수정 후 같은 76개 TestID가 통과했다.

`saved_audit_run_v1`은 ledger field를 `energy_eV`로 가정하여 KeyError로 중단되었다. 실제 이름 `energy_eV_with_anchor_subtracted`로 audit adapter 한 곳을 수정했고, 새 run이 완료되었다. 중단된 run의 부분 검사를 성공 항목으로 세지 않았다. 두 최초 실패의 source, 실행 기록, stdout/stderr는 모두 남아 있다. Production source 또는 과학 계산에 대한 실패 finding은 발견하지 않았다.

## 주장 상한

근거 상태는 **직접 유도된 exact toy 관계 + 실제 실행한 독립 산술 검산**이다. 두 OFF track의 여섯 구간과 네 seam에 한정한다. 새 전역 path certificate, coupled gas trajectory 검증, 실제 atomic photon/heat/recoil 입력, receiver adoption 또는 production 승격을 뜻하지 않는다. 최종 decision review는 별도의 담당자가 수행해야 한다.
