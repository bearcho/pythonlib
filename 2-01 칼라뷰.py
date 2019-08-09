from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
import math
import numpy as np


### 메모리를 확보해서 반환하는 함수
def alloc2DMemory(height, width):
    retMemory = [];
    tmpList = []
    for i in range(height):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(width):
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory


##############################################
########### 칼라 영상 데이터 처리 ##########
##############################################
from PIL import Image


def loadImage(fname):
    global window, canvas, paper, inW, inH, outW, outH, inImage, outImage, filename, photo
    inImageR, inImageG, inImageB = [], [], []  # 초기화
    # 파일 크기 계산
    photo = Image.open(fname)
    inW = photo.width;
    inH = photo.height
    # 빈 메모리 확보 (2차원 리스트)
    inImage = []
    inImage.append(alloc2DMemory(inH, inW))
    inImage.append(alloc2DMemory(inH, inW))
    inImage.append(alloc2DMemory(inH, inW))
    # 파일 --> 메모리로 한개씩 옮기기
    photoRGB = photo.convert('RGB')
    for i in range(inH):
        for k in range(inW):
            r, g, b = photoRGB.getpixel((k, i))
            inImage[0][i][k] = r
            inImage[1][i][k] = g
            inImage[2][i][k] = b

    # print(inImageR[100][100],inImageG[100][100],inImageB[100][100])


def openFile():
    global window, canvas, paper, inW, inH, outW, outH, inImage, outImage, filename
    filename = askopenfilename(parent=window, filetypes=(("영상 파일", "*.gif;*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    # 파일 --> 메모리
    loadImage(filename)

    # Input --> outPut으로 동일하게 만들기.
    equal()


def display():
    global window, canvas, paper, inW, inH, outW, outH, inImage, outImage, filename
    if canvas != None:
        canvas.destroy()

    ### 고정된 화면을 준비 ###
    VIEW_X, VIEW_Y = 512, 512
    if VIEW_X >= outW and VIEW_Y >= outH:  # 원영상이 256이하면
        VIEW_X = outW;
        VIEW_Y = outH
        step = 1
    else:
        if outW > outH:
            step = outW / VIEW_X
        else:
            step = outH / VIEW_X

    window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X / 2, VIEW_Y / 2), image=paper, state='normal')

    import numpy
    rgbString = ''  # 여기에 전체 픽셀 문자열을 저장할 계획
    for i in numpy.arange(0, outH, step):
        tmpString = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            try:
                r, g, b = outImage[0][i][k], outImage[1][i][k], outImage[2][i][k]
            except:
                pass
            tmpString += ' #%02x%02x%02x' % (r, g, b)
        rgbString += '{' + tmpString + '} '
    paper.put(rgbString)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


##################################

def equal():  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    # 메모리 할당
    outImage = []
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))

    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = inImage[rgb][i][k]
    display()


def addImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    # 메모리 할당
    outImage = []
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))

    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    value = askinteger("","")
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                data = inImage[rgb][i][k] + value
                if data > 255 :
                    outImage[rgb][i][k] = 255
                elif  data < 0 :
                    outImage[rgb][i][k] = 0
                else :
                    outImage[rgb][i][k] = inImage[rgb][i][k] + value
    display()


def greyImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    # 메모리 할당
    outImage = []
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))
    outImage.append(alloc2DMemory(outH, outW))

    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    num = [0.2126, 0.7152, 0.0722]
    for i in range(inH):
        for k in range(inW):
            value = 0
            for rgb in range(3):
                value += inImage[rgb][i][k] * num[rgb]
            for rgb in range(3):
                outImage[rgb][i][k] = int(value)

    display()
# 0.2126 R + 0.7152 G + 0.0722 B
## 변수 선언 부분 ##
window = None
canvas = None
XSIZE, YSIZE = 256, 256
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4

## 메인 코드 부분 ##
window = Tk()
window.title('CJ 파이썬 라이브러리')
window.geometry('500x500')
canvas = Canvas(window, height=XSIZE, width=YSIZE)

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window);
window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=None)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=None)

pixelMenu = Menu(mainMenu);
mainMenu.add_cascade(label='화소점처리', menu=pixelMenu)
pixelMenu.add_command(label='동일영상', command=equal)
pixelMenu.add_command(label='밝게하기', command=addImage)
pixelMenu.add_command(label='그레이로', command=greyImage)

canvas.pack()
window.mainloop()