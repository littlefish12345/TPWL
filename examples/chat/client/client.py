import os,sys
sys.path.append(os.getcwd()+"\\..\\..\\..\\api\\TPWL_rsa_api")
import TPWL_rsa

s = TPWL_rsa.TPWL_C()
s.create(1024)
s.connect(("127.0.0.1",5000))
while True:
    data = input(">>>")
    s.send(data.encode())
    if data == "quit":
        break
s.close()
