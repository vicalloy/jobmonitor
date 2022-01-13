import os

from lbjobmonitor.models import Job

d_job = Job(id="id", name="name", description="description")
d_job_1 = Job(id="id1", name="name1", description="description1")
d_job_2 = Job(id="id2", name="name2", description="description2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
