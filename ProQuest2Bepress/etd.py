import os


class ETD:
    def __init__(self, department, directory):
        self.department = department
        self.etd_dir = directory
        self.etd_name = os.path.basename(os.path.normpath(self.etd_dir))

        # Scan for files in this ETD
        self.xml = None
        self.resource_files = []
        for dirpath, _, files in os.walk(self.etd_dir):
            for filen in files:
                filepath = os.path.join(dirpath, filen)
                if os.path.splitext(filepath)[1] != ".xml":
                    self.resource_files += [filepath]
                else:
                    self.xml = filepath

        if self.xml is None:
            raise Exception("ETD missing XML")

        if len(self.resource_files) > 1:
            self.has_add_attachments = True

