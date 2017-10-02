import subprocess

def motherboard():
    """For standard Linux installations with sys info files"""
    try:  
        manufacturer_and_name = subprocess.run("grep '' /sys/class/dmi/id/board_vendor && grep '' /sys/class/dmi/id/board_name", 
            shell=True, 
            stdout=subprocess.PIPE, 
            universal_newlines=True).stdout.split('\n')
        return manufacturer_and_name[0].strip(' '), manufacturer_and_name[1].strip(' ')
    except:
        # Thought you said standard?
        """For those fuckers that *don't* have standard insallations, let's try dmidecode."""
        try:
            manufacturer_and_name = subprocess.run("dmidecode | grep -A3 '^System Information'", 
                shell=True, 
                stdout=subprocess.PIPE, 
                universal_newlines=True).stdout.split('\n')
            motherboard_vendor = manufacturer_and_name[1].strip('\tManufacturer: ')
            motherboard_name = manufacturer_and_name[2].strip('\tProduct Name: ')
            if motherboard_vendor == 'System manufacturer' and motherboard_name == 'System Product Name':
            # Someone has some weird shit going on, I give up.
                return None, None
            else:
            # Ok, so that worked. Thanks dmidecode <3
                return motherboard_vendor, motherboard_name
        except:
            # We've exhausted our patches, maybe I'll find one in the future
            return None, None
