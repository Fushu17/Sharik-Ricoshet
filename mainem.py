import random
import time
from tkinter import *  # Импортируем модуль


class Ball:
    def __init__(self, canvas, paddle, color, tk, lev):
        self.lev = lev
        self.tk = tk
        self.canvas = canvas
        self.speed = self.canvas.winfo_height() / 350
        if lev >= 3:
            self.speed = self.speed * 2
        self.ball_r = self.canvas.winfo_height() / 75
        if self.lev == 1 or self.lev == 2 or self.lev == 3:
            self.bricks = Brick(self.canvas, ).draw_start(rows=4, colums=10)
        else:
            self.bricks = Brick(self.canvas, ).draw_start(rows=4, colums=20)
        if self.lev == 2 or self.lev == 3 or self.lev == 4 or self.lev == 5:
            self.blocks, self.blocks0 = Block(self.canvas, self.lev).draw()
        self.paddle = paddle
        self.paddle_pos = self.canvas.coords(self.paddle.id)

        self.id = canvas.create_oval(self.canvas.winfo_height() // 2 - self.ball_r,
                                     self.canvas.winfo_width() // 2 - self.ball_r,
                                     self.canvas.winfo_height() // 2 + self.ball_r,
                                     self.canvas.winfo_width() // 2 + self.ball_r,
                                     fill=color,
                                     outline="black")
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -self.speed
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.score = 0
        self.score_t = Label(self.canvas, text=f"{self.score}", font="Hack 20")
        self.score_t.pack(anchor=SW)

    def hit_paddle(self, pos):
        self.paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= self.paddle_pos[0] and pos[0] <= self.paddle_pos[2]:
            if pos[3] >= self.paddle_pos[1] and pos[3] <= self.paddle_pos[3]:
                return True
            return False

    def draw(self):
        self.score_t.config(text=f'{self.score}')
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.speed
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -self.speed
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= self.canvas_width:
            self.x = -self.speed
        brick = self.get_brick(pos)
        if brick:
            self.y = -self.y
            self.canvas.delete(brick)
            self.bricks.pop(self.bricks.index(brick))
            self.score += 1

        if self.lev != 1:
            g_b = self.g_b(pos)

            block = self.get_block(pos)

            if g_b:
                self.x = -self.x

            elif block:
                self.y = -self.y

        self.canvas.move(self.id, self.x, self.y)

    def g_b(self, pos):
        for block in self.blocks0:
            xb1, yb1, xb2, yb2 = self.canvas.coords(block)
            if (xb1 < pos[0] < xb2 or xb1 > pos[3] > xb2) and (yb1 < pos[1] < yb2 or yb1 < pos[3] < yb2):
                return block

    def get_block(self, pos):
        for block in self.blocks:
            xb1, yb1, xb2, yb2 = self.canvas.coords(block)
            if (xb1 < pos[0] < xb2 or xb1 > pos[3] > xb2) and (yb1 < pos[1] < yb2 or yb1 < pos[3] < yb2):
                return block

    def get_brick(self, pos):
        if len(self.bricks) == 0:
            self.tk.destroy()
            Win().create_win()
            return 0
        for brick in self.bricks:
            xb1, yb1, xb2, yb2 = self.canvas.coords(brick)
            if xb1 < pos[0] < xb2 and yb1 < pos[1] < yb2:
                return brick


class Block:
    def __init__(self, canvas, lev):
        self.canvas = canvas
        self.lev = lev

    def draw(self):
        if self.lev != 1 and self.lev != 5:
            blocks = []
            blocks0 = []
            blocks.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 16.8,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 6.7,
                                             self.canvas.winfo_height() // 1.51, fill="blue"))
            blocks.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.86,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.34,
                                             self.canvas.winfo_height() // 1.51, fill="blue"))
            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 16.8,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 16.8 + 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))
            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 6.7 - 10,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 6.7,
                                             self.canvas.winfo_height() // 1.51, fill="green"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.86,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.86 + 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.34,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.34 - 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))
            return blocks, blocks0
        elif self.lev == 5:
            blocks = []
            blocks0 = []
            blocks.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 16.8, self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 6.7,
                                             self.canvas.winfo_height() // 1.51, fill="blue"))
            blocks.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.86, self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.34,
                                             self.canvas.winfo_height() // 1.51, fill="blue"))
            blocks.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 3.5, self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 2.8,
                                             self.canvas.winfo_height() // 1.51, fill="blue"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 16.8,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 16.8 + 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))
            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 6.7 - 10,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 6.7,
                                             self.canvas.winfo_height() // 1.51, fill="green"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.86,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.86 + 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 1.34,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 1.34 - 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))

            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 3.5,
                                             self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 3.5 - 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))
            blocks0.append(
                self.canvas.create_rectangle(self.canvas.winfo_width() // 2.8, self.canvas.winfo_height() // 1.6,
                                             self.canvas.winfo_width() // 2.8 + 10,
                                             self.canvas.winfo_height() // 1.51, fill="green"))
            return blocks, blocks0


class Brick:
    def __init__(self, canvas):
        self.bricks_part = 0.3
        self.canvas = canvas

    def draw_start(self, rows, colums):
        bricks = []

        self.h_brick = (self.canvas.winfo_height() * self.bricks_part) / rows
        self.w_brick = self.canvas.winfo_width() / colums
        for y in range(rows):
            for x in range(colums):
                red, green, blue = (random.randint(0, 255) for _ in range(3))
                color = f'#{red:0>2x}{green:0>2x}{blue:0>2x}'
                brick = self.canvas.create_rectangle(x * self.w_brick, y * self.h_brick,
                                                     x * self.w_brick + self.w_brick,
                                                     y * self.h_brick + self.h_brick, fill=color, outline="black")
                bricks.append(brick)
        return bricks


class Paddle:
    def __init__(self, canvas, color, output_color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(325, 575, 575, 600,
                                          fill="green", outline=output_color)
        # self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.left = False
        self.right = False
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', lambda event: self.turning(2))
        self.canvas.bind_all('<KeyPress-Right>', lambda event: self.turning(1))
        self.canvas.bind_all('<KeyRelease-Right>', lambda event: self.turning(-1))
        self.canvas.bind_all('<KeyRelease-Left>', lambda event: self.turning(-2))

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] >= 0 and self.x < 0:
            self.canvas.move(self.id, self.x, 0)
        elif pos[2] <= self.canvas_width and self.x > 0:
            self.canvas.move(self.id, self.x, 0)

    def turning(self, direction):
        # 1 право 2 лево -1 право отпустил -2 отпустил лево
        if direction == 1:
            self.right = True
            self.x = 10
        elif direction == 2:
            self.x = -10
            self.left = True
        elif direction == -2:
            self.left = False
            if self.right is False or self.x == -3:
                self.x = 0
                if self.right is True:
                    self.x = 10
        elif direction == -1:
            self.right = False
            if self.left is False or self.x == 3:
                self.x = 0
                if self.left is True:
                    self.x = -10


class Start_Game0:
    def __init__(self, old_win=None):
        self.old_win = old_win
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.geometry("800x600")

    def End(self):
        self.tk.destroy()

    def Start(self):
        self.old_win.destroy()
        canvas = Canvas(self.tk, highlightthickness=0)
        canvas.pack(expand=True, fill=BOTH)
        self.tk.update()

        paddle = Paddle(canvas, color='green', output_color="black")
        ball = Ball(canvas, paddle, color='red', tk=self.tk, lev=1)

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                try:
                    self.tk.destroy()
                    Lose().create_win()
                except:
                    pass
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.005)


class Start_Game1:
    def __init__(self, old_win=None):
        self.old_win = old_win
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.geometry("800x600")

    def End(self):
        self.tk.destroy()

    def Start(self):
        self.old_win.destroy()
        canvas = Canvas(self.tk, highlightthickness=0)
        canvas.pack(expand=True, fill=BOTH)
        self.tk.update()

        paddle = Paddle(canvas, color='green', output_color="black")
        ball = Ball(canvas, paddle, color='red', tk=self.tk, lev=2)

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                try:
                    self.tk.destroy()
                    Lose().create_win()
                except:
                    pass

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.005)


class Start_Game2:
    def __init__(self, old_win=None):
        self.old_win = old_win
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.geometry("800x600")

    def End(self):
        self.tk.destroy()

    def Start(self):
        self.old_win.destroy()
        canvas = Canvas(self.tk, highlightthickness=0)
        canvas.pack(expand=True, fill=BOTH)
        self.tk.update()

        paddle = Paddle(canvas, color='green', output_color="black")
        ball = Ball(canvas, paddle, color='red', tk=self.tk, lev=3)

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                try:
                    self.tk.destroy()
                    Lose().create_win()
                except:
                    pass
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.003)


class Start_Game3:
    def __init__(self, old_win=None):
        self.old_win = old_win
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.geometry("800x600")

    def End(self):
        self.tk.destroy()

    def Start(self):
        self.old_win.destroy()
        canvas = Canvas(self.tk, highlightthickness=0)
        canvas.pack(expand=True, fill=BOTH)
        self.tk.update()

        paddle = Paddle(canvas, color='green', output_color="black")
        ball = Ball(canvas, paddle, color='red', tk=self.tk, lev=4)

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                try:
                    self.tk.destroy()
                    Lose().create_win()
                except:
                    pass
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.003)


class Start_Game4:
    def __init__(self, old_win=None):
        self.old_win = old_win
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.geometry("800x600")

    def End(self):
        self.tk.destroy()

    def Start(self):
        self.old_win.destroy()
        canvas = Canvas(self.tk, highlightthickness=0)
        canvas.pack(expand=True, fill=BOTH)
        self.tk.update()

        paddle = Paddle(canvas, color='green', output_color="black")
        ball = Ball(canvas, paddle, color='red', tk=self.tk, lev=5)

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                try:
                    self.tk.destroy()
                    Lose().create_win()
                except:
                    pass
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.003)


class Lose:
    def __init__(self):
        pass

    def create_win(self):
        mainWin = Tk()  # Создаем главное окно программы
        mainWin.title('Мой первый графический интерфейс')  # Устанавливаем заголовок
        # mainWin.configure(bg='black')
        mainWin.wm_attributes("-topmost", 1)  # Делаем отображение окна поверх всех остальных
        mainWin.geometry("800x600")
        self.canvas = Canvas(mainWin, highlightthickness=0)
        self.canvas.pack(expand=True, fill=BOTH)
        mainWin.update()
        self.bind_but(mainWin)
        return mainWin

    def bind_but(self, mainWin):
        f = Frame(self.canvas)
        Label(f, text="Проигрыш", font=f'Z003 {int(self.canvas.winfo_height() * 0.2)}').grid(
            row=0, column=0,
            columnspan=2)

        but_2 = Button(f,
                       text='Уровни',  # Создаем кнопку и присваиваем ее в переменную
                       width=15, height=5,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font='Hack 16',
                       command=lambda: switch_windows(old_win=mainWin,
                                                      new_win=choiseLev().create_win()))  # устанавливаем шрифт и размер надписи

        but_1 = (Button(f,
                        text='Выход',  # Создаем кнопку и присваиваем ее в переменную
                        width=15, height=5,  # Устанавливаем размер кнопки
                        bg='gray', fg='black',  # цвет фона и надписи
                        activebackground='black',  # цвет нажатой кнопки
                        activeforeground='gray',  # цвет надписи когда кнопка нажата
                        font='Hack 16',
                        command=lambda: quit(mainWin=mainWin)))
        but_2.grid(row=1, column=0)
        but_1.grid(row=1, column=1)  # устанавливаем шрифт и размер надписи

        f.pack(pady=self.canvas.winfo_height() / 4)


class Win():
    def __init__(self):
        pass

    def create_win(self):
        mainWin = Tk()  # Создаем главное окно программы
        mainWin.title('Мой первый графический интерфейс')  # Устанавливаем заголовок
        # mainWin.configure(bg='black')
        mainWin.wm_attributes("-topmost", 1)  # Делаем отображение окна поверх всех остальных
        mainWin.geometry("800x600")
        self.canvas = Canvas(mainWin, highlightthickness=0)
        self.canvas.pack(expand=True, fill=BOTH)
        mainWin.update()
        self.bind_but(mainWin)
        return mainWin

    def bind_but(self, mainWin):
        f = Frame(self.canvas)
        Label(f, text="Победа", font=f'Z003 {int(self.canvas.winfo_height() * 0.2)}').grid(
            row=0, column=0,
            columnspan=2)

        but_2 = Button(f,
                       text='Уровни',  # Создаем кнопку и присваиваем ее в переменную
                       width=15, height=5,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font='Hack 16',
                       command=lambda: switch_windows(old_win=mainWin,
                                                      new_win=choiseLev().create_win()))  # устанавливаем шрифт и размер надписи

        but_1 = (Button(f,
                        text='Выход',  # Создаем кнопку и присваиваем ее в переменную
                        width=15, height=5,  # Устанавливаем размер кнопки
                        bg='gray', fg='black',  # цвет фона и надписи
                        activebackground='black',  # цвет нажатой кнопки
                        activeforeground='gray',  # цвет надписи когда кнопка нажата
                        font='Hack 16',
                        command=lambda: quit(mainWin=mainWin)))
        but_2.grid(row=1, column=0)
        but_1.grid(row=1, column=1)  # устанавливаем шрифт и размер надписи

        f.pack(pady=self.canvas.winfo_height() / 4)


class MainWin():
    def __init__(self):
        pass

    def create_win(self):
        mainWin = Tk()  # Создаем главное окно программы
        mainWin.title('Мой первый графический интерфейс')  # Устанавливаем заголовок
        # mainWin.configure(bg='black')
        mainWin.wm_attributes("-topmost", 1)  # Делаем отображение окна поверх всех остальных
        mainWin.geometry("800x600")
        self.canvas = Canvas(mainWin, highlightthickness=0)
        self.canvas.pack(expand=True, fill=BOTH)
        mainWin.update()
        self.bind_but(mainWin)
        return mainWin

    def bind_but(self, mainWin):
        f = Frame(self.canvas)
        Label(f, text="Шарик-рикошет",
              font=f'Z003 {int(self.canvas.winfo_height() // 11)}').grid(
            column=0,
            row=0,
            columnspan=2)

        but_2 = Button(f,
                       text='Начать игру',  # Создаем кнопку и присваиваем ее в переменную
                       width=15, height=5,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font='Hack 16',
                       command=lambda: switch_windows(old_win=mainWin,
                                                      new_win=choiseLev().create_win()))  # устанавливаем шрифт и размер надписи

        but_1 = Button(f,
                       text='Выход',  # Создаем кнопку и присваиваем ее в переменную
                       width=15, height=5,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font='Hack 16',
                       command=lambda: quit(mainWin=mainWin))  # устанавливаем шрифт и размер надписи

        but_2.grid(column=0, row=1)
        but_1.grid(column=1, row=1)

        f.pack(pady=self.canvas.winfo_height() / 4)


class choiseLev:
    def __init__(self):
        pass

    def create_win(self):
        choiseLev = Tk()
        choiseLev.withdraw()
        choiseLev.configure()
        # choiseLev.wm_attributes("-topmost", 1)  # Делаем отображение окна поверх всех остальных
        # choiseLev.attributes("-fullscreen", True)
        choiseLev.geometry("800x600")
        self.canvas = Canvas(choiseLev, highlightthickness=0)
        self.canvas.pack(expand=True, fill=BOTH)

        choiseLev.update()
        self.bind_but(choiseLev)
        return choiseLev

    def bind_but(self, choiseLev):
        f = Frame(self.canvas)

        but_0 = Button(f,
                       text='Выход',  # Создаем кнопку и присваиваем ее в переменную
                       width=39,  # height=15,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font='Hack 10',
                       command=lambda: quit(mainWin=choiseLev))  # устанавливаем шрифт и размер надписи

        but_0.grid(column=0, row=2, columnspan=5)

        width = 4
        height = 2

        posy = 200
        posx = 230

        font_size = 10

        but_1 = Button(f,
                       text='1',  # Создаем кнопку и присваиваем ее в переменную
                       width=width, height=height,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font=f'Hack {font_size}',

                       command=lambda: Start_Game0(choiseLev).Start())  # устанавливаем шрифт и размер надписи

        but_1.grid(column=0, row=0, padx=5, pady=5)

        but_2 = Button(f,
                       text='2',  # Создаем кнопку и присваиваем ее в переменную
                       width=width, height=height,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font=f'Hack {font_size}',
                       command=lambda: Start_Game1(choiseLev).Start())  # устанавливаем шрифт и размер надписи

        but_2.grid(column=1, row=0, padx=5, pady=5)

        but_3 = Button(f,
                       text='3',  # Создаем кнопку и присваиваем ее в переменную
                       width=width, height=height,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font=f'Hack {font_size}',
                       command=lambda: Start_Game2(choiseLev).Start())  # устанавливаем шрифт и размер надписи

        but_3.grid(column=2, row=0, padx=5, pady=5)

        but_4 = Button(f,
                       text='4',  # Создаем кнопку и присваиваем ее в переменную
                       width=width, height=height,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font=f'Hack {font_size}',
                       command=lambda: Start_Game3(choiseLev).Start())  # устанавливаем шрифт и размер надписи

        but_4.grid(column=3, row=0, padx=5, pady=5)

        but_5 = Button(f,
                       text='5',  # Создаем кнопку и присваиваем ее в переменную
                       width=width, height=height,  # Устанавливаем размер кнопки
                       bg='gray', fg='black',  # цвет фона и надписи
                       activebackground='black',  # цвет нажатой кнопки
                       activeforeground='gray',  # цвет надписи когда кнопка нажата
                       font=f'Hack {font_size}',
                       command=lambda: Start_Game4(choiseLev).Start())  # устанавливаем шрифт и размер надписи

        but_5.grid(column=4, row=0, padx=5, pady=5)
        f.pack(pady=250)


def switch_windows(old_win, new_win):
    old_win.destroy()
    new_win.deiconify()


def quit(mainWin):
    mainWin.destroy()


if __name__ == '__main__':
    MainWin().create_win().mainloop()  # запускаем главный цикл обработки событий
