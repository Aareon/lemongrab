def screen():
    """Try to get that damn screen. If you can't, it's probably headless"""
    try:
        from screeninfo import get_monitors
        resolution = get_monitors()
        return str(resolution[0]).strip('monitor()').split('+')[0]
    except:
        return None
