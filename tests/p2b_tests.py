import glob
import os
import shutil
import unittest

from ProQuest2Bepress import config, paths
from ProQuest2Bepress.util import listdir_fullpath, add_slash, j, bname, strip_ext, unzip
from ProQuest2Bepress import p2b_exceptions as ex


class MyTestCase(unittest.TestCase):

    def clean_dirs(self):
        # Remove everything from the UPLOAD_DIR and WORKING_DIR
        rm_files = glob.glob(config.UPLOAD_DIR + "/*")
        rm_files += glob.glob(config.WORKING_DIR + "/*")
        for f in rm_files:
            if os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                shutil.rmtree(f)

    # Called before each test is run.
    def setUp(self):
        # Read in the config values. We'll need them.
        config.load_config("settings.conf")

        self.clean_dirs()
        try:
            os.remove('./.seen.txt')
            os.remove('./.broken.txt')
        except OSError:
            pass

        self.test_dirs = [f for f in listdir_fullpath("./TestFiles/") if os.path.isdir(f)]
        self.zip_files = dict()
        self.etd_dirs = dict()
        for test_dir in self.test_dirs:
            # Get a list of the filename of every zip file in ./TestFiles/
            self.zip_files[test_dir] = [os.path.basename(f) for f in listdir_fullpath(test_dir) if os.path.isfile(f)]
            # Get a list of the basenames of every etd
            self.etd_dirs[test_dir] = [os.path.splitext(os.path.basename(f))[0] for f in self.zip_files[test_dir]]

    # Called after each test finishes
    def tearDown(self):
        self.clean_dirs()

    # Copy each zip from ./TestFiles/ to UPLOAD_DIR
    def addFiles(self):
        for test_dir in self.test_dirs:
            shutil.copytree(test_dir, config.UPLOAD_DIR + "/" + os.path.basename(os.path.normpath(test_dir)))


class TestUtilMethods(MyTestCase):

    def test_unzip(self):
        self.addFiles()
        for test_dir in self.test_dirs:
            upload_dir = os.path.join(config.UPLOAD_DIR, os.path.basename(test_dir)) + os.sep
            for i in range(len(self.zip_files[test_dir])):
                try:
                    unzip(j(upload_dir, self.zip_files[test_dir][i]), config.WORKING_DIR)
                except ex.P2BException as e:
                    print e
                    #email.email_failure(filename, error_msg, config.RESULT_EMAILS, config.SMTP_SERVER, config.SMTP_USER, config.SMTP_PASSWORD)
                # Check that a new directory was made for the etd
                self.assertTrue(os.path.exists(j(config.WORKING_DIR, self.etd_dirs[test_dir][i])))
                # Check that there are files present in the newly created directory
                self.assertTrue(glob.glob(j(config.WORKING_DIR, self.etd_dirs[test_dir][i], "/*")) is not None)


if __name__ == '__main__':
    print "WARNING: This test suite WILL remove everything from the configured directories!"
    response = raw_input("Really continue? (y/n) ")
    if response == "y":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)