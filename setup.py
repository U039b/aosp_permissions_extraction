#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if sys.version_info.major == 3 and sys.version_info.minor < 3:
    print('Unfortunately, your python version is not supported!\n Please upgrade at least to python 3.3!')
    sys.exit(1)

if sys.platform == 'darwin' or sys.platform == 'win32':
    print('Unfortunately, we do not support your platform %s' % sys.platform)
    sys.exit(1)

install_requires = []

setup(name='aosp_permissions_extraction',
      version='1.0.0',
      description='Extract translated descriptions of permissions and groups from AOSP .',
      author='U+039b',
      author_email='forensic@0x39b.fr',
      url='https://github.com/U039b/aosp_permissions_extraction',
      packages=find_packages(exclude=['*.tests', '*.tests.*', 'test*', 'tests']),
      install_requires=install_requires,
      # zip_safe = False,
      scripts=['./aosp_permissions_extraction/extract_aosp_permissions.py'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Natural Language :: English',
          'Topic :: Security',
          'Topic :: Utilities',
      ]
      )
