import os
import socket
import subprocess
import time
import errno
import psutil
from vlcrc import VLCRemote


class PlayerController(object):

    def __init__(self, vlc_path, pidfile, sockfile):
        self.vlc_pidfile = pidfile
        self.vlc_path = vlc_path
        self.sockfile = sockfile
        self.socket = None

    def __del__(self):
        if self.socket:
            self.socket.close()

    def connect(self):

        if self.socket is None:

            time.sleep(1)

            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.settimeout(2)
            self.socket.connect(self.sockfile)

    def send(self, cmd, start_if_required=True, is_short_cmd=False):

        if start_if_required:
            self.start_vlc_if_required()

        if not self.vlc_is_running():
            return None

        start_word = cmd.split(' ')[0]
        sentinel = '%s: returned 0 (no error)' % start_word

        self.connect()

        self.socket.send(cmd + '\n')

        ok = False

        msg = ''

        while True:

            try:
                data = self.socket.recv(1)

                if not data:
                    break
                else:
                    msg += data

                if msg.endswith('\r\n'):

                    msg = msg.strip()

                    if is_short_cmd:
                        break
                    else:
                        if msg == sentinel:
                            ok = True
                        else:
                            ok = False

                        print msg

                    msg = ''

            except socket.error, e:

                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK or err == 'timed out':
                    break

        print msg
        return msg.strip()

    def play(self, filename):
        self.send('clear')
        self.send('add ' + filename)

    def stop(self):
        pid = self.get_vlc_pid()
        process = psutil.Process(pid)
        process.kill()
        time.sleep(1)

    def pause(self):
        return self.send('pause')

    def seek(self, offset):
        return self.send('seek ' + str(offset))

    def jump_forward(self):
        time = self.get_time()
        return self.seek(time + 30)

    def jump_backward(self):
        time = self.get_time()
        return self.seek(time - 30)

    def get_time(self):
        return int(self.send('get_time', False, True))

    def get_length(self):
        return int(self.send('get_length', False, True))

    def get_title(self):
        return self.send('get_title', False, True)

    def get_is_playing(self):

        res = self.send('is_playing', False, True)
        if res:
            return res[:1] == '1'
        else:
            return False

    def get_vlc_pid(self):

        pid = None
        if os.path.exists(self.vlc_pidfile):
            with open(self.vlc_pidfile) as pidfile:
                pidstr = pidfile.readline()
                pidstr = pidstr.strip()
                if len(pidstr):
                    pid = int(pidstr)

        return pid

    def vlc_is_running(self):

        pid = self.get_vlc_pid()

        if pid and psutil.pid_exists(pid):
            process = psutil.Process(pid)

            if process.status == 'running':
                return True

        return False

    def start_vlc_if_required(self):

        if not self.vlc_is_running():
            self.start_vlc()

    def start_vlc(self):

        if os.path.exists(self.vlc_pidfile):
            os.unlink(self.vlc_pidfile)

        process = subprocess.Popen('%s --extraintf oldrc --rc-unix %s --rc-fake-tty --play-and-exit --quiet' % (self.vlc_path, self.sockfile),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   close_fds=True)

        time.sleep(1)

        with open(self.vlc_pidfile, "wt") as pidfile:
            self.pid = process.pid
            pid = "%d\n" % process.pid
            pidfile.write(pid)

