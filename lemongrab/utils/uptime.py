import uptime as up

def humantime(seconds):
    minute, seconds = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    return "{0} days, {1} hours, and {2} minutes".format(day, hour, minute)

def uptime():
    return humantime(int(up.uptime()))
