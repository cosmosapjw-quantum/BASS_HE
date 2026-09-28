from pathlib import Path
import importlib.util,pytest
spec=importlib.util.spec_from_file_location('cloud_cli',Path(__file__).resolve().parents[2]/'scripts/run_cloud_replay.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def test_missing_data_mount_precedes_run_creation(tmp_path,monkeypatch):
    from bass_he.cloud.resources import HostInventory
    monkeypatch.setattr(module,'inventory',lambda path:HostInventory(64,64,128*1024**3,0,False,()))
    out=Path('/srv/bass-he/runs/test-missing-mount')
    with pytest.raises(RuntimeError,match='BLOCKED_DATA_MOUNT'):module.admit_storage(out,{'storage_mode':'mounted_host','workers':1,'worker_rss_p95_bytes':1024})
    assert not out.exists()
def test_local_sandbox_caps_two(tmp_path):
    cap=module.admit_storage(tmp_path/'run',{'storage_mode':'local_sandbox','workers':32})
    assert cap(42)==2
