#!/usr/bin/env python

from setuptools import setup, find_packages
import tupload

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='tupload',
      version=tupload.__version__,
      description='Telegram bot to fetch files from the client',
      long_description=long_description,
      author='Ritiek Malhotra',
      author_email='ritiekmalhotra123@gmail.com',
      packages=find_packages(),
      entry_points={
            'console_scripts': [
                  'tupload = tupload.tupload:command_line',
            ]
      },
      url='https://www.github.com/ritiek/tupload',
      keywords=['telegram', 'bot', 'upload', 'download', 'files'],
      license='MIT',
      download_url='https://github.com/ritiek/tupload/archive/v' + tupload.__version__ + '.tar.gz',
      classifiers=[],
      install_requires=[
            'telepot',
      ]
     )
