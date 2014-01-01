import os
import subprocess
from django.conf import settings
from django.http import HttpResponse
import psutil
import time


class DownloadManager(object):

    def __init__(self, download_dir, pidfile_filename, config_filename):

        self.pidfile_filename = pidfile_filename
        self.config_filename = config_filename
        self.download_dir = download_dir

    def launch_if_required(self):

        if os.path.exists(self.pidfile_filename):

            with open(self.pidfile_filename) as pidfile:

                self.pid = int(pidfile.readline())

                if psutil.pid_exists(self.pid):
                    process = psutil.Process(self.pid)

                    if process.status == psutil.STATUS_DEAD:
                        self.launch_downloader()
                else:
                    self.launch_downloader()
        else:
            self.launch_downloader()

    def launch_downloader(self):

        print "Launching download process..."

        if os.path.exists(self.pidfile_filename):
            os.unlink(self.pidfile_filename)

        process = subprocess.Popen('/usr/local/bin/aria2c --conf-path=%s --dir=%s' % (self.config_filename, self.download_dir),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   close_fds=True)
        time.sleep(1)

        with open(self.pidfile_filename, "wt") as pidfile:
            pid = "%d\n" % process.pid
            pidfile.write(pid)

    def add_download(self, url):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))
        gid = s.aria2.addUri([url])

        return gid

    def remove_download(self, gid):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))

        try:
            res = s.aria2.remove(gid)
            return res
        except xmlrpclib.Fault:
            return None

    def purge_results(self):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))
        res = s.aria2.purgeDownloadResult()

        return res

    def get_active_downloads(self):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))
        items = s.aria2.tellActive()

        return items

    def get_waiting_downloads(self):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))
        items = s.aria2.tellWaiting(0, 100)

        return items

    def get_stopped_downloads(self):

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://%s:%s/rpc' % (settings.ARIA2_HOST, settings.ARIA2_PORT))
        items = s.aria2.tellWaiting(0, 100)

        return items

