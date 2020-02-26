from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt5_client_20200130 import Ui_Form
import dialog
import socket
import time

s = None
s_file = None
# socket delay time (seconds)
s_delay_time = 0.15
# 0 : NOT run, 1: run process, 2: suspend run
runs = 0

class Thread_run_protocol(QtCore.QThread):
    response_label = QtCore.pyqtSignal(str)
    run_button = QtCore.pyqtSignal(str)
    btn_enable = QtCore.pyqtSignal(bool)
    
    def __init__(self, window, thcon):
        super().__init__(window)
        self.ui = window.ui
        self.thcon = thcon
        
    def run(self):
        global s
        global runs
        
        word = "runp"
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        s.send(word.encode('utf-8'))
        self.run_button.emit("Suspend")
        runs = 1
        
        while True:
            data = s.recv(1024)
            dec = data.decode('utf-8')
            print(dec)
        
            if dec.strip() == "200 OK Finished Run":
                self.run_button.emit("Run")
                self.btn_enable.emit(True)
                runs = 0
                break
                
    def suspend(self):
        global runs
        word = "susp"
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        s.send(word.encode('utf-8'))        
        runs = 2
        self.run_button.emit("Resume")
        
    def resume(self):
        global runs
        word = "resume"
        
        if not s:
            self.thcon.start()
            time.sleep(s_delay_time)
        
        s.send(word.encode('utf-8'))  
        runs = 1
        self.run_button.emit("Suspend")

class Thread_trans_file(QtCore.QThread):
    response_label = QtCore.pyqtSignal(str)

    def __init__(self, window):
        super().__init__(window)
        self.ui = window.ui
        
    def run(self):
        global s_file
        #host = '192.168.1.177'
        host = self.ui.lineEdit.text()
    
        # Define the port on which you want to connect 
        #port = 12356
        port = int(self.ui.lineEdit_2.text())
    
        try:
            s_file = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
            # connect to server
            s_file.connect((host,port))
    
            self.response_label.emit("File thread connect to " + host + " is successful!")
            
            word = "trans_file"
            s_file.send(word.encode('utf-8'))
            
            data = s_file.recv(1024)
            dec = data.decode('utf-8')
            print(dec)
            
            if dec.strip() == "200 OK Trans File": 
                f = open(dialog.file_loc,'rb')
                l = f.read(1024)
                print("Prepare for file upload")
                self.response_label.emit("Prepare for file upload")
                while (l):
                    s_file.send(l)
                    #print('Sent ',repr(l))
                    l = f.read(1024)
                f.close()
            print('Done sending')
            s_file.close()
            
            self.response_label.emit("Finished file upload")
            
        except Exception as e:
            s_file = None
            self.response_label.emit(str(e))

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
        
        self.dialog = dialog.App()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.th = Thread_send_cmd(self)
        self.th.response_label.connect(self.set_rsp_label)
        self.th.con_button.connect(self.set_con_button)        
        self.thcon = Thread_con(self, self.th)
                
        self.th_tfile = Thread_trans_file(self)
        self.th_tfile.response_label.connect(self.set_rsp_label)       
        
        self.th_run = Thread_run_protocol(self, self.thcon)
        self.th_run.response_label.connect(self.set_rsp_label)
        self.th_run.run_button.connect(self.set_run_button)
        self.th_run.btn_enable.connect(self.set_enable_button)
        
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
        self.ui.pushButton_11.clicked.connect(lambda:self.get_file_loc())
        self.ui.pushButton_12.clicked.connect(lambda:self.th_tfile.start())
        self.ui.pushButton_13.clicked.connect(lambda:self.suspend_resume_run())
        self.ui.listWidget.clicked.connect(lambda: self.show_list())
    
    def suspend_resume_run(self):
        if 0 == runs:
            self.th_run.start()  
            self.ui.pushButton_13.setEnabled(False)
            
        #elif 1 == runs: #running
        #    self.th_run.suspend()
        #elif 2 == runs: #suspend
        #    self.th_run.resume()
    
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
        
    def set_run_button(self, text):
        self.ui.pushButton_13.setText(text)
        
    def set_enable_button(self, b):
        self.ui.pushButton_13.setEnabled(b)
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            #print('Enter pressed')
            self.client_send()
    
    def get_file_loc(self):
        dialog.App.openFileNameDialog(self.dialog)
        self.ui.label_8.setText(dialog.file_loc)
        
        if dialog.file_loc:
            self.ui.pushButton_12.setEnabled(True)
        else:
            self.ui.pushButton_12.setEnabled(False)
    
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
        
        if not self.ui.listWidget.currentItem():
            self.ui.label_5.setText("Current item of Labware is None")
            return
        
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
        
        