import os,sys
sys.path.append(os.getcwd()+"/../")
import TPWL

s = TPWL.socket()
s.connect(("127.0.0.1",5000))
while True:
    data = input(">>>")
    s.send(data.encode())
    if data == "quit":
        break
s.close()
