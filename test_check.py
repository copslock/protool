import pytest
from configparser import ConfigParser
from telnetlib import Telnet
import time
import logging
logging.basicConfig(level=logging.INFO)
from basedir import basedir
import os


class TestCheck:
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
        tn = Telnet(host, port=23)
        tn.read_until(b'login')
        tn.write(user.encode('ascii')+b"\n")
        tn.read_until(b'Password')
        tn.write(password.encode('ascii')+b"\n")
        yield tn
        time.sleep(1)
        tn.close()

    def test_restoredefault(self, test_setup):

        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase"+b"\n")
        tn.write(b"killall boa"+b"\n")
        tn.write(b"/userfs/bin/mtd write /userfs/romfile.cfg romfile"+b"\n")
        tn.write(b"prolinecmd restore default"+b"\n")
        comval = "restore default success"
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("restore default .....")
            time.sleep(100)
        time.sleep(90)

        assert content.find(comval) != -1

    def test_GPONSN(self, test_setup):

        tn.write(b"tcapi get GPON_ONU SerialNumber"+b"\n")
        comval = config['produce']['GPONSN']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_MAC(self, test_setup):
        tn.write(b"ifconfig br0"+b"\n")
        comval = config['produce']['MAC']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read mac error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_productclass(self, test_setup):
        tn.write(b"prolinecmd productclass display"+b"\n")
        comval = config['produce']['productclass']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read productclass error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_manufacturerOUI(self, test_setup):
        tn.write(b"prolinecmd manufacturerOUI display"+b"\n")
        comvalupper = config['produce']['MAC'].upper()
        value = ''.join(comvalupper.split(':'))[:6]
        try:
            content = tn.read_until(value.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read manufacturerOUI error .....")
            time.sleep(100)
        assert content.find(value) != -1

    def test_CustomerSWVersion(self, test_setup):
        tn.write(b"tcapi get DeviceInfo_devParaStatic CustomerSWVersion"+b"\n")
        comval = config['produce']['CustomerSWVersion']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read CustomerSWVersion error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_CustomerHWVersion(self, test_setup):
        tn.write(b"tcapi get DeviceInfo_devParaStatic CustomerHWVersion"+b"\n")
        comval = config['produce']['CustomerHWVersion']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read CustomerHWVersion error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_WLanSSID(self, test_setup):
        tn.write(b"tcapi get WLan_Entry0 SSID"+b"\n")
        comvalupper = config['produce']['mac'].upper()[8:]
        value = ''.join(comvalupper.split(':'))
        WlanSSID = "SILK_{}".format(value)
        
        try:
            content = tn.read_until(WlanSSID.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read WLanSSID error .....")
            time.sleep(100)
        assert content.find(WlanSSID) != -1

    @pytest.fixture
    def test_WLanAuthModeifopen(self, test_setup):
        tn.write(b"tcapi get WLan_Entry0 AuthMode"+b"\n")
        comval = 'open'
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read WLanAuthMode error .....")
            time.sleep(100)
        if content.find(comval) == -1:
            return True
        else:
            return False

    def test_WLanAuthMode(self, test_setup, test_WLanAuthModeifopen):
        result = test_WLanAuthModeifopen
        if result:
            pytest.skip("WLanAuthMode is open")
        tn.write(b"tcapi get WLan_Entry0 AuthMode"+b"\n")
        comval = 'open'
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read WLanAuthMode error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_WLanWPAPSK(self, test_setup, test_WLanAuthModeifopen):
        result = test_WLanAuthModeifopen
        if result:
            pytest.skip("WLanAuthMode is open")
        tn.write(b"tcapi get WLan_Entry0 WPAPSK"+b"\n")
        comval = config['WLanWPAPSK']['comval']
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read WLanWPAPSK error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_Txpower(self, test_setup):
        tn.write(b"cat /proc/kmsg &"+b"\n")
        # need this sleep 1
        time.sleep(1)
        tn.write(b"echo show_BoB_information >/proc/pon_phy/debug"+b"\n")
        comval = 'Tx power = -40 dBm'
        try:
            content = tn.read_until(comval.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read Txpower error .....")
            time.sleep(100)
        assert content.find(comval) != -1

    def test_exceptledallon(self, test_setup):
        tn.write(b"sys led on"+b"\n")

    def test_exceptledalloff(self, test_setup):
        tn.write(b"sys led off"+b"\n")
