try:
    from slackclient import SlackClient  # NOQA
except ImportError:
    SlackClient = None
    pass


class BaseMessageBackend:

    def start(self):
        pass

    def send_job_notify(self, job):
        pass

    def send_jobs_notify(self, jobs, all_job_count):
        pass

    def send_raw_message(self, content, title=''):
        pass

    def finish(self):
        pass


class IMMessageBackend(BaseMessageBackend):

    def __init__(self, show_jobs_count=True):
        super().__init__()
        self.show_jobs_count = show_jobs_count

    def send_job_notify(self, job):
        content = '------------------------\n'
        content += "%s" % job.description
        self.send_raw_message(content)

    def send_jobs_notify(self, jobs, all_job_count):
        if not self.show_jobs_count:
            return
        content = '------------- job count: %s -------------\n' % all_job_count
        self.send_raw_message(content)


class CLIMessageBackend(IMMessageBackend):

    def send_raw_message(self, content):
        print(content)


class FileMessageBackend(IMMessageBackend):
    def __init__(self, fn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fn = fn

    def start(self):
        self.f = open(self.fn, 'a+')

    def finish(self):
        self.f.close()

    def send_raw_message(self, content):
        self.f.write(content)
        self.f.write('\n')


class SlackMessageBackend(IMMessageBackend):

    def __init__(self, slack_api_key, channel):
        super().__init__()
        self.slack_api_key = slack_api_key
        self.channel = channel

    def send_raw_message(self, content):
        if not SlackClient:
            print('you must install slackclient')
            return
        sc = SlackClient(self.slack_api_key)
        sc.api_call(
            "chat.postMessage",
            channel=self.channel,
            text=content
        )
