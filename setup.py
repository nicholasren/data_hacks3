#!/usr/bin/env python

from distutils.core import setup

version = "0.0.1"
setup(name='data_hacks3',
      version=version,
      description='Command line utilities for data analysis',
      author=['Jehiah Czebotar', 'Xiaojun Ren'],
      author_email='nicholas.x.ren@gmail.com',
      url='https://github.com/nicholasren/datahacks3',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Intended Audience :: System Administrators',
            'Topic :: Terminals',
            ],
      download_url="http://github.com/downloads/nicholasren/data_hacks3/data_hacks3-%s.tar.gz" % version,
      scripts = ['data_hacks/histogram.py', 
                'data_hacks/ninety_five_percent.py',
                'data_hacks/run_for.py',
                'data_hacks/bar_chart.py',
                'data_hacks/sample.py']
     )
