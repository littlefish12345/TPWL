import rsa,time
import socket as sock

def version(): #返回版本号
    return 'beta 0.18'

class TPWL_CONN: #定义通讯类
    def __init__(self,conn,s_key,g_key,bits): #获取来自服务端类的收发密钥(公钥)
        self.conn = conn
        self.s_key = s_key
        self.g_key = g_key
        self.bits = bits
    
    def recv(self,buffsize): #接收数据
        all_data = b''
        while True:
            data = self.conn.recv(67108864) #接收来自客户端的数据
            if data == b'done':
                break
            else:
                all_data = all_data+data

        all_encoded_list = []
        i = 0
        one_pack_size = round(self.bits/8)
        while True:
            if len(all_data) <= (i+1)*one_pack_size:
                all_encoded_list.append(all_data[i*one_pack_size:])
                break
            all_encoded_list.append(all_data[i*one_pack_size:(i+1)*one_pack_size])
            i = i+1
        
        decoded_list = []

        for data_encoded in all_encoded_list:
            decoded = rsa.decrypt(data_encoded, self.g_key[1]) #反复解密数据
            decoded_list.append(decoded)
        
        all_decoded = b''.join(decoded_list)
        
        return all_decoded #返回解密后的数据
    
    def send(self,data): #发送数据
        data_list = []
        i = 0
        max_message = round(self.bits/8-11)

        while True:
            if len(data) <= (i+1)*max_message:
                data_list.append(data[i*max_message:])
                break
            data_list.append(data[i*max_message:(i+1)*max_message])
            i = i+1

        encoded_list = []
        for data_for in data_list:
            added_data = rsa.encrypt(data_for,self.s_key) #用接收成功的公钥加密
            encoded_list.append(added_data)

        all_data = b''.join(encoded_list)

        all_data_pack = []
        i = 0
        while True:
            if len(data) <= (i+1)*67108864:
                all_data_pack.append(all_data[i*67108864:])
                break
            all_data_pack.append(all_data[i*67108864:(i+1)*67108864])
            i = i+1
        
        for pack_data in all_data_pack:
            self.conn.send(pack_data)
            time.sleep(0.01)
        self.conn.send(b'done')

        return 0 #发送成功返回0

    def close(self): #关闭这个连接
        self.conn.close()

class socket: #定义socket类
    def __init__(self): #创建服务端
        self.s = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
        
    def bind(self,addr): #绑定地址
        self.s.bind(addr)
        return

    def listen(self,num): #监听端口
        self.s.listen(num)
        return

    def accept(self): #获取连接并进行协议交换公钥
        conn,addr = self.s.accept() #获取连接
        
        s_key = None #定义公钥私钥变量
        g_key = None
        
        bits = int(conn.recv(8192).decode()) #获取加密位数

        s_key = rsa.PublicKey.load_pkcs1(conn.recv(bits)) #获取公钥

        (public_key, private_key) = rsa.newkeys(bits) #生成密钥对
        g_key = (public_key, private_key)

        conn.send(g_key[0].save_pkcs1()) #发送公钥

        conn = TPWL_CONN(conn,s_key,g_key,bits) #创建TPWL通讯类
        
        return conn,addr #返回TPWL通讯类和客户端

    def connect(self,addr,bits=1024): #连接服务端
        self.bits = bits
        self.g_key = None
        
        (public_key, private_key) = rsa.newkeys(bits) #创建密钥对(默认1024位)
        self.g_key = (public_key, private_key)
        
        self.addr = addr
        self.s_key = None
        
        self.s.connect(self.addr) #连接服务端
        
        self.s.send(str(self.bits).encode()) #发送密钥位数
        
        self.s.send(self.g_key[0].save_pkcs1()) #发送公钥
            
        self.s_key = rsa.PublicKey.load_pkcs1(self.s.recv(self.bits)) #接收公钥
        
        return 0 #协议通讯成功返回0

    def recv(self,buffsize): #接收数据
        all_data = b''
        while True:
            data = self.s.recv(67108864) #接收来自客户端的数据
            if data == b'done':
                break
            else:
                all_data = all_data+data
        all_encoded_list = []
        i = 0
        one_pack_size = round(self.bits/8)
        while True:
            if len(all_data) <= (i+1)*one_pack_size:
                all_encoded_list.append(all_data[i*one_pack_size:])
                break
            all_encoded_list.append(all_data[i*one_pack_size:(i+1)*one_pack_size])
            i = i+1
        
        decoded_list = []
        for data_encoded in all_encoded_list:
            decoded = rsa.decrypt(data_encoded, self.g_key[1]) #反复解密数据
            decoded_list.append(decoded)
        
        all_decoded = b''.join(decoded_list)
        return all_decoded #返回解密后的数据
    
    def send(self,data): #发送数据
        data_list = []
        i = 0
        max_message = round(self.bits/8-11)

        while True:
            if len(data) <= (i+1)*max_message:
                data_list.append(data[i*max_message:])
                break
            data_list.append(data[i*max_message:(i+1)*max_message])
            i = i+1

        encoded_list = []
        for data_for in data_list:
            added_data = rsa.encrypt(data_for,self.s_key) #用接收成功的公钥加密
            encoded_list.append(added_data)

        all_data = b''.join(encoded_list)

        all_data_pack = []
        i = 0
        while True:
            if len(data) <= (i+1)*67108864:
                all_data_pack.append(all_data[i*67108864:])
                break
            all_data_pack.append(all_data[i*67108864:(i+1)*67108864])
            i = i+1
        
        for pack_data in all_data_pack:
            self.s.send(pack_data)
            time.sleep(0.01)
        self.s.send(b'done')

        return 0 #发送成功返回0

    def close(self): #关闭socket
        self.s.close()
