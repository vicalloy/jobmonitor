lbjobmonitor
==========

[![image](https://secure.travis-ci.org/vicalloy/jobmonitor.svg?branch=master)](http://travis-ci.org/vicalloy/jobmonitor)
[![codecov.io](https://codecov.io/github/vicalloy/jobmonitor/coverage.svg?branch=master)](https://codecov.io/github/vicalloy/jobmonitor)

招聘网站信息监控工具，监控招聘网站工作岗位更新情况并发送通知。

## 目的

- 招聘网站的问题
	- 招聘网站每天都会显示大量的岗位更新，但大多岗位都是常年发布，要从这些岗位里过滤出真正更新的岗位并不容易。
	- 招聘网站的搜索功能还不够完善，做不了高度个性化的定制化搜索条件。
	- 专业论坛的招聘版块，几乎没有搜索功能。
- 这个工具可以做什么
	- 支持定制招聘网站搜索条件，并对网站提供的标准搜索功能进行少量增强。
	- 对检索到的工作岗位进行过滤，如果该岗位之前已发布过，自动忽略。
	- 可部署在服务器上，设置定时任务方式定时推送岗位更新，支持多种消息推送方式。
	- 新工作岗位通知方式支持：显示到控制台、保存到文件、发送到Slack（强烈推荐Slack）。注：如果想支持微信、邮件的通知，需要自行扩展。
	- 内置了51JOB和V2EX的支持。注：如需要支持其他招聘网站，需要自行进行扩展。

## 使用范例

- 初始化项目

```
$ mkdir jobs
$ cd jobs
$ pip install pipenv --upgrade
$ pipenv --python 3.6
$ pipenv shell
$ pipenv install lbjobmonitor
```


- 创建`jobs.py`。使用`python jobs.py`执行查询。
- 可在服务器上使用crontab设置定时任务，定期检查

```python
# jobs.py
import os

from lbjobmonitor.message import CLIMessageBackend
from lbjobmonitor.message import FileMessageBackend
from lbjobmonitor.monitor import QCWYJobMonitor
from lbjobmonitor.storage import JobMonitorJsonStorage


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR


def qcwy():
    params = {  # 51job的查询参数。51job设置好查询条件后发起查询，通过chrome的调试功能查看请求的具体参数。
        'saltype': '',  # 薪资范围
        'keyword': 'python',  # 关键词
        'postchannel': '0000',
        'keywordtype': '2',
        'jobarea': '080200',  # 地区编码
        'pagesize': '5',  # 每页记录数
        '': ''
    }
    storage = JobMonitorJsonStorage(base_path=DATA_DIR)  # 使用JSON方式将工作列表保存到当前目录
    message_backend_list = [  # 显示的推送方式
        CLIMessageBackend(),  # 显示到控制台
        FileMessageBackend(fn=os.path.join(DATA_DIR, 'jobs.txt'))  # 保存到文件
    ]

    monitor = QCWYJobMonitor(
        storage=storage, message_backend_list=message_backend_list)
		# monitor.max_page_idx = 1  # 最多查询页数，设置成1方便调试
    skip_words = ['AI']
    monitor.monitor_jobs(params=params, skip_words=skip_words)  # 执行查询


if __name__ == "__main__":
    qcwy()
```

## 构架说明

- JobMonitor # 工作岗位监控类，需要根据网站给出具体实现。
	- job_class
		- Job  # 将通过API查询返回的工作信息转换为标准的Job对象
	- storage
		- JobMonitorStorage  # 历史工作列表的存储实现类
	- message_backend_list
		- [BaseMessageBackend]  # 消息发送的后端实现

## 代码导航

- [monitor.py](https://github.com/vicalloy/jobmonitor/blob/master/lbjobmonitor/monitor.py)
	- JobMonitor  # 工作岗位监控基础类
	- QCWYJobMonitor  # 51JOB岗位监控实现
	- V2exJobMonitor  # V2EX岗位监控实现
- [storage.py](https://github.com/vicalloy/jobmonitor/blob/master/lbjobmonitor/storage.py)
	- JobMonitorStorage  # 存储区基础类
	- JobMonitorJsonStorage  # 将信息以json方式保存到文件的存储区实现
- [message.py](https://github.com/vicalloy/jobmonitor/blob/master/lbjobmonitor/message.py)
	- BaseMessageBackend 消息发送处理后端基础类
	- IMMessageBackend IM类消息的后端基础类
	- CLIMessageBackend 将消息发送到控制台
	- FileMessageBackend 将消息保存到文件
	- SlackMessageBackend 将消息发送到Slack
	- TelegramMessageBackend 将消息发送到Telegram
- [models.py](https://github.com/vicalloy/jobmonitor/blob/master/lbjobmonitor/models.py)
	- Job 岗位信息基础数据类
	- QCWYJob 51JOB的岗位信息解析类
	- V2exJob V2EX的岗位信息解析类
