# Import socket module 
import socket
    
def piclient():
    # local host IP '127.0.0.1' 
    host = '192.168.1.177'
  
    # Define the port on which you want to connect 
    port = 12356
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host,port))

    return s
    
def client_send(s, word): 
    
    s.send(word.encode('utf-8'))
    print(word)
    sent_wd = [x.strip() for x in word.split(' ')]
    
    data = s.recv(1024)
    print(data)
    resp = [x.strip() for x in data.decode('utf-8').split(' ')]
            

def Main():

    s = piclient()
    for _ in range(3):
        client_send(s, 'blink')
        
    client_send(s, 'end')
        
if __name__ == "__main__":
    Main()
