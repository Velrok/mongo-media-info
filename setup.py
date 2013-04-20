#!/usr/bin/env python

from setuptools import setup, find_packages


find_packages()

setup(name='Distutils',
      version='0.0',
      description='mongo-media-info',
      author='Velrok',
      author_email='waldemar.schwan@gmail.com',
      url='https://github.com/Velrok/mongo-media-info',
      dependency_links=['https://github.com/doganaydin/themoviedb/archive/master.zip']
     )
