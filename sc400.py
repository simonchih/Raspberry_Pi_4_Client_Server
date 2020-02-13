import sys
import glob
import serial
import time
from _thread import *

baud = 9600
com_port = '/dev/ttyUSB0'

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def set_com_port(port):
    global com_port
    
    com_port = port

def write(command, read = True):
    addr = '@1 '
    CR= '\r'
    
    com = bytes(addr + command + CR, 'ascii')
    with serial.Serial(com_port, baud) as ser:
        print("Is open = ", ser.is_open)       
        ser.write(com)       
        if read:
            s = ser.read()
            print(s)
        ser.flush()   
        
def demo():
    # Demo code
    for n in ['n1', 'n2', 'n3', 'n4']:
        write(n)
        time.sleep(1)
        
    for f in ['f1', 'f2', 'f3', 'f4']:
        write(f)
        time.sleep(1)
    # End demo
        
def Main():
    print("List port = ", serial_ports())

    demo()
        
#if __name__ == '__main__': 
#    Main()