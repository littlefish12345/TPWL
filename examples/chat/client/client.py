import os,sys
sys.path.append(os.getcwd())
import TPWL_C

s = TPWL_C.TPWL_C(8192)
s.create(1,1024)
s.connect(("127.0.0.1",5000))
while True:
    s.send(input(">>>"))
s.close()
