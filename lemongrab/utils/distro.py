try:
    import distro as dist
    import platform
except:
    pass

def distro():
    uname = platform.uname()
    distribution = ""
    if "linux" in uname.system.lower():
        return distribution.join(i + " " for i in dist.linux_distribution()).rstrip(" ")
    elif "windows" in uname.system.lower():
        return "windows"

def distro_txt():
    return dist.linux_distribution()[0].split(" ")[0]
