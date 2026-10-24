# HE-ANG-CCC-EXCHANGE — Science 인계, C10 전달 대기

조건부 CCC equal-sharing adapter는 독립 C9 PASS_AFTER_CORRECTION과 root의
PASS_SCOPED 판정을 받았다. R1–R10/C1–C9의19단계를 확보했다. C10은
PENDING_DELIVERY이며 Science S, 실제 draft PR, delivery D 및 central observation/
backup ACK E는 아직 게시 영수증이 없다. 현재 파일에 미래 commit ID를
꾸며 넣지 않는다. 실제 publication metadata는 `delivery/PUBLICATION.json`에
후속 기록하고 불변 science identity와 움직이는 전달 HEAD를 구별한다.

## 재개에 필요한 결과

- Baseline BASS_HE: c8f5818c61d14872837abf7e9bc1a73c670ae25c.
- 새 경로: research/he_ang_ccc_exchange_20261024/.
- 원전: Bray physics/9906008v3 Eq2,21,24–27; Stelbovics physics/9905020v1 TableI.
  위치·PDF 원본 SHA256/bytes는 source/PRIMARY_SOURCES.json에 있다.
- 정확한 핵심 식: U=|a|²+|b|², C=|a+s b|², D=|a−s b|², 2U=C+D.
  확인한 v3 Eq26의 인쇄 minus를 해당 식에 한정해 교정했다.
- 경로는 raw amplitudes, 이미 coherent density, 이미 spin-weighted coherent
  density, phase-missing intensities를 구별한다. 상대 위상을 새로 만들거나
  factor4/2! 또는 spin weights를 중복 적용하지 않는다.
- Source/producer/kinematics/preparation와 exact equal-energy point 및
  density unit/measure를 맞춘 조건부 산술이다. Metadata declaration을
  물리적 source certificate로 승격하지 않는다.
- 실제 TP TableI의8개4CCC값은 0.0172,0.0145,0.0137,0.0135,
  0.0072,0.0081,0.0069,0.0069다. N/Npos와 원문 strings를 보존했다.
  이미 적용된 factor-four를 다시 곱하지 않고 printed BRM 대비 ratio만 계산했다.

## 실제 실행과 검토

처음 planned3child는14testmethods, actual8source rows/65manufactured phases,
plot1회였다. C9-01은 mixed tiny coherent remainder의 assertion scale floor가
너무 커서 상대오차를 검산하지 못한 oracle 결함이다. Kernel은 변경하지
않고 expected_C를 명시 scale로 넣은 test05 한 method만 reserve로 실행했다.
14initialPASS와1targetedPASS, 원래 코드·raw log·closed finding을 모두 보존했다.
측정4child+runner CPU1.410021s/wall1.4436621759814443s이며 reserve1회 사용했다.
새cap8/30 안의 측정 구간이지만 prelaunch RUN.lock 실패의 부모CPU는
UNKNOWN_NOT_ZERO이므로 end_to_end_cpu_cap_established=false다.
미측정 host 준비/문서 I/O, Wolfram 전체remoteCPU도0으로 만들지 않았다.

독립 R6의 worked-example 산술오류 교정과 최초 informalPASS의 한계,
Wolfram optional phase-query warning/NOT_ADOPTED, Matplotlib temp-cache warning,
prelaunch lock 실패/명시적 stale-lock cleanup 모두 실제 근거에 남겼다.
추가 replay나 provider solve는 하지 않았다. Baseline의 기존205selectedfiles는
모두 GitSHA1/size 보존을 재확인했다. 이는 file integrity이고 과학 suite가 아니다.

## 전달 상태와 다음 물리 입력

B1 preparation15/20 archive는 실제40303bytes가 양쪽 provider에서 readback됐다.
`delivery/B1_BACKUP_ACK.json`에 실제 IDs와 localhash가 있다. 그 이후의 science,
C9, 최종 delivery/central observation backup은 실제 후속 ACK로 채운다.
원격 provider가 independentSHA256를 반환하지 않으면 그 한계도 그대로 쓴다.

부모 HE-ANG과 HE-ANG-SOURCE-PAYLOAD는 SOURCE_INPUT_PENDING이다.
full H joint amplitude/event payload, phase/support/count/frame/recoil/uncertainty
의무가 열린다. 새strongno-go와 전체물리목표완료를 주장하지 않는다.
C9-NB-01,C23E,다른39centralnodes와기존HE38/X1/contract/Hex/DDCS20상태는 유지한다.

다음 승인된 전달은 c8f5818c baseline 위 additive draft branch 게시와 현재central
HEAD 위 이 subunit의 observation만 추가하는 일이다. 실제expectedSHA와
force=false를 사용하고 no_merge/no_activation을 유지한다. 게시 후 S/PR과
실제중앙관측/backupACK를 기록해C10을완료한다.
