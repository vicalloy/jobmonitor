from lbjobmonitor.storage import JobMonitorJsonStorage

from .data import DATA_DIR


def test_job_monitor_json_storage():
    storage = JobMonitorJsonStorage(base_path=DATA_DIR)
    obj = [1, 2, 3]
    data_type = "test_job_monitor_json_storage"
    storage.dump(data_type=data_type, obj=obj)
    assert storage.load(data_type=data_type) == obj
