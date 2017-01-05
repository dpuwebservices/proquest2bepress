import lxml.etree as ET
import os
import re
import time
import subprocess

import config
import dropbox
import p2b_email as email
import p2b_exceptions as e
from regex import fulltext_pattern, xml_header_pattern
from util import j, get_bname


def dropboxify(etd):
    link_map = dict()
    for fpath in etd.resource_files:
        fname = os.path.basename(fpath)
        db_path = j(config.DB_DIR, etd.department, etd.etd_name, fname)

        try:
            dropbox.upload_file(fpath, db_path)
            share_link = dropbox.share_file(db_path)
            link_map[fname] = share_link
        except Exception as ex:
            print e
            print "Error uploading to dropbox!"
            print "Sending error report..."
            error_msg = "There was a problem uploading %s to Dropbox.\n"\
                        "Full error follows:\n"\
                        "%s" % (fname, ex)
            raise e.MyException(error_msg, etd.etd_name + ".zip")
    return link_map


def combine_xmls(xmls):
    out = """<?xml version="1.0" encoding="UTF-8"?>\r\n"""
    out += """<?xml-stylesheet type="text/xsl" href="result.xsl"?>\r\n"""
    out += """<DISS_Documents>"""
    for xml in xmls:
        with open(xml, "rb") as xmlf:
            xml_text = xmlf.read()
            stripped_xml_text = re.sub(xml_header_pattern, "", xml_text)
            out += stripped_xml_text
    out += """</DISS_Documents>"""
    return out


def xslt_transform(xml):
    dom = ET.fromstring(xml)
    xslt = ET.parse(config.XSLT_PATH)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    result = ET.tostring(newdom, pretty_print=True)
    return result

# We define a global link_map that can be read from replace_link()
# We will set this in replace_links to the appropriate link_map
global_link_map = dict()


def replace_link(m):
    """
    Takes a <fulltext-url> tag and replaces the relative URL with the appropriate Dropbox link.
    Parameters:
        m: The sting containing the full tag.
    """
    inner_link = m.group(1)
    try:
        new_link = global_link_map[inner_link]
    except Exception as ex:
        print "Unmatched file!"
        print "Sending error report..."
        error_msg = "A file referenced in the xml could not be mapped to a Dropbox url.\n"\
                    "Full error:\n"\
                    "%s" % ex
        raise e.MyException(error_msg)

    return "<fulltext-url>" + new_link + "</fulltext-url>"


def replace_links(xml, link_map):
    global global_link_map
    global_link_map = link_map
    new_xml_text = re.sub(fulltext_pattern, replace_link, xml)
    return new_xml_text


def process_batch(folder, etds):
    batchname = "batch" + str(int(time.time()))
    xmls = []
    master_link_map = dict()
    # This is a mapping of ETD -> a list of resource files
    # for ETDs that have >1 resources.
    # We need this for sending emails at the end.
    etds_with_extra = dict()
    for etd in etds:
        xmls += [etd.xml]
        print "Dropboxifying %s" % etd.etd_name
        new_link_map = dropboxify(etd)
        master_link_map.update(new_link_map)
        if len(etd.resource_files) > 1:
            extra_atts = [get_bname(rf) for rf in etd.resource_files]
            etds_with_extra[etd] = extra_atts
            print etd.etd_dir + ' has extra attachments. The FULL list:'
            print ", ".join(extra_atts)


    batch_dir = j(config.WORKING_DIR, batchname)
    try:
        os.mkdir(batch_dir)
    except OSError as ex:
        print config.WORKING_DIR + "/" + batchname + ": " + "That directory already exists! Possible unclean runthrough?"
        print "Sending error report..."
        error_msg = "Tried to create batch directory %s but it already exists! This means that the script has already tried processing "\
                    "this file. The script has likely forgotten what files it has seen (check  that .seen.txt and .broken.txt exist)"\
                    % batch_dir
        raise e.MyException(error_msg, batchname)

    print "Combining all XMLs..."
    combined = combine_xmls(xmls)
    print "Transforming combined XML using XSLT..."
    transformed = xslt_transform(combined)
    print "Replacing links..."
    finished = replace_links(transformed, master_link_map)
    print "Uploading finished batch XML..."
    finished_xml = batch_dir + "/" + batchname + ".xml"
    with open(finished_xml, "w+") as f:
        f.write(finished)
    upload_folder = os.path.basename(folder)
    subprocess.check_call([config.DBUPLOADER_PATH, "upload", finished_xml, config.DB_DIR + "/" + upload_folder + "/" + batchname + "/" + batchname + ".xml"])
    if config.SEND_EMAILS == 1:
        if len(etds_with_extra.keys()) > 0:
            email.email_batch_success_atts(upload_folder, batchname, etds_with_extra, config.RESULT_EMAILS, config.SMTP_SERVER, config.SMTP_USER, config.SMTP_PASSWORD)
        else:
            email.email_batch_success(upload_folder, batchname, config.RESULT_EMAILS, config.SMTP_SERVER, config.SMTP_USER, config.SMTP_PASSWORD)
    print "Done processing batch!"

