import subprocess

def shell():
    """Get the current shell"""
    try:
        return subprocess.run("$SHELL --version", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip('\n').split('(')[0]
    except:
        return None
