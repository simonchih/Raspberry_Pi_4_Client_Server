from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt5_client_20200130 import Ui_Form
import socket
import time

s = None

class Thread_con(QtCore.QThread):
    def __init__(self, window, thsc):
        super().__init__(window)
        self.ui = window.ui
        self.thsc = thsc
        
    def run(self):
        global s
        # local host IP '127.0.0.1' 
        #host = '192.168.1.177'
        host = self.ui.lineEdit.text()
    
        # Define the port on which you want to connect 
        #port = 12356
        port = int(self.ui.lineEdit_2.text())
    
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
            # connect to server on local computer 
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
    def con_dis(self):
        global s
        if s:
            self.th.word = "dis"
            self.th.start()
            time.sleep(0.1)
            s = None
            self.th.con_button.emit("Connect")
        else:
            self.thcon.start()
            
    def set_rsp_label(self, text):
        self.ui.label_5.setText(text)
        
    def set_con_button(self, text):
        self.ui.pushButton.setText(text)
    
    def send_cmd(self, word):
        self.th.word = word
        self.th.start()
    
    def client_send(self): 
        global s
        word = self.ui.lineEdit_3.text()
        
        self.th.word = word
        self.th.start()
    
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
            time.sleep(0.1)
        
        # handle both connected and disconnected
        self.send_cmd(word)
    
    def cright(self): 
        global s
        word = "right"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(0.1)
        
        # handle both connected and disconnected
        self.send_cmd(word)       
        
    def cback(self): 
        global s
        word = "back"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(0.1)
        
        # handle both connected and disconnected
        self.send_cmd(word)
    
    def cforward(self): 
        global s
        word = "forward"
        
        v = self.radio_value(self.ui)
            
        word = word + " " + str(v)
        
        if not s:
            self.thcon.start()
            time.sleep(0.1)
        
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
            time.sleep(0.1)
        
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
            time.sleep(0.1)
        
        # handle both connected and disconnected
        self.send_cmd(word)
        
        