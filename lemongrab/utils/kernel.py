import platform

def kernel():
    uname = platform.uname()
    return [uname.machine, uname.system, uname.release]
