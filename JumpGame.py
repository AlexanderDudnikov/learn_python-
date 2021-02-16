from tkinter import *
import random
import time


class Ball:      #Мяч
    def __init__(self, canvas, paddle, score, color): #Холст, отбивающая поверхность, счет,цвет
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color) #рисуем круг(5аргументов,левый верхний угол, нижний правый угол и цвет)
        self.canvas.move(self.id, 245, 100) #перемещаем круг приблизительно в центр холста
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts) #перемешали элемнты списка стартс
        self.x = starts[0] #поместили значение первого элемента списка
        self.y = -3 #для ускорения мяча
        self.canvas_height = self.canvas.winfo_height() #текущая высота холста
        self.canvas_width = self.canvas.winfo_width() #текущая ширина холста
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True
        return False

    def draw(self):  #для отскока мяча от границ холста
        self.canvas.move(self.id, self.x, self.y) #идинтификатор круга, перемещений по горизонтали и по вертикале
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:    #Код для проверки столкновения с отбивной
            self.y = -3                     #
        if pos[0] <= 0:                     #
            self.x = 3                      #
        if pos[2] >= self.canvas_width:     #
            self.x = -3                     #


class Paddle:  #отбивающая поверхность
    def __init__(self, canvas, color):      #принимаем аргументы холст и цвет
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)  #для перемещения отбивной
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)  #при нажатии стрелки влево, двигает влево
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right) #при нажатии стрелки вправо, двигает вправо
        self.canvas.bind_all('<Button-1>', self.start_game)   #для начала нажать ПКМ

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0: #если левая Х координата меньше или ровна 0
            self.x = 0 #обнуляем Х
        elif pos[2] >= self.canvas_width: #Если правая x-координата больше или равна ширине холста
            self.x = 0  #обнуляем Х

    def turn_left(self, evt):   #перемещение влево
        self.x = -2

    def turn_right(self, evt):    #перемещение вправо
        self.x = 2

    def start_game(self, evt):
        self.started = True

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)

tk = Tk()
tk.title("Game") #Заголовок проекта
tk.resizable(0, 0)  #Аргументы(0,0)означают: размер окна должен быть неизменным(по горизонтали и (по вертикали))
tk.wm_attributes("-topmost", 1) #Указываем, что окно должно быть поверх всех окон
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()   #холст изменит размер в соответствии со значениями ширины и высоты, указанными в предыдущей строке кода
tk.update() #обновление экрана


score = Score(canvas, 'green')
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle,score, 'red')
game_over_text = canvas.create_text(250, 200, text='GAME OVER', state='hidden')



while 1:
    if ball.hit_bottom == False and paddle.started == True:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        time.sleep(1)
        canvas.itemconfig(game_over_text, state='normal')
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

