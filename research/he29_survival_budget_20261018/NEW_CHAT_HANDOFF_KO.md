# 다음 채팅 시작점 — HE29 최적화 후속

$physmath-research-loop로 BASS_HE HE29를 이어간다. 사용자 목표는 여기서 가능한 코드 수정·경량 검증·게시·백업을 끝내 NCP에는컴파일/작은환경수정/실제실행만남기는것이다.

먼저 최신 GitHub와 관련 Drive/Dropbox에서 새 native 반환을 확인한다. 이번2026-10-20 intake에서는 HE29 기준해0/4,optionalcanaryNOT_RUN,새NCP제출0이었다. 미반환NCP프로세스는미관측이다. quota도구의재시도/재연결금지를지킨다. 다른REI/VigilODE의native결과로HE29를완료처리하지않는다.

## 반드시 실제 읽을 파일

`README_KO.md`, `DAG_STATUS.json`, `CODEX_HANDOFF_PROMPT_KO.md`, 이 파일, 기존 `results/publication_retry/{DELIVERY,CLOSEOUT_RECEIPT}.json`과 새 `optimization_20261020/{README_KO,NCP_HANDOFF_KO,RESEARCH_KO,PERFORMANCE_KO}.md`, `optimization_20261020/{DAG_STATUS,DELIVERY}.json`.

## 고정 source와 이번 결과

- repo https://github.com/cosmosapjw-quantum/BASS_HE
- DraftPR78 https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
- branch research/he29-survival-budget-20261018
- 이번시작HEAD329f838399f24d3952f780d469ad657d8630c4e2
- 첫최적화checkpoint8cb0ebb91a78d2f1b751caa1c3ffc5d170ddfe41,19파일actualreadbackMATCH
- 원래과학source/tests1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f
- ownerf7830e2f55e7a1938bc3c98f61b60651f8dae474,HE28parenta41dd37124e34cb22bb9782aaf687a0da91640b7
- 새실행ABI2codepin은새DELIVERY의implementation_publication.code_commit을읽는다. 문서HEAD와구분한다.

입력manifest62자리SHA하나의누락4b를a70archive전체/내부SHA로보정했다.22DATA실제복원/preflight/독립검토PASS. 원본1569에는기존pytest재사용overlay와새manifestrepairpatch둘을적용해야한다. 상위Codexhandoff의그대로명령이있다. source실행은Git에서,archive는DATA만사용한다. 사용자파일전달요청과옛PUBLISH.sh복구는없다.

새canonicalCSR조립은원래값/structure와정확히같고조립실험8.35–8.78배다. 새RustpackedJVP는같은상태/time정확cache와원래누산순서를지켜합성IVP1.38–1.53배다. 모든1/2/4thread endpoint비트/attempt동일하나2/4는느려NCP기본1이다. 두배율은다른실험이므로곱하지않는다. 실제HE29native속도·전역메모리는아직미측정이다.

## 재사용과 다음native

HE28pilot/6transport,HE29finite-donor90/720과50tests,기존VigilODE96Python/3smoke/23Schur는재실행하지않는다. 원래네m8/GL4/q0(Radau+DOP853)쌍(r2,512),(r4,512),(r8,512),(r4,1024)을우선한다. 반환있으면source/binary/tableidentity를읽고분석한다. 네쌍모두admit뒤optionalr4/table512packedcanary한개만가능하다. 새runner는4/4및runtime/원본source/input/binary/tableidentity와process상한을검증한다.

90/720의maxfinite-donor구간폭2.2487671447191104e-12와GL256/512차2.7755575615628914e-16은기존조건부범위와수치안정성결과다. 연속적분엄밀오차나기체온도전역상한이아니다. 원래반응률·물리식·fraction1e-11및온도1e-9K·보존gate를유지한다. continuousspectrum/fullEoR/wholeupstreamGrackle/관측Bianchi+CMB는HOLD다.

새코드/실행/재사용근거를DAG에분리하고각checkpoint의실제게시와백업readback을기록한다. 기존c47/798,7bf/882는불변보존하며새두provider백업은새DELIVERY를따른다. 현재standalone1.0.0연구루프와과거1.3.0근거를구분한다. 이번C/R세부단계는새DAG와연구보고서를읽고완료항목을반복하지않는다.
