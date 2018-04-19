from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='lemongrab',
    version='0.1dev',
    author = "Aareon <https://github.com/Aareon>",
    packages=['lemongrab',],
    license='MIT License',
    long_description=long_description,
    install_requires=[
    'distro==1.0.4',
    'psutil==5.2.2',
    'py-cpuinfo==3.2.0',
    'screeninfo==0.3',
    'uptime==3.0.1'
    ],
)
