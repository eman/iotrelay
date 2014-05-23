# handler/setup.py

from setuptools import setup


setup(name='iotrelay-sample-handler',
      install_requires=['iotrelay'],
      py_modules=['iotrelay_sample_handler'],
      entry_points={
          'iotrelay': ['handler=iotrelay_sample_handler:Handler']
      }
)
