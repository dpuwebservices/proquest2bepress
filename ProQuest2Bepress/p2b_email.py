from __future__ import absolute_import

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_success(dirname, addresses, smtp_server, smtp_user, smtp_password):
    """
    Email administrator a success message.
    Parameters:
        dirname: Name of unzipped ProQuest ETD directory
    """
    # Set up multipart message
    msg = MIMEMultipart()
    msg['Subject'] = '%s is ready for upload' % dirname
    msg['To'] = ', '.join(addresses)
    msg['From'] = "p2b@localhost"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Create and add body
    body = "%s/Output.xml is ready to be uploaded." % dirname
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    # Send the email using SMTP
    s = smtplib.SMTP(smtp_server, 25)
    if smtp_user and smtp_password:
        s.login(smtp_user, smtp_password)
    s.sendmail("p2b@localhost", addresses, msg.as_string())
    s.quit()


def email_batch_success(upload_folder, batchname, addresses, smtp_server, smtp_user, smtp_password):
    # Set up multipart message
    msg = MIMEMultipart()
    msg['Subject'] = '%s/%s/%s is ready for upload' % (upload_folder, batchname, batchname + '.xml')
    msg['To'] = ', '.join(addresses)
    msg['From'] = "p2b@localhost"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Create and add body
    body = "%s/%s/%s is ready to be uploaded to Bepress.\n" % (upload_folder, batchname, batchname + '.xml')
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    # Send the email using SMTP
    s = smtplib.SMTP(smtp_server, 25)
    if smtp_user and smtp_password:
        s.login(smtp_user, smtp_password)
    s.sendmail("p2b@localhost", addresses, msg.as_string())
    s.quit()


def email_batch_success_atts(upload_folder, batchname, etds_with_extra, addresses, smtp_server, smtp_user, smtp_password):
    # Set up multipart message
    msg = MIMEMultipart()
    msg['Subject'] = '%s/%s/%s is ready for upload with intervention needed' % (upload_folder, batchname, batchname + '.xml')
    msg['To'] = ', '.join(addresses)
    msg['From'] = "p2b@localhost"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Create and add body
    body = "%s/%s/%s is ready to be uploaded to Bepress.\n" % (upload_folder, batchname, batchname + '.xml')
    body += "In addition, you will need to upload some of the following attachments for the ETDs listed.\n"
    body += "You can find them in the etd folders in your department's dropbox folder.\n"
    body += "The full text attachment should already be configured.\n"
    for etd in etds_with_extra.keys():
        body += etd.etd_name + ': ' + ', '.join(etds_with_extra[etd]) + "\n"
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    # Send the email using SMTP
    s = smtplib.SMTP(smtp_server, 25)
    if smtp_user and smtp_password:
        s.login(smtp_user, smtp_password)
    s.sendmail("p2b@localhost", addresses, msg.as_string())
    s.quit()


def email_success_attachments(dirname, attachments, addresses, smtp_server, smtp_user, smtp_password):
    """
    Email administrator a success message with need for manual attachments.
    Parameters:
        dirname: Name of unzipped ProQuest ETD directory
    """
    # Set up multipart message
    msg = MIMEMultipart()
    msg['Subject'] = '%s requires manual intervention' % dirname
    msg['To'] = ', '.join(addresses)
    msg['From'] = "p2b@localhost"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Create and add body
    body = "%s/Output.xml is ready to be uploaded.\n" % dirname
    body += "Additionally the following files will need to be manually attached: \n"
    for att in attachments:
        body += os.path.basename(att) + "\n"
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    # Send the email using SMTP
    s = smtplib.SMTP(smtp_server, 25)
    if smtp_user and smtp_password:
        s.login(smtp_user, smtp_password)
    s.sendmail("p2b@localhost", addresses, msg.as_string())
    s.quit()


def email_failure(culprit, message, addresses, smtp_server, smtp_user, smtp_password):
    """
    Email administrator a failure message.
    Parameters:
        culprit: Name of file that resulted in an error
        message: Full message detailing error
    """
    # Set up multipart message
    msg = MIMEMultipart()
    msg['Subject'] = 'Processing of %s FAILED!' % culprit
    msg['To'] = ', '.join(addresses)
    msg['From'] = "p2b@localhost"
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # Create part from passed in message
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)

    # Send the email using SMTP
    s = smtplib.SMTP(smtp_server, 25)
    if smtp_user and smtp_password:
        s.login(smtp_user, smtp_password)
    s.sendmail("p2b@localhost", addresses, msg.as_string())
    s.quit()