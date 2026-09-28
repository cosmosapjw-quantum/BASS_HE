"""Conservative host inventory and worker admission."""
from dataclasses import dataclass
from pathlib import Path
import math, os
@dataclass(frozen=True)
class HostInventory:
    affinity: int
    quota_cpus: int|None
    effective_memory: int|None
    memory_current: int|None
    data_mount: bool
    unknown_limits: tuple[str,...]
    @property
    def usable_cpus(self):return min(self.affinity,self.quota_cpus) if self.quota_cpus is not None else None

def _read(path):
    try:return path.read_text().strip()
    except (OSError,ValueError):return None

def inventory(data_path:Path=Path('/srv/bass-he')):
    affinity=len(os.sched_getaffinity(0));meminfo=_read(Path('/proc/meminfo'))
    osmem=int(next(x.split()[1] for x in meminfo.splitlines() if x.startswith('MemTotal:')))*1024 if meminfo else None
    groups=_read(Path('/proc/self/cgroup')) or ''; rel=next((x.split(':')[-1].lstrip('/') for x in groups.splitlines() if x.startswith('0::')),None)
    unknown=[];quota=[];memlimits=[];current=None
    if rel is None:unknown.append('cgroup path')
    else:
        path=Path('/sys/fs/cgroup')/rel
        while path.is_relative_to('/sys/fs/cgroup'):
            cpu=_read(path/'cpu.max');memory=_read(path/'memory.max')
            if cpu is None:unknown.append(str(path/'cpu.max'))
            elif cpu.split()[0]!='max':
                try:quota.append(max(0,int(cpu.split()[0])//int(cpu.split()[1])))
                except (ValueError,ZeroDivisionError):unknown.append(str(path/'cpu.max'))
            if memory is None:unknown.append(str(path/'memory.max'))
            elif memory!='max':
                try:memlimits.append(int(memory))
                except ValueError:unknown.append(str(path/'memory.max'))
            if path==Path('/sys/fs/cgroup'):break
            path=path.parent
        raw=_read(Path('/sys/fs/cgroup')/rel/'memory.current')
        try:current=int(raw) if raw is not None else None
        except ValueError:unknown.append('memory.current')
    effective=min([osmem,*memlimits]) if osmem else None
    if effective is None:unknown.append('effective memory')
    if current is None:unknown.append('memory.current')
    mountinfo=_read(Path('/proc/self/mountinfo')) or ''
    mount=data_path.is_mount() and any(
        line.split(' - ',1)[0].split()[4]==str(data_path) and line.split(' - ',1)[1].split()[0]=='ext4'
        for line in mountinfo.splitlines() if ' - ' in line
    )
    return HostInventory(affinity,min(quota) if quota else (affinity if rel is not None and not any('cpu.max' in x for x in unknown) else None),effective,current,mount,tuple(unknown))

def worker_limit(profile,host:HostInventory,ready_count:int,worker_rss_p95:int):
    if not host.data_mount:raise RuntimeError('BLOCKED_DATA_MOUNT')
    if worker_rss_p95 <= 0:raise ValueError('positive measured worker RSS required')
    if host.unknown_limits or host.usable_cpus is None or host.effective_memory is None or host.memory_current is None:raise RuntimeError('BLOCKED_UNKNOWN_RESOURCE_LIMIT')
    if host.memory_current >= .65*host.effective_memory:return 0
    reserve=int(profile.get('controller_reserve_bytes',0))+int(profile.get('memory_buffer_bytes',0))
    memworkers=max(0,math.floor((.75*host.effective_memory-reserve)/worker_rss_p95))
    return max(0,min(int(profile.get('workers',32)),host.usable_cpus,memworkers,ready_count))

def render_service(profile,host:HostInventory):
    if not host.data_mount or host.effective_memory is None:raise RuntimeError('BLOCKED_DATA_MOUNT_OR_MEMORY')
    soft=int(.65*host.effective_memory);hard=int(.75*host.effective_memory)
    return f'''[Unit]
Description=BASS HE replay %i
RequiresMountsFor=/srv/bass-he
After=local-fs.target
[Service]
Type=exec
User=bass-he
Group=bass-he
WorkingDirectory=/srv/bass-he/source/current
ExecStart=/srv/bass-he/env/current/bin/python scripts/run_cloud_replay.py resume --out /srv/bass-he/runs/%i
Restart=no
KillMode=control-group
TimeoutStopSec=15s
MemoryHigh={soft}
MemoryMax={hard}
NoNewPrivileges=yes
[Install]
WantedBy=multi-user.target
'''
