# E13C5/PR19 NCP 실행 반환

PASS_SCOPED_HOST_PARITY_AND_REDUCTION. Actual physics=1, exact reduction=1, 두 단계 actual exit=0. Fresh physics parity 일치, reducer PASS_SCOPED_POSTPROCESSING, 774 checks / 302 comparisons, failed=0 / disjoint=0. Source/lock 변경 및 retry 0회.

고정 scientific core `f2fefc0c51de41f8ea036a21ba2e0728c3260490`, delivery `b6c2d1468a63042d56b8cf4b3d13bc72dcff198a`. 기존 사용자 tracked/untracked 변경을 보존하고 detached worktree 및 새 archive 복원 경로를 사용했다. 발견한 기존 NCP evidence는 verify-only/NO_SCIENCE fixture였고 actual 성공 반환은 없었다. 이를 성공으로 재사용하지 않았다.

외부 archive 3455297 bytes / SHA `e2aac517d7088c5d5d17f7ee994c6b084a33a9c1df5e5e28eb99d5de6af8634f`, payload5 검증. 내부 archive 3843064 bytes / SHA `291b57399184bb3042ec1b3e0aae4a648b6ba909273d8dbd50752954df639cf3`, payload851 검증. 두 ZIP 모두 absolute/.. / symlink/중복 member 거절 및 CRC 검사를 수행했다. 19 runtime files의 크기·SHA와 immutable commit bytes가 일치하고 CONTINUATION_LOCK 자체 SHA `a1ccb4f352a7bd12d97419b09dc41bc2782332ae01c4a7b8173f3cdd3bcdbef7`도 전후 일치한다. 정확 source/input/PLAN/baseline hash는 NCP_EXECUTION_SUMMARY.json 및 CONTINUATION_IDENTITY.json에 보존한다.

실제 interpreter /usr/bin/python3, CPython 3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0], libmpdec 2.5.1, Linux. CPU affinity 0–63, guest topology는 HOST.json에 있다. 실제 cgroup /sys/fs/cgroup/user.slice/user-0.slice/session-2.scope: cpu.max=max 100000, memory.max=max; memory.current snapshot=10510827520 bytes. Runner root cgroup null 항목을 실제 scope 관찰로 보완했으며 science source는 수정하지 않았다. MemTotal=131885312 kB, MemAvailable=129165780 kB. Process1/thread1/MPI0, 허용 OMP/OPENBLAS/MKL/NUMEXPR threads1만 기록했다. 모든 환경이나 credential을 수집하지 않았다.

Actual wrapper argv:

```text
/usr/bin/python3 code/ncp_continue.py --package /root/BASS_HE_runtime/E13C5_SCIENTIFIC_291b57399184_20261011/BASS_HE_E13C5_INCOMING_ANCHOR_ENCLOSURE_20261011_v1 --out /root/BASS_HE_runtime/E13C5_NCP_RETURN_20261011_RUN01 --execute
```

Physics actual argv·RUN·stdout/stderr는 PHYSICS_HOST_RUN.json과 physics/NCP_RESULT.json, reducer argv·RUN·로그는 EXACT_REDUCTION_RUN.json에 보존했다. Physics child cap=180초/1GiB, outer wrapper=205초/1GiB, reducer=60초/1GiB. 시작 UTC 2026-10-11T00:46:15.900805+00:00, 종료 2026-10-11T00:46:43.208015+00:00. Physics child wall 26.822553433초, outer physics wall 26.983636982초, reduction wall 0.271999641초. Physics peak RSS 23552 KiB는 address-space cap과 다르다. Reduction의 별도 measured RSS는 reducer가 기록하지 않아 미측정이며 cap만 주장한다. Exit0, signal 없음, timeout 없음.

N512/P60 OFF0·OFF700 각각3segment, 동일 local certificate2 재사용 및 local enclosure4 신규. 새 coefficient evaluation4096. Physics canonical projection SHA `f4d0f8c7e37e5c8a013ab133af748173f3ef1a8247f413f4798fdb3518c04a86`가 baseline과 일치한다. Fresh raw RESULTS SHA `49925547da42c6233f0b62e50a7bd3f1de0a6beea775aee9291800d152c1a8f3`는 reducer current input SHA와 일치한다. Reduction projection file 전체419815 bytes / SHA `f0681b18032e4de92db2a4d4c867d00895cf761bbdb5a57c571fba6e0e01bb69` 일치. Canonical-object hash와 newline 포함 file hash를 구별한다. 첫 불일치 없음. 수치 반올림/제외/허용오차 변경 없음.

OFF0/OFF700만 교체하고 열 경로 유지, OFF/KF/GM 합 각각 유지. 세 gas history를 합산하지 않았다. 기존 독립 PASS_SCOPED 및 lineage review는 그대로 재사용하며 이번 실행자가 새 독립 과학 판정을 부여하지 않는다. Scope는 captured fixed-gas selected paths와 conditional exact reduction이며 physical model의 독립 데이터 검증이나 full first2/full spectrum 인증이 아니다.

전체 fresh output와 runner RETURN_MANIFEST를 보존했다. Report/summary 추가분은 FINAL_RETURN_MANIFEST로 별도 봉인한다. 첫 실패/repair 없음, 별도 preflight·suite·refinement·E13C4 반복·old continuous/native/gas/Newton·full first2 실행0. Publication 및 백업은 별도 actual delivery receipt가 기록하며 upload ACK와 remote restore를 구분한다.

baseline_RCT=OFF; actual atomic photon/heat/recoil=null; physical/production=HOLD; full first2=HOLD_RESOURCE_AUTHORIZATION; HE-F2/F09=OPEN; receiver adoption=SEPARATE; legacy Gamma alias3.543295=FAIL; uniform full-path certificate=false 유지.

다음 node E13C5_SELECTED_SUBSET_BUDGET_AND_MISSING_NODE_COMPLEMENT_CONTRACT는 준비 연구로 남긴다. 새 coefficient/solver0 기본이며 E13C6/full first2를 시작하지 않았다. Merge·타인 메시지0.
