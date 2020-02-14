from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt5_client_20200130 import Ui_Form
import socket
import time

s = None
# socket delay time (seconds)
s_delay_time = 0.15

class Thread_con(QtCore.QThread):
    def __init__(self, window, thsc):
        super().__init__(window)
        self.ui = window.ui
        self.thsc = thsc
        
    def run(self):
        global s
        #host = '192.168.1.177'
        host = self.ui.lineEdit.text()
    
        # Define the port on which you want to connect 
        #port = 12356
        port = int(self.ui.lineEdit_2.text())
    
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
            # connect to server
            s.connect((host,port))
    
            self.thsc.response_label.emit("Connect to " + host + " is successful!")
            self.thsc.con_button.emit("Disconnect")
            
        except Exception as e:
            s = None
            self.thsc.response_label.emit(str(e))
            self.thsc.con_button.emit("Connect")

class Thread_send_cmd(QtCore.QThread):
    response_label = QtCore.pyqtSignal(str)
    con_button = QtCore.pyqtSignal(str)

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.ui = window.ui
        self.word = ""
    
    # send command
    def run(self):
        global s
    
        if self.word:    
            if s:
                try:            
                    s.send(self.word.encode('utf-8'))
                    print(self.word)
                    #sent_wd = [x.strip() for x in self.word.split(' ')]
                    
                    data = s.recv(1024)
                    print(data)
                    #resp = [x.strip() for x in data.decode('utf-8').split(' ')]
                    
                    self.response_label.emit(str(data))
                except Exception as e:
                    s = None
                    self.response_label.emit(str(e))
                    self.con_button.emit("Connect")
            else:
                self.response_label.emit("Disconnected, can not send command!")
        else:
            self.response_label.emit("NULL!!!")

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.show_items = False
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.th = Thread_send_cmd(self)
        self.th.response_label.connect(self.set_rsp_label)
        self.th.con_button.connect(self.set_con_button)        
        self.thcon = Thread_con(self, self.th)
        
        self.ui.pushButton.clicked.connect(lambda: self.con_dis())
        self.ui.pushButton_2.clicked.connect(lambda: self.cback())
        self.ui.pushButton_3.clicked.connect(lambda: self.cforward())
        self.ui.pushButton_4.clicked.connect(lambda: self.cleft())
        self.ui.pushButton_5.clicked.connect(lambda: self.cright())
        self.ui.pushButton_6.clicked.connect(lambda: self.cup())
        self.ui.pushButton_7.clicked.connect(lambda: self.cdown())
        self.ui.pushButton_8.clicked.connect(lambda: self.client_send())
        self.ui.pushButton_9.clicked.connect(lambda: self.json_load())
        self.ui.pushButton_10.clicked.connect(lambda:self.json_save())
        self.ui.listWidget.clicked.connect(lambda: self.show_list())
        
    def con_dis(self):
        global s
        if s:
            self.send_cmd("dis")
            time.sleep(s_delay_time)
            s = None
            self.th.con_button.emit("Connect")
        else:
            self.thcon.start()
            
    def set_rsp_label(self, text):
        self.ui.label_5.setText(text)
        
    def set_con_button(self, text):
        self.ui.pushButton.setText(text)
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            #print('Enter pressed')
            self.client_send()
    
    def show_list(self):
        if False == self.show_items: # show
            self.ui.listWidget.setGeometry(QtCore.QRect(110, 100, 221, 151))
            self.show_items = True
        else: # hide
            self.ui.listWidget.setGeometry(QtCore.QRect(110, 100, 221, 21))
            self.show_items = False
            
        if "Other" == self.ui.listWidget.currentItem().text():
            self.ui.lineEdit_4.setEnabled(True)
        else:
            self.ui.lineEdit_4.setEnabled(False)
    
    def json_load(self):
        global s
        word = "load_json"
        
        slot = self.slot_value(self.ui)
        
        word = word + " " + str(slot)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        self.send_cmd(word)
    
    def json_save(self):
        global s
        word = "save_json"
        
        slot = self.slot_value(self.ui)
        
        if "Other" == self.ui.listWidget.currentItem().text():
            item_text = "'%s'" % self.ui.lineEdit_4.text().strip()
        else:
            item_text = "'%s'" % self.ui.listWidget.currentItem().text().strip()
        
        word = word + " " + str(slot) + " " + item_text
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        self.send_cmd(word)
    
    def slot_value(self, ui):
        slot = 1
        
        if ui.radioButton_9.isChecked():
            slot = 1
        elif ui.radioButton_10.isChecked():
            slot = 2
        elif ui.radioButton_11.isChecked():
            slot = 3
        elif ui.radioButton_12.isChecked():
            slot = 4
        elif ui.radioButton_13.isChecked():
            slot = 5
        elif ui.radioButton_14.isChecked():
            slot = 6
        elif ui.radioButton_15.isChecked():
            slot = 7
        elif ui.radioButton_16.isChecked():
            slot = 8
        elif ui.radioButton_17.isChecked():
            slot = 9
        elif ui.radioButton_18.isChecked():
            slot = 10
        elif ui.radioButton_19.isChecked():
            slot = 11
        elif ui.radioButton_20.isChecked():
            slot = 12
        elif ui.radioButton_21.isChecked():
            slot = 13
        elif ui.radioButton_22.isChecked():
            slot = 14
        elif ui.radioButton_23.isChecked():
            slot = 15
        elif ui.radioButton_24.isChecked():
            slot = 16
        elif ui.radioButton_25.isChecked():
            slot = 17
        elif ui.radioButton_26.isChecked():
            slot = 18
        elif ui.radioButton_27.isChecked():
            slot = 19
        elif ui.radioButton_28.isChecked():
            slot = 20
            
        return slot
    
    def send_cmd(self, word):
        self.th.word = word
        self.th.start()
    
    def client_send(self): 
        global s
        
        word = self.ui.lineEdit_3.text()
        self.send_cmd(word)
    
    def radio_value(self, ui):
        v = 0.1
    
        if ui.radioButton.isChecked():
            v = 20
        elif ui.radioButton_2.isChecked():
            v = 10
        elif ui.radioButton_3.isChecked():
            v = 5
        elif ui.radioButton_4.isChecked():
            v = 1
        elif ui.radioButton_5.isChecked():
            v = 0.5
        elif ui.radioButton_6.isChecked():
            v = 0.1
            
        return v
    
    def pipette_mount(self, ui):
        m = "'a'"
            
        if ui.radioButton_7.isChecked():
            m = "'a'"
        elif ui.radioButton_8.isChecked():
            m = "'b'"
            
        return m
    
    
    def cleft(self): 
        global s
        word = "left"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)
    
    def cright(self): 
        global s
        word = "right"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)       
        
    def cback(self): 
        global s
        word = "back"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)
    
    def cforward(self): 
        global s
        word = "forward"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)
        
    def cup(self): 
        global s
        word = "up"
        
        v = self.radio_value(self.ui)
        m = self.pipette_mount(self.ui)
        
        word = word + " " + m + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)
        
    def cdown(self): 
        global s
        word = "down"
        
        v = self.radio_value(self.ui)
        m = self.pipette_mount(self.ui)
        
        word = word + " " + m + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        # handle both connected and disconnected
        self.send_cmd(word)
        
        