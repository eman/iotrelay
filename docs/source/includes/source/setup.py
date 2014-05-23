# source/setup.py

from setuptools import setup


setup(name='iotrelay-sample-source',
      install_requires=['iotrelay'],
      py_modules=['iotrelay_sample_source'],
      entry_points={
          'iotrelay': ['source=iotrelay_sample_source:DataSource']
      }
)
