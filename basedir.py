import sys
import os
if getattr(sys, 'frozen', False):
    basedir = os.path.join(sys._MEIPASS, 'data')
else:
    basedir = os.path.dirname(os.path.abspath(__file__))