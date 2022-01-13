import requests
from bs4 import BeautifulSoup

from .models import Job, QCWYJob, V2exJob

__all__ = (
    "JobMonitor",
    "QCWYJobMonitor",
    "V2exJobMonitor",
)


class JobMonitor:
    url = ""
    job_class = Job
    max_page_idx = 999
    all_job_ids_data_type = "all_job_ids"

    def __init__(self, storage, message_backend_list=()):
        self.storage = storage
        self.message_backend_list = message_backend_list
        self.reset()

    def reset(self):
        self.old_job_ids = self.load_old_job_ids()
        self.all_job_ids = []
        self.new_job_ids = []
        self.new_jobs = []

    def load_old_job_ids(self):
        return self.storage.load(data_type=self.all_job_ids_data_type, default=[])

    def update_old_job_ids(self):
        return self.storage.dump(
            data_type=self.all_job_ids_data_type, obj=list(self.all_job_ids)
        )

    def get_org_job_item_list(self, params, page_idx=1):
        return []

    def get_jobs(self, params, page_idx=1):
        org_job_item_list = self.get_org_job_item_list(params, page_idx)
        return [self.job_class(e) for e in org_job_item_list]

    def need_notify(self, job, skip_words, params):
        return not self.need_skip(job, skip_words, params)

    def need_skip(self, job, skip_words, params):
        for w in skip_words:
            if w in job.name.lower():
                return True
            if w in job.detail.lower():
                return True
        return False

    def on_get_new_job(self, job):
        for message_backend in self.message_backend_list:
            message_backend.send_job_notify(job)

    def on_start(self):
        for message_backend in self.message_backend_list:
            message_backend.start()

    def on_finish(self):
        self.update_old_job_ids()
        for message_backend in self.message_backend_list:
            message_backend.send_jobs_notify(self.new_jobs, len(self.all_job_ids))
            message_backend.finish()

    def is_new_job(self, job):
        return job.id not in self.old_job_ids

    def monitor_jobs(self, params=None, skip_words=()):
        self.reset()
        self.on_start()

        page_idx = 1
        while page_idx <= self.max_page_idx:
            jobs = self.get_jobs(params, page_idx)
            if len(jobs) <= 0:
                break
            for job in jobs:
                if not self.need_notify(job, skip_words, params):
                    continue
                self.all_job_ids.append(job.id)
                if self.is_new_job(job):
                    self.new_job_ids.append(job.id)
                    self.new_jobs.append(job)
                    self.on_get_new_job(job)
            page_idx += 1
        self.on_finish()


class QCWYJobMonitor(JobMonitor):
    url = "http://appapi.51job.com/api/job/search_job_list.php"
    job_class = QCWYJob
    all_job_ids_data_type = "51job_all_job_ids"

    def get_org_job_item_list(self, params, page_idx=1):
        params["pageno"] = page_idx
        r = requests.get(self.url, params=params, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find_all("item")


class V2exJobMonitor(JobMonitor):
    url = "https://www.v2ex.com/api/topics/show.json?node_name=jobs"
    job_class = V2exJob
    all_job_ids_data_type = "v2ex_all_job_ids"
    max_page_idx = 1

    def get_org_job_item_list(self, params, page_idx=1):
        r = requests.get(self.url)
        return r.json()  # topics

    def need_notify(self, job, skip_words, params):
        if not super().need_notify(job=job, skip_words=skip_words, params=params):
            return False

        title_keywords = params.get("title_keywords", [])
        for k in title_keywords:
            if k in job.name:
                return True

        content_keywords = params.get("content_keywords", [])
        content = "%s %s" % (job.name, job.detail)
        content = content.lower()
        for k in content_keywords:
            if k not in content:
                return False
        return True
