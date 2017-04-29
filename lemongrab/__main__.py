#!/usr/bin/env python3

from . import osclasses

if __name__ == '__main__':
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
    
