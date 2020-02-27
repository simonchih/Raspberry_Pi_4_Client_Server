import RPi.GPIO as GPIO
import socket
import time

# import thread module 
from _thread import *
import threading
import json

# Control sc400 if needed
import sc400

import process_run

end_server = False 
client = None
addr = None
s = None

working_dict = "/home/pi"
protocol_name = "protocol.py"

proc_protocol = None

def runp():
    print("Start to Run Protocol")

def susp():
    proc_protocol.susp()
    print("Protocol Suspend")
    
def resume():
    proc_protocol.resu()
    print("Protocol Resume")
    
def cancel():
    proc_protocol.cancel()
    print("Cancel Protocol")
                    
def save_json(slot, item_text):
    path = '%s/slot/%d.json' % (working_dict, slot)
    
    try:
        data = load_json(slot)
    except Exception as e:
        data = {}
        
    data['slot'] = slot
    data[item_text] = {"A1": [0, 0, 0]}
    
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def load_json(slot):
    path = '%s/slot/%d.json' % (working_dict, slot)
    with open(path) as json_file:
        data = json.load(json_file)
        
    return data

# blinking function
def blink(pin = 7):
    # to use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BOARD)

    # set up GPIO output channel, we set GPIO4 (Pin 7) to OUTPUT
    GPIO.setup(pin, GPIO.OUT)
    
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
    
    GPIO.cleanup()
    return

def left(value = 0.1):
    print("Left %f" % float(value))
    
def right(value = 0.1):
    print("Right %f" % float(value))
    
def forward(value = 0.1):
    print("Forward %f" % float(value))
    
def back(value = 0.1):
    print("Back %f" % float(value))
    
def up(mount, value = 0.1):
    print("Pipette " + str(mount) + " Up %f" % float(value))
    
def down(mount, value = 0.1):
    print("Pipette " + str(mount) + " Down %f" % float(value))

def end():
    global end_server
    global client

    print('End server')

    end_server = True
    client = None

def dis():
    print('Bye')

def trans_file():
    print("200 OK Trans File")

# thread fuction 
def threaded(c):   
    global s
    global proc_protocol
        
    while(True):
        try:
            # data received from client 
            data = c.recv(1024)
            resp = [x.strip() for x in data.decode('utf-8').split(' ')]
            
            cmd = resp[0]
            if not cmd:
                continue
        
            alen = len(resp)
            cmd_func = cmd + '('

            for i in range(1, alen):
                if i == alen - 1: #last
                    cmd_func += resp[i]
                else:
                    cmd_func += resp[i] + ','
                    
            cmd_func += ')'
            eval(cmd_func)  
            
            
            if 'end' == resp[0]:
                c.close()
                s.shutdown(socket.SHUT_RDWR)
                s.close()                
                break
            elif 'dis' == resp[0]:                
                c.close()
                break
            elif 'trans_file' == resp[0]:
                c.send("200 OK Trans File".encode('utf-8'))
                with open('%s/%s' % (working_dict, protocol_name), 'wb') as f:
                    print('file opened')
                    while True:
                        #print('receiving data...')
                        data = c.recv(1024)
                        #print('data=%s', (data))
                        if not data:
                            break
                        # write data to a file
                        f.write(data)
                
                f.close()
                print('Successfully get the file')
            elif 'runp' == resp[0]:
                proc_protocol = process_run.run_protocol(c)
                proc_protocol.start()
                c.send("runp".encode('utf-8'))
            else:
                # send back reversed string to client 
                c.send(data)
                print(data)
                
        except Exception as e:
            print(e)
            if not e:
                break
            else:
                try:
                    c.send(str(e).encode())
                except Exception as ee:
                    print(ee)
                    break
    
def main():
    global client
    global s
    
    host = ""
     
    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 12356
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind((host, port)) 
    print("socket binded to post", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening")
  
    #start_new_thread(thread_accept, (s, ))
    # a forever loop until client wants to exit 
    while True:
        
        # establish connection with client 
        try:
            #hold in s.accept()
            client, addr = s.accept()            
        except:
            if True == end_server:
                break
        
        if client:
            # lock acquired by client 
            #print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1]) 
        
            # Start a new thread and return its identifier 
            start_new_thread(threaded, (client,))
            
    print("Exit Pi Server")

if __name__ == "__main__":
    main()