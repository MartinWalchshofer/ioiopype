from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

ver = {}
with open(os.path.join(dir, 'ioiopype', '__version__.py')) as v:
    exec(v.read(), ver)

pkg = find_packages()

setup(
    name='ioiopype',
    version=ver['__version__'],
    packages=pkg,
    install_requires=requirements,
    classifiers=[
        #'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',

        "Programming Language :: Python :: 3",
    ],
    author='Martin Walchshofer',
    author_email='mwalchshoferyt@gmail.com',
    description='A realtime processing framework for python',
    license='MIT',
    url='https://github.com/MartinWalchshofer/ioiopype',
)