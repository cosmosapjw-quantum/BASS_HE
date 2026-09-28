# SHARED_C64_R3: lifted-homotopy claim gate, rho analytic domain, total-error firewall, a-priori pruning bound

Date: 2026-09-28. Scope: research-only. Production `src/`, Eq.(55), physical probability, scientific tolerance, Nmax/channel authority are unchanged.

## 0. Fresh state used for this node

GitHub connector fresh read:

- PR #17: open draft, base `2c3812e390b91b89da1de30988b3933646b79f30`, current HEAD `96a6e4317a54e9eae825f66292743f9785df80e0`.
- `aac8f822dc10a215e7c59259bd339965c4ffe23c -> 96a6e431...` is exactly one commit ahead and adds only four evidence files under `R2_followup/20260928T1315Z/`; no delivered R2 code changed.
- PR #15 remains at `af3ed44ce3cc1023aa8a1370ab2981aa76760869`.
- PR #16 remains at `2c3812e390b91b89da1de30988b3933646b79f30`; `resume-004/RUN_RETURN.json` still reports PASS runtime evidence while explicitly leaving CODE-I02 independent scientific rereview pending.

The follow-up R2 run executed immutable commit `aac8f822...`, tree `765a8d3133bc30eea6bc6e00e50424cc288fd56c`, and only `--verify-only`: seven trace files matched exact size/SHA input identity. Host pytest/NumPy/SymPy were absent, so no tests or saved-trace numerical replay were run there. This is `INPUT_IDENTITY_VERIFIED`, not scientific validation. `scientific_PROMOTE=HOLD`, `Eq55=NOT_RUN` remain unchanged.

Drive and Dropbox metadata fresh reads confirm the current follow-up objects and the original R1 archive IDs/sizes. In particular the RUN_RETURN object is 3799 bytes on both providers and the locally materialized provider readback hashes to the recorded SHA256 `79e1730434e0bd992b7c39eb31a7d51c3fddcbfa70653b3100dfa84d82272bd5`. This closes content identity for that small object only; it does not imply a new restore test of every backup artifact.

## 1. SOURCE / DERIVED separation

SOURCE carried from R1/R2:

\[
A(\rho)=\int_{\Gamma}G(R)K(\rho,R)\,dR,\qquad
K(\rho,R)=\left(1-\frac{\rho^2}{R^2}\right)^{-1/2},
\]

with the common-contour construction admitted only as a research candidate. Existing R2 bounds are for the fixed discrete Simpson trace and do not include global same-sheet homotopy, exact-spectrum error, quadrature true error, or floating-point enclosure.

DERIVED in R3 are the results below.

## 2. Lifted-homotopy theorem: the missing common-contour authority is topological, not another epsilon

Let \(\Sigma\) be the spectral Riemann surface carrying the two selected analytic sheets and let \(\pi:\Sigma\to D\subset\mathbb C_R\) be the projection. Write the action one-form

\[
\omega_\rho = G(\tilde R)K(\rho,\pi(\tilde R))\,dR.
\]

Consider the original lifted contour \(\widetilde\Gamma_\rho\) and a candidate common lifted contour \(\widetilde\Gamma_*\). If there exists a fixed-endpoint homotopy on the *lifted* surface between them whose image avoids all singularities of \(\omega_\rho\), then Cauchy/Stokes gives

\[
\int_{\widetilde\Gamma_\rho}\omega_\rho
=
\int_{\widetilde\Gamma_*}\omega_\rho.
\]

If the two base contours have different real-axis anchors, append the connecting real-axis bridge. When the bridge value of \(G K\,dR\) is real, only the real part changes and therefore

\[
\operatorname{Im}A_\rho
=
\operatorname{Im}A_* .
\]

This is the precise form of the R1 contour-deformation claim. A finite numerical sheet gap along two sampled paths is not by itself a proof of this lifted homotopy.

For the current nonlinear finite-CF spectral system \(F(z,R)=0\), \(z=(p,\lambda)\), ordinary sheets are locally analytic wherever

\[
\det \partial_zF\neq0.
\]

Thus a practical global certificate must exclude unintended solutions of

\[
F_1=0,\qquad F_2=0,\qquad \det\partial_zF=0
\]

throughout the swept homotopy domain, apart from the intended fold whose winding class is deliberately preserved. It must also exclude CF chart poles and kernel singularities and preserve the same branch-point winding/monodromy class. Existing pointwise continuation residuals and 32/64 agreement are diagnostics, not this exclusion proof.

Recommended eventual authority is an interval/Krawczyk or argument-principle exclusion over a cell decomposition of the swept domain, with the known fold isolated in its own certified box. Until such a certificate exists, common-contour replacement remains `RESEARCH_CANDIDATE_NOT_PRODUCTION`.

## 3. Exact analytic disk in rho, and what it does not say

For fixed nonzero \(R\), the kernel as a function of complex \(\rho\) has branch points at \(\rho=\pm R\). For a compact continuous contour \(\Gamma\), define

\[
r_* = \inf_{R\in\Gamma}|R|.
\]

Then the binomial series about \(\rho=0\) is uniformly convergent on every closed disk \(|\rho|\le r<r_*\), and \(r_*\) is the exact radius of the common Taylor germ because the nearest kernel singularity set is \(\{\pm R:R\in\Gamma\}\).

This settles one previously ambiguous point: `rho_max < r_min` is not merely a convenient inequality. It is the exact open-disk radius for the kernel germ about zero.

It is *not* necessarily the maximal interval along positive real \(\rho\). If the nearest \(R\) is off the real axis, analytic continuation along the real axis may extend beyond \(r_*\) before encountering a real singularity or a branch-topology obstruction. Production use should therefore distinguish:

- `CERTIFIED_OPEN_DISK`: rigorous sufficient domain around zero;
- `MAXIMAL_REAL_RHO_INTERVAL`: still OPEN and requires continuation/topology analysis.

The R3 implementation computes the finite-trace analogue \(r_*^{(d)}=\min_j|R_j|\) and explicitly labels its scope `FINITE_TRACE_KERNEL_ONLY`.

## 4. Total error budget firewall

Once and only once the lifted homotopy is independently certified, a numerical action approximation may be bounded as

\[
E_{\rm total}
\le E_{\rm spectral}+E_{\rm quadrature}+E_{\rho\text{-interp}}+E_{\rm roundoff}.
\]

Homotopy is deliberately *not* inserted as a guessed small numerical term. If same-sheet homotopy is unknown, the total-error composer fails closed.

If a pointwise exact-spectrum gap error enclosure \(|\widehat G-G|\le\varepsilon_G\) is available on the unchanged contour, then for \(q=(\rho_{\max}/r_*)^2<1\),

\[
E_{\rm spectral}(\rho)
\le \int_\Gamma \varepsilon_G(R)|K(\rho,R)|\,|dR|
\le \frac{1}{\sqrt{1-q}}\int_\Gamma \varepsilon_G(R)|dR|.
\]

The existing 32/64 shared-node difference is not such an exact-spectrum enclosure. Likewise, Simpson 32/64 agreement is not a rigorous quadrature remainder without an independent derivative/enclosure argument. R2's interpolation term remains the only currently analytic finite-trace component.

For floating-point production certification, either interval/ball arithmetic should enclose kernel evaluation and summation, or a forward-error calculation must include both local kernel evaluation error and the summation factor \(\gamma_n\sum_j|t_j|\). R3 does not invent a numerical value for these missing components.

## 5. New a-priori hybrid pruning theorem

R2's exact hybrid telescope used the true downstream adjoint \(\lambda^T_e\), so it did not yet authorize pruning *before* the exact event probability \(p_e\) was computed. R3 removes that logical obstacle under one additional contract: a cheap approximate probability \(q_e\) and a certified radius

\[
|p_e-q_e|\le\epsilon_e
\]

must be available without performing the expensive exact event calculation.

Let \(Q_e\) be the approximate event matrices, \(T_e\) the unknown true matrices with the same reversible or one-way sink topology, \(y^Q_e\) the approximate upstream population, and

\[
(\lambda_e^Q)^T=w^TQ_{m-1}\cdots Q_{e+1}.
\]

For a bounded observable \(0\le w_i\le1\), define its oscillation

\[
\operatorname{osc}(w)=\max_i w_i-\min_i w_i.
\]

Every column-stochastic event maps row-vector components into their convex hull, so oscillation is nonincreasing downstream. For either supported event topology,

\[
\|v^T(T_k-Q_k)\|_\infty
\le \epsilon_k\operatorname{osc}(v).
\]

Telescoping the downstream chain therefore gives

\[
\|\lambda_e^T-\lambda_e^Q\|_\infty
\le \operatorname{osc}(w)\sum_{k>e}\epsilon_k.
\]

Hence

\[
|\lambda^T_{e,j}-\lambda^T_{e,i}|
\le
S_e
\equiv
\min\!\left[
\operatorname{ÜØß]ÊK[XWWÞÙKKW[XWWÞÙK__
ÂÜ\]Ü[Y^ÛÜØßJÊWÝ[WÞÚÏ_W\Ú[ÛÚÂYÚKBH^XÝXYÛÛX][Û\È[Ý[Y
Ú]Ý]ÛÝÚ[Ê
ÙW
N]\ÚXH][Â×Ù_H\Ú[ÛÙH×ÙHWWÞÙK_K^WWÞÙK_BÛK]Ø^HÚ[ÎÂ×Ù_H\Ú[ÛÙH×ÙHWWÞÙK_KB\YÜBÂ[HßHÝ[WÙHÙKBÚ]
ÙW
HÚ][XÝK\È\È[XÝX[K\[ÜH[[ÈÙ\YXØ]H
ÛÛ][Û[Û[YÚX\

WÙK\Ú[ÛÙJW
HÛÛXÝÊYØZ[[È
\Ú[ÛÙW
H[XYH\]Z\\ÈH^XÝ\KMJHÛÛ\]][Û\H\ÈÈÜYY[Y][È[[È]]Ü^][ÛHÛÛÝ[[ØÙ\XH[Z]\ÈØ\\Y^XÝNY
×
H\ÈÛÛÝ[
Ü\]Ü[Y^Æ÷67×rÓÂæBFR6W'FfVBö'6W'f&ÆRW'&÷"2¦W&òf÷"ç7Fö67F2WfVçBW'&÷'2Â2&WV&VB'&ö&&ÆG6öç6W'fFöâà ¢22bâ×ÆVÖVçFFöâæBDD@ ¤æWr&W6V&6ÖöæÇÖöGVÆS¢6öÖÖöåö6öçF÷W%ö6öçG&7Bçà ¥$TBf'7C  ¢ÒFW7BÖöGVÆRw&GFVâ&Vf÷&R×ÆVÖVçFFöã°¢ÒFW7F6öÆÆV7FöâfÆVBvFÖöGVÆTæ÷Df÷VæDW'&÷#¢6öÖÖöåö6öçF÷W%ö6öçG&7FWB"à ¤u$TTâgFW"ÖæÖÂ×ÆVÖVçFFöã  ¢Òbóbfö7W6VBFW7G253°¢Òæò$55ôR&öGV7Föâ6÷W&6R×÷'FVC°¢Òæò7V7G&Â6öÇfS°¢Òæò6Æ÷VB'Vã°¢ÒæòöÆB66VçFf27VFR&W'Vâà ¤6W&FR7çFWF27G&W726V6²W6VBÃ&æFöÒR×7FFRòBÖWfVçB6ç2vFW7B6×ÆVBç6FRFR&öÖ6VBW'&÷"&ÆÇ3  ¢Ò&÷VæBföÆFöç3¢°¢ÒÖ7GVÂò#2'Væær&÷VæF¢ãccs#3cs3C#C&°¢ÒÖVFâ7GVÂò#2'Væær&÷VæF¢ã#sc#c3sc3C°¢ÒÖVFâ#2'Væær&÷VæBò7VÒW6¢ã3ss3S#csss3f°¢ÒR#2'Væær&÷VæBò7VÒW6¢ãSCCCc#à ¥FW6R&R7çFWF27Fö67F2fÆFFöâöæÇâæòFöÖ2&ö&&ÆGÂ7&÷726V7FöâÂWâSRÂ÷"&öGV7Föâ7VVGW26ÆÖVBà ¢22râ4ôDRÔ"&WfWr&W&Föà ¥FRæFWVæFVçB&WfWvW"×W7Bç7V7B"3RBW7BVBc6VCCF6S663#63s##scsccÂæ÷BFRÖ÷fær"3rWF÷&ær6öçFWBâFR&WfWr6÷VÆBWÆ6FÇFW7Böç7V7C  £âVæGöçB&æFæröb7FFUöÂ7FFUö&Â&ÂÂÆÖ&FÂFWFÂ£Â£"ÂFöÆW&æ6RÂ&ö&R66ÆRÂöÆ7°£"â7FÆRÖfVÆB&V¦V7Föâö67W'2&Vf÷&RvVöÖWG'°£2âçF7BrÖ'&æ6&Vf÷"&VÖç2fÆBW6ær"3b&W7VÖRÓBöæÇ27W÷'Fær'VçFÖRWfFVæ6S°£BâÖ76æræVvFfR×FW7B6÷fW&vRf÷"7FFUöÂFöÆW&æ6VÂæB&ö&U÷66ÆV276W76VB&FW"Fâ6ÆVçFÇ77VÖVC°£RâFR4#Sb&æFær2âVæ¶WVB6VÆbÖ6öç67FVæ76V6·7VÒÂæ÷BWFVçF6Gâ¦öçFÇf'&6FVBVæGöçB¶6W'Ff6FR·&V6ö×WFVB62÷WG6FRFR7FÆRÖ6÷wV&çFVRVæÆW72FR&WfWvW"FV6FW2FR6ÆÒ×W7B&R7G&VæwFVæVC°£bâVçW6VBFvæ÷7F26W'Ff6FRfVÆG2&Ræ÷B66FVçFÆÇ&VÆVBöâF÷vç7G&VÓ°£râ6ÆÒ6VÆær27FFVBW7FÇ¢6Æ÷7W&Röb4ôDRÔ"FöW2æ÷BWF÷&¦RWâSRVæÆW72FRæFWVæFVçBFV66öâ&WGW&ç27&F6ÃÓÂ×÷'FçCÓÂ$ôÔõDSÕ52ÂWSUöæWEöæöFUöWF÷&¦VC×G'VRà ¤6VÆbÖ6öçFæVBæFöfb27F÷&VB6W&FVÇ24ôDUô%ôäDUTäDTåEõ$U$UdUuôäDôdeô´òæÖFâF2&W6V&6F&VBFöW2æ÷B6VÆbÖ6W'FgæFWVæFVæ6Rà ¢22âvFRgFW"#0 ¢Ò4ôDRÔ¢4Äõ4TBà¢Ò4ôDRÔ"×ÆVÖVçFFöâö6Æ÷VB'VçFÖS¢52WfFVæ6RW7G2à¢Ò4ôDRÔ"fö7W6VBæFWVæFVçB66VçFf2&W&WfWs¢$UT$TBòäõB%TâW&Rà¢Ò6öÖÖöâÖ6öçF÷W"ÆgFVB6ÖR×6VWBöÖ÷F÷¢õTâà¢Ò¶W&æVÂ&öFÆ÷"F6³¢DU$dTC²fæFR×G&6R×ÆVÖVçFFöâ4T4´TBà¢ÒÖÖÂ÷6FfR×&VÂ&öçFW'fÃ¢õTâà¢ÒF÷FÂçVÖW&6ÂW'&÷#¢5E%T5EU$RDU$dTBÂfÇVW2$Äô4´TB'7V7G&Â÷VG&GW&R÷&÷VæFöfbWF÷&FW2æBöÖ÷F÷vFRà¢Ò'&B&RÖ6ö×WFFöâ'Vææs¢DU$dTB²5åDUD4ÄÅô4T4´TBÂ6öæFFöæÂöâ6V6W'FfVBWfVçBW'&÷"&Fà¢Ò66VçFf5õ$ôÔõDSÔôÄFà¢ÒWSSÔäõEõ%Tæà¢Ò6öçFçWVÕööæ¦FöãÔäõEôDÔEDTFà