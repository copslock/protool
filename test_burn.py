import pytest
from configparser import ConfigParser
from telnetlib import Telnet
import time
import os
import logging
from basedir import basedir
logging.basicConfig(level=logging.INFO)


class TestBurn:

    @pytest.fixture
    def test_setup(self):
        global config
        config = ConfigParser()
        path = os.path.join(basedir, 'config.ini')
        config.read(path, encoding='utf-8')
        host = "192.168.100.1"
        user = "Silknet"
        password = "Silknet@dmin"
        global tn
        print("tn.open())))")
        tn = Telnet(host, port=23)
        tn.read_until(b'login')
        tn.write(user.encode('ascii')+b"\n")
        tn.read_until(b'Password')
        tn.write(password.encode('ascii')+b"\n")
        yield tn
        print("tn.close())))")
        time.sleep(1)
        tn.close()
    

    def test_MACburn(self, test_setup):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        time.sleep(1)
        tn.write(b"prolinecmd clear 1"+b"\n")
        comvalupper = config['produce']['MAC'].upper()
        comvallower = config['produce']['MAC'].lower()
        value = ''.join(comvalupper.split(':'))
        tn.write("sys mac {}\n".format(value).encode('ascii'))
        judge = "new mac addr = {}".format(comvallower)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        time.sleep(90)
        assert content.find(judge) != -1


    def test_productclassburn(self, test_setup):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        comval = config['produce']['productclass']
        tn.write("prolinecmd productclass set {}\n".format(comval).encode('ascii'))
        
        judge = "buf is:{}".format(comval)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        assert content.find(judge) != -1

    
    def test_OUIburn(self, test_setup):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        comvalupper = config['produce']['MAC'].upper()
        comvallower = config['produce']['MAC'].lower()
        value = ''.join(comvalupper.split(':'))[:6]
        tn.write("prolinecmd manufacturerOUI set {}\n".format(value).encode('ascii'))
        
        judge = "buf is:{}".format(value)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        assert content.find(judge) != -1


    def test_serialnumburn(self, test_setup):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        comvalupper = config['produce']['MAC'].upper()
        value = ''.join(comvalupper.split(':'))
        tn.write("prolinecmd serialnum set {}\n".format(value).encode('ascii'))
        
        judge = "buf is:{}".format(value)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        assert content.find(judge) != -1


    def test_restoredefault(self, test_setup):

        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        tn.write(b"killall boa"+b"\n")
        tn.write(b"/userfs/bin/mtd write /userfs/romfile.cfg romfile"+b"\n")
        tn.write(b"prolinecmd restore default"+b"\n")
        comval = 'restore default success'
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("restore default .....")
            time.sleep(100)
        time.sleep(90)

        assert content.find(comval) != -1


    def test_createwan(self, test_setup):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'produce_Georgia(1.2).txt')
        with open(path, 'r') as fp:
            for line in fp:
                tn.write(line.encode("ascii")+b'\n')

            
        



    


    

