import ConfigParser

from p2b_exceptions import InvalidConfig

# Time options
SLEEP_TIME = None
BATCH_TIMEOUT = None
# Directory options
UPLOAD_DIR = None
WORKING_DIR = None
DB_DIR = None
# XSLT options
XSLT_PATH = None
# SMTP options
SMTP_SERVER = None
SMTP_USER = None
SMTP_PASSWORD = None
# Email options
RESULT_EMAILS = None
# Dropbox options
DBUPLOADER_PATH = None
# email options
SEND_EMAILS = None

config = None


def valid_config():
    # Check that all options are present
    time_options = ['sleep_time', 'batch_timeout']
    for option in time_options:
        if (not config.has_option('time', option)) or (config.get('time', option) == ''):
            print "Missing option in [time]: %s" % option
            return False
    dirs_options = ['upload_dir', 'working_dir', 'dropbox_dir']
    for option in dirs_options:
        if (not config.has_option('dirs', option)) or (config.get('dirs', option) == ''):
            print "Missing option in [dirs]: %s" % option
            return False
    xslt_options = ['xslt_path']
    for option in xslt_options:
        if (not config.has_option('xslt', option)) or (config.get('xslt', option) == ''):
            print "Missing option in [xslt]: %s" % option
            return False
    smtp_options = ['smtp_server']
    for option in smtp_options:
        if (not config.has_option('smtp', option)) or (config.get('smtp', option) == ''):
            print "Missing option in [smtp]: %s" % option
            return False
    dropbox_options = ['dbuploader_path']
    for option in dropbox_options:
        if (not config.has_option('dropbox', option)) or (config.get('dropbox', option) == ''):
            print "Missing option in [dropbox]: %s" % option
            return False
    email_options = ['send_emails']
    for option in email_options:
        if (not config.has_option('email', option)) or (config.get('email', option) == ''):
            print "Missing option in [email]: %s" % option
            return False

    return True


def set_globals():
    global SLEEP_TIME, BATCH_TIMEOUT, UPLOAD_DIR, WORKING_DIR, DB_DIR, \
        XSLT_PATH, SMTP_SERVER, SMTP_USER, SMTP_PASSWORD, DBUPLOADER_PATH, SEND_EMAILS
    SLEEP_TIME = float(config.get('time', 'sleep_time'))
    BATCH_TIMEOUT = float(config.get('time', 'batch_timeout'))
    UPLOAD_DIR = config.get('dirs', 'upload_dir')
    WORKING_DIR = config.get('dirs', 'working_dir')
    DB_DIR = config.get('dirs', 'dropbox_dir')
    XSLT_PATH = config.get('xslt', 'xslt_path')
    SMTP_SERVER = config.get('smtp', 'smtp_server')
    DBUPLOADER_PATH = config.get('dropbox', 'dbuploader_path')
    SEND_EMAILS = int(config.get('email', 'send_emails'))
    # Optionals
    if config.has_option('smtp', 'smtp_user'):
        SMTP_USER = config.get('smtp', 'smtp_user')
    if config.has_option('smtp', 'smtp_password'):
        SMTP_PASSWORD = config.get('smtp', 'smtp_password')


def get_email_opt(directory):
    if not config.has_option('email', directory):
        raise InvalidConfig("Missing email mapping")
    return config.get('email', directory)


def load_config(filename):
    """
    Loads options from settings.conf into global variables.
    """
    global config
    config = ConfigParser.ConfigParser()
    config.read(filename)
    if not valid_config():
        raise InvalidConfig("Invalid config")
    set_globals()