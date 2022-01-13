import json
import os


class JobMonitorStorage:
    def load(self, data_type, default=None):
        pass

    def dump(self, data_type, obj):
        pass


class JobMonitorJsonStorage(JobMonitorStorage):
    def __init__(self, base_path):
        self.base_path = base_path

    def get_file_name(self, data_type):
        fn = "%s.json" % data_type
        return os.path.join(self.base_path, fn)

    def load(self, data_type, default=None):
        file_name = self.get_file_name(data_type=data_type)
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except EnvironmentError:
            print("oops")
        return default

    def dump(self, data_type, obj):
        file_name = self.get_file_name(data_type=data_type)
        with open(file_name, "w") as f:
            json.dump(obj, f)
