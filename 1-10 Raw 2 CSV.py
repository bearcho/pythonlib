from tkinter import *
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
from  tkinter.messagebox import *
import math
import numpy as np
import csv

### 함수부

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
    loadImage(filename) # 파일 --> 입력메모리
    equal() # 입력메모리--> 출력메모리

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


def equal():  #동일영상 알고리즘
    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    # 여기 부터 영상처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]

    display()

def addImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            imnum = inImage[i][k] + value
            if(imnum > 255):
                outImage[i][k] = 255
            else:
                outImage[i][k] = inImage[i][k] + value

    display()

def minusImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            imnum = inImage[i][k] + value
            if(imnum <= 0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = inImage[i][k] + value

    display()

def divImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    hap = 0
    for i in range(inH):
        hap += sum(inImage[i])

    avg = hap // (inH * inW)

    for i in range(inH):
        for k in range(inW):
            imnum = inImage[i][k]
            if(imnum <= avg):
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255

    display()

def divImage2():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    pixelList = []

    hap = 0
    for i in range(inH):
        pixelList += inImage[i]

    pixelList.sort()
    avg = pixelList[inH*inW//2]

    for i in range(inH):
        for k in range(inW):
            imnum = inImage[i][k]
            if(imnum <= avg):
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255

    display()

def oppImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            imnum = inImage[i][k]
            if(imnum <= 127):
                outImage[i][k] = 255 - imnum
            else:
                outImage[i][k] = 255 - imnum

    display()

def swichImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = inH;
    outW = inW;
    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][inW-1-k]

    display()

def depressImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    value = askinteger("숫자입력", "숫자 : ", minvalue=1, maxvalue=255)
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = int(inH/ value);
    outW = int(inW / value);
    print(outH,outW)
    # outH = inH;
    # outW = inW;

    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i*value][k*value]
            print(i*2 , k*2 )

    display()

def inpressImage():  #동일영상 알고리즘

    global window, canvas,paper,inImage, outImage,inW, outW, inH, outH,filename

    if inImage == None:
        return
    value = askinteger("숫자입력", "숫자 : ", minvalue=1, maxvalue=255)
    # 출력이미지의 크기를 결정(알고리즘에 따라서 달라짐)
    outH = int(inH * value);
    outW = int(inW * value);
    print(outH,outW)
    # outH = inH;
    # outW = inW;

    # 메모리 확보
    outImage = alloc2DMemory(outH, outW)
    #value = askinteger("숫자입력","숫자 : ",minvalue=1, maxvalue=255)
    # 여기 부터 영상처리 알고리즘
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[int(i/value)][int(k/value)]


    display()


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

### 전연 변수부
window, canvas,paper = [None] *3
inImage, outImage = None, None
inW, outW, inH, outH = [0] * 4
filename = None

### 메인코드 부
window = Tk()
window.title('CJON 컴퓨터 비전 ver 0.01')
status = Label(window,text='', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
canvas = Canvas(window, height=512, width = 512)
paper=PhotoImage(width=512, height=512)
canvas.create_image ( (512/2, 512/2), image=paper, state="normal")

mainMenu = Menu(window);window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=None)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=None)

visionMenu = Menu(mainMenu);mainMenu.add_cascade(label='컴퓨터비전', menu=visionMenu)
visionMenu.add_command(label='밝게하기', command=addImage)
visionMenu.add_command(label='어둡게하기', command=minusImage)
visionMenu.add_command(label='완전흑백만들기', command=divImage)
visionMenu.add_command(label='완전흑백만들기(중위수)', command=divImage2)
visionMenu.add_command(label='반전하기', command=oppImage)
visionMenu.add_command(label='좌우 위치바꾸기', command=swichImage)
visionMenu.add_command(label='화면 축소하기', command=depressImage)
visionMenu.add_command(label='화면 확대하기', command=inpressImage)


dataMenu = Menu(mainMenu);mainMenu.add_cascade(label='데이터분석/변환', menu=dataMenu)
dataMenu.add_command(label='CSV로 저장', command=saveCSV)

# dataMenu = Menu(mainMenu);mainMenu.add_cascade(label='데이터분석', menu=dataMenu)
# dataMenu.add_command(label='밝게하기', command=saveCSV)

canvas.pack()

window.mainloop()

# if __name__ == '__main__':
#     pass