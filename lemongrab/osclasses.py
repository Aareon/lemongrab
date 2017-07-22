import platform
import getpass
import subprocess
import psutil
import uptime
from collections import namedtuple
import os

# I KNOW IT'S UGLY
# I'M SORRY
# THIS NEEDS A LOT OF CLEANING UP

white = '\033[1;37;49m'
blue = '\033[0;34;49m'
red = '\033[0;31;49m'
light_red = '\033[1;31;49m'
green = '\033[0;32;49m'
yellow = '\033[1;33;49m'
lime = '\033[1;32;49m'
light_blue = '\033[1;34;49m'
reset = '\033[0m'


# Modified variables, this is to be made more dynamic in the future
text_color_dict = {'ubuntu': light_red, 'mint': lime, 'fedora': light_blue,
                   'windows$10': light_red, 'windows$8': light_red, 'windows7': green}
                   
distro_color_dict = {'ubuntu': (light_red, white, yellow), 
                     'mint': (lime, white), 'fedora': (blue, white),
                     'windows$10': (blue,), 'windows$8': (blue,),
                     'windows$7': (red, green, blue, yellow)}



                     
def ddhhmmss(seconds):
    minute, seconds = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    return "{0} days {1} hours {2} minutes".format(day, hour, minute)

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
    

class OS:
    def __init__(self):
        self.uname = platform.uname()
        self.username = getpass.getuser()
        self.uptime = ddhhmmss(int(uptime.uptime()))

        if self.check_cpu_info():
            x = ''
            cpu = self.cpuinfo.get_cpu_info()
            self.brand = [v for v in cpu['brand'].rstrip().split(' ') if v != x]
            for item in self.brand:
              x = x + item + ' '
            self.brand = x[:-1]
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
      """Get the version of bash currently installed. Needs patches"""
      try:
        return subprocess.run("bash --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
      except:
        return None


    def fetch_specs(self):
      """Create a pretty little tuple with all our specs"""
      Specs = namedtuple('Specs', 'uname username uptime brand hz shell mem_used mem_total disk_free disk_total screen')
      specs = Specs(uname=self.uname, username=self.username, uptime=self.uptime, brand=self.brand, hz=self.hz, shell=self.shell, mem_used=self.mem_used,
                    mem_total=self.mem_total, disk_free=self.disk_free, disk_total=self.disk_total, screen=self.screen)
      return specs


    def get_screen(self):
      """Try to get that damn screen. If you can't, it's probably headless"""
      try:
          from screeninfo import get_monitors
          screen = get_monitors()
          return str(screen[0]).strip('monitor()').split('+')[0]
      except:
          return None

    def check_cpu_info(self):
      """Try to get the cpu information, if you can't tell it to use psutil"""
      try:
          self.cpuinfo = __import__('cpuinfo')
          return True
      except:
          return False


class Linux:
    def __init__(self, specs):
      """Set arbitrary strings for attaching to the logo,
       maybe even fuck something up!"""
       
      self.distribution = self.get_distro()

      self.system = specs.uname.system
      self.release = specs.uname.release
      self.node = specs.uname.node
      self.logo, logo_name = get_logo(self.distribution, self.release)

      packages = self.get_packages(logo_name)

      self.motherboard_vendor, self.motherboard_name = self.get_motherboard()
      self.color =  text_color_dict.get(logo_name, light_red)
      
      self.username = '{0}{1}{2}@{0}{3}{4}'.format(self.color, specs.username, white, self.node, reset)
      self.kernel = '{0}Kernel: {1}{2} Linux {3}'.format(self.color, reset, specs.uname.machine, specs.uname.release)
      self.os = '{0}OS: {1}{2}'.format(self.color, reset, self.distribution.lstrip())
      self.uptime = '{0}Uptime: {1}{2}'.format(self.color, reset, specs.uptime)

      self.packages = ''
      if packages:
        self.packages = '{0}Packages: {1}{2}'.format(self.color, reset, packages)

      self.shell = '{0}Shell: {1}{2}'.format(self.color, reset, specs.shell)
      self.hdd = '{0}HDD: {1}{2} / {3} (Free/Total)'.format(self.color, reset, specs.disk_free, specs.disk_total)
      self.cpu = '{0}CPU: {1}{2} @ {3}'.format(self.color, reset, specs.brand, specs.hz)
      self.ram = '{0}RAM: {1}{2} / {3} (Used/Total)'.format(self.color, reset, specs.mem_used, specs.mem_total)

      self.screen = ''
      if specs.screen:
        self.screen = '{0}Resolution: {1}{2}'.format(self.color, reset, specs.screen)

      self.motherboard = ''
      if self.motherboard_vendor and self.motherboard_vendor:
        self.motherboard = '{0}Motherboard: {1} {2} {3}'.format(self.color, reset, self.motherboard_vendor.lstrip(), self.motherboard_name)
      
      self.dist_colors = distro_color_dict.get(logo_name, (white,))



    def get_distro(self):
      """Just get the name of the distro, if I can"""
      import distro
      distribution = ''
      for item in distro.linux_distribution():
          distribution += ' ' + item
      return distribution


    def get_packages(self, distro):
      """Attempt to get a number of installed packages."""
      if distro in ['ubuntu', 'mint']:
        try:
          return subprocess.run("dpkg -l | grep -c '^ii'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
        except:
          return None
      elif distro in ['fedora', 'centos']:
          return self.redhat_packages()


    def get_motherboard(self):
      """For standard Linux installations with sys info files"""
      try:  
        manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", 
                                               shell=True, 
                                               stdout=subprocess.PIPE, 
                                               universal_newlines=True).stdout.split('\n')
        return manufacturer_and_name[0].strip(' '), manufacturer_and_name[1].strip(' ')
      except:
        # Thought you said standard?
        return self.motherboard_patches()

    def redhat_packages(self):
      try:
        packages = subprocess.run("rpm -qa | wc -l", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
        if packages != '0':
          return packages
        else:
          return None
      except:
        return None

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
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.packages,
                                self.shell, self.hdd, self.cpu, self.ram, self.screen, self.motherboard, reset)
      else:
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.packages,
                                self.shell, self.hdd, self.cpu, self.ram, self.motherboard, self.screen, reset)


class Windows:
    def __init__(self, specs):
      self.system = specs.uname.system
      self.release = specs.uname.release
      self.node = specs.uname.node
      self.logo, logo_name = get_logo(self.system, self.release)

      self.color = text_color_dict.get(logo_name, light_red)

      self.username = '{0}{1}{2}@{0}{3}'.format(self.color, specs.username, white, self.node)
      self.kernel = '{0}Kernel: {1}{2} {3}'.format(self.color, reset, specs.uname.machine, specs.uname.release)
      self.os = '{0}OS: {1}{2} {3}'.format(self.color, reset, specs.uname.system, specs.uname.release)
      self.uptime = '{0}Uptime: {1}{2}'.format(self.color, reset, specs.uptime)
      self.shell = '{0}Shell: {1}{2}'.format(self.color, reset, specs.shell)
      self.hdd = '{0}HDD: {1}{2} / {3} (Free/Total)'.format(self.color, reset, specs.disk_free, specs.disk_total)
      self.cpu = '{0}CPU: {1}{2} @ {3}'.format(self.color, reset, specs.brand, specs.hz)
      self.ram = '{0}RAM: {1}{2} / {3} (Used/Total)'.format(self.color, reset, specs.mem_used, specs.mem_total)

      self.screen = ''
      if specs.screen:
        self.screen = '{0}Resolution: {1}{2}'.format(self.color, reset, specs.screen)

      motherboard_vendor = subprocess.run("wmic baseboard get manufacturer", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')[2].rstrip()
      motherboard_name = subprocess.run("wmic baseboard get product", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n\t').split('\n')[2].rstrip()
      self.motherboard = '{0}Motherboard: {1}{2} {3}'.format(self.color, reset, motherboard_vendor, motherboard_name)

      self.dist_colors = distro_color_dict.get(logo_name, (white,))

    def display(self):
      if self.screen:
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.screen, self.motherboard, reset)
      else:
        return self.logo.format(*self.dist_colors, self.username, self.os, self.kernel, self.uptime, self.shell, self.hdd, self.cpu, self.ram, self.motherboard, self.screen, reset)



def get_logo(system, release):
    versioned = ["windows"]
    os_name = system.lower().lstrip(' ')
    if ' ' in os_name:
        os_name = os_name.split(' ')
        if 'linux' in os_name:
            os_name.remove('linux')
        os_name = os_name[0]
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    
    if os_name in versioned:
        file = os.path.join(script_dir, "logos/{}${}".format(os_name, release))
    else:
        file =  os.path.join(script_dir, "logos/{}".format(os_name))
   
    #try:
    #    with open(file) as f:
    #        return f.read(), os_name
    #
    #except FileNotFoundError:
    #    return None
    with open(file) as f:
        if os_name not in versioned:
            return f.read(), os_name
        return f.read(), '{}${}'.format(os_name, release)
