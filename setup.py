from distutils.core import setup
import os

def getDeviceDirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

def autoPopulatePackages():
    devicesPath = os.getcwd()+'/pybiolab/devices'
    brandDirs = getDeviceDirectories(devicesPath)
    for brand in brandDirs:
        packages.append('pybiolab.devices.' + brand)
    
packages=[
    'pybiolab',
    'pybiolab.devices',
]

autoPopulatePackages()

requiredPackages=[
    'serial',
    'httplib',
    'urllib',
    'xbee',
]

setup(
    name='pyBioLab',
    version='0.1',
    author='Charles Fracchia',
    author_email='charlesfracchia@gmail.com',
    packages=packages,
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Python tools for automating biological equipment',
    long_description=open('README').read(),
    requires=requiredPackages,
    provides=packages,
)
