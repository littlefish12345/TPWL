import rsa,time
from socket import *

def version():
    return 0.01

class TPWL_C:
    def __init__(self,buffsize):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.buffsize = buffsize
        return None

    def create(self,times,bits):
        self.times = times
        self.bits = bits
        self.g_keys = []
        
        for i in range(0,self.times):
            try:
                (public_key, private_key) = rsa.newkeys(bits)
                self.g_keys.append((public_key, private_key))
            except:
                return 1
        return 0

    def connect(self,addr):
        self.addr = addr
        self.s_keys = []
        
        try:
            self.s.connect(self.addr)
        except:
            return 1
        
        self.s.send(str(self.times).encode())
        time.sleep(0.01)
        self.s.send(str(self.bits).encode())
        
        for i in range(0,self.times):
            try:
                self.s.send(self.g_keys[i][0].save_pkcs1())
                time.sleep(0.01)
            except:
                return 2
            
        for i in range(0,self.times):
            try:
                self.s_keys.append(rsa.PublicKey.load_pkcs1(self.s.recv(self.buffsize)))
            except:
                return 3            
        return 0

    def send(self,data):
        try:
            added_data = rsa.encrypt(data.encode(),self.s_keys[0])
            for i in range(1,self.times):
                added_data = rsa.encrypt(added_data,self.s_keys[i])
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
            decoded = rsa.decrypt(data, self.g_keys[0][1])
            for i in range(1,self.times):
                decoded = rsa.decrypt(data, self.g_keys[i][1])
            decoded = decoded.decode()
        except:
            return 2

        return decoded

    def close(self):
        self.s.close()
