'''fsf'''
import graphic
from PyQt5.QtWidgets import QApplication, QWidget

import os
import sys


def main():
    '''fsf'''
    app = QApplication(sys.argv)

    para = graphic.para_interface()

    app.exec_(app.exec())


if __name__ == '__main__':
    main()
    
        