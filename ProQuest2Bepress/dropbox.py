import re
import subprocess

import config

# Captures the URL
share_link_pattern = re.compile(r' > Share link: (.*)\n')


def upload_file(ifpath, ofpath):
    try:
        subprocess.check_call([config.DBUPLOADER_PATH, "upload", ifpath, ofpath])
    except subprocess.CalledProcessError as e:
        print e
        raise Exception("Error uploading file")


def share_file(fpath):
    output = subprocess.check_output([config.DBUPLOADER_PATH, "share", fpath])
    match = re.search(share_link_pattern, output)
    if match is not None:
        share_link = match.group(1)
        share_link = share_link[:-1] + "1"
        return share_link
    raise Exception("Error sharing file")