#!/usr/bin/env python3
#
# queue and send URL notifications
#
#
# written by Andreas 'ads' Scherbaum
#
#
# license:
#  * MIT license (https://opensource.org/licenses/mit-license.php)
#
#
# version history:
#  * 2019-05-05: version 1.0


import sys
import os
import logging
import time
import requests
import uuid
import fcntl


# start logging with 'info'
logging.basicConfig(level = logging.INFO,
		    format = '%(levelname)s: %(message)s')



#######################################################################
# helper functions


# print_help()
#
# print the usage
#
# parameter:
#  none
# return:
#  none
def print_help():
    print("")
    print("Usage: %s <spool directory> [<URL>]" % (str(sys.argv[0])))
    print("")



# send_url()
#
# send a URL
#
# parameter:
#  - URL
# return:
#  - 0: OK
#  - 1: not ok, retry possible
#  - 2: not ok, no retry possible
def send_url(url):
    session = requests.session()
    rs = session.request('GET', url)

    ret = 2

    if (rs.status_code == 200):
        ret = 0
    elif (rs.status_code > 200 and rs.status_code < 399):
        ret = 1
    elif (rs.status_code == 400):
        ret = 1
    elif (rs.status_code == 408):
        ret = 1
    elif (rs.status_code == 429):
        ret = 1
    elif (rs.status_code > 400 and rs.status_code < 499):
        ret = 2
    elif (rs.status_code >= 500):
        ret = 1

    logging.debug("send_url: %s" % (str(ret)))

    return ret



# spool_url()
#
# add a URL to the spool directory
#
# parameter:
#  - URL
# return:
#  none
def spool_url(url, spool_directory):
    spool_file = os.path.join(spool_directory, str(uuid.uuid4()))

    try:
        f = open(spool_file, "w")
        f.write(url)
        f.close()
    except IOError:
        logging.error("Can't open spool file for writing!")
        sys.exit(1)

    logging.info("Placed message in spool: %s" % (url))



# lock_file()
#
# lock a lockfile
#
# parameter:
#  - lockfile name
# return:
#  - True if successful, False otherwhise
def lock_file(entry_lock):
    f = open(entry_lock, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False
    return True



# send_spool_entry()
#
# send a single spool entry
#
# parameter:
#  - message file name
# return:
#  none
def send_spool_entry(entry):
    entry_lock = entry + ".lock"

    # acquire lock on file
    if (lock_file(entry_lock) is True):
        # lock acquired, open message file
        logging.debug("Acquired lock for: %s" % (entry))
        try:
            f = open(entry, "r")
            url = f.read()
            f.close()
        except IOError:
            logging.error("Can't open spool file (%s) for reading!" % (entry))
            sys.exit(1)

        logging.debug("Sending message: %s" % (url))
        res = send_url(url)

        if (res == 0):
            logging.info("Successfully sent message from spool")
        elif (res == 1):
            logging.debug("Not successful sending message from spool, will try again")
        elif (res == 2):
            logging.info("Not successful sending message from spool, will not try again")

        if (res == 0 or res == 2):
            # either successfully sent, or no longer worth sending
            os.remove(entry)
            try:
                os.remove(entry_lock)
            except OSError:
                pass

        time.sleep(1)

    else:
        logging.debug("Can't acquire lock for: %s" % (entry))



# send_spool()
#
# go over all entries in spool directory and send them
#
# parameter:
#  - spool directory
# return:
#  none
def send_spool(spool_directory):
    entries = os.listdir(spool_directory)
    for entry in entries:
        entry_full = os.path.join(spool_directory, entry)
        entry_lock = entry_full + ".lock"
        if (os.path.isfile(entry_full) and not entry.endswith(".lock")):
            send_spool_entry(entry_full)




#######################################################################
# main

# requires one or two parameters
if (len(sys.argv) < 2):
    print_help()
    sys.exit(1)


spool_directory = str(sys.argv[1])
try:
    notification_url = str(sys.argv[2])
except IndexError:
    notification_url = ""


logging.debug("Spool directory: %s" % (spool_directory))
if (len(notification_url) > 0):
    logging.debug("Notification URL: %s" % (notification_url))
else:
    logging.debug("Send all notifications from spool")


if (os.path.exists(spool_directory)):
    if (os.path.isdir(spool_directory) is False):
        logging.error("Spool directory (%s) is not a directory!" % (spool_directory))
        sys.exit(1)
else:
    try:
        os.mkdir(spool_directory, 0o750)
        logging.debug("Created spool directory: %s" % (spool_directory))
    except PermissionError:
        logging.error("Could not create spool directory: %s" % (spool_directory))
        sys.exit(1)


# if a URL is provided, try sending it, otherwise spool it
if (len(notification_url) > 0):
    res = send_url(notification_url)
    if (res == 1):
        # place URL in spool
        spool_url(notification_url, spool_directory)
        time.sleep(1)
        # try again, once
        send_spool(spool_directory)
else:
    # cron job, check spool directory and send everything
    send_spool(spool_directory)

