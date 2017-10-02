import subprocess

def packages():
    """Attempt to get a number of installed packages."""
    try:
        packages = subprocess.run("dpkg -l | grep -c '^ii'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
    except:
        try:
            packages = subprocess.run("rpm -qa | wc -l", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n')
        except:
            return None
    if packages != 0:
        return packages
