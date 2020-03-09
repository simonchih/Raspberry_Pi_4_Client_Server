# coordinates, left hand rule
x = 0.0 # left +, right -
y = 0.0 # forward +, back -
z_a = 0.0 # down +, up -
z_b = 0.0 # down +, up -

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