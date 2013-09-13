#!/usr/bin/env python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from qt.main import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
    
    sys.exit()

