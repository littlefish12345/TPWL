import rsa,time
from socket import *

def version(): #打印版本号
    return 'beta 0.12'

class TPWL_C: #定义客户端类
    def __init__(self): #创建客户端
        self.s = socket(AF_INET,SOCK_STREAM)

    def create(self,bits): #创建密钥对
        self.bits = bits
        self.g_key = None
        
        (public_key, private_key) = rsa.newkeys(bits)
        self.g_key = (public_key, private_key)
        
        return 0 #创建成功返回0

    def connect(self,addr): #连接服务端
        self.addr = addr
        self.s_key = None
        
        self.s.connect(self.addr) #连接服务端
        
        self.s.send(str(self.bits).encode()) #发送密钥位数
        
        self.s.send(self.g_key[0].save_pkcs1()) #发送公钥
            
        self.s_key = rsa.PublicKey.load_pkcs1(self.s.recv(self.bits)) #接收公钥
        
        return 0 #协议通讯成功返回0

    def send(self,data): #发送数据
        
        added_data = rsa.encrypt(data,self.s_key) #用接收成功的公钥加密

        self.s.send(added_data) #把加密后的数据发送至服务器
        
        return 0 #发送成功返回0

    def recv(self,buffsize): #接收数据
        

        data = self.s.recv(buffsize) #接收来自服务器的数据
        
        decoded = rsa.decrypt(data, self.g_key[1]) #解密数据

        return decoded #返回解密后的数据

    def close(self): #关闭socket
        self.s.close()
