#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='humans-of-paris',
      url='',
      author='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version='0.0.1',
      install_requires=[
          'numpy==1.15.1',
          'pytest==3.7.4',
          'rope==0.11.0',
          'autopep8==1.4',
          'yapf==0.23.0',
          'gunicorn==19.7.1',
          'eventlet==0.21.0',
          'gevent==1.4.0'
      ],
      include_package_data=True,
      zip_safe=False)
