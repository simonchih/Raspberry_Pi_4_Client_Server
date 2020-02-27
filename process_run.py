from multiprocessing import Process
import psutil
import threading
import time

import protocol

class run_protocol(threading.Thread):
    def __init__(self, c):
        super().__init__()
        self.c = c
        self.p = None
        self.ps = None
        
    def run(self):
        global run_status
        
        self.p = Process(target=protocol.main, args=())
        self.p.start()
        self.ps = psutil.Process(self.p.pid)
        self.p.join()
        try:
            self.c.send("200 OK Finished Run".encode('utf-8'))    
        except:
            print("Can't response the protocol is finished run")
            
    def susp(self):
        global run_status
        
        if self.ps:
            self.ps.suspend()
        
    def resu(self):
        global run_status
        
        if self.ps:
            self.ps.resume()
            
    def cancel(self):
        global run_status
        
        if self.ps:
            self.ps.terminate()
            if self.c:
                self.c.send("Terminate protocol running".encode('utf-8'))  
            else:
                print("Can't response the protocol is terminated")