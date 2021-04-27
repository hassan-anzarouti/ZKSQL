import sys
from time import time
import os
import re
import pyodbc
from time import time
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const
consql = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=server ip;'
                      'Database=db name;'
                      'uid=user;pwd=password;')
t1=time()
cursor = consql.cursor()
cursor.execute("Delete from zkteco.dbo.Attendances")
consql.commit()
conn = None
# create ZK instance
zkHQ = ZK('IP ADDRESS', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)


def conandinsert(zk):
    try:
        # connect to device
        conn = zk.connect()
        attendances = conn.get_attendance()
        param = []
        for att in attendances:
            stringg=(str(att))
            m = re.search(r"[\.]* ([0-9]*) : ([\d-]*) ([\d:]*)", stringg)
            templist=[]
            templist.append(m[1])
            xtimestamp = f"{m[2]} {m[3]}"
            templist.append(xtimestamp)
            param.append(templist)
        cursor.fast_executemany = True
        cursor.executemany("insert into zkteco.dbo.Attendances (AttendanceID,Date) values (?,?);",param)
        consql.commit()

    except Exception as e:
        print ("Process terminate : {}".format(e))

    finally:
        if conn:
            conn.disconnect()

conandinsert(zkHQ)

t2=time()
consql.close()
print(f"took {t2-t1} s")