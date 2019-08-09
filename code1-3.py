from tkinter import *
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
from  tkinter.messagebox import *
import math
import numpy as np
import time
import pymysql
import os.path


conn = pymysql.connect(host='127.0.0.1', user='aiUser', password='1234', database='aidb', charset='utf8')
curr = conn.cursor()

sql = "SELECT count(*)  from rawTable where fname = 'cat01_256.raw'"
curr.execute(sql)
fnameList = curr.fetchall()
curr.execute(sql)
fsize = int(curr.fetchone()[0])
print(fsize)
# inH = inW = int(math.sqrt(fsize))
sql2 = "SELECT  row , col, value from rawTable where fname = 'cat01_256.raw'"
curr.execute(sql2)

# inImage = np.zeros((fsize,3),dtype='float') for문 돌려서 한번씩 수행 해야 할것 같음

inImage = []
i = 0
while True:
    try:
        row, col,value = curr.fetchone()
        inImage.append([row, col,value])
    except Exception as ex:
        print(ex)
        break

npinImage = np.array(inImage)
print(npinImage.max())
print(npinImage.min())


### 3. (필요시) 커밋
conn.commit()

### 4. 연결 종료
conn.close()
curr.close()
print("끝")
