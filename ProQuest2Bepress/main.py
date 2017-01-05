import os
import subprocess
import sys
import time

import config
import p2b_exceptions as e
import transform as t
from util import j, strip_ext, listdir_fullpath, get_bname, get_ext, unzip
from etd import ETD


# Python 2.6's subprocess module does not have check_call
# We will add it here
if "check_output" not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


def poll_uploaddir(folder, seen_files):
    """
    Checks for new files in the upload dir.
    Parameters:
        seen_files: A list of already seen filepaths
    """
    before = dict([(f, None) for f in seen_files if os.path.isfile(f)])
    after = dict([(f, None) for f in listdir_fullpath(folder) if os.path.isfile(f)])
    added = [f for f in after if f not in before]
    if added: 
        return added
    return None


def run_listener():
    seen_files_f = open(".seen.txt", "a+")
    seen_files = [line.strip() for line in seen_files_f.readlines()]
    with open(".broken.txt", "a+") as b:
        seen_files += [line.strip() for line in b.readlines()]

    current_batch_files = dict()
    current_batch_times = dict()
    current_batch_etds = []

    # Main run loop
    while True:
        # List of all subdirectories directly below the UPLOAD_DIR
        departments = [f for f in listdir_fullpath(config.UPLOAD_DIR) if os.path.isdir(f)]
        for dept in departments:
            if dept not in current_batch_times:
                current_batch_times[dept] = int(time.time())
            if dept not in current_batch_files:
                current_batch_files[dept] = []

            bname = get_bname(dept)
            try:
                if config.SEND_EMAILS == 1:
                    config.RESULT_EMAILS = config.get_email_opt(bname).split(",")
            except e.InvalidConfig as ex:
                print "No email confiugred for %s option in [email]" % bname
                print "Skipping this folder until one is configured."
                continue
            new = poll_uploaddir(dept, seen_files)
            if new is not None:
                # There were new files. But are they already in our current batch?
                # If not, add them and reset our timeout counter.
                for newf in new:
                    if newf not in current_batch_files[dept]:
                        current_batch_times[dept] = int(time.time())
                        current_batch_files[dept] += new
                        print dept + ": Added: ", ", ".join(new)
                        break
            if len(current_batch_files[dept]) > 0 and (int(time.time()) - current_batch_times[dept]) > (config.BATCH_TIMEOUT * 60):
                # There were new files and it's been long enough. Unzip and process them.
                for new_f in current_batch_files[dept]:
                    seen_files += [str(os.path.join(dept, new_f))]
                    seen_files_f.write(str(os.path.join(dept, new_f)) + "\n")

                    if get_ext(new_f) == ".zip":
                        try:
                            dest_dir = j(config.WORKING_DIR, strip_ext(get_bname(new_f)))
                            unzip(new_f, dest_dir)
                            new_etd = ETD(dept.split("/")[-1], dest_dir)
                            current_batch_etds += [new_etd]
                        except e.MyException as ex:
                            # If we reach this point, one of the uploaded zips was not able to be processed.
                            # In this case we want to add it to .broken.txt so that the script can keep running while ignoring
                            # the file that caused the error.
                            print "There was a problem processing %s. An email has been sent detailing the issue." % new_f
                            print "Adding %s to .broken.txt. Please fix the issue, then remove the entry in .broken.txt!" % new_f
                            with open(".broken.txt", "a+") as b:
                                b.write(new_f + "\n")
                    else:
                        print "Non-zip file in upload directory!"

                t.process_batch(dept, current_batch_etds)

                # Finally, remove the current batch from our dictionary
                current_batch_files[dept] = []
                current_batch_etds = []

        time.sleep(config.SLEEP_TIME)


def main():
    try:
        config.load_config("settings.conf")
    except e.InvalidConfig as ex:
        print ex
        sys.exit()

    try:
        run_listener()
    except e.P2BException as ex:
        print "NOT sending email..."


if __name__ == '__main__':
    __package__ = "ProQuest2Bepress"
    main()
