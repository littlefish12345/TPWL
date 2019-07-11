import os,sys
sys.path.append(os.getcwd()+"\\..\\..\\..\\api\\TPWL_server_api")
import TPWL_S

s = TPWL_S.TPWL_S()
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
