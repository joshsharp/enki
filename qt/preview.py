#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

class PreviewDialog(QDialog):
    
    def __init__(self,parent):
        QDialog.__init__(self,parent)
        self.setWindowTitle("Preview")
    