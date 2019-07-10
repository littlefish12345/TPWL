import rsa,time
from socket import *

def version():
    return 0.11

class TPWL_C:
    def __init__(self,buffsize):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.buffsize = buffsize
        return None

    def create(self,bits):
        self.bits = bits
        self.g_key = None
        
        try:
            (public_key, private_key) = rsa.newkeys(bits)
            self.g_key = (public_key, private_key)
        except:
                return 1
        return 0

    def connect(self,addr):
        self.addr = addr
        self.s_key = None
        
        try:
            self.s.connect(self.addr)
        except:
            return 1
        
        self.s.send(str(self.bits).encode())
        
        try:
            self.s.send(self.g_key[0].save_pkcs1())
        except:
            return 3
            
        try:
            self.s_key = rsa.PublicKey.load_pkcs1(self.s.recv(self.buffsize))
        except:
            return 2          
        return 0

    def send(self,data):
        try:
            added_data = rsa.encrypt(data.encode(),self.s_key)
        except:
            return 1
        
        try:
            self.s.send(added_data)
        except:
            return 2
        
        return 0

    def recv(self):
        try:
            data = self.s.recv(self.buffsize)
        except:
            return 1
        
        try:
            decoded = rsa.decrypt(data, self.g_key[1]).decode()
        except:
            return 2

        return decoded

    def close(self):
        self.s.close()
