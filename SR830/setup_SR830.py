#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "Gavin"

from setuptools import setup, find_packages


setup(name='SR830',
      version='0.0.1',
      description='A simple package controlling Standford SR830.',
      author='Gavin',
      author_email='jw.yu@zju.edu.cn',
      url='https://github.com/MrGavinYu/Automation',
	  py_modules=['SR830'],
      license="GPLv3",
      classifiers=[
		  "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3", 
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],

      python_requires='>=3.0',   # Python 的版本约束
			# 其他依赖的约束
      install_requires=[
          "pyvisa>=1.11.1",]
      )

