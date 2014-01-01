import os
from subprocess import Popen, call
import psutil
import time

cwd = os.getcwd()
print cwd

l = psutil.get_pid_list()

rspid = None

for pid in l:

    try:
        process = psutil.Process(pid)

        cmdline = str(process.cmdline)

        if 'manage.py' in cmdline:
            print process.cmdline
            rspid = process.pid
            break

    except psutil.AccessDenied:
        pass

if rspid is not None:
    process = psutil.Process(rspid)
    print "Killing process %d" % rspid
    process.kill()
    time.sleep(1)

print "Upgrading"

call('/usr/bin/git pull .', shell=True)
time.sleep(1)

print "Restarting..."

Popen('python manage.py runserver 0.0.0.0:8000', shell=True, close_fds=True)

