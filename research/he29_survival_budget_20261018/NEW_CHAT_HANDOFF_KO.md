# 새 대화에서 이어갈 프롬프트 — HE29 HPC64

아래 내용을 새 대화 첫 요청으로 사용한다.

```text
$physmath-research-loop로 BASS_HE HE29 작업을 이어서 진행해 줘.
필요한 새 이론·코딩 연구는 SciSpace/Exa/Wolfram을 쓰되 완료된 연구·검증을 반복하지 마. 사용자에게 파일 전송이나 터미널 작업을 요구하지 마. 여기서 가능한 코드 수정은 여기서 끝내고 push하며 NCP는 compile/작은 환경 수정/실제 실행만 맡게 해.

[저장소와 현재 실행 pin]
Repository https://github.com/cosmosapjw-quantum/BASS_HE
PR78 https://github.com/cosmosapjw-quantum/BASS_HE/pull/78
branch research/he29-survival-budget-20261018
PR78은 Draft/open/unmerged로 유지. merge하지 마.
새 HPC64 실행 code pin 802a32361288bf5aa0e0d1f63c912768f1a1d407
code tree bf52fcabc3b03e00df140d2fdf913f05b3699d08, 실제 changed63/63 Git readback PASS.
후속 문서 HEAD는 별도다. 시작할 때 실제 최신HEAD/PR본문과 DELIVERY를 읽어.
이전 publication a02ae998570d5a0a4fffdf46299ee77b1c738759, 이번 intake cbbed9c3da6b41914527e322d2cb9bea9dc7b1f3 실제8/8 readback. 단계마다중복파일이있으므로고유파일수로합산하지마.

[먼저 읽기]
research/he29_survival_budget_20261018/의 README_KO.md,DAG_STATUS.json,CODEX_HANDOFF_PROMPT_KO.md,NEW_CHAT_HANDOFF_KO.md.
현재 lane hpc64_20261021의 README_KO.md,RESEARCH_KO.md,DAG_STATUS.json,DELIVERY.json,NCP_HANDOFF_KO.md.
evidence의 GITHUB_DELTA_64C,BACKUP_DELTA_64C,PERSONAL_CONTEXT_RAW,PENDING_INVENTORY,INTAKE_PUBLICATION_READBACK,CODE_PUBLICATION_READBACK,C9_REVIEW,각BACKUP_RECEIPT를 실제 읽어.
이전 native_intake_20261020T1315Z의 DELIVERY/DAG/RESEARCH/NCP_HANDOFF와 반환identity/저장분석은 재사용 근거다.

[연구 전에 새 실제 반환 확인]
다른 대화·현재GitHub/관련branch/repo·백업의 이후 변경분부터 확인. 기존 intake는BASS_HE85branches와관련repo의명시적bounded범위,Dropbox부분pagination이었다. 다른대화조회는실제서비스오류. 모든대화나미게시실행의부재를주장하지마.
새 PACKED_RAW/RESULT/실패/timeout/부분 trace가 있으면 source/binary/table/input/runtime/thread identity를 읽고 분석부터 해. 새NCP실행전에접근가능한실행자가실제/proc와저장결과를관측해야한다. Remote Desktop Commander의기존quota/no-retry금지를유지하고어떤메서드도다시호출하지마. 이번NCP제출0/시작0,원격process UNOBSERVED다. 별도NCP/SSH실행자는당시metadata범위에서발견되지않았다.

[완료된 원래 native 반환]
네 m8/GL4/q0 pair: r2/512,r4/512,r8/512,r4/1024 모두Radau+DOP853 admitted4/4,한cohort. 절대다시제출하지마.
반환PR80 089d6afba06bb35f303fc704163d75f5761ec9df.
BASS_HE_HE29_NATIVE_RETURN_20261020_c1c4c061.tar.gz 276206340bytes SHA c1c4c06149bf9561141bc0f6b6f39c280bd554a5e1252ed0825f0e950f1c10c6
Dropbox id:BSpOijBcT10AAAAAAD_Z-w; 이전실제raw payload292/292,member293PASS재사용.
Native binary4691224bytes SHA a82e540797322027deaab6e6bcb2bde746de737adeedbf144313598c65f5b7e9.
저장된09929 REFERENCE_BUDGET SHA582e59e8f6b43698b060b44cc17aa2496358ba0491b66e84215e0ed01dcd9f00,exit0,6residual/3contrast/4exactzero closures,transport DATA18/18. 재분석CLI를반복하지마.

[이번 완료한 새 연구/코드]
proper-time source table의독립행을spawn pool/64-rowchunks로구성하고원래canonicaldigest/행내산술을유지한다. exactsource/runtime/thread/spec/cache와실제NPYbytes/fulltablehash를확인한다.
BatchedNativeOwner는원래nativecall/응답/순서를유지하면서B256flush/fsync를쓴다. hardkill시마지막완료fsync이후성공point최대255개의trace가durable하지않을수있는변경된계약이다. segment/RAW/failure/closebarrier,stickyIOerror,completegzipreadback/countgate후에만RESULT허용.
host_plan은actualaffinity/cgroupancestor/memory/cwdprocess/CPU55/공유flock을읽는다. rootcgroup파일누락은확인된actualglobalroot signature만예외. 그외관측실패는HOLD.
batch_entry는기존canary/partial을보존하고1개의미완료canary만실행한다. build최대8jobs,table최대48workers,기본8CPU및max16GiB/20%memoryreserve. solverthread1. 수치/Rustcore는원래a5/a21재사용.
새test62distinct methods:table11+trace11+worker10+host12+batch12+cwd2+root4,각새범위첫PASS. 이전검사재실행0. 실제256x640row subsetbytes동일1회,manufacturedgzip/fsync9sample,syntax2blocks,제조archivepayload2/2member3은별도근거.
단일독립C9에서cgroup호환성finding1수정,openblocker0. 같은검토를R6/C9에재사용. R/C이번단위는게시보존영수증범위내마감,실제nativecanary는pending. plugin1.3과초기standalone1.0이력을구분하되버전때문에반복하지마.
작은row probe는직렬0.7128s/병렬1.1771s로병렬이느렸다. 제조I/O중앙값1.9774→0.6100s(3.242x)는그범위만이다. 이전pair의table비율3.79%,table만제거한상한1.0394x. 실제NCP64/HE29속도미측정. 기존8.35–8.78x와1.38–1.53x배율및새I/O배율을곱하지마.

[실제 다음 한 작업]
과거ABI1/ABI2인계의중복을제거하면ready미완료HE29과학job은r4/table512 packedcanary1개다. 다른모델C2H1/C2H2및연속모형HOLD를임의로readyqueue에넣지마.
새code 802a32361288bf5aa0e0d1f63c912768f1a1d407; packedcore a5d4711460c09b310b78c9692aa62534b7a843d3; watchdog ed5adca43f474553a9bce7f5de45d464be5905cb; VigilODE a21d573980f66fe02891bd216153443b5352f921.
NCP_HANDOFF의고정Gitcheckout과ncp/RUN_READY.sh를사용. actualhostobserve→baseline/dataidentity→bridge재사용또는compile→tablecache→thread1canary→raw/admit/returnarchive. 새solver/무조건grid확대/oldtransport/benchmark/완료tests재실행금지.
baseline /root/HE29_REFERENCE_20261020T120000Z의references,build,venv재사용.
DATA /root/HE29_NCP_20261020T105630Z/checkouts/baseline1569/research/he29_survival_budget_20261018 재사용. source/manifest는a5Git. INPUT복원만을위해START_REFERENCES/PUBLISH를부르지마.
Python3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0],NumPy2.3.5,SciPy1.17.0; r4table SHA919ca6f42028bffc37cb208916ee5a9927356eb99344fe467f9b98e30e9fddcd.
전체table이sameNCPcohort에서goldenSHA를재현하는지는아직실행전gate다.

[보존]
이전77324b4c,9092f990DropboxrawPASS재사용. 원래intake8350/7a86/f6/567DriveUNKNOWN은변하지않는다.
이번stage1 BASS_HE_HE29_HPC64_INTAKE_20261021_4e3a8030.tar.gz,15195bytes,SHA4e3a8030d7d7d6e0e3f1e4767cf282750252f75090502f380f9612dd017a8d87,Dropboxid:BSpOijBcT10AAAAAAD_aGA,payload9/member10rawPASS. 새Driveupload1회는ACK/ID없음,requested55초deadline미작동,640.2초후parentinterrupt. 실제human취소가아니다. exactname1회NOT_FOUND_OBSERVED,UNKNOWN유지,재시도/우회0. 이후Drive추가호출금지유지.
이번code/research backup: BASS_HE_HE29_HPC64_CODE_RESEARCH_20261021_aa274776.tar.gz,135774bytes,SHAaa27477614c4b4670901d5d891aa1835d0e928030368eb59ff7b449432131ae0,Dropboxid:BSpOijBcT10AAAAAAD_aHQ,실제payload70/member71rawPASS,Drive0. 최신docs/finalcloseoutarchive identity는현재DELIVERY와각BACKUP_RECEIPT,PR78본문을실제로읽어. 백업성공을과학동등성으로해석하지마.

[과학 gate]
absfraction1e-11,방법간온도1e-9K,number3e-15/H,energy3e-12eV/H,species3e-12,원래positivity,rtol1e-10/atol_scaled1e-12및19ledger full-state norm유지. finite-candidate hull은저장된수치후보범위이며trueODEerrorradius가아니다. 연속스펙트럼/전역온도상한/전체EoR/wholeGrackle/관측Bianchi-CMB HOLD.
각단계에서재사용/새실행,실제DAG/Git게시/백업상태를구분해기록해.
```
