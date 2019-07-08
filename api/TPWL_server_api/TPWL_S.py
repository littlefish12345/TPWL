import os,socket,rsa,time

def version():
    return 0.01

class TPWL_CONN():
    def __init__(self,conn,s_keys,g_keys,buffsize,times):
        self.conn = conn
        self.buffsize = buffsize
        self.times = times
        self.s_keys = s_keys
        self.g_keys = g_keys
        return 0
    
    def recv(self):
        try:
            data = self.conn.recv(self.buffsize)
        except:
            return 1
        
        try:
            de_data = rsa.decrypt(data, self.g_keys[0][1])
            for i in range(1,times):
                de_data = rsa.decrypt(de_data, self.g_keys[i][1])
            de_data = de_data.decode()
        except:
            return 2
        
        return de_data
    
    def send(self,data):
        try:
            added_data = rsa.encrypt(data.encode(),self.s_keys[0])
            for i in range(i,self.times):
                added_data = rsa.encrypt(added_data,self.s_keys[i])
        except:
            return 1
        
        try:
            self.conn.send(added_data)
        except:
            return 2
        
        return 0

class TPWL_S():
    def __init__(self,buffsize):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.buffsize = buffsize
        return 0
        
    def blind(self,addr):
        self.s.blind(addr)
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

        for i in range(0:times):
            try:
                s_keys.append(rsa.PublicKey.load_pkcs1(conn.recv(self.buffsize)))
            except:
                return 1

        for i in range(0:times):
            try:
                (public_key, private_key) = rsa.newkeys(bits)
                g_keys.append((public_key, private_key))
            except:
                return 2

        for i in range(0:times):
            try:
                conn.send(g_keys[i][0].save_pkcs1())
                time.sleep(0.01)
            except:
                return 3

        conn = TPWL_CONN(conn,s_keys,g_keys,self.buffsize,self.times)
        return conn,addr
