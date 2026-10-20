# HE29 후속 분석: 공유 기준해와 부분 반환

2026-10-20 05:57 UTC 재개 단위다. 최신 GitHub·관련 저장소·백업·로컬 반환을 먼저 읽었다. 확인 범위에서 새 HE29 기준해는 **0/4**다. 실제 미게시 NCP 프로세스는 관측하지 못했다. Remote Desktop Commander의 기존 월간 quota 및 재시도·재연결 금지 상태는 유지한다.

## 이 checkpoint의 실제 상태

| 축 | 상태와 근거 |
|---|---|
| DAG | R1/R2 intake 완료. 공유 기준해의 signed 분해와 부분 반환 분류 구현으로 진행 |
| 게시 | 직전 publication `1765522318438e966e61d8a72f12084550da399d`에서 이어지는 새 intake checkpoint. 실제 commit/readback은 후속 `evidence/INTAKE_PUBLICATION.json`에 기록 |
| 백업 | 직전 COMPLETE `77f1c73e…`와 CLOSEOUT `3380c7c4…`의 dual raw PASS 재사용. 새 checkpoint의 provider 접수·readback은 실제 반환 후 별도 기록 |
| 새 실행 | HE29 native 0, HE28 transport 0, 기존 source·최적화 검사 재실행 0 |

## 재사용과 새 작업의 경계

원래 HE29 science/test revision은 `1569f3718cd4b17a16936ad3d72bc7d5ed9b0f4f`, native owner는 `f7830e2f55e7a1938bc3c98f61b60651f8dae474`다. 완성된 ABI2 최적화 코드는 `a5d4711460c09b310b78c9692aa62534b7a843d3`, VigilODE는 `a21d573980f66fe02891bd216153443b5352f921`을 유지한다.

기존 `src/analyze_return.py`는 이미 time difference·mixed difference·sign change를 계산했다. 원본 archive의 저장된 `NATIVE_RETURN_AUDIT.json`을 DATA evidence로 복원했으며 계산을 다시 실행하지 않았다. 원본 member 및 SHA는 `evidence/reused/PROVENANCE.json`에 있다.

이번 구현은 다음 세 기능을 담당한다.

1. 저장된 transport 온도와 동일 model/table의 Radau·DOP853 기준 후보를 잇는 signed decomposition.
2. 같은 기준해 변수를 반복 사용한 계수를 먼저 합쳐 상쇄를 보존하는 정확한 선형식과 finite-candidate hull.
3. RESULT가 완성되기 전의 method-only·실패·timeout 상태 및 method별 시간의 판독.

finite-candidate hull은 저장된 두 수치 후보의 범위다. 참 ODE 해의 오차반경이나 연속 스펙트럼 인증을 뜻하지 않는다. 원래 물리식·반응률·허용치는 유지한다. 기준해가 없는 행은 HOLD로 출력한다.

## intake 근거

- `evidence/BASS_GITHUB_DELTA.json`: 83개 BASS_HE branch의 변경 대조, PR78 및 반환 채널.
- `evidence/RELATED_GITHUB_DELTA.json`: VigilODE·REI·REC·HH·BASS·bass_cr의 새 source/binary/result identity.
- `evidence/BACKUP_DELTA_INTAKE.json`: 이전 전체 census를 재사용한 최신 provider 변경분 및 실제 읽기 범위.
- `evidence/PERSONAL_CONTEXT_INTAKE.json`: 다른 대화 검색 오류 및 이전 파일 결과를 현재 실행 완료로 사용하지 않은 근거.
- `evidence/LOCAL_INTAKE_AND_GAPS.json`: 로컬 native 부재 관측과 기존 구현에서 확인한 분석 연결의 공백.

관련 프로젝트에는 새 실행 결과가 있지만 HE29 네 쌍의 계약과 다르다. 검색 회수·날짜 필터·미게시 프로세스의 관측 한계는 각각의 receipt에 남긴다.

## 다음 실제 실행

m8/GL4/q0의 `(r2,512)`, `(r4,512)`, `(r8,512)`, `(r4,1024)`에서 각각 Radau+DOP853. 반환된 case는 다시 실행하지 않는다. 네 쌍이 모두 admit된 뒤에만 단일 r4/table512 packed canary가 선택 가능하다. 실행은 Git의 고정 source에서 시작하고 archive에서는 검증된 DATA만 사용한다. 기존 인계의 두 실행 경계 patch를 유지한다.

연속 스펙트럼, 전역 gas-temperature 오차상한, 전체 EoR, upstream Grackle 전체 동등성, 관측 Bianchi/CMB는 해당 범위 검증 전까지 HOLD다.
