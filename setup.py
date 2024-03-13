from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ioiopype',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'my_package_cli=my_package.cli:main', #TBD
        ],
    },

    author='Martin Walchshofer',
    author_email='mwalchshofer@gmx.net',
    description='A realtime processing framework for python',
    license='MIT',
    url='https://github.com/MartinWalchshofer/ioiopype',
)