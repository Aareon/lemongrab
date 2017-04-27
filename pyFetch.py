import sys
import os
import platform
import json
import getpass
import subprocess
import cpuinfo
import psutil
from screeninfo import get_monitors
from multiprocessing.pool import ThreadPool
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


def get_shell():
    return subprocess.run("$SHELL --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]


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
    if os == 'linux':
        manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        manufacturer = manufacturer_and_name[0]
        name = manufacturer_and_name[1]
    else:
        manufacturer = subprocess.run("wmic baseboard get manufacturer", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')[2].rstrip()
        name = subprocess.run("wmic baseboard get product", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n\t').split('\n')[2].rstrip()
    return manufacturer, name


def get_specs(username, uname, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=None, shell_version=None):
    specs = []
    specs.append('{}@{}'.format(username, uname.node))

    if 'linux' in uname.system.lower():
        specs.append('OS: {}'.format(system))
        specs.append('Kernel: {} Linux {}'.format(uname.machine, uname.release))
    else:
        specs.append('OS: {} {}'.format(uname.system, uname.release))
    specs.append('Uptime: {}'.format(uptime))

    if 'linux' in uname.system.lower():
        specs.append('Packages: {}'.format(packages))
        specs.append('Shell: {}'.format(shell_version))

    specs.append('HDD: {} / {} (Free/Total)'.format(disk_free, disk_total))

    specs.append('CPU: {} @ {}'.format(cpu_brand, cpu_hz))
    specs.append('RAM: {} / {} (Used/Total)'.format(mem_used, mem_total))

    if screen:
        specs.append('Resolution: {}'.format(screen))

    specs.append('Motherboard: {} {}'.format(motherboard_vendor, motherboard_name))

    for item in specs:
        print(item)

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

    if 'linux' in uname.system.lower():
        linux_future = pool.apply_async(linux)
        system = linux_future.get()

        packages_future = pool.apply_async(get_packages)
        packages = packages_future.get()

        shell_future = pool.apply_async(get_shell)
        shell = shell_future.get()

        motherboard_future = pool.apply_async(get_motherboard, ('linux',))
        motherboard_vendor, motherboard_name = motherboard_future.get()

        get_specs(username, uname, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=packages, shell_version=shell)
    else:
        motherboard_future = pool.apply_async(get_motherboard, ('windows',))
        motherboard_vendor, motherboard_name = motherboard_future.get()
        get_specs(username, uname, mem_total, mem_used, cpu_brand, cpu_hz, disk_free, disk_total, screen, motherboard_vendor, motherboard_name, packages=None, shell_version=None)
