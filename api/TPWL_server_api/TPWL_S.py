import rsa,time
from socket import *

def version():
    return 0.11

class TPWL_CONN:
    def __init__(self,conn,s_key,g_key,buffsize):
        self.conn = conn
        self.buffsize = buffsize
        self.s_key = s_key
        self.g_key = g_key
        return None
    
    def recv(self):
        try:
            data = self.conn.recv(self.buffsize)
        except:
            return 1
        
        try:
            decoded = rsa.decrypt(data, self.g_key[1]).decode()
        except:
            return 2

        return decoded
    
    def send(self,data):
        try:
            added_data = rsa.encrypt(data.encode(),self.s_key)
        except:
            return 1
        
        try:
            self.conn.send(added_data)
        except:
            return 2
        
        return 0

    def close(self):
        self.conn.close()

class TPWL_S:
    def __init__(self,buffsize):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.buffsize = buffsize
        return None
        
    def bind(self,addr):
        self.s.bind(addr)
        return 0

    def listen(self,num):
        self.s.listen(num)
        return 0

    def accept(self):
        conn,addr = self.s.accept()
        s_key = None
        g_key = None
        bits = int(conn.recv(self.buffsize).decode())

        try:
            s_key = rsa.PublicKey.load_pkcs1(conn.recv(self.buffsize))
        except:
            return 1

        try:
            (public_key, private_key) = rsa.newkeys(bits)
            g_key = (public_key, private_key)
        except:
            return 2

        try:
            conn.send(g_key[0].save_pkcs1())
        except:
            return 3

        conn = TPWL_CONN(conn,s_key,g_key,self.buffsize)
        return conn,addr

    def close(self):
        self.s.close()
