u"""Sleep inhibitor to keep the operating system alive while streaming data"""

from __future__ import absolute_import
import platform


class WindowsInhibitor:
    u"""
    Prevent OS sleep/hibernate in windows; code from:\r\n
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py \r\n
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx
    """

    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    @staticmethod
    def inhibit():
        u"""Inhibit Windows from sleeping"""

        import ctypes
        print(u"Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS |
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    @staticmethod
    def release():
        u"""Allow Windows to sleep again"""

        import ctypes
        print(u"Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)


class LinuxInhibitor:
    u"""
    Prevent OS sleep/hibernate in Linux based systems; code from \r\n
    https://stackoverflow.com/a/61947613 \r\n
    """

    def __init__(self):
        pass

    COMMAND = u'systemctl'
    ARGS = [u'sleep.target', u'suspend.target', u'hibernate.target', u'hybrid-sleep.target']

    def inhibit(self):
        u"""Inhibit Linux distributions from sleeping"""

        import subprocess
        subprocess.run([self.COMMAND, u'mask', *self.ARGS])

    def release(self):
        u"""Allow Linux distributions to sleep"""

        import subprocess
        subprocess.run([self.COMMAND, u'unmask', *self.ARGS])


class MacInhibitor:
    u"""
    Prevent OS sleep/hibernate in Linux based systems; code from \r\n
    https://stackoverflow.com/a/61947613 \r\n
    TODO: This code is currently untested due to lack of hardware.
    """

    COMMAND = u'caffeinate'
    BREAK = '\003'

    _process = None

    def __init__(self):
        pass

    def inhibit(self):
        u"""Inhibit Mac from sleeping"""

        from subprocess import Popen, PIPE
        self._process = Popen([self.COMMAND], stdin=PIPE, stdout=PIPE)

    def release(self):
        u"""Allow Mac to sleep"""

        self._process.stdin.write(self.BREAK)
        self._process.stdin.flush()
        self._process.stdin.close()
        self._process.wait()


class SleepInhibitor:
    u"""Determines which operating system we are currently running on and uses the appropriate inhibitor."""

    operating_system = u''

    def __init__(self):
        self.operating_system = {
            u'Windows': WindowsInhibitor,
            u'Darwin': MacInhibitor,
        }.get(platform.system(), LinuxInhibitor)()

    def inhibit(self):
        u"""Inhibit the host operating system from sleeping"""

        self.operating_system.inhibit()

    def release(self):
        u"""Allow the host operating system to sleep again"""

        self.operating_system.release()
