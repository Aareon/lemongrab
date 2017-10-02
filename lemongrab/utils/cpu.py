import cpuinfo

def cpu():
    cpus = cpuinfo.get_cpu_info()
    num_cpus = cpus.get("count", "")
    hz_actual = cpus.get("hz_actual_raw", "")[0]
    hz_advertised = cpus.get("hz_advertised_raw", "")[0]

    cpu_brand = cpus.get("brand").split(" @")[0].split(" ")

    # Some CPU brands have this weird character that fucks everything up
    while "" in cpu_brand:
        for i, e in enumerate(cpu_brand):
            if e == "":
                del cpu_brand[i]

    new_cpu_brand = "".join(i + " " for i in cpu_brand).rstrip(" ")

    if not num_cpus:
        num_cpus = ""
    else:
        num_cpus = "({})".format(num_cpus)

    cpu_average = 0
    if hz_actual and hz_advertised:
        cpu_average += ((hz_actual/1000000000) + (hz_advertised/1000000000))/2
    else:
        cpu_average = ""
    return new_cpu_brand, cpu_average, num_cpus
