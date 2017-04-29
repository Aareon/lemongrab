import platform
import getpass
import subprocess
import psutil
import uptime
from collections import namedtuple


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

        self.shell = self.get_shell()


    def get_shell(self):
        try:
            self.shell = subprocess.run("bash --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
        except:
            self.shell = None


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
    def __init__(self, specs):
      """Set arbitrary strings for attaching to the logo,
       maybe even fuck something up!"""
      self.green = '\033[0;32;49m'
      self.lime = '\033[1;32;49m'
      self.white = '\033[1;37;49m'
      self.light_red = '\033[0;1;39m'
      self.yellow = '\033[1;33;49m'
      self.reset = '\033[0m'

      self.distribution = self.get_distro()

      self.system = specs.uname.system
      self.release = specs.uname.release
      self.node = specs.uname.node
      self.logo, logo_name = Logos(self.distribution, self.release)

      packages = self.get_packages()

      self.motherboard_vendor, self.motherboard_name = self.get_motherboard()

      self.color = self.text_colors(logo_name)
      self.username = '{0}{1}{2}@{0}{3}{4}'.format(self.color, specs.username, self.white, self.node, self.reset)
      self.kernel = '{0}Kernel: {1}{2} Linux {3}'.format(self.color, self.reset, specs.uname.machine, specs.uname.release)
      self.os = '{0}OS: {1}{2}'.format(self.color, self.reset, self.distribution)
      self.uptime = '{0}Uptime: {1}{2}'.format(self.color, self.reset, specs.uptime)

      self.packages = ''
      if packages:
        self.packages = '{0}Packages: {1}{2}'.format(self.color, self.reset, packages)

      self.shell = '{0}Shell: {1}{2}'.format(self.color, self.reset, specs.shell)
      self.hdd = '{0}HDD: {1}{2} / {3} (Free/Total)'.format(self.color, self.reset, specs.disk_free, specs.disk_total)
      self.cpu = '{0}CPU: {1}{2} @ {3}'.format(self.color, self.reset, specs.brand, specs.hz)
      self.ram = '{0}RAM: {1}{2} / {3} (Used/Total)'.format(self.color, self.reset, specs.mem_used, specs.mem_total)

      self.screen = ''
      if specs.screen:
        self.screen = '{0}Resolution: {1}{2}'.format(self.color, self.reset, specs.screen)

      self.motherboard = ''
      if self.motherboard_vendor and self.motherboard_vendor:
        self.motherboard = '{0}Motherboard: {1}{2} {3}'.format(self.color, self.reset, self.motherboard_vendor, self.motherboard_name)

      self.dist_colors = self.distro_colors(logo_name)


    def text_colors(self, logo_name):
      color_dict = {'ubuntu': self.light_red, 'mint': self.lime}
      return color_dict.get(logo_name, self.light_red)


    def distro_colors(self, logo_name):
      color_dict = {'ubuntu': (self.light_red, self.white, self.yellow), 'mint': (self.lime, self.white)}
      return color_dict.get(logo_name, (self.white,))


    def get_distro(self):
      """Just get the name of the distro, if I can"""
      import distro
      distribution = ''
      for item in distro.linux_distribution():
          distribution += ' ' + item
      return distribution


    def get_packages(self):
      """Attempt to get a number of installed packages. No patches available for this one, yet."""
      try:
        return subprocess.run("dpkg -l | grep -c '^ii'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
      except:
        return None


    def get_motherboard(self):
      """For standard Linux installations with sys info files"""
      try:  
        manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        return manufacturer_and_name[0], manufacturer_and_name[1]
      except:
        # Thought you said standard?
        return self.motherboard_patches()


    def motherboard_patches(self):
      """For those fuckers that *don't* have standard insallations, let's try dmidecode."""
      try:
        manufacturer_and_name = subprocess.run("dmidecode | grep -A3 '^System Information'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        motherboard_vendor = manufacturer_and_name[1].strip('\tManufacturer: ')
        motherboard_name = manufacturer_and_name[2].strip('\tProduct Name: ')
        if motherboard_vendor == 'System manufacturer' and motherboard_name == 'System Product Name':
          # Someone has some weird shit going on, I give up.
          return None, None
        else:
          # Ok, so that worked. Thanks dmidecode <3
          return motherboard_vendor, motherboard_name
      except:
        # We've exhausted our patches, maybe I'll find one in the future
        return None, None


    def display(self):
      """Display the specs gathered using the strings constructed in __init__"""
      if self.screen:
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.packages, self.shell, self.hdd, self.cpu, self.ram, self.screen, self.motherboard)
      else:
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.packages, self.shell, self.hdd, self.cpu, self.ram, self.motherboard, self.screen)


class Windows:
    def __init__(self, specs):
      self.white = '\033[1;37;49m'
      self.blue = '\033[0;34;49m'
      self.red = '\033[0;31;49m'
      self.light_red = '\033[0;1;49m'
      self.green = '\033[0;32;49m'
      self.yellow = '\033[1;33;49m'
      self.reset = '\033[0m'

      self.system = specs.uname.system
      self.release = specs.uname.release
      self.node = specs.uname.node
      self.logo, logo_name = Logos(self.system, self.release)

      self.username = '{0}{1}{2}@{0}{3}'.format(self.light_red, specs.username, self.white, self.node)
      self.kernel = '{0}Kernel: {1}{2} {3}'.format(self.light_red, self.reset, specs.uname.machine, specs.uname.release)
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

      if logo_name == 'windows810':
        self.colors = (self.blue,)
      else:
        self.colors = (self.red, self.green, self.blue, self.yellow)


    def display(self):
      if self.screen:
        return self.logo.format(*self.colors, self.username, self.os, self.kernel, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.screen, self.motherboard)
      else:
        return self.logo.format(*self.colors, self.username, self.os, self.kernel, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.motherboard, self.screen)



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
  windows7 = """{0}

         ,.=:^!^!t3Z3z.,
        :tt:::tt333EE3                  
        Et:::ztt33EEE  {1}@Ee.,      ..,   {4}{0}
       ;tt:::tt333EE7 {1};EEEEEEttttt33#   {5}{0}
      :Et:::zt333EEQ. {1}SEEEEEttttt33QL   {6}{0}
      it::::tt333EEF {1}@EEEEEEttttt33F    {7}{0}
     ;3=*^```'*4EEV {1}:EEEEEEttttt33@.    {8}{2}
     ,.=::::it=., ` {1}@EEEEEEtttz33QF     {9}{2}
    ;::::::::zt33)   {1}'4EEEtttji3P*      {10}{2}
   :t::::::::tt33.{3}:Z3z..  {1}`` {3},..g.      {11}{2}
   i::::::::zt33F {3}AEEEtttt::::ztF       {12}{2}
  ;:::::::::t33V {3};EEEttttt::::t3        {13}{2}
  E::::::::zt33L {3}@EEEtttt::::z3F        {2}
 (3=*^```'*4E3) {3};EEEtttt:::::tZ`        {2}
             ` {3}:EEEEtttt::::z7          {3}
                 'VEzjt:;;z>*`\033[0m
  """

  ubuntu = """{0}
                          ./+o+-       {3}{1}
                  yyyyy- {0}-yyyyyy+      {4}{1}
               ://+//////{0}-yyyyyyo      {5}{2}
           .++ {1}.:/++++++/-{0}.+sss/`      {6}{2}
         .:++o:  {1}/++++++++/:--:/-      {7}{2}
        o:+o+:++.{1}`..```.-/oo+++++/     {8}{2}
       .:+o:+o/.          {1}`+sssoo+/    {9}{1}
  .++/+:{2}+oo+o:`             {1}/sssooo.   {10}{1}
 /+++//+:{2}`oo+o               {1}/::--:.   {11}{1}
 \+/+o+++{2}`o++o               {0}++////.   {12}{1}
  .++.o+{2}++oo+:`             {0}/dddhhh.   {13}{2}
       .+.o+oo:.          {0}`oddhhhh+    {2}
        \+.++o+o`{0}`-````.:ohdhhhhh+    {2}
         `:o+++ {0}`ohhhhhhhhyo++os:    {2}
           .o:{0}`.syhhhhhhh/{2}.oo++o`       {0}
               /osyyyyyyo{2}++ooo+++/       {2}
                   ````` {2}+oo+++o\:
                          `oo++.\033[0m

  """

  mint = """
                                       {2}{0}
 MMMMMMMMMMMMMMMMMMMMMMMMMmds+.        {3}{0}
 MMm----::-://////////////oymNMd+`     {4}{0}
 MMd      {1}/++                {0}-sNMd:    {5}{0}
 MMNso/`  {1}dMM    `.::-. .-::.` {0}.hMN:   {6}{0}
 ddddMMh  {1}dMM   :hNMNMNhNMNMNh: {0}`NMm   {7}{0}
     NMm  {1}dMM  .NMN/-+MMM+-/NMN` {0}dMM   {8}{0}
     NMm  {1}dMM  -MMm  `MMM   dMM. {0}dMM   {9}{0}
     NMm  {1}dMM  -MMm  `MMM   dMM. {0}dMM   {10}{0}
     NMm  {1}dMM  .mmd  `mmm   yMM. {0}dMM
     NMm  {1}dMM`  ..`   ...   ydm. {0}dMM
     hMM- {1}+MMd/-------...-:sdds  {0}dMM
     -NMm- {1}:hNMNNNmdddddddddy/`  {0}dMM
      -dMNs-{1}``-::::-------.``    {0}dMM
       `/dMNmy+/:-------------:/yMMM{0}
          ./ydNMMMMMMMMMMMMMMMMMMMMM{0}
             \.MMMMMMMMMMMMMMMMMMM\033[0m
  """

  if 'windows' in system.lower():
    if '10' or '8' in release:
      return windows810, 'windows810'
    else:
      return windows7, 'windows7'
  elif 'ubuntu' in system.lower():
    return ubuntu, 'ubuntu'
  elif 'mint' in system.lower():
    return mint, 'mint'


if __name__ == '__main__':
    computer = OS()
    specs = computer.fetch_specs()
    if 'Windows' in specs.uname:
        logo = Windows(specs)
    elif 'Linux' in specs.uname:
        logo = Linux(specs)
    else:
        logo = No_Logo(specs)
    print(logo.display())
