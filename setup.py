from distutils.core import setup
import sys

if sys.version_info[:2] < (3, 0):
    sys.exit('lemongrab requires python 3 or higher.')

    
setup(
    name='lemongrab',
    version='0.1dev',
    author = "Aareon <https://github.com/Aareon>",
    packages=['lemongrab','logos'],
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=[
    'distro==1.0.4',
    'psutil==5.2.2',
    'py-cpuinfo==3.2.0',
    'screeninfo==0.3',
    'uptime==3.0.1'
    ],
    entry_points={
            'console_scripts': [
                'lemongrab = lemongrab.__main__:main'
            ]
        },
    
)
