#!/usr/bin/env python
import os.path
import sys
# Setup script adapted from wal-e

# Version file managment scheme and graceful degredation for
# setuptools borrowed and adapted from GitPython.
try:
    from setuptools import setup, find_packages

    # Silence pyflakes
    assert setup
    assert find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Utility function to read the contents of short files.
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

VERSION = read(os.path.join('dvm', 'VERSION')).strip()

install_requires = [
    l for l in read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

tests_require = [
    'nose==1.2.1',
    'mock==1.0.0',
    'coverage==3.5.2',
]

setup(
    name="dvm",
    version=VERSION,
    packages=find_packages(),

    install_requires=install_requires,
    extras_require=dict(tests=tests_require),

    # metadata for upload to PyPI
    author="Brian Oldfield",
    author_email="brian@oldfield.io",
    description="Dotfile management made easy",
    long_description=read('README.md'),
    classifiers=['Topic :: Desktop Environment',
                 'Topic :: System :: Shells'],
    platforms=['any'],
    license="MIT",
    keywords=("shell bash dotfile"),
    url="https://github.com/boldfield/dvm",
    download_url='https://github.com/boldfield/dvm/tarball/{}'.format(VERSION),

    package_data={'dvm': ['VERSION']},

    # install command line utility
    entry_points={'console_scripts': ['dvm=dvm.cmd:main']})
