# BASS_HE ENDPOINT14 — 끝점 조건을 유지한 각분포 차수 민감도

## 결과
**330MeV에서 endpoint-zero full nonnegative even-sextic 각분포는 고정된 네 EXFOR DCS 민감도 창을 모두 만족한다.** 동일한 창과 endpoint조건에서 앞서확정한evenquartic가족은EMPTY였으므로,그배제에는차수제한이실질적으로작용한다. 이번단위는정확한유리수증인과전역양성성증명,고정N1/4/16의유한포함집합,같은사건aperture의최소·최대certificate를구성하고실제실행했다.

채택범위는 `ACCEPT_SCOPED_ENDPOINT_ZERO_SEXTIC_REFERENCE`다. 단일initialcampaign **8PASS0FAIL**, exactsavedreader **PASS**, Wolframoneevaluation **14literalzero+16True**, saved-onlyplotone **PASS**를얻었다. 최종비저자과학admission및source/central/transport완료는각review와외부종료권위문서로확정한다. 이문서는수학·과학결과를설명한다.

## 1. 최신 자료에서 정한 다음 질문
TANGENT13의실제S10 `049e79cb453b92ac663c4e0a93577a8364c3cf54`를baseline으로현재관련7repo1450heads/18terminalpages를조사했다. 이전census대비new6,moved8,removed0이며,PR state=all240records/8pages중2026-10-22이후171개를확인했다. 선별PR13sections/commit15bodies/sciencesource16files/currentAGENTS2files를읽었다.
백업은Librarydelta62metadata/1terminal과선택8전체문서/10readwindows,Dropboxdossier5337/9terminal및BASS_BACKUPS344/1terminal을확인했다. Drive문서delta1/1terminal,archivefolder1000cap을기록했다. Privatecontext검색은SERVICE_ERROR였으므로전체대화접근을주장하지않는다. 접근범위·시점·raw와publicsafe구분은sources의조사기록을따른다.

최신타repo의조건부EOS/thermaljet/CRenergy-sum/molecularregistry/staticlapse결과는각자의scope로통합했다. 접근한자료에서HEphysicalopen세묶음을닫는actualpayload는확인하지못했다. QUARTIC12최대값과T13최소값은이미완결돼있어이를반복하지않고,330MeVendpoint배제의degree민감도를선택했다.

## 2. 원자료와수학모형
실제반응은EXFORM0475002의He4(g,d)d,두deuteron채널이다. theta_cm의nominal값과330MeV DCS창은다음과같다.

| theta_cm | DCS deterministic window (nb/sr) | 고정증인의DCS 근삿값 |
|---:|---:|---:|
|46°|[0.11,0.17]|0.169635913719409|
|61°|[0.11,0.21]|0.118769127531032|
|73°|[0.02,0.12]|0.118315855717065|
|87°|[0.14,0.24]|0.140040508293858|

마지막열은표시용근삿값이다. 실제membership은각nominalcosine의인증된interval에서계산한exactrationalenclosure로판정했다. ERR-S창은결정론적민감도창이며jointconfidenceinterval로다루지않는다. 다른energygrid의M0475003total6점은결합·보간하지않았다.

mu=cos(theta_cm),z=mu²라하고

\[
f(\mu)=(1-\mu^2)(a_0+a_1\mu^2+a_2\mu^4),\qquad
r(z)=a_0+a_1z+a_2z^2\ge0\quad(0\le z\le1)
\]

를쓴다. a의단위는nb/sr이고signedcoefficients를허용한다. 모든evensextic중q(1)=0인함수는이형태이며,degree<=4는정확히a2=0인부분가족이다. Declareduniformazimuth,restenergies,targetatrestkinematicreference,same-eventdetectorunion은그대로유지했다.

## 3. 직접적인feasible증인
사전고정한

\[
(a_0,a_1,a_2)=\left(\frac{1411}{10000},-\frac14,\frac{33}{25}\right)
\]

은

\[
r(z)=\frac{33}{25}\left(z-\frac{25}{264}\right)^2+
\frac{170627}{1320000}>0
\]

로정리된다. 따라서f는[-1,1]에서비음수이고양끝에서0이다. 정규화는

\[
D=\int_{-1}^{1}f(\mu)d\mu=
\frac43a_0+\frac4{15}a_1+\frac4{35}a_2
=\frac{14297}{52500}>0.
\]

이계수는새실행에서네창모두를통과했다. 실행후후보를조정하지않았다. a2가0이아니므로기존quarticendpoint가족밖에있고,두가족의feasibility차이를실제구성으로보인다.

## 4. Full-family경계를얻는방법
46/61/87degree의분리된세z값에서Lagrange보간을사용하면모든참된허용계수는|a|<=(75,150,75)에포함된다. 계산의B160box는이증명된포함상자다. |f'|<=18B와87degree의양의lowerwindow에서D>=49/14400000을얻고,실제savedmu주변interval이[-1,1]안에있음을확인했다.

Signeda를위해(1-z)z^j의interval중점오차를모든세성분에반영했다. 데이터를수축한inner와확장한outer부등식은각각참가족의충분·필요조건이다. N1/4/16의cellBernsteincontrols는r의전구간양성을보장하는innercone,gridnode값은necessaryoutercone을준다.

각3차원polytope에서모든activeconstrainttriple을정확히풀고모든부등식을확인했다. 총24690bases,26savedvertexoccurrences다. Inner/outer정점수는N1에서6/4,N4에서4/4,N16에서4/4이며네nestedinclusion이모두성립했다. 독립reader는candidate나정점을다시찾지않고저장된행·정점·증인·극값·반올림을검사한다. 완전성의근거에는producer의exhaustiveloop와유계polytope정리가함께들어간다.

## 5. Same-eventaperture와새weightedmoments
HEMISPHERES는fullazimuth실험실polarcosine창A=[0,1],B=[-1,0],CAPS는A=[1/2,1],B=[-1,-1/2]다. 관측량은같은사건의두교차배치합집합에들확률이다.

고정된330MeVkinematicmap의K<0단조성을확인하면eventset은C=[-1,-t]union[t,1]이다. 기존zerothmomentk0=2(1-t)의certificate에서tinterval을복구하고

\[
k_j=2\left[\frac{1-t^{2j+1}}{2j+1}
-\frac{1-t^{2j+3}}{2j+3}\right],\qquad j=0,1,2
\]

의단조성으로새weightedmoments를감쌌다. 같은threshold로재구성한기존monomial세성분은두geometry모두exactequality였다. 기존geometry/preimage/trigonometrycampaign을반복하지않고새basis에필요한적분만수행했다.

P_g=(k_g.a)/(d.a)의interval평가는음수계수에서상·하moment를뒤집는다. 분모가양수인convexcombination을분모가중치로쓰면concavenumeratorlower의최솟값과convexupper의최댓값은outer정점에서얻는다. Inner증인은각trueextremum의반대쪽경계를제공한다.

## 6. 실제수용확률범위와해상도비교
아래는N16fullconditionalfamily의확률범위를포함하는바깥방향12자리표시다.

| Geometry | Full-family probability enclosure | True minimum bracket | True maximum bracket |
|---|---|---|---|
|HEMISPHERES|[0.747050288674,0.783542448014]|[0.747050288674,0.747050288675]|[0.783542448013,0.783542448014]|
|CAPS|[0.317079169073,0.404464291607]|[0.317079169073,0.317079169074]|[0.404464291606,0.404464291607]|
|FULL|[1,1]|[1,1]|[1,1]|

N4와N16의exact결과는일치한다. HEMISPHERESminimum/maximum의exactbracket폭은약7.6967122e-15/4.3811398e-15, CAPS는1.4224758e-14/1.0097285e-14다. N1CAPSmaximum은[0.392235444930,0.404464291607]로더넓었고,사전고정된N4/N16에서좁아졌다. 추가mesh는없었다.

이표의전체range폭은허용된모델변동이고,각최소·최대값주위의아주작은bracket폭은계산certificate폭이다. 실제실험적불확실성을1e-14수준으로알게되었다는뜻은없다. 그림은저장결과만그린참조로,정확한정량권위는이표와savedfractions다. 오른쪽상단legend와N16HEMISPHERES상한표식에국소겹침이있음을기록했다.

## 7. 실제검증·자원·정책교정
Actualinitialonecampaign:8PASS0FAIL,construction1,reader6polytopes26verticesPASS. WholeCPU2.020525s/wall1.9446278749965131s/RSS15752KiB. Sourcepin은S05이며9sciencefiles/2inputs를결속했다.
Wolframoneevaluator:14literalzero+16True,isErrorfalse,warning없음. RemoteCPU/wall은미제공null. Contextdocumentationresponse는evaluator와분리했다.
Saved-onlyplotone:wholeCPU1.635101s/wall1.5717367499964894s/RSS66088KiB,scienceimports/calls0. Root와비저자reviewer가실제PNG를읽어평가한다.
실행전누락된87mu확장구간control과도함수주석부호를최소교정했고과학scope/tolerance를바꾸지않았다. 새science실패0/repair0이다. S04DropboxtwoFETCH_FAILED는봉인된같은bytes를새전달참조로재전송해해결했으며source/science반복은0이다. 이후실제transport이력은STAGE_ACKS및최종영수증을따른다.

## 8. DAG와물리입력
독립과학수용시Local은**14complete+1inheritedpartial+3physicalopen /18**이된다. 중앙은**28/88,HEdelta0**다. R1–R10/C1–C10의20workproducts와scientificDAG노드수를혼동하지않는다.
세physicalopen은event/inclusivenormalization+liquid-Heelectron/target-motion/responseprojection;actualfullangular/polarizationlaw+photonencounterflux/history;namednonthermalbirth/deposition/thermalization+globalspeciesbinding이다.
Bindingsoleowner=population_rest_energy_witness. independent_binding_RHS/Gamma_thermal/Cv/species_heating/thermal_deposition=null,birth_pool=UNASSIGNED,global_physical_completion=null,L4=false,production=NOT_APPROVED,activation=false를유지한다.
T13/Q12/EXFOR11/HARMONIC10scopedcompletion,KINEMATIC08partial,PHOTON05plotCPUfailure,HARMONIC10initial24PASS+1FAIL/targeted1PASS와T13runnerfailure/targetedrepair를보존한다. 완료science/test/CAS/plot/ACKed백업을재실행하지않는다.

## 출처와정확한권위
데이터는IAEAEXFORmasterM0475: https://nds.iaea.org/nrdc/exfor-master/entry/m/m0475.txt . 실제보존source와savedinput의hash는CONTRACT.md에있다.
Arends et al.(1976),PhysicsLettersB62,411–412,DOI10.1016/0370-2693(76)90671-7;Rice et al.(2000),PhysicalReviewC61,064612,DOI10.1103/PhysRevC.61.064612;Silverman et al.(1984),PhysicalReviewC29,35,DOI10.1103/PhysRevC.29.35. 각본문접근수준은sources/literature/PRIMARY_SUPPORT_KO.md에분리했다.330MeV의actualdegree6law를이들metadata/abstract에서추론하지않는다.
Intervalpositivepolynomial의일반배경은Nie/Demmel저자공개PDF https://mathweb.ucsd.edu/~njw/PUBLICPAPERS/TrnShapOptCoef.pdf §2다. 이번핵심논증은THEORY.md의직접factorization/positivity/weakboundconstruction이다.
Finalsource/centralcommit과actualtransport는BASS_HE_ENDPOINT14_HANDOFF_KO_20261028.md,BASS_HE_ENDPOINT14_CLOSEOUT_20261028.json,STAGE_ACKS.json,CENTRAL_PUBLICATION_RECEIPT.json,FINAL_DELIVERY_TRANSPORT_RECEIPT.json을따른다. GitS10/PRE_CAS의pending은각생성시점snapshot으로보존한다.
