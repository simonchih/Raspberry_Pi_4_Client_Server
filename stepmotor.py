from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import threading
import time

# coordinates, left hand rule
x = 0.0 # left +, right -
y = 0.0 # forward +, back -
z_a = 0.0 # down +, up -
z_b = 0.0 # down +, up -

class motor_move(threading.Thread):
    def __init__(self, m, f, v): # m = kit.stepper (1)
        super().__init__()
        self.m = m
        self.f = f
        self.tenv = int(10*v)
        
    def run(self):
        print('self.tenv = %d' % self.tenv) #temp
        print('self.f = %s' % self.f) #temp
        
        #self.m.release()
        
        for _ in range(self.tenv):
            #self.m.onestep(direction=self.f)
            self.m.onestep(direction=self.f, style=stepper.DOUBLE)
            time.sleep(0.01)

def left(value = 0.1):
    global x
    
    kit = MotorKit()
    th_x = motor_move(kit.stepper1, stepper.FORWARD, value)
    th_x.start()
    th_x.join()
    
    x += value
    
def right(value = 0.1):
    global x
    
    kit = MotorKit()
    th_x = motor_move(kit.stepper1, stepper.BACKWARD, value)
    th_x.start()
    th_x.join()
    
    x -= value
    
def forward(value = 0.1):
    global y
    
    kit = MotorKit()
    th_y = motor_move(kit.stepper2, stepper.FORWARD, value)
    th_y.start()
    th_y.join()
    
    y += value
    
def back(value = 0.1):
    global y
    
    kit = MotorKit()
    th_y = motor_move(kit.stepper2, stepper.BACKWARD, value)
    th_y.start()
    th_y.join()
    
    y -= value
    
def up(mount, value = 0.1):
    global z_a
    global z_b
    
    if 'a' == mount:
        z_a -= value
    elif 'b' == mount:
        z_b -= value
        
def down(mount, value = 0.1):
    global z_a
    global z_b
    
    if 'a' == mount:
        z_a += value
    elif 'b' == mount:
        z_b += value