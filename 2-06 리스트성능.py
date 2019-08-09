from tkinter import *
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
from  tkinter.messagebox import *
import math
import numpy as np
import time

### 함수부 ###
### 메모리를 확보해서 반환하는 함수
def alloc2DMemory(height, width) :
    retMemory = [];   tmpList = []
    for i in range(height):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(width):
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory

def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname) # 파일 크기 확인
    inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)
    inImage = []; tmpList = []
    # 메모리 할당
    inImage= None
    inImage = alloc2DMemory(inH, inW)

    print(len(inImage))

    # 파일 --> 메모리로 데이터 로딩
    fp = open(fname, 'rb') # 파일 열기(바이너리 모드)
    for  i  in range(inH) :
        for  k  in  range(inW) :
            inImage[i][k] =  int(ord(fp.read(1)))
    fp.close()

def openFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    start = time.time()
    loadImage(filename) # 파일 --> 입력메모리
    equal() # 입력메모리--> 출력메모리
    seconds = time.time() - start
    status.configure(text=status.cget('text') + '\t\t 걸린초 :' + '{0:.2f}'.format(seconds))
def display() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH, VIEW_X, VIEW_Y
    # 기존에 캐버스 있으면 뜯어내기.
    if canvas != None:
        canvas.destroy()
    # 화면 준비 (고정됨)
    VIEW_X, VIEW_Y = 512, 512
    if VIEW_X >= outW or VIEW_Y >= outH:  # 영상이 512미만이면
        VIEW_X = outW
        VIEW_Y = outH
        step = 1  # 건너뛸숫자
    else:
        step = outW / VIEW_X  # step을 실수도 인정. 128, 256, 512 단위가 아닌 것 고려.

    window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))
    canvas = Canvas(window, width=VIEW_X, height=VIEW_Y)
    paper = PhotoImage(width=VIEW_X, height=VIEW_Y)
    canvas.create_image((VIEW_X / 2, VIEW_X / 2), image=paper, state='normal')

    # 화면에 출력. 실수 step을 위해서 numpy 사용
    rgbString = ''  # 여기에 전체 픽셀 문자열을 저장할 계획
    for i in np.arange(0, outH, step):
        tmpString = ''
        for k in np.arange(0, outW, step):
            i = int(i);            k = int(k)  # 첨자이므로 정수화
            r = g = b = outImage[i][k];
            tmpString += ' #%02x%02x%02x' % (r, g, b)
        rgbString += '{' + tmpString + '} '
    paper.put(rgbString)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))
###############################
def  equal() :  # 동일 영상 알고리즘
    global window, canvas, paper,inImage, outImage ,inW, outW, inH, outH, filename
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;  outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(inH) :
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    ########################################
    display()

def  addImage() :  # 더하기 영상 알고리즘
    global window, canvas, paper,inImage, outImage ,inW, outW, inH, outH, filename
    if inImage == None :
        return
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;  outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    value = askinteger("숫자입럭", "숫자 :", minvalue=1, maxvalue = 255)
    for i in range(inH) :
        for k in range(inW):
            data = inImage[i][k] + value
            if data > 255 :
                outImage[i][k] = 255
            else :
                outImage[i][k] = inImage[i][k] + value
    ########################################
    display()

def  bwImage() :  #
    global window, canvas, paper,inImage, outImage ,inW, outW, inH, outH, filename
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;  outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    hap = 0
    for i in range(inH) :
        hap += sum(inImage[i])
    avg = hap // (inH*inW)
    for i in range(inH) :
        for k in range(inW):
            if inImage[i][k] > avg :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
    ########################################
    display()
def  bwImage2() :  #
    global window, canvas, paper,inImage, outImage ,inW, outW, inH, outH, filename
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;  outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    pixelList = []
    for i in range(inH) :
        pixelList += inImage[i]
    pixelList.sort()
    avg = pixelList[inH*inW//2]
    for i in range(inH) :
        for k in range(inW):
            if inImage[i][k] > avg :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
    ########################################
    display()

def reverseImage() :
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;
    outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255- inImage[i][k]
    ########################################
    display()
def mirrorImage():
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH;
    outW = inW
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][inW-k-1]
    ########################################
    display()
def zoomOutImage():
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    scale = askinteger("","")
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH // scale
    outW = inW // scale
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(inH):
        for k in range(inW):
            outImage[i//scale][k//scale] = inImage[i][k]
    ########################################
    display()
def zoomOutImage2():
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    scale = askinteger("","")
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH // scale
    outW = inW // scale
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(outH):
        for k in range(outW):
            hap = 0
            for m in range(scale) :
                for n in range(scale) :
                    hap += inImage[i*scale+m][k*scale+n]
            avg = hap // (scale*scale)
            outImage[i][k] = avg
    ########################################
    display()

def zoomInImage():
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    scale = askinteger("", "")
    # (중요!) 출력이미지의 크기를 결정(알고리즘에 따라서..)
    outH = inH * scale
    outW = inW * scale
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    ###### 여기가 진짜 영상처리 알고리즘 ######
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//scale][k//scale]
    ########################################
    display()

import csv
def saveCSV() :
    global window, canvas, paper, inImage, outImage, inW, outW, inH, outH, filename
    csvName = asksaveasfilename(parent=window,
       filetypes=(("CSV파일", "*.CSV"), ("모든파일", "*.*")))

    with open(csvName,'w', newline='') as wfp :
        csv_wfp = csv.writer(wfp, delimiter=',')
        # 헤더 처리
        csv_wfp.writerow(['row', 'col', 'value'])
        for i in range(outH):
            for k in range(outW):
                rowList = [i, k, outImage[i][k]]
                csv_wfp.writerow(rowList)

    messagebox.showinfo("성공","저장 성공")



def openCSV() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    csvName = askopenfilename(parent=window,
                               filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    with  open(csvName, 'r', newline='') as rfp:
            csv_rfp = csv.reader(rfp, delimiter=',')
            # 라인수 카운트
            header = next(csv_rfp)
            fsize = sum(1 for line in csv_rfp)
            inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)
            inImage = [];
            tmpList = []
            # 메모리 할당
            inImage = None
            inImage = alloc2DMemory(inH, inW)
            rfp.seek(0,0)
            header = next(csv_rfp)

            for  r in csv_rfp :
                row, col, value = list(map(int,r))
                inImage[row][col] = value

    equal() # 입력메모리--> 출력메모리
import pymysql
import os.path
def saveMysql():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH


    ### 1. 커넷션 생성 및 커서 준비

    conn = pymysql.connect(host='127.0.0.1', user='aiUser', password='1234', database='aidb', charset='utf8')
    curr = conn.cursor()

    ### 2. sql 준비 및 실행
    # sql = "CREATE TABLE IF NOT EXISTS imageTable(fname CHAR(20), X SMALLINT , Y SMALLINT, R SMALLINT, G SMALLINT, B SMALLINT)"
    # curr.execute(sql)
    fname = os.path.basename(filename)
    for i in range(outH):
        for k in range(outW):
            r = g = b = outImage[i][k]
            sql = "insert into imageTable(fname, x, y, r, g ,b) values('"
            sql += fname + "'," + str(i) + "," + str(k) + "," + str(r) + "," + str(g) + "," +str(b) + ")"
            curr.execute(sql)

    ### 3. (필요시) 커밋
    conn.commit()

    ### 4. 연결 종료
    conn.close()
    curr.close()
    print("끝")

def openMySQL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global selectedIndex

    ### 1. 커넷션 생성 및 커서 준비

    conn = pymysql.connect(host='127.0.0.1', user='aiUser', password='1234', database='aidb', charset='utf8')
    curr = conn.cursor()

    ### 2. sql 준비 및 실행
    sql = "SELECT DISTINCT fname from imageTable"
    curr.execute(sql)
    fnameList = curr.fetchall()
    ##작은 서브 윈도우 뛰우기
    popWindow = Tk()
    listbox = Listbox(popWindow)
    listbox.pack()
    for item in fnameList:
        listbox.insert(END,item)

    selectedIndex=None

    def btnClick():
        global selectedIndex
        selectedIndex = listbox.curselection()[0]
        popWindow.quit()
        popWindow.destroy()

    button = Button(popWindow, text = '요거', command=btnClick)
    button.pack()
    popWindow.mainloop()

    ##이 위치에서 파일명이 결정됨
    print(selectedIndex)
    seFname = fnameList[selectedIndex][0]
    print(seFname)

    ##메모리 할당
    sql = "SELECT count(*) FROM imagetable WHERE fname='" + seFname + "'"
    curr.execute(sql)
    fsize = int(curr.fetchone()[0])
    inH = inW = int(math.sqrt(fsize))

    inImage = None
    inImage = alloc2DMemory(inH, inW)

    sql = "SELECT x,y,r,g,b from imagetable where fname = '" + seFname + "'"
    curr.execute(sql)

    while True:
        try:
            x,y,r,g,b = curr.fetchone()
            inImage[x][y] = r

        except :
            break

    ### 3. (필요시) 커밋
    conn.commit()

    ### 4. 연결 종료
    conn.close()
    curr.close()
    equal()
    print("끝")

def saveColorMysql():
    pass

def openColorMySQL():
    pass

### 전역 변수부 ###
window, canvas, paper = [None] * 3
inImage, outImage = None, None
inW, outW, inH, outH = [0] * 4
filename = None

### 메인코드부 ###
window = Tk()
window.title('CJON 컴퓨터 비전 Ver 0.01')
status = Label(window, text='', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
canvas = Canvas(window, height=512, width=512)
paper = PhotoImage(width=512, height=512)
canvas.create_image ( (512/2, 512/2), image=paper, state="normal")
mainMenu = Menu(window);window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=None)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=None)

visionMenu = Menu(mainMenu);mainMenu.add_cascade(label='컴퓨터비전', menu=visionMenu)
visionMenu.add_command(label='밝게하기', command=addImage)
visionMenu.add_command(label='흑백 만들기(평균)', command=bwImage)
visionMenu.add_command(label='흑백 만들기(중위수)', command=bwImage2)
visionMenu.add_command(label='반전', command=reverseImage)
visionMenu.add_command(label='좌우위치 바꾸기', command=mirrorImage)
visionMenu.add_command(label='축소', command=zoomOutImage)
visionMenu.add_command(label='축소(평균값)', command=zoomOutImage2)
visionMenu.add_command(label='확대', command=zoomInImage)

dataMenu = Menu(mainMenu);mainMenu.add_cascade(label='데이터분석/변환', menu=dataMenu)
dataMenu.add_command(label='CSV로 저장', command=saveCSV)
dataMenu.add_command(label='CSV에서 불러오기', command=openCSV)
dataMenu.add_command(label='mysql로 저장', command=saveMysql)
dataMenu.add_command(label='mysql에서 불러오기', command=openMySQL)
dataMenu.add_command(label='mysql로 칼라 저장', command=saveColorMysql)
dataMenu.add_command(label='mysql에서 칼라 불러오기', command=openColorMySQL)
canvas.pack()
window.mainloop()