import platform
import getpass
import subprocess
import psutil
from collections import namedtuple
from utils import uptime

#os = ('linux', 'windows')
#system = uname.system
#name = ('windows 10/8', linux_distribution)
#distro = ('Microsoft Windows 10 Home (v10.0.15063) 64-bit', 'Ubuntu 16.04 Xenial Xerus')

def humanbytes(B):
   """Return the given bytes as a human friendly KB, MB, GB, or TB string"""
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)


def ddhhmmss(seconds):
    day = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minute = seconds // 60
    return "%d days %d hours %d minutes" % (day, hour, minute)

class OS:
    def __init__(self):
        self.uname = platform.uname()
        self.username = getpass.getuser()
        self.uptime = ddhhmmss(int(uptime.uptime()))

        if self.check_cpu_info():
            cpu = self.cpuinfo.get_cpu_info()
            self.brand = cpu['brand'].rstrip()
            self.hz = cpu['hz_actual']
        else:
            self.brand = platform.processor()
            self.hz = str(psutil.cpu_freq().max/1000) + ' GHz'

        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('.')

        self.mem_used = humanbytes(mem.used)
        self.mem_total = humanbytes(mem.total)

        self.disk_free = humanbytes(disk.free)
        self.disk_total = humanbytes(disk.total)

        self.screen = self.get_screen()

        try:
            self.shell = subprocess.run("bash --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
        except:
            self.shell = 'N/A'

    def fetch_specs(self):
        Specs = namedtuple('Specs', 'uname username uptime brand hz shell mem_used mem_total disk_free disk_total screen')
        specs = Specs(uname=self.uname, username=self.username, uptime=self.uptime, brand=self.brand, hz=self.hz, shell=self.shell, mem_used=self.mem_used,
                      mem_total=self.mem_total, disk_free=self.disk_free, disk_total=self.disk_total, screen=self.screen)
        return specs

    def get_screen(self):
        try:
            from screeninfo import get_monitors
            screen = get_monitors()
            return str(screen[0]).strip('monitor()').split('+')[0]
        except:
            return None

    def check_cpu_info(self):
        try:
            self.cpuinfo = __import__('cpuinfo')
            return True
        except:
            return False


class Linux:
    def __init__(self):
        import distro
        self.distribution = ''
        for item in distro.linux_distribution():
            self.distribution += ' ' + item


class Windows:
    def __init__(self, specs):
      self.white = '\033[1;37;40m'
      self.blue = '\033[0;34;40m'
      self.light_red = '\033[0;1;31m'
      self.reset = '\033[0m'

      self.system = specs.uname.system
      self.release = specs.uname.release
      self.node = specs.uname.node
      self.logo = Logos(self.system, self.release)

      self.username = '{0}{1}{2}@{0}{3}{4}'.format(self.light_red, specs.username, self.white, self.node, self.reset)
      self.kernel = '{0}Kernel: {1}{2}{3}'.format(self.light_red, self.white, specs.uname.machine, self.reset)
      self.os = '{0}OS: {1}{2} {3}'.format(self.light_red, self.reset, specs.uname.system, specs.uname.release)
      self.uptime = '{0}Uptime: {1}{2}'.format(self.light_red, self.reset, specs.uptime)
      self.shell = '{0}Shell: {1}{2}'.format(self.light_red, self.reset, specs.shell)
      self.hdd = '{0}HDD: {1}{2} / {3} (Free/Total)'.format(self.light_red, self.reset, specs.disk_free, specs.disk_total)
      self.cpu = '{0}CPU: {1}{2} @ {3}'.format(self.light_red, self.reset, specs.brand, specs.hz)
      self.ram = '{0}RAM: {1}{2} / {3} (Used/Total)'.format(self.light_red, self.reset, specs.mem_used, specs.mem_total)

      self.screen = ''
      if specs.screen:
        self.screen = '{0}Resolution: {1}{2}'.format(self.light_red, self.reset, specs.screen)

      motherboard_vendor = subprocess.run("wmic baseboard get manufacturer", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')[2].rstrip()
      motherboard_name = subprocess.run("wmic baseboard get product", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n\t').split('\n')[2].rstrip()
      self.motherboard = '{0}Motherboard: {1}{2} {3}'.format(self.light_red, self.reset, motherboard_vendor, motherboard_name)


    def display(self):
      if self.screen:
        return self.logo.format(self.blue, self.username, self.kernel, self.os, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.screen, self.motherboard)
      else:
        return self.logo.format(self.blue, self.username, self.kernel, self.os, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.motherboard, self.screen)



def Logos(system, release):
  # ---------------------- LOGOS START ----------------------------
  windows810 = """{0}
                                  ..,  {1}{0}
                      ....,,:;+ccllll  {2}{0}
        ...,,+:;  cllllllllllllllllll  {3}{0}
  ,cclllllllllll  lllllllllllllllllll  {4}{0}
  llllllllllllll  lllllllllllllllllll  {5}{0}
  llllllllllllll  lllllllllllllllllll  {6}{0}
  llllllllllllll  lllllllllllllllllll  {7}{0}
  llllllllllllll  lllllllllllllllllll  {8}{0}
  llllllllllllll  lllllllllllllllllll  {9}{0}
                                       {10}{0}
  llllllllllllll  lllllllllllllllllll
  llllllllllllll  lllllllllllllllllll
  llllllllllllll  lllllllllllllllllll
  llllllllllllll  lllllllllllllllllll
  llllllllllllll  lllllllllllllllllll
  llllllllllllll  lllllllllllllllllll
  `'ccllllllllll  lllllllllllllllllll
         `'""*::  :ccllllllllllllllll
                       ````''\"*::clll
                                   ``\033[0m

  """
  if 'windows' in system.lower():
    if '10' or '8' in release:
      return windows810
  else:
    return


if __name__ == '__main__':
    computer = OS()
    specs = computer.fetch_specs()
    if 'Windows' in specs.uname:
        logo = Windows(specs)
    elif 'Linux' in specs.uname:
        linux = Linux(specs)
    else:
        no_logo = No_Logo(specs)
    print(logo.display())
