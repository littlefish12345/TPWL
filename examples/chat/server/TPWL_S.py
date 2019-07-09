import rsa,time
from socket import *

def version():
    return 0.01

class TPWL_CONN:
    def __init__(self,conn,s_keys,g_keys,buffsize,times):
        self.conn = conn
        self.buffsize = buffsize
        self.times = times
        self.s_keys = s_keys
        self.g_keys = g_keys
        return None
    
    def recv(self):
        try:
            data = self.conn.recv(self.buffsize)
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
    
    def send(self,data):
        try:
            added_data = rsa.encrypt(data.encode(),self.s_keys[0])
            for i in range(1,self.times):
                added_data = rsa.encrypt(added_data,self.s_keys[i])
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
        s_keys = []
        g_keys = []
        times = int(conn.recv(self.buffsize).decode())
        bits = int(conn.recv(self.buffsize).decode())

        for i in range(0,times):
            try:
                s_keys.append(rsa.PublicKey.load_pkcs1(conn.recv(self.buffsize)))
            except:
                return 1

        for i in range(0,times):
            try:
                (public_key, private_key) = rsa.newkeys(bits)
                g_keys.append((public_key, private_key))
            except:
                return 2

        for i in range(0,times):
            try:
                conn.send(g_keys[i][0].save_pkcs1())
                time.sleep(0.01)
            except:
                return 3

        conn = TPWL_CONN(conn,s_keys,g_keys,self.buffsize,times)
        return conn,addr

    def close(self):
        self.s.close()
