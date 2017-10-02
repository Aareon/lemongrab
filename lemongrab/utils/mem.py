try:
    import psutil
except:
    pass


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

def hdd():
    free_space = 0
    total_space = 0
    for item in psutil.disk_partitions():
        disk = psutil.disk_usage(item.mountpoint)
        free_space += disk.free
        total_space += disk.total
    return humanbytes(free_space), humanbytes(total_space)

def ram():
    mem = psutil.virtual_memory()
    return [humanbytes(mem.used), humanbytes(mem.total)]
