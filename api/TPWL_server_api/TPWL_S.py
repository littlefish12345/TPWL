import rsa,time
from socket import *

def version(): #打印版本号
    return 'beta 0.12'

class TPWL_CONN: #定义通讯类
    def __init__(self,conn,s_key,g_key): #获取来自服务端类的收发密钥(公钥)
        self.conn = conn
        self.s_key = s_key
        self.g_key = g_key
    
    def recv(self,buffsize): #接收数据
        
        data = self.conn.recv(buffsize) #接收来自客户端的数据
        
        decoded = rsa.decrypt(data, self.g_key[1]) #解密数据

        return decoded #返回解密后的数据
    
    def send(self,data): #发送数据
        
        added_data = rsa.encrypt(data,self.s_key) #用接收成功的公钥加密
        
        self.conn.send(added_data) #把加密后的数据发送至服务器

        return 0 #发送成功返回0

    def close(self): #关闭这个连接
        self.conn.close()

class TPWL_S: #定义服务端类
    def __init__(self): #创建服务端
        self.s = socket(AF_INET,SOCK_STREAM)
        
    def bind(self,addr): #绑定地址
        self.s.bind(addr)
        return 0

    def listen(self,num): #监听端口
        self.s.listen(num)
        return 0

    def accept(self): #获取连接并进行协议交换公钥
        conn,addr = self.s.accept() #获取连接
        
        s_key = None #定义公钥私钥变量
        g_key = None
        
        bits = int(conn.recv(8192).decode()) #获取加密位数

        s_key = rsa.PublicKey.load_pkcs1(conn.recv(bits)) #获取公钥

        (public_key, private_key) = rsa.newkeys(bits) #生成密钥对
        g_key = (public_key, private_key)

        conn.send(g_key[0].save_pkcs1()) #发送公钥

        conn = TPWL_CONN(conn,s_key,g_key) #创建TPWL通讯类
        
        return conn,addr #返回TPWL通讯类和客户端

    def close(self): #关闭socket
        self.s.close()
