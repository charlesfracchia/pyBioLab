from distutils.core import setup
import os

def getDeviceDirectories(dir):
    """Get the subdirectories for each device brand"""
    pass
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

def autoPopulatePackages():
    """Add each device brand folder to the list of packages to be built"""
    pass
    devicesPath = os.getcwd()+'/pybiolab/devices'
    brandDirs = getDeviceDirectories(devicesPath)
    for brand in brandDirs:
        packages.append('pybiolab.devices.' + brand)
    
packages=[
    'pybiolab',
    'pybiolab.classes',
    'pybiolab.classes.medical', #add dynamically in future by modifying autoPopulate()
    'pybiolab.devices',
]

autoPopulatePackages()  #Automatically adds all the device definitions to the list of built packages

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
