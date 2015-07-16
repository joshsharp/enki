#!/usr/bin/env python
from distutils.core import setup
import qt, twitter
import py2exe

setup(
    options = {
        'py2exe': {
     
            'includes': ['PySide.QtNetwork'],
     
        }
    },
    packages=['qt','twitter'],
    windows=['enki.py']
) 
