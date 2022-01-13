import os

from lbjobmonitor.message import CLIMessageBackend, FileMessageBackend

from .data import DATA_DIR, d_job


def test_cli_message_backend():
    message_backend = CLIMessageBackend()
    message_backend.send_raw_message("hello")
    message_backend.send_job_notify(job=d_job)
    message_backend.send_jobs_notify(jobs=[d_job], all_job_count=10)

    message_backend = CLIMessageBackend(show_jobs_count=False)
    message_backend.send_jobs_notify(jobs=[d_job], all_job_count=10)


def test_file_message_backend():
    message_backend = FileMessageBackend(os.path.join(DATA_DIR, "jobs.txt"))
    message_backend.start()
    message_backend.send_raw_message("hello")
    message_backend.send_job_notify(job=d_job)
    message_backend.send_jobs_notify(jobs=[d_job], all_job_count=10)
    message_backend.finish()
