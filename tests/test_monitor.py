import os

from lbjobmonitor.message import CLIMessageBackend, FileMessageBackend
from lbjobmonitor.models import Job
from lbjobmonitor.monitor import JobMonitor, QCWYJobMonitor, V2exJobMonitor
from lbjobmonitor.storage import JobMonitorJsonStorage

from .data import DATA_DIR, d_job, d_job_1, d_job_2


class SimpleJob(Job):
    def parse_job_id(self, org_job_item):
        return org_job_item.id

    def parse_job_name(self, org_job_item):
        return org_job_item.name

    def parse_job_description(self, org_job_item):
        return org_job_item.description


class SimpleJobMonitor(JobMonitor):
    job_class = SimpleJob
    max_page_idx = 1

    def get_org_job_item_list(self, params, page_idx=1):
        return params


def rm_file(base_fn):
    try:
        fn = os.path.join(DATA_DIR, base_fn)
        os.remove(fn)
    except EnvironmentError:
        print("oops")


def test_job_monitor():
    rm_file("all_job_ids.json")

    skip_words = ["1"]
    storage = JobMonitorJsonStorage(base_path=DATA_DIR)
    monitor = SimpleJobMonitor(
        storage=storage,
    )

    old_jobs = [d_job]
    monitor.monitor_jobs(params=old_jobs)
    assert monitor.old_job_ids == []
    assert monitor.all_job_ids == ["id"]
    assert monitor.new_job_ids == ["id"]
    assert monitor.new_jobs[0].id == d_job.id

    old_jobs = [d_job, d_job_1, d_job_2]
    monitor.monitor_jobs(params=old_jobs, skip_words=skip_words)
    assert monitor.old_job_ids == ["id"]
    assert monitor.all_job_ids == ["id", "id2"]
    assert monitor.new_job_ids == ["id2"]
    assert monitor.new_jobs[0].id == d_job_2.id


def test_51job_monitor():
    rm_file("51job_all_job_ids.json")

    params = {
        "saltype": "",
        "keyword": "python",
        "postchannel": "0000",
        "keywordtype": "2",
        "jobarea": "080200",
        "pagesize": "5",
        "": "",
    }
    storage = JobMonitorJsonStorage(base_path=DATA_DIR)
    message_backend_list = [
        CLIMessageBackend(),
        FileMessageBackend(fn=os.path.join(DATA_DIR, "jobs.txt")),
    ]

    monitor = QCWYJobMonitor(storage=storage, message_backend_list=message_backend_list)
    monitor.max_page_idx = 1
    monitor.monitor_jobs(params=params)
    assert monitor.old_job_ids == []
    assert len(monitor.all_job_ids) == 5


def test_v2ex_monitor():
    rm_file("v2ex_all_job_ids.json")

    params = {"title_keywords": ["[", "北", ","], "content_keywords": [], "": ""}
    skip_words = ["实习"]
    storage = JobMonitorJsonStorage(base_path=DATA_DIR)
    message_backend_list = [
        CLIMessageBackend(),
        FileMessageBackend(fn=os.path.join(DATA_DIR, "jobs.txt")),
    ]

    monitor = V2exJobMonitor(storage=storage, message_backend_list=message_backend_list)
    monitor.monitor_jobs(params=params, skip_words=skip_words)
    assert len(monitor.all_job_ids) > 0

    rm_file("v2ex_all_job_ids.json")
    params = {"title_keywords": [], "content_keywords": ["，"], "": ""}
    monitor.monitor_jobs(params=params, skip_words=skip_words)
    assert len(monitor.all_job_ids) > 0

    rm_file("v2ex_all_job_ids.json")
    params = {
        "title_keywords": ["aa bb cc dd xx"],
        "content_keywords": ["aa bb cc dd xx"],
        "": "",
    }
    monitor.monitor_jobs(params=params, skip_words=skip_words)
    assert len(monitor.all_job_ids) == 0
