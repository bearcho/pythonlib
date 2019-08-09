from tkinter import *
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
from  tkinter.messagebox import *
import math
import numpy as np
import time
import pymysql
import os.path


filename = 'C:/AI/data/RAW/Pet_RAW(256x256)/cat01_256.raw'
fsize = os.path.getsize(filename) # 파일 크기 확인
inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)

inImage= None
inImage = np.fromfile(filename, dtype='uint8')

inImage = inImage.reshape(inH,inW)

print(type(inImage))
print(inImage)
conn = pymysql.connect(host='127.0.0.1', user='aiUser', password='1234', database='aidb', charset='utf8')
curr = conn.cursor()


fname = os.path.basename(filename)
for i in range(inH):
    for k in range(inW):

        sql = "insert into rawTable(fname, row, col, value) values('"
        sql += fname + "'," + str(i) + "," + str(k) + "," + str(inImage[i][k]) + ")"
        curr.execute(sql)

### 3. (필요시) 커밋
conn.commit()

### 4. 연결 종료
conn.close()
curr.close()
print("끝")
