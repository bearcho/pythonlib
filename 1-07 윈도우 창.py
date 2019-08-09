from tkinter import *

### 함수부


### 전연 변수부
window, canvas,paper = [None] *3

### 메인코드 부
window = Tk()
canvas = Canvas(window, height=512, width = 512)
paper=PhotoImage(width=512, height=512)
canvas.create_image ( (512/2, 512/2), image=paper, state="normal")

mainMenu = Menu(window);window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=None)
fileMenu.add_command(label='저장', command=None)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=None)


canvas.pack()

window.mainloop()

# if __name__ == '__main__':
#     pass