import platform
import getpass
import subprocess
import cpuinfo
import psutil
from screeninfo import get_monitors
from uptime import uptime

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

class LogoMaker:
    def __init__(self):
        computer = Computer()
        self.w = '\033[1;37;40m'
        self.y = '\033[1;33;40m'
        self.r = '\033[0;31;40m'
        self.lr = '\033[0;1;31m'
        self.g = '\033[0;32;40m'
        self.b = '\033[0;34;40m'
        self.xx = '\033[0m'

        self.username = f'{self.lr}{computer.username}{self.w}@{self.lr}{computer.uname.node}{self.xx}'
        self.kernel = f'{self.lr}Kernel: {self.xx}{computer.uname.machine}'
        
        if 'linux' in computer.uname.system.lower():
            self.system = f'{self.lr}OS: {self.xx}{computer.uname.system}'
            self.kernel = f'{self.lr}Kernel: {self.xx}{computer.uname.machine} Linux {computer.uname.release}'
        else:
            self.system = f'{self.lr}OS: {self.xx}{computer.uname.system} {computer.uname.release}'
        self.uptime = f'{self.lr}Uptime: {self.xx}{computer.uptime}'

        self.packages = None

        if 'linux' in computer.uname.system.lower():
            self.packages = f'{self.lr}Packages: {self.xx}{computer.packages}'

        self.shell = f'{self.lr}Shell: {self.xx}{computer.shell}'
        self.hdd = f'{self.lr}HDD: {self.xx}{computer.disk_free} / {computer.disk_total} (Free/Total)'
        self.cpu = f'{self.lr}CPU: {self.xx}{computer.brand} @ {computer.hz}'
        self.ram = f'{self.lr}RAM: {self.xx}{computer.mem_used} / {computer.mem_total} (Used/Total)'

        self.screen = None

        if computer.screen:
            self.screen = f'{self.lr}Resolution: {self.xx}{computer.screen}'

        self.motherboard = f'{self.lr}Motherboard: {self.xx}{computer.motherboard_vendor} {computer.motherboard_name}'
        
        if computer.os == 'ubuntu':
            self.ubuntu()
        elif computer.os == '10/8':
            self.win10_8()
        elif computer.os == 'win':
            self.old_win()
        else:
            self.n_a()

    def ubuntu(self):
        print(f"{self.w}              .-.                                                              {self.username}\n"
              f"{self.y}        .-'``{self.w}(|||)                                                             {self.system}\n"
              f"{self.y}     ,`\ \    {self.w}`-`{self.y}.                 88                         88               {self.kernel}\n"
              f"{self.y}    /   \ '``-.   `                88                         88               {self.uptime}\n"
              f"{self.y}  .-.  ,       `___:      88   88  88,888,  88   88  ,88888, 88888  88   88    {self.packages}\n"
              f"{self.y} (:::) :       {self.w} ___{self.y}       88   88  88   88  88   88  88   88  88    88   88    {self.shell}\n"
              f"{self.y}  `-`  `       {self.w},   :{self.y}      88   88  88   88  88   88  88   88  88    88   88    {self.hdd}\n"
              f"{self.y}    \   /{self.w} ,..-`   ,{self.y}       88   88  88   88  88   88  88   88  88    88   88    {self.cpu}\n"
              f"{self.y}     `./ {self.w}/    {self.y}.-.{self.w}`{self.y}        '88888'  '88888'  '88888'  88   88  '8888 '88888'    {self.ram}")
        if self.screen:
            print(
                f"{self.w}        `-..-{self.y}(   )                                                                          {self.screen}")
            print(
                f"{self.y}              `-`                                                                                           {self.motherboard}")
        else:
            print(
                f"{self.w}        `-..-{self.y}(   )                                                             {self.motherboard}")
        print(f"{self.y}              `-`{self.xx}")
        
    def win10_8(self):
        print(f"{self.b}                                  ..,   {self.username}\n"
              f"{self.b}                      ....,,:;+ccllll   {self.system}\n"
              f"{self.b}        ...,,+:;  cllllllllllllllllll   {self.kernel}\n"
              f"{self.b}  ,cclllllllllll  lllllllllllllllllll   {self.uptime}\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.shell}\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.hdd}\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.cpu}\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.ram}")
        if self.screen:
            print(f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.screen}\n"
                  f"                                        {self.motherboard}")
        else:
            print(f"{self.b}  llllllllllllll  lllllllllllllllllll   {self.motherboard}\n")

        print(f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  llllllllllllll  lllllllllllllllllll\n"
              f"{self.b}  `'ccllllllllll  lllllllllllllllllll\n"
              f"{self.b}           `'""*::  :ccllllllllllllllll\n"
              f"{self.b}                        ````''\"*::cll\n"
              f"{self.b}                                   ``")
        
    def old_win(self):
        print(f"{self.lr}         ,.=:^!^!t3Z3z.,\n"
              f"{self.lr}        :tt:::tt333EE3                  {self.username}\n"
              f"{self.lr}        Et:::ztt33EEE  {self.g}@Ee.,      ..,\n"
              f"{self.lr}       ;tt:::tt333EE7 {self.g};EEEEEEttttt33#   {self.system}\n"
              f"{self.lr}      :Et:::zt333EEQ. {self.g}SEEEEEttttt33QL   {self.kernel}\n"
              f"{self.lr}      it::::tt333EEF {self.g}@EEEEEEttttt33F    {self.uptime}\n"
              f"{self.lr}     ;3=*^```'*4EEV {self.g}:EEEEEEttttt33@.    {self.shell}\n"
              f"{self.b}     ,.=::::it=., {self.lr}` {self.g}@EEEEEEtttz33QF     {self.hdd}\n"
              f"{self.b}    ;::::::::zt33)   {self.g}'4EEEtttji3P*      {self.cpu}\n"
              f"{self.b}   :t::::::::tt33.{self.y}:Z3z..  {self.g}`` {self.y},..g.      {self.ram}")
        if self.screen:
            print(f"{self.b}   i::::::::zt33F {self.y}AEEEtttt::::ztF       {self.screen}\n"
                  f"{self.b}  ;:::::::::t33V {self.y};EEEttttt::::t3        {self.motherboard}")
        else:
            print(f"{self.b}   i::::::::zt33F {self.y}AEEEtttt::::ztF       \n"
                  f"{self.b}  ;:::::::::t33V {self.y};EEEttttt::::t3")
        print(f"{self.b}  E::::::::zt33L {self.y}@EEEtttt::::z3F        \n"
              f"{self.b} (3=*^```'*4E3) {self.y};EEEtttt:::::tZ`        \n"
              f"{self.b}             ` {self.y}:EEEEtttt::::z7          \n"
              f"{self.y}                 'VEzjt:;;z>*`        ")
        
    def n_a(self):
        print(
            f"{self.username}\n{self.system}\n{self.kernel}\n{self.uptime}\n{self.shell}\n{self.hdd}\n{self.cpu}\n{self.ram}")
        if self.screen:
            print(self.screen)
        print(
            f"{self.motherboard}\nThis OS does not have a logo added yet. Post an issue on the GitHub repository to request support")

class Computer(object):
    def __init__(self):
        linux_distro = ['ubuntu','fedora','mint']
        self.uname = platform.uname()
        self.username = getpass.getuser()
        self.uptime = ddhhmmss(int(uptime()))
        self.cpu = cpuinfo.get_cpu_info()
        self.brand = self.cpu['brand'].rstrip()
        self.hz = self.cpu['hz_actual']
        mem = psutil.virtual_memory()
        self.mem_total = humanbytes(mem.total)
        self.mem_used = humanbytes(mem.used)
        disk = psutil.disk_usage(".")
        self.disk_free = humanbytes(disk.free)
        self.disk_total = humanbytes(disk.total)
        self.screen = self.get_screen()

        if 'ubuntu' in self.uname.version.lower():
            self.os = 'ubuntu'
        elif 'windows' in self.uname.system.lower():
            if '10' or '8' in self.uname.release:
                self.os = '10/8'
            else:
                self.os = 'win'
        else:
            self.os = 'nothing'

        self.packages = None

        if self.os in linux_distro:
            self.packages = self.get_packages()
            manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
            self.motherboard_vendor, self.motherboard_name = manufacturer_and_name[0], manufacturer_and_name[1]
        else:
            self.motherboard_vendor = subprocess.run("wmic baseboard get manufacturer", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')[2].rstrip()
            self.motherboard_name = subprocess.run("wmic baseboard get product", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n\t').split('\n')[2].rstrip()


        try:
            self.shell = subprocess.run("bash --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
        except:
            self.shell = 'N/A'

    def get_screen(self):
        try:
            return str(get_monitors()[0]).strip('monitor()').split('+')[0]
        except:
            return None

    def get_packages(self):
        try:
            return subprocess.run("dpkg -l | grep -c '^ii'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
        except:
            return None

if __name__ == '__main__':
    make_logo = LogoMaker()
