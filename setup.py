#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='mongo_media_info',
      version='0.1',
      description='mongo-media-info',
      author='Velrok',
      packages=find_packages(),
      author_email='waldemar.schwan@gmail.com',
      url='https://github.com/Velrok/mongo-media-info',
      install_requires=['sh', 'PIL', 'requests', 'tmdb', 'pymongo'],
      dependency_links=['git+https://github.com/doganaydin/themoviedb@327be58d0dfef87f5fcdce3aaaa83e5a12a6e5af']
     )
