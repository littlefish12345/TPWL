import os,sys
sys.path.append(os.getcwd())
import TPWL_S

s = TPWL_S.TPWL_S(8192)
s.bind(("127.0.0.1",5000))
s.listen(3)
conn,addr = s.accept()
while True:
    print(conn.recv())
conn.close()
s.close()
