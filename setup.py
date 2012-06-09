from distutils.core import setup

packages=[
    'pybiolab',
    'pybiolab.devices',
    'pybiolab.devices.newbrunswick',
]

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
