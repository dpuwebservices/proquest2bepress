import os


def add_slash(m):
    """
    Helper function that appends a / if one does not exist.
    Prameters:
        m: The string to append to.
    """
    if m[-1] != "/":
        return m + "/"
    else:
        return m


class Directory:
    path_string = None

    def __init__(self, in_string, ignore=False):
        if not ignore and not os.path.isdir(os.path.normpath(in_string)):
            raise OSError("Not a vaild path: " + in_string)

        self.path_string = add_slash(in_string)

    def as_string(self):
        return os.path.normpath(self.path_string)

    def basename(self):
        res = os.path.basename(os.path.normpath(self.path_string))
        return res

    def parent_dir(self, ignore=False):
        res_text = os.path.dirname(os.path.normpath(self.path_string).rstrip("/"))
        if not ignore and not os.path.isdir(res_text):
            raise OSError("Not a vaild path")
        return Directory(res_text, ignore=ignore)

    def append_dir(self, app_string, ignore=False):
        res_text = os.path.join(self.path_string, app_string)
        if not ignore and not os.path.isdir(res_text):
            raise OSError("Not a vaild path")
        return Directory(res_text, ignore=ignore)

    def append_file(self, app_string, ignore=False):
        res_text = os.path.join(self.path_string, app_string)
        if not ignore and not os.path.isfile(res_text):
            raise OSError("Not a vaild file")
        return Directory(res_text, ignore=ignore)


class File:
    file_string = None

    def __init__(self, in_string, ignore=False):
        if not ignore and not os.path.isfile(in_string):
            raise OSError("Not a vaild file: " + in_string)

        self.file_string = add_slash(in_string)

    def as_string(self):
        return os.path.normpath(self.file_string)

    def basename(self):
        res = os.path.basename(os.path.normpath(self.file_string))
        return res

    def extension(self):
        res = self.basename()
        res = os.path.splitext(res)[-1]
        return res

    def without_extension(self):
        res = self.basename()
        res = os.path.splitext(res)[0]
        return res

    def parent_dir(self, ignore=False):
        res_text = os.path.dirname(os.path.normpath(self.file_string).rstrip("/"))
        if not ignore and not os.path.isfile(res_text):
            raise OSError("Not a vaild directory")
        return Directory(res_text, ignore=ignore)