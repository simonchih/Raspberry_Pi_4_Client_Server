from adafruit_motorkit import MotorKit
import threading

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
        for _ in range(self.tenv):
            self.m.onestep(direction=self.f)

def left(value = 0.1):
    global x
    
    x += value
    
def right(value = 0.1):
    global x
    
    x -= value
    
def forward(value = 0.1):
    global y
    
    y += value
    
def back(value = 0.1):
    global y
    
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