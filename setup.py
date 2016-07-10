#!/usr/bin/env python
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))

description = 'IoT Relay - Relay data between data sources and destinations.'

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())

setup(name='iotrelay',
      version='1.2.0',
      description=description,
      long_description='\n\n'.join(long_descriptions),
      author='Emmanuel Levijarvi',
      author_email='emansl@gmail.com',
      url='http://iot-relay.readthedocs.org',
      license='BSD',
      py_modules=['iotrelay'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Home Automation',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3'],
      keywords='IoT relay time series',
      entry_points={
          'console_scripts': ['iotrelay=iotrelay:main'],
      })
