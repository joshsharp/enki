#!/usr/bin/env python
from distutils.core import setup
import py2exe

setup(
    options = {
        'py2exe': {
     
            'includes': ['PySide.QtNetwork'],
     
        }
    },
    console=['main.py']
) 
