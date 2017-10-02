import cpuinfo

def cpu():
    cpus = cpuinfo.get_cpu_info()
    num_cpus = cpus.get("count", "")
    hz_actual = cpus.get("hz_actual_raw", "")[0]
    hz_advertised = cpus.get("hz_advertised_raw", "")[0]

    cpu_brand = cpus.get("brand").strip("(R)").split(" ")
    new_cpu_brand = "".join(item + " " for item in cpu_brand if item != " ").rstrip(" ")

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
