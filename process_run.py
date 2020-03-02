from multiprocessing import Process
import psutil
import threading
import time

import protocol

# 0: NOT run, 1: run process, 2: suspend
run_status = 0

class run_protocol(threading.Thread):
    def __init__(self, c):
        super().__init__()
        self.c = c
        self.p = None
        self.ps = None
        
    def run(self):
        global run_status
        
        if 0 == run_status:
            run_status = 1
            self.p = Process(target=protocol.main, args=())
            self.p.start()
            self.ps = psutil.Process(self.p.pid)
            self.p.join()
            run_status = 0
            try:
                self.c.send("200 OK Finished Run".encode('utf-8'))    
            except:
                print("Can't response the protocol is finished run")
        else:
            try:
                self.c.send("Process is under running".encode('utf-8'))    
            except:
                print("Can't response the process is running.")
            
    def susp(self):
        global run_status
        
        if self.ps:           
            self.ps.suspend()
            run_status = 2
        
    def resu(self):
        global run_status
        
        if self.ps:
            self.ps.resume()
            run_status = 1
            
    def cancel(self):
        global run_status
        
        if self.ps:
            self.ps.terminate()
            run_status = 0
            if self.c:
                self.c.send("200 OK Terminate Run".encode('utf-8'))  
            else:
                print("Can't response the protocol is terminated")