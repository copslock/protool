from PyQt5.QtWidgets import  QWidget, QLabel, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QGridLayout

import pytest
from basedir import basedir
import os
import sys
from configparser import ConfigParser


class para_interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'para'
        self.left = 400
        self.top = 400
        self.width = 300
        self.height = 260
        self.initUI()
        
        

    def initUI(self):
        
        self.config = ConfigParser()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label_GPONSN = QLabel('GPONSN:')
        label_MAC = QLabel('MAC:')
        label_productclass = QLabel('productclass:')
        label_CustomerSWVersion = QLabel('CustomerSWVersion:')
        label_CustomerHWVersion = QLabel('CustomerHWVersion:')

        self.GPONSNlabel = QLabel('')
        self.MAClabel = QLabel('')
        self.productclasslabel = QLabel('')
        self.CustomerSWVersionlabel = QLabel('')
        self.CustomerHWVersionlabel = QLabel('')



        button_GPONSN = QPushButton("")
        button_GPONSN.clicked.connect(self.setGPONSN)
        button_MAC = QPushButton("")
        button_MAC.clicked.connect(self.setMAC)
        button_productclass = QPushButton("")
        button_productclass.clicked.connect(self.setproductclass)
        button_CustomerSWVersion = QPushButton("")
        button_CustomerSWVersion.clicked.connect(self.setCustomerSWVersion)
        button_CustomerHWVersion = QPushButton("")
        button_CustomerHWVersion.clicked.connect(self.setCustomerHWVersion)
        button_submit = QPushButton("submit")
        button_submit.clicked.connect(self.exec_interface)
        button_submit.clicked.connect(self.setconfigpara)



        layout = QGridLayout()
        layout.addWidget(label_GPONSN, 0, 0)
        layout.addWidget(self.GPONSNlabel, 0, 1)
        layout.addWidget(button_GPONSN, 0, 2)
        layout.addWidget(label_MAC, 1, 0)
        layout.addWidget(self.MAClabel, 1, 1)
        layout.addWidget(button_MAC, 1, 2)
        layout.addWidget(label_productclass, 2, 0)
        layout.addWidget(self.productclasslabel, 2, 1)
        layout.addWidget(button_productclass, 2, 2)
        layout.addWidget(label_CustomerSWVersion, 3, 0)
        layout.addWidget(self.CustomerSWVersionlabel, 3, 1)
        layout.addWidget(button_CustomerSWVersion, 3, 2)
        layout.addWidget(label_CustomerHWVersion, 4, 0)
        layout.addWidget(self.CustomerHWVersionlabel, 4, 1)
        layout.addWidget(button_CustomerHWVersion, 4, 2)
        layout.addWidget(button_submit, 5, 2)

        self.setconfigpara()
        self.setLayout(layout)
        self.show()
        


    def setconfigpara(self):
        path = os.path.join(basedir, 'config.ini')
        self.config.read(path, encoding='utf-8')
        self.config.set('produce', 'GPONSN', self.GPONSNlabel.text())
        self.config.set('produce', 'MAC', self.MAClabel.text())
        self.config.set('produce', 'productclass', self.productclasslabel.text())
        self.config.set('produce', 'CustomerSWVersion', self.CustomerSWVersionlabel.text())
        self.config.set('produce', 'CustomerHWVersion', self.CustomerHWVersionlabel.text())
        with open(path, 'w') as config_file:
            self.config.write(config_file)


    def setGPONSN(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "GPONSN:", QLineEdit.Normal,"")
        if okPressed and text != '':
            self.GPONSNlabel.setText(text)


    def setMAC(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "MAC:", QLineEdit.Normal,"")
        if okPressed and text != '':
            self.MAClabel.setText(text)



    def setproductclass(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "productclass:", QLineEdit.Normal,"")
        if okPressed and text != '':
            self.productclasslabel.setText(text)


            
    def setCustomerSWVersion(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "CustomerSWVersion:", QLineEdit.Normal,"")
        if okPressed and text != '':
            self.CustomerSWVersionlabel.setText(text)



    def setCustomerHWVersion(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "CustomerHWVersion:", QLineEdit.Normal,"")
        if okPressed and text != '':
            self.CustomerHWVersionlabel.setText(text)



    def exec_interface(self):
        self.widget = exec_interface()

class exec_interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'exec'
        self.reportpath = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "report.xml")
        self.left = 400
        self.top = 400
        self.width = 300
        self.height = 260
        self.initUI()
        

    def on_burn_button_clicked(self):
            path = os.path.join(basedir, "test_burn.py")
            pytest.main(args=[path, '--junitxml={}'.format(self.reportpath)])
    

    def on_check_button_clicked(self):
            path = os.path.join(basedir, "test_check.py")
            pytest.main(args=[path, '--junitxml={}'.format(self.reportpath)])

        
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        layout = QGridLayout()
        
        burn_button = QPushButton('burn')
        burn_button.clicked.connect(self.on_burn_button_clicked)
        check_button = QPushButton('check')
        check_button.clicked.connect(self.on_check_button_clicked)
        layout.addWidget(burn_button, 0, 0)
        layout.addWidget(check_button, 1, 0)
        self.setLayout(layout)
        self.show()
        
    