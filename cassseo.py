
"""Case-study
Разработчики:
Bayanova A. 70%, Shmatov D. 75%
"""

import tkinter as tk
import copy


class Board():

    def __init__(self, size=5, boardtype='Bordered'):

        self.shirina = size
        self.boardtype = boardtype
        self.kletki = {}
        self.polye = {}
        self.staroe = {}
        self.glavnoe = {}
        self.novoepolye()

    def novoepolye(self):

        self.root = tk.Tk()
        self.cell_size = 20
        self.knopka1 = tk.Button(self.root, text='ГОООООО!',width = self.shirina + 5, command=self.run)
        self.knopka1.grid(row=0, column=0,sticky="W")
        self.knopka2 = tk.Button(self.root, width = self.shirina, text='Выход', command=lambda: self.root.destroy())
        self.knopka2.grid(row=0, column=0,sticky="E")
        self.fa = tk.Label(self.root, text='Назначьте живые клетки!')
        self.fa.grid()
        self.width = self.shirina * self.cell_size

        self.life = 'yellow'
        self.smert = 'pink'

        self.shirinaums = tk.IntVar()
        self.shirinaums.set(0)

        self.loop = tk.IntVar()
        self.loop.set(1)

        self.alive = tk.IntVar()
        self.alive.set(0)

        self.root.title('Игра Жизнь!')

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.width,
                                bg=self.smert)
        self.canvas.grid()

        self.canvas.bind('<ButtonPress-1>', self.redraw)
        self.canvas.bind('<ButtonPress-3>', self.redraw)

        for i in range(self.shirina):
            for j in range(self.shirina):
                pos = (i, j)
                self.polye[pos] = False
                x1 = 1 + self.cell_size * j
                y1 = 1 + self.cell_size * i
                x2 = self.cell_size + self.cell_size * j - 1
                y2 = self.cell_size + self.cell_size * i - 1

                rect = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                    outline='black', width=1, fill=self.smert,
                                                    tag=pos)
                self.canvas.itemconfig(rect, )

                self.kletki[pos] = [rect, False]

        self.root.mainloop()



    def redraw(self, event):

        jj = int(event.x / self.cell_size)
        ii = int(event.y / self.cell_size)
        pos = (ii, jj)

        if event.num == 1:
            color = self.life
            self.kletki[pos][-1] = True
        elif event.num == 3:
            color = self.smert
            self.kletki[pos][-1] = False

        self.canvas.itemconfig(self.kletki[pos][0], fill=color)

    def clear(self):

        for i in range(self.shirina):
            for j in range(self.shirina):
                pos = (i, j)
                self.kletki[pos][-1] = False
                self.canvas.itemconfig(self.kletki[pos][0], fill=self.smert)
    def restart(self):

        self.clear()
        self.knopka2.config(text='Выход' , command=lambda: self.root.destroy())
        self.fa.config(text='Назначьте живые клетки')
        self.knopka1.config(text='Попробовать!' , command=self.run)

        self.loop.set(1)
        self.alive.set(0)


    def run(self):

        self.knopka1.config(text='АСТАНАВИСЬ!', command=self.restart)


        game = True
        while game == True:
            t = 0
            self.loop.set(int(self.loop.get()) + 1)
            for i in range(self.shirina):
                for j in range(self.shirina):
                    pos = (i, j)
                    self.polye[pos] = self.kletki[pos][-1]

            self.staroe = copy.deepcopy(self.polye)

            if (int(self.loop.get()) % 2 == 0):
                self.glavnoe = copy.deepcopy(self.polye)

            for i in range(self.shirina):
                for j in range(self.shirina):
                    pos = (i, j)
                    self.kletki[pos][-1] = self.dead_or_alive(pos)
                    self.polye[pos] = self.kletki[pos][-1]

                    if self.kletki[pos][-1]:
                        color = self.life
                        t += 1
                    else:
                        color = self.smert
                    self.canvas.itemconfig(self.kletki[pos][0], fill=color)

            self.alive.set(t)
            msg = 'Score %s.' % (self.loop.get())
            self.fa.config(text=msg)

            self.root.update()


            if (int(self.alive.get()) == 0):

                self.knopka2.config(text='Выйти',command=lambda: self.root.destroy())
                self.knopka1.config( text='Заново', command=self.run)
                self.fa.config(text='Ты проиграл!')
                game = False


            elif (self.staroe == self.polye):
                self.knopka2.config(text='Выйти',command=lambda: self.root.destroy())
                self.knopka1.config(text='Заново', command=self.restart)
                self.fa.config(text='Счет - %s' % (self.loop.get()))
                game = False

            elif (self.glavnoe == self.polye):
                self.knopka2.config(text='Выйти', command=lambda: self.root.destroy())
                self.knopka1.config(text='Заново', command=self.restart)
                self.fa.config(text='Счет - %s' % (self.loop.get()))
                game = False

    def board_type(self, pos):
        self.ryadom = []
        for i in range(-1, 2, 1):
            posx = pos[0] + i
            for j in range(-1, 2, 1):
                posy = pos[-1] + j
                if ((posx < 0 or posy < 0) or ((posx > self.shirina - 1 or posy > self.shirina - 1))):
                    pass
                else:
                    self.ryadom.append((posx, posy))


    def dead_or_alive(self, pos):

        self.board_type(pos)

        self.ryadom.remove(pos)
        okolo = 0
        for i in self.ryadom:
            if self.staroe[i]:
                okolo += 1

        if (self.staroe[pos]):
            if (okolo == 2 or okolo == 3):
                q = True
            else:
                q = False
        else:
            if (okolo == 3):
                q = True
            else:
                q = False

        return q

def create_board(pos):

    bsize = pos[0]
    s = bsize.get()
    Board(s)


def main():
    game = tk.Tk()
    game.title('Игра жизнь!')
    slab = tk.Label(game, width=25, text="Размер поля")
    slab.grid(column=0, row=1)

    bsize = tk.IntVar()
    bsize.set(10)

    bs = tk.Entry(game, textvariable=bsize)
    bs.grid(column=0, row=2)

    gbut = tk.StringVar()
    gbut.set('Bordered')

    pos = [bsize, gbut]
    bbut = tk.Button(game, width=10, text='Начать', command=lambda pos=pos: create_board(pos))
    bbut.grid(column = 0, row = 3, sticky="E")
    bbut = tk.Button(game, width=10, text='Выход', command=lambda : game.destroy())
    bbut.grid(column = 0, row = 3, sticky="W")

    game.mainloop()

if __name__ == "__main__":
    main()