'''fsf'''
import graphic
from PySide2.QtWidgets import QApplication
import os
import sys


def main():
    '''fsf'''
    app = QApplication(sys.argv)

    app.setStyle(u"Fusion")

    para = graphic.para_interface()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
        