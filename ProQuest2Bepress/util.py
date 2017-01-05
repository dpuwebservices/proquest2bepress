import contextlib
import os
import zipfile

import p2b_exceptions as e


def listdir_fullpath(d):
    """
    Returns directory listing with FULL paths.
    Parameters:
        d: The directory to list.
    """
    return [os.path.join(d, f) for f in os.listdir(d)]


def add_slash(m):
    """
    Helper function that appends a / if one does not exist.
    Parameters:
        m: The string to append to.
    """
    if m[-1] != "/":
        return m + "/"
    else:
        return m


def j(head, *tails):
    return os.path.join(head, *tails)


def get_bname(path):
    return os.path.basename(os.path.normpath(path))


def strip_ext(path):
    return ''.join(os.path.splitext(path)[0:-1])


def get_ext(path):
    return os.path.splitext(path)[-1]


def unzip(zip_path, dest_dir):
    try:
        os.mkdir(dest_dir)
    except OSError as ex:
        print dest_dir + ": " + "That directory already exists! Possible unclean runthrough?"
        print "Sending error report..."
        error_msg = "Tried to extract %s but %s already exists! This means that the script has already tried processing "\
                    "this file. The script has likely forgotten what files it has seen (check  that .seen.txt and .broken.txt exist)"\
                    % (zip_path, dest_dir)
        raise e.P2BException(error_msg, zip_path)

    try:
        with contextlib.closing(zipfile.ZipFile(zip_path, 'r')) as myzip:
            myzip.extractall(dest_dir)
    except IOError as ex:
        print zip_path + ": " + "No such file in upload directory!"
        print "Sending error report..."
        os.rmdir(dest_dir)
        error_msg = "Tried to extract %s but there was no such file!" % zip_path
        raise e.MyException(error_msg, zip_path)