'''
Created on Jan 15, 2014

@author: jshor
'''
from distutils.core import setup, Extension

module1 = Extension('InhibitionC',
                    sources = ['inhibition.cpp'])

setup (name = 'InhibitionInC',
       version = '1.0',
       description = 'This is a package using in Grid-to-Place Cells to \
       quickly calculate the inhibition.',
       ext_modules = [module1])