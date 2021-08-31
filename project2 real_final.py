from tkinter import *
import random
import tkinter.messagebox

tk = Tk()
tk.title("계산기 게임")
tk.minsize(width=400,height=550)
tk.maxsize(width=400,height=550)

global string, num_count, quiz_count, timer, score, timebonus_count, five_in_a_row
btns = []
timer = 30
running = 0
number = (1,2,3,4,5,6,7,8,9,0)
operation = ("+", "-", "X")
string = []
num_count = 0

quiz_count = 1
score = 0
timebonus_count = 0
five_in_a_row = 0


def msgbox():
    tkinter.messagebox.showwarning("연산자 오류", "숫자를 먼저 입력해주세요.")

def msgbox2():
    tkinter.messagebox.showwarning("자리수 오류", "한자리수 연산만 가능합니다.\n한자리수 숫자 입력 후 연산자를 입력해주세요.")

def msgbox3():
    tkinter.messagebox.showwarning("연산자 오류", "한개의 연산자만 입력해주세요.")

def msgbox4():
    tkinter.messagebox.showwarning("횟수 제한", "5번만 가능합니다.")

def timeup():
    tkinter.messagebox.showwarning("타임 오버", "당신의 점수는 {}".format(score))

def clearlev():
    timerText.destroy()
    tkinter.messagebox.showinfo("클리어!","당신의 점수는 {}".format(score))

def setrandom():
    global quiz_count, ran, timebonus_count
    if timebonus_count >= 1:
        timebonus_button.pack(padx = 10)

    ran = random.randrange(10,100)
    random_num.configure(text = ran,font = ("bold",20))
    Label(tk,text = "Level {}".format(quiz_count)).place(x = 300,y = 20)
    quiz_count += 1
    if five_in_a_row == 5:
        five_in_a_row_board.place(x = 20, y = 40)
    else:
        five_in_a_row_board.place_forget()

def clicked(i):
    global string
    string.append(i)
    result.configure(text = string, font = ("bold",18),fg = "red")

    if string[0] in operation:
        msgbox()
        reset()

    cnt = 0

    for cnt in range (0, len(string)-1):
        if len(string) > 1:
            if string[cnt] in number:
                if string[cnt+1] in number:
                    msgbox2()
                    reset()
            elif string[cnt] in operation:
                if string[cnt+1] in operation:
                    msgbox3()
                    reset()
    
def startTimer():
    if (running):
        global timer
        if timer > 0:
            timer -= 1
        else:
            dis()
            timeup()
            quit()
        timerText.configure(text=str(timer),fg = "blue")
    tk.after(1000,startTimer)
        
def time2score():
    global score
    score = score + timer*5
    scoreboard.configure(text = "당신의 점수 : " + str(score))

def dis():
    for x in (btns):
        a = x
        a.config(state=DISABLED)

def start():
    global running
    running = 1
    reset()
    setrandom()
    pass_button.pack(pady = 20)
    num_count_board.place(x = 20, y = 350)
    num_count_chance_button.place(x = 20, y = 370)
    start_button.pack_forget()
    scoreboard.configure(text = "당신의 점수 : " + str(score))
    
def stop():
    global running
    running = 0

def next():
    global running, timer, timebonus_count, five_in_a_row
    running = 1
    reset()
    time2score()
    if five_in_a_row == 5:
        time2score()
    if quiz_count == 11:
        time2score()
        stop()
        clearlev()
        quit()   
    
    five_in_a_row += 1

    if timer >= 25:
        timebonus_count += 1
        timebonus_board.configure(text = "시간 보너스 개수 : " + str(timebonus_count))
    timer = 30
    setrandom()
    timerText.configure(text=str(timer),fg = "blue")

def next2pass():
    global running, timer, five_in_a_row, num_count
    running = 1
    num_count = 0
    num_count_board.configure(text = "남은 기회 : " + str(5 - num_count))
    reset()
    if quiz_count == 11:
        clearlev()
        quit()
    five_in_a_row = 0
    setrandom()
    timer = 30
    timerText.configure(text=str(timer),fg = "blue")
    pass_button.pack_forget()


def equal():
    global num_count, ran, score, timer, five_in_a_row

    if "X" in string:
        i = len(string) - 2
        while True :
            if i<1:
                break
            if (string[i] == "X") :
                string[i - 1] = string[i - 1] * string[i + 1]
                del string[i]
                del string[i]
            i -=2

    if "+" in string:
      res_list = list(filter(lambda x: string[x] == "+", range(len(string))))
      for i in range (0, len(res_list)):
            string[res_list[0] - 1] = string[res_list[0] - 1] + string[res_list[0] + 1]
            del string[res_list[0]]
            del string[res_list[0]]

    if "-" in string:
      res_list = list(filter(lambda x: string[x] == "-", range(len(string))))
      for i in range (0, len(res_list)):
        string[res_list[0] - 1] = string[res_list[0] - 1] - string[res_list[0] + 1]
        del string[res_list[0]]
        del string[res_list[0]] 
        
    if string[0] == ran:
        del string[0]
        result.configure(text = "정답!", font = ("bold",20),fg = "red")
        num_count = 0
        num_count_board.configure(text = "남은 기회 : " + str(5 - num_count))
        stop()
        tk.after(1000,next)

    else:
        del string[0]
        result.configure(text = "땡!", font = ("bold",20),fg = "red")
        num_count += 1
        if num_count <= 5: 
            num_count_board.configure(text = "남은 기회 : " + str(5 - num_count))

    if num_count == 6:
        msgbox4()
        reset()
        if quiz_count == 11:
            clearlev()
            quit()
        setrandom()
        timer = 30
        score -= 100
        if score < 0:
            score = 0
        scoreboard.configure(text = "당신의 점수 : " + str(score))
        five_in_a_row = 0
        num_count = 0
        num_count_board.configure(text = "남은 기회 : " + str(5 - num_count))

        result.configure(text = string[0], font = ("bold",20),fg = "red")

def reset():
    global string
    string = []
    result.configure(text = string, font = ("bold",20))

def timebonus():
    global timebonus_count
    global timer
    timer += 10
    timerText.configure(text=str(timer),fg = "blue")
    timebonus_count -= 1
    timebonus_board.configure(text = "시간 보너스 개수 : " + str(timebonus_count))
    if timebonus_count == 0:
        timebonus_button.pack_forget()
        timerText.configure(text=str(timer),fg = "blue")


def num_count_chance():
    global num_count
    num_count -= 5
    num_count_board.configure(text = "남은 기회 : " + str(5 - num_count))
    num_count_chance_button.place_forget()


timebonus_button = Button(tk, text="10초 추가!",font = "18",width = 16, bg = "silver", command = timebonus)

pass_button = Button(tk, text="한 번 패스",font = "18",width = 16, bg = "silver", command = next2pass)


pack_up = Frame(tk,width = 400, height = 40)
pack_up.pack(pady = 20)

grid_down = Frame(tk,width = 400, height = 300)
grid_down.pack()

random_num = Label(pack_up,text = string, pady = 20)
random_num.pack()

timerText = Label(pack_up, text = "30", padx = 30, relief = "solid")
timerText.pack(side = "right")

result = Label(grid_down,text = "")
result.grid(row = 1, column = 5, columnspan = 4, sticky = 'n')

scoreboard = Label(tk,text = "당신의 점수 : " + str(score))
scoreboard.place(x = 20,y = 20)

timebonus_board = Label(tk,text = "시간 보너스 개수 : " + str(timebonus_count))
timebonus_board.place(x = 260, y = 40)

num_count_board = Label(tk,text = "남은 기회 : " + str(5 - num_count))

start_button = Button(tk, text="start",font = "18",width =16,bg = "silver", command = start)
start_button.pack(pady = 18)
btns.append(start_button)

num_count_chance_button = Button(tk, text="+5",bg = "silver", command = num_count_chance)

five_in_a_row_board = Label(tk,text = "점수 2배!")

b7 = Button(grid_down, text="7",font = "20",bg = "silver", command = lambda:clicked(7))
b7.grid(row = 2, column = 5, sticky = 'n',padx = 10, pady = 10)
btns.append(b7)
b8 = Button(grid_down, text = "8",font = "20",bg = "silver", command = lambda:clicked(8))
b8.grid(row = 2, column = 6, sticky = 'n',padx = 10, pady = 10)
btns.append(b8)
b9 = Button(grid_down, text = "9",font = "20",bg = "silver", command = lambda:clicked(9))
b9.grid(row = 2, column = 7, sticky = 'n',padx = 10, pady = 10)
b_mul = Button(grid_down, text = "X",font = "20",bg = "silver", command = lambda:clicked("X"))
b_mul.grid(row = 2, column = 8, sticky = 'n',padx = 10, pady = 10)
btns.append(b_mul)
btns.append(b9)
b4 = Button(grid_down, text="4",font = "20",bg = "silver", command = lambda:clicked(4))
b4.grid(row = 3, column = 5, sticky = 'n', padx = 10, pady = 10)
btns.append(b4)
b5 = Button(grid_down, text = "5",font = "20",bg = "silver", command = lambda:clicked(5))
b5.grid(row = 3, column = 6, sticky = 'n',padx = 10, pady = 10)
btns.append(b5)
b6 = Button(grid_down, text = "6",font = "20",bg = "silver", command = lambda:clicked(6))
b6.grid(row = 3, column = 7, sticky = 'n',padx = 10, pady = 10)
btns.append(b6)
b_min = Button(grid_down, text = "-",font = "20",bg = "silver", command = lambda:clicked("-"))
b_min.grid(row = 3, column = 8, sticky = 'n',padx = 10, pady = 10)
btns.append(b_min)
b1 = Button(grid_down, text="1",font = "20",bg = "silver", command = lambda:clicked(1))
b1.grid(row = 4, column = 5, sticky = 'n', padx = 10, pady = 10)
btns.append(b1)
b2 = Button(grid_down, text = "2",font = "20",bg = "silver", command = lambda:clicked(2))
b2.grid(row = 4, column = 6, sticky = 'n',padx = 10, pady = 10)
btns.append(b2)
b3 = Button(grid_down, text = "3",font = "20",bg = "silver", command = lambda:clicked(3))
b3.grid(row = 4, column = 7, sticky = 'n',padx = 10, pady = 10)
btns.append(b3)
b_add = Button(grid_down, text = "+",font = "20",bg = "silver", command = lambda:clicked("+"))
b_add.grid(row = 4, column = 8, sticky = 'n',padx = 10, pady = 10)
btns.append(b_add)
b_res = Button(grid_down, text = "c",font = "20",bg = "silver", command = reset)
b_res.grid(row = 5, column = 5, sticky = 'n',padx = 10, pady = 10)
btns.append(b_res)
b0 = Button(grid_down, text = "0",font = "20",bg = "silver", command = lambda:clicked(0))
b0.grid(row = 5, column = 6, sticky = 'n',padx = 10, pady = 10)
btns.append(b0)
b_eq = Button(grid_down, text = "=",font = "20",bg = "silver",width = 7, command = equal)
b_eq.grid(row = 5, column = 7,columnspan=2, sticky = 'n',padx = 10, pady = 10)
btns.append(b_eq)

startTimer()




tk.mainloop()
