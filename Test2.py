import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import *
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#
#import paho.mqtt.client as mqtt
import json
import paho.mqtt.client as mqtt
from Import import MOBIUS_API as MA
import threading, requests, time
import csv
import re

IP='210.105.85.20'
Topic='Smartcs/ITS'


class GetInfDev:
    def __init__(self, value = None, LDev = None,
                 BDev = None, DESdev = None):
        self._value = value
        self._Ldev = LDev
        self._BDev = BDev
        self._DESdev = DESdev
        # getting the values

    @property
    def value(self):
        print('Getting value')
        return self._value
        # setting the values

    @property
    def LDev(self):
        # setting the values
        return self._Ldev

    @property
    def BDev(self):
        # setting the values
        return self._BDev

    @property
    def DESdev(self):
        # setting the values
        return self._DESdev

    @value.setter
    def value(self, value):
        print('Setting value to ' + value)
        self._value = value
        # deleting the values

    @LDev.setter
    def LDev(self, LDev):
        print('Setting value to ' + LDev)
        self._Ldev = LDev
        # deleting the values

    @BDev.setter
    def BDev(self, BDev):
        print('Setting value to ' + BDev)
        self._BDev = BDev
        # deleting the values

    @DESdev.setter
    def DESdev(self, DESdev):
        print('Setting value to ' + DESdev)
        self._DESdev = DESdev
        # deleting the values

    @value.deleter
    def value(self):
        print('Deleting value')
        del self._value

    @LDev.deleter
    def LDev(self):
        # setting the values
        del self._Ldev

    @BDev.deleter
    def BDev(self):
        # setting the values
        del self._BDev

    @DESdev.deleter
    def DESdev(self):
        # setting the values
        del self._DESdev

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("disconnect :" ,str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in=json.loads(m_decode) #decode json data
    if len(m_in) > 30:
        DATA = m_in
        if int(DATA['D-N']) == 1:
            exec_iot = DATA['exec_iot']
            AE_Status_Sub = DATA['AE_Status_Sub_Scube']
            boot_time = DATA['boot_time']
        else:
            exec_iot = DATA['exec_thyme']
            AE_Status_Sub = DATA['AE_Status_Sub']
            boot_time = DATA[' boot_time']
        mydb = MA.mydb
        db_name = MA.db_name[6]
        MA.insert_data_to_db(mydb, db_name, m_in, 6)
        ldev = GetInfDev(None, str(DATA['D-ID'].strip()), str(DATA['current_datetime']), str(DATA['PF-IP'].strip()))
        if not ldev.LDev:
            ldev.LDev = ['NONE']
        if not ldev.BDev:
            ldev.BDev = ['NONE']
        if not ldev.DESdev:
            ldev.DESdev = ['NONE']
        DES, AE_type, ITS, S_num, Administrator, M_NUM, Status, Dir, file, ftp_pw = MA.AE_seek(ldev.LDev, ldev.DESdev)
        items = []
        items.append(DES)
        print(DES)
        #print('>> ' +  devList +' '+ ldev.BDev +' '+DES+' : Data Upload Complete!!!')

def mqtt_exe():
    txtfilename = "result_file/Book.csv"
    try:
        username = "gw318"
        with open(txtfilename, 'rt') as f:
            reader = csv.reader(f, delimiter=',')  # good point by @paco
            for row in reader:
                if str(row[0]).split(" ")[0] == username:
                    print(str(row))

        print("data is not exsit")
    except AttributeError:
        print("file not exist yet")
        pass  # fallback to dict

if __name__=='__main__':
    #mqtt_thread = threading.Thread(target=mqtt_exe)
    #mqtt_thread.daemon = True
    #mqtt_thread.start()
    mqtt_exe()

