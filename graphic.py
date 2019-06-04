from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import traceback
from basedir import basedir
import os
import sys
from configparser import ConfigParser
import re
import logging
import unittest
import HtmlTestRunner
import test_proburn
import test_procheck


class logSignal(QObject):
    log = Signal(object)

class log(logging.Handler):
    def __init__(self):
        super().__init__()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.signal = logSignal()

    def emit(self, record):
        msg = self.format(record)
        self.signal.log.emit(msg)




class WorkerSignals(QObject):
    result = Signal()
    finished = Signal()
    error = Signal(tuple)
    


class Worker(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    def run(self):
        
        logging.info("Thread start")
        try:
            self.fn()
            self.signals.result.emit()
        except:
            logging.info("except")
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        finally:
            self.signals.finished.emit()


class para_interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'para'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 400
        self.initUI()
        
        

    def initUI(self):
        
        self.config = ConfigParser()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.configlayout()

        self.clearbutton()
        self.submitbutton()
        
        self.show()

    def font(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)

        return font

    def configlayout(self):
        layoutWidget = QWidget(self)
        layoutWidget.setGeometry(QRect(40, 40, 300, 150))
        layout = QGridLayout()
        layoutWidget.setLayout(layout)
        
        names = ['GPONSN:', '', 
                'MAC:', '', 
                'productclass:', '', 
                'CustomerSWVersion:', '',
                'CustomerHWVersion:',  '',]

        positions = [(i, j) for i in range(5) for j in range(2)]
        
        for position, name in zip(positions, names):
            row, column = position
            if column == 0:
                label = QLabel(name)
                label.setFont(self.font())
                #label.setStyleSheet("QLabel{font-size: 15px; \
                #                   font-family: Arial;}")
                layout.addWidget(label, *position)
            if column == 1:
                if row == 0:
                    self.GPONSNline = QLineEdit(name)
                    layout.addWidget(self.GPONSNline, *position)
                if row == 1:
                    self.MACline = QLineEdit(name)
                    layout.addWidget(self.MACline, *position)
                if row == 2:
                    self.productclassline = QLineEdit(name)
                    layout.addWidget(self.productclassline, *position)
                if row == 3:
                    self.CustomerSWVersionline = QLineEdit(name)
                    layout.addWidget(self.CustomerSWVersionline, *position)
                if row == 4:
                    self.CustomerHWVersionline = QLineEdit(name)
                    layout.addWidget(self.CustomerHWVersionline, *position)
        

    def clearbutton(self):
        button = QPushButton(self)
        button.setGeometry(QRect(250, 300, 75, 25))
        button.setText("clear")
        button.setFont(self.font())
        button.setStyleSheet("border: 2px solid red;\
                            border-width:2px;\
                            border-radius:10px;")
        button.clicked.connect(self.clear)


    def submitbutton(self):
        button = QPushButton(self)
        button.setGeometry(QRect(350, 300, 75, 25))
        button.setText("submit")
        button.setFont(self.font())

        button.setStyleSheet("border: 2px solid red;\
                            border-width:2px;\
                            border-radius:10px;")

        button.clicked.connect(self.submit)


    def clear(self):
        self.GPONSNline.clear()
        self.MACline.clear()
        self.productclassline.clear()
        self.CustomerSWVersionline.clear()
        self.CustomerHWVersionline.clear()

    
    def MAC_judge(self):
        text = self.MACline.text()
        if re.match(r'\b[A-Fa-f0-9]+\b', text) and len(text) == 12:
            alist = []
            for i in range(0, len(text), 2):
                alist.append(text[i:i+2])
            text = ':'.join(alist)
            self.MACline.setText(text)
            self.MACline.setStyleSheet("color: black;")
        elif re.match(r'\b([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2}\b', text):
            self.MACline.setStyleSheet("color: black;")
        else:
            self.MACline.setStyleSheet("color: red;")
            return False

        return True


    def generateconfig(self):

        path = os.path.join(basedir, 'config.ini')
        self.config.read(path, encoding='utf-8')
        self.config.set('produce', 'GPONSN', self.GPONSNline.text())
        self.config.set('produce', 'MAC', self.MACline.text())
        self.config.set('produce', 'productclass', self.productclassline.text())
        self.config.set('produce', 'CustomerSWVersion', self.CustomerSWVersionline.text())
        self.config.set('produce', 'CustomerHWVersion', self.CustomerHWVersionline.text())
        with open(path, 'w') as config_file:
            self.config.write(config_file)
            

    def submit(self):
        if self.MAC_judge():
            self.generateconfig()

            self.close()
            self.widget = exec_interface()


class exec_interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'exec'
        self.reportpath = os.path.dirname(os.path.abspath(sys.executable))
        self.left = 400
        self.top = 200
        self.width = 600
        self.height = 500
        self.initUI()
    


    def initUI(self):
        self.threadpool = QThreadPool()
        #print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        
        self.execlayout()
        self.returnbutton()
        self.setup_logger()

        self.show()
    

    def font(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)

        return font

    def thread_error(self, tup):
        exctype, value, traceback_string = tup
        logging.info(exctype)
        logging.info(value)
        logging.info(traceback_string)

    def thread_complete(self):
        logging.info("Thread complete!")


    def testcasepass(self):
        logging.info("Pass")


    def on_burn_button_clicked(self):
        path = os.path.join(basedir, "report_template.html")
        unittest.main(module = 'test_proburn',
                      testRunner=HtmlTestRunner.HTMLTestRunner(output=self.reportpath, template = path),
                      exit=False)

    
    def burn(self):
        worker = Worker(self.on_burn_button_clicked)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.error.connect(self.thread_error)
        worker.signals.result.connect(self.testcasepass)
        self.threadpool.start(worker)
        

    def on_check_button_clicked(self):
        path = os.path.join(basedir, "report_template.html")
        unittest.main(module='test_procheck',
                      testRunner=HtmlTestRunner.HTMLTestRunner(output=self.reportpath, template = path),
                      exit=False)


    def check(self):
        worker = Worker(self.on_check_button_clicked)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.error.connect(self.thread_error)
        self.threadpool.start(worker)


    def execlayout(self):
        layoutWidget = QWidget(self)
        layoutWidget.setGeometry(QRect(20, 20, 100, 75))
        layout = QGridLayout()
        layoutWidget.setLayout(layout)
        
        names = ['burn', 
                'check',]

        positions = [(i, j) for i in range(2) for j in range(1)]

        for position, name in zip(positions, names):
            row, column = position
            if column == 0:
                button = QPushButton(name)
                button.setFont(self.font())
                #button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                #button.setMaximumSize(75,25)
                button.setStyleSheet("border: 2px solid red;\
                            border-width:2px;\
                            border-radius:10px;")
                if row == 0:
                    button.clicked.connect(self.burn)
                if row == 1:
                    button.clicked.connect(self.check)
                layout.addWidget(button, *position)


    def para_interface(self):
        self.close()
        self.widget = para_interface()

    
    def returnbutton(self):
        button = QPushButton(self)
        button.setText("return")
        button.setGeometry(QRect(500, 440, 75, 25))
        button.setFont(self.font())
        button.setStyleSheet("border: 2px solid red;\
                    border-width:2px;\
                    border-radius:10px;")
        button.clicked.connect(self.para_interface)


    def setup_logger(self):
        PlainTextEdit = QPlainTextEdit(self)
        PlainTextEdit.setGeometry(QRect(150, 20, 430, 400))
        PlainTextEdit.setFont(self.font())
        handler = log()
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        handler.signal.log.connect(PlainTextEdit.appendPlainText)


