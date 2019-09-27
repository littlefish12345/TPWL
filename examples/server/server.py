import os,sys
sys.path.append(os.getcwd()+"/../../")
import TPWL

s = TPWL.socket()
s.bind(("127.0.0.1",5000))
s.listen(3)
conn,addr = s.accept()
while True:
    data = conn.recv(8192).decode()
    if data == "quit":
        break
    print(data)
conn.close()
s.close()
