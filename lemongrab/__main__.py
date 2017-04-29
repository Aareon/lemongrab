#!/usr/bin/env python3

from . import osclasses

def main():
    computer = osclasses.OS()
    specs = computer.fetch_specs()
    
    if 'Windows' in specs.uname:
        logo = osclasses.Windows(specs)
    elif 'Linux' in specs.uname:
        logo = osclasses.Linux(specs)
    else:
        logo = osclasses.NoLogo(specs)
    print(logo.display())
    

if __name__ == '__main__':
    main()