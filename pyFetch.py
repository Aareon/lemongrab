import platform
import getpass
import subprocess
import cpuinfo
import psutil
from screeninfo import get_monitors
from multiprocessing.pool import ThreadPool
from uptime import uptime

w = '\033[1;37;40m'
y = '\033[1;33;40m'
r = '\033[0;31;40m'
lr = '\033[0;1;31m'
g = '\033[0;32;40m'
b = '\033[0;34;40m'
xx = '\033[0m'

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


def linux():
    import distro
    distro_info = distro.linux_distribution()
    dist_name = distro_info[2].split(' ')[0]
    return '{} {} {}'.format(distro_info[0], distro_info[1], dist_name)


def get_uname():
    return platform.uname()


def get_user():
    return getpass.getuser()


def get_uptime():
    return ddhhmmss(int(uptime()))


def get_cpu():
    cpu = cpuinfo.get_cpu_info()
    brand = cpu['brand'].rstrip()
    hz = cpu['hz_actual']
    return brand, hz


def get_mem():
    mem = psutil.virtual_memory()
    return humanbytes(mem.total), humanbytes(mem.used)


def get_packages():
    return subprocess.run("dpkg -l | grep -c '^ii'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')


def get_shell(os):
    if 'linux' in os:
        return subprocess.run("$SHELL --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
    else:
        return subprocess.run("bash --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]


def get_disk():
    disk = psutil.disk_usage(".")
    return humanbytes(disk.free), humanbytes(disk.total)


def get_screen():
    try:
        screen = str(get_monitors()[0]).strip('monitor()').split('+')[0]
        return screen
    except:
        return None


def get_motherboard(os):
    if 'linux' in os:
        manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        manufacturer = manufacturer_and_name[0]
        name = manufacturer_and_name[1]
    else:
        manufacturer = subprocess.run("wmic baseboard get manufacturer", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')[2].rstrip()
        name = subprocess.run("wmic baseboard get product", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n\t').split('\n')[2].rstrip()
    return manufacturer, name

class LogoMaker:
    def __init__(self, username, os, kernel, uptime, packages, shell, hdd, cpu, ram, motherboard, screen=False):
        self.username = username
        self.os = os
        self.kernel = kernel
        self.uptime = uptime
        self.packages = packages
        self.shell = shell
        self.hdd = hdd
        self.cpu = cpu
        self.ram = ram
        self.motherboard = motherboard
        self.screen = screen

    def ubuntu(self):
        print(f"{w}              .-.                                                              {self.username}\n"
              f"{y}        .-'``{w}(|||)                                                             {self.os}\n"
              f"{y}     ,`\ \    {w}`-`{y}.                 88                         88               {self.kernel}\n"
              f"{y}    /   \ '``-.   `                88                         88               {self.uptime}\n"
              f"{y}  .-.  ,       `___:      88   88  88,888,  88   88  ,88888, 88888  88   88    {self.packages}\n"
              f"{y} (:::) :       {w} ___{y}       88   88  88   88  88   88  88   88  88    88   88    {self.shell}\n"
              f"{y}  `-`  `       {w},   :{y}      88   88  88   88  88   88  88   88  88    88   88    {self.hdd}\n"
              f"{y}    \   /{w} ,..-`   ,{y}       88   88  88   88  88   88  88   88  88    88   88    {self.cpu}\n"
              f"{y}     `./ {w}/    {y}.-.{w}`{y}        '88888'  '88888'  '88888'  88   88  '8888 '88888'    {self.ram}")
        if self.screen:
          print(f"{w}        `-..-{y}(   )                                                                          {self.screen}")
          print(f"{y}              `-`                                                                                           {self.motherboard}")
        else:
          print(f"{w}        `-..-{y}(   )                                                             {self.motherboard}")
        print(f"{y}              `-`{xx}")


    def win810(self):
        print(f"{b}                                  ..,   {self.username}\n"
              f"{b}                      ....,,:;+ccllll   {self.os}\n"
              f"{b}        ...,,+:;  cllllllllllllllllll   {self.kernel}\n"
              f"{b}  ,cclllllllllll  lllllllllllllllllll   {self.uptime}\n"
              f"{b}  llllllllllllll  lllllllllllllllllll   {self.shell}\n"
              f"{b}  llllllllllllll  lllllllllllllllllll   {self.hdd}\n"
              f"{b}  llllllllllllll  lllllllllllllllllll   {self.cpu}\n"
              f"{b}  llllllllllllll  lllllllllllllllllll   {self.ram}")
        if self.screen:
              print(f"{b}  llllllllllllll  lllllllllllllllllll   {self.screen}\n"
                    f"                                        {self.motherboard}")
        else:
            print(f"{b}  llllllllllllll  lllllllllllllllllll   {self.motherboard}\n")

        print(f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  llllllllllllll  lllllllllllllllllll\n"
              f"{b}  `'ccllllllllll  lllllllllllllllllll\n"
              f"{b}           `'""*::  :ccllllllllllllllll\n"
              f"{b}                        ````''\"*::cll\n"
              f"{b}                                   ``")


    def not_win10(self):
        print(f"{lr}         ,.=:^!^!t3Z3z.,\n"
              f"{lr}        :tt:::tt333EE3                  {self.username}\n"
              f"{lr}        Et:::ztt33EEE  {g}@Ee.,      ..,\n"
              f"{lr}       ;tt:::tt333EE7 {g};EEEEEEttttt33#   {self.os}\n"
              f"{lr}      :Et:::zt333EEQ. {g}SEEEEEttttt33QL   {self.kernel}\n"
              f"{lr}      it::::tt333EEF {g}@EEEEEEttttt33F    {self.uptime}\n"
              f"{lr}     ;3=*^```'*4EEV {g}:EEEEEEttttt33@.    {self.shell}\n"
              f"{b}     ,.=::::it=., {lr}` {g}@EEEEEEtttz33QF     {self.hdd}\n"
              f"{b}    ;::::::::zt33)   {g}'4EEEtttji3P*      {self.cpu}\n"
              f"{b}   :t::::::::tt33.{y}:Z3z..  {g}`` {y},..g.      {self.ram}")
        if self.screen:
            print(f"{b}   i::::::::zt33F {y}AEEEtttt::::ztF       {self.screen}\n"
                  f"{b}  ;:::::::::t33V {y};EEEttttt::::t3        {self.motherboard}")
        else:
            print(f"{b}   i::::::::zt33F {y}AEEEtttt::::ztF       \n"
                  f"{b}  ;:::::::::t33V {y};EEEttttt::::t3")
        print(f"{b}  E::::::::zt33L {y}@EEEtttt::::z3F        \n"
              f"{b} (3=*^```'*4E3) {y};EEEtttt:::::tZ`        \n"
              f"{b}             ` {y}:EEEEtttt::::z7          \n"
              f"{y}                 'VEzjt:;;z>*`        ")

    def nothing(self):
        print(f"{self.username}\n{self.os}\n{self.kernel}\n{self.uptime}\n{self.shell}\n{self.hdd}\n{self.cpu}\n{self.ram}")
        if self.screen:
            print(self.screen)
        print(f"{self.motherboard}\nThis OS does not have a logo added yet. Post an issue on the GitHub repository to request support")


def get_specs(username, uname, uptime, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=None, shell_version=None):
    username = f'{lr}{username}{w}@{lr}{uname.node}{xx}'
    kernel = f'{lr}Kernel: {xx}{uname.machine}'

    if 'linux' in uname.system.lower():
        os = f'{lr}OS: {xx}{system}'
        kernel = f'{lr}Kernel: {xx}{uname.machine} Linux {uname.release}'
    else:
        os = f'{lr}OS: {xx}{uname.system} {uname.release}'
    uptime = f'{lr}Uptime: {xx}{uptime}'

    packages = None

    if 'linux' in uname.system.lower():
        packages = f'{lr}Packages: {xx}{packages}'

    shell = f'{lr}Shell: {xx}{shell_version}'
    hdd = f'{lr}HDD: {xx}{disk_free} / {disk_total} (Free/Total)'
    cpu = f'{lr}CPU: {xx}{cpu_brand} @ {cpu_hz}'
    ram = f'{lr}RAM: {xx}{mem_used} / {mem_total} (Used/Total)'

    if screen:
        screen = f'{lr}Resolution: {xx}{screen}'

    motherboard = f'{lr}Motherboard: {xx}{motherboard_vendor} {motherboard_name}'
    make_logo = LogoMaker(username,os,kernel,uptime,packages,shell,hdd,cpu,ram,motherboard,screen)

    if 'ubuntu' in uname.version.lower():
        make_logo.ubuntu()
    elif 'windows' in uname.system.lower():
        if '10' or '8' in uname.release:
            #Add Win10 Logo!!!
            make_logo.win810()
        else:
            make_logo.not_win10()
    else:
        make_logo.nothing()

if __name__ == '__main__':
    pool = ThreadPool(processes=5)

    mem_future = pool.apply_async(get_mem)
    mem_total, mem_used = mem_future.get()

    uname_future = pool.apply_async(get_uname)
    uname = uname_future.get()

    username_future = pool.apply_async(get_user)
    username = username_future.get()

    uptime_future = pool.apply_async(get_uptime)
    uptime = uptime_future.get()

    cpu_future = pool.apply_async(get_cpu)
    cpu_brand, cpu_hz = cpu_future.get()

    disk_future = pool.apply_async(get_disk)
    disk_free, disk_total = disk_future.get()

    screen_future = pool.apply_async(get_screen)
    screen = screen_future.get()

    system = uname.system
    node = uname.node
    release = uname.release
    version = uname.version
    machine = uname.machine

    shell_future = pool.apply_async(get_shell, (system,))
    shell = shell_future.get()

    if 'linux' in uname.system.lower():
        linux_future = pool.apply_async(linux)
        system = linux_future.get()

        packages_future = pool.apply_async(get_packages)
        packages = packages_future.get()

        motherboard_future = pool.apply_async(get_motherboard, ('linux',))
        motherboard_vendor, motherboard_name = motherboard_future.get()

        get_specs(username, uname, uptime, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=packages, shell_version=shell)
    else:
        motherboard_future = pool.apply_async(get_motherboard, ('windows',))
        motherboard_vendor, motherboard_name = motherboard_future.get()
        get_specs(username, uname, uptime, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=None, shell_version=shell)
