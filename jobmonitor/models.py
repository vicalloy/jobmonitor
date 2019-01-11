class Job:

    def __init__(self, org_job_item=None, id="", name="", description=""):
        if org_job_item:
            self.parse(org_job_item)
        else:
            self.id = id
            self.name = name
            self.description = description

    def parse_job_id(self, org_job_item):
        return ""

    def parse_job_name(self, org_job_item):
        return ""

    def parse_job_description(self, org_job_item):
        return ""

    def parse(self, org_job_item):
        self.id = self.parse_job_id(org_job_item)
        self.name = self.parse_job_name(org_job_item)
        self.description = self.parse_job_description(org_job_item)


class QCWYJob(Job):

    def parse_job_id(self, org_job_item):
        return org_job_item.jobid.text

    def parse_job_name(self, org_job_item):
        return org_job_item.jobname.text

    def parse_job_description(self, org_job_item):
        description = org_job_item.coname.text
        description += '\n%s' % org_job_item.jobname.text
        description += '\n%s' % org_job_item.cotype.text
        description += '\n%s' % org_job_item.providesalary.text
        description += '\n%s' % org_job_item.workyear.text
        description += '\n%s' % org_job_item.jobarea.text
        description += '\n%s' % org_job_item.jobinfo.text
        description += '\n%s' % org_job_item.issuedate.text
        return description

    def parse(self, org_job_item):
        self.id = self.parse_job_id(org_job_item)
        self.name = self.parse_job_name(org_job_item)
        self.description = self.parse_job_description(org_job_item)
