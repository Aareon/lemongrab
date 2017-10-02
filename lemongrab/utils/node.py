import platform
try:
    import psutil
except:
    pass

def node():
    try:
        import psutil
    except:
        return None
    uname = platform.uname()
    return psutil.Process().environ()["USER"], uname.node
