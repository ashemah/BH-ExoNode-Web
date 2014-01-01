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

        if 'manage.py' in cmdline and 'exo_node' in cmdline:
            print process.cmdline
            rspid = process.pid

    except psutil.AccessDenied:
        pass

process = psutil.Process(rspid)

print "Killing process"

process.kill()

print "Upgrading"

time.sleep(1)

print "Restarting..."

Popen('python manage.py runserver 0.0.0.0:8000', shell=True)

