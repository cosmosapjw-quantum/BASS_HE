# HE-ANG-CBA-NORDSIECK

**PASS_SCOPED_DIRECT_CBA — 독립 R6 PASS, R7 PASS_WITH_DIAGNOSTIC, 독립 C9 및 root PASS.** 고정핵 수소1s의 labelled direct Coulomb–Born analytic model과 유한 수치 fixture를 확보했다. 이번 과학 스냅샷은18/20이며 R10/C10 실제 전달은 pending이다.

핵심은 원전1/r 적분 I를 eta고정으로 미분한 K=-partial_lambda I, matched eta=lambda/p에서 직교성을 보존하는 direct-Delta 안정식, delta-normalized form factor와 절대 TDCS=4*(pf*p/pi_momentum)*|F_D|²/Delta^4다. 자세한 정의·단위·가정은 [THEORY_KO.md](THEORY_KO.md)의(1)–(9)에 있다.

[실제 결과와 비용](RESULTS_KO.md) · [20단계 evidence/checkpoint](LOOP_PROGRESS.json) · [claim gate](CLAIM_GATE.json) · [copyable handoff](HANDOFF_RESEARCH_KO.md) · [independent C9](reviews/C9_REPORT.json) · [그림](results/figures/CBA_NORDSIECK.png)

14tests 및9generic/4quadrature/16tiny/7normalization/73illustration controls가 통과했다. 실제3children CPU4.987974s/wall5.122489414992742s, 할당20/60, reserve미사용이다. Wolfram2evaluator+1context의 최초 structural false 결과와 targeted diagnostic 교정, preSTART lock 실패 및 비용unknown을 보존했다.

전체 HE-ANG SOURCE_INPUT_PENDING, physical_provider=false, event_sigma=false, physical_recoil_distribution=false, HE-X1 empirical correction=false, global completion=null이다. Exchange/full-count/validity/finite-M dynamics와 calibrated uncertainty를 별도로 충족한다. Source fulltext/PDF/page images는 공개하지 않는다. 이 단위 뒤 새 science loop를 자동 시작하지 않는다.
