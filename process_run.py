import threading
import protocol

# 0: NOT run, 1: run process, 2: suspend run
run_status = 0

class run_protocol(threading.Thread):
    def __init__(self, c):
        super().__init__()
        self.c = c
        
    def run(self):
        global run_status
        
        run_status = 1
        protocol.main()
        if self.c:
            self.c.send("200 OK Finished Run".encode('utf-8'))
            run_status = 0    
        else:
            print("Can't response the protocol is finished run")