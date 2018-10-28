import tkinter as tk
from math import (
    atan,
    cos,
    pi,
    sin,
    sqrt,
)
from time import sleep
from typing import Dict, Tuple, List


class App:
    t = 0
    curentEntry = None
    args: Dict = {
        'A': 0.00003,
        'B': 0,
        'C': 0.00008,
        'N': 40,
    }
    a: int = int(
        sqrt(
            (
                2 * (
                    sqrt(
                        (args['A'] - args['C'])
                        * (args['A'] - args['C'])
                        + args['B'] * args['B']
                    )
                    + args['A'] 
                    + args['C']
                )
            )
            / (
                4 * args['A'] * args['C'] 
                - args['B'] * args['B']
            )
        )
    )
    b: int = int(
        sqrt(
            2 / (
                sqrt(
                    (args['A'] - args['C'])
                    *(args['A'] - args['C'])
                    + args['B'] * args['B']
                ) + args['A'] + args['C'])
        )
    )
    cc: float = sqrt(a * a - b * b)
    e: float = cc / a
    p: float = a * (1 - e * e)

    def __init__(self):
        self.app = tk.Tk()
        self.W: int = self.app.winfo_width()
        self.H: int = self.app.winfo_height()
        self.mxSize: Tuple = self.app.wm_maxsize()
        self.mxSize = (self.mxSize[0] / 2, self.mxSize[1] / 2)
        self.app.wm_geometry(
            '%ix%i+%i+%i' % (
                self.mxSize[0],
                self.mxSize[1],
                -7,
                0,
            )
        )
        self.canvas = tk.Canvas(
            self.app,
            width=self.mxSize[0],
            height=self.mxSize[1] * 2,
        )
        self.app.grid()
        self.canvas.grid(column=0, row=0, sticky=tk.NE)
        print('app w=%i,h=%i' % (self.W, self.H))
        print('cnv w=%i,h=%i' % (self.mxSize[0], self.mxSize[1]))
        self.txt = tk.StringVar(self.canvas)
        self.entry = tk.Entry(
            self.canvas,
            textvariable=self.txt,
            width=5,
            font='Courier 8',
        )
        self.cnvWindEntr = self.canvas.create_window(
            25,
            25,
            window=self.entry,
            state=tk.HIDDEN,
            tag='entry',
        )
        for key in self.args:
            self.app.bind(
                '<KeyPress-'+key.lower()+'>',
                self.edit_arg,
            )
          
        self.app.bind('<KeyPress-Return>', self.enter_arg2)
        self.app.bind('<Control-KeyPress-Return>', self.enter_arg)
        self.app.bind('<Control-KeyPress-q>', self.quit)
        
        self.app.bind(
            '<KeyPress-space>',
            lambda *args, **kwargs: self.draw_next(),
        )
        self.app.bind(
            '<Control-KeyPress-space>',
            lambda *args, **kwargs: self.draw_ellipse(),
        )
        # self.draw()
        self.draw_ellipse(0)
        self.app.mainloop()

    def draw_next(self):
        try:
            next(self.draw__iter)
        except StopIteration:
            pass

    def edit_arg(self, key: tk.Event):
        if key.char.upper() in self.args:
            self.canvas.itemconfigure(self.cnvWindEntr, state=tk.NORMAL)
            self.curentEntry = key.char.upper()
            self.txt.set(self.args[key.char.upper()])
            self.entry.takefocus = 1
            self.canvas.focus(self.cnvWindEntr)

    def enter_arg2(self, event):
        self.args[self.curentEntry] = float(self.txt.get())
        self.canvas.itemconfigure(self.cnvWindEntr, state=tk.HIDDEN)

    def enter_arg(self, event):
        temp: float = self.args[self.curentEntry]
        self.args[self.curentEntry] = float(self.txt.get())
        if (self.args['A'] * self.args['C'] - self.args['B'] * self.args['B'] <= 0):

          print('args ERROR')
          self.args[self.curentEntry] = temp
        else:
          self.canvas.itemconfigure(self.cnvWindEntr, state=tk.HIDDEN)
          self.draw()

    def create_line(
            self,
            x1,
            y1,
            x2,
            y2,
    ):
        self.canvas.create_line(
          int(x1 + self.mxSize[0] // 2),
          int(y1 + self.mxSize[1] // 2),
          int(x2 + self.mxSize[0] // 2),
          int(y2 + self.mxSize[1] // 2),
        )

    def create_rectangle(
            self,
            x1,
            y1,
            x2,
            y2,
            w=0,
            h=0,
    ):
        self.canvas.create_rectangle(
            int(x1 + self.mxSize[0] // 2 + w),
            int(y1 + self.mxSize[1] // 2 + h),
            int(x1 + self.mxSize[0] // 2 - w),
            int(y1 + self.mxSize[1] // 2 - h),
        )

    def step1(self):
        vr: float = (
            sqrt(
                (self.args['A']-self.args['C'])
                * (self.args['A']-self.args['C'])
                + self.args['B'] * self.args['B']
            )
            + self.args['A']
            + self.args['C']
        )
        self.a = int(
            sqrt(
                (2 * vr)
                / (
                    4 
                    * self.args['A']
                    * self.args['C']
                    - self.args['B']
                    * self.args['B']
                )
            )
        )
        self.b = min(
            int(sqrt(2 / vr)),
            self.a,
        )
        self.a = max(
            int(
                sqrt(
                    (2*vr)
                    / (
                        4
                        * self.args['A']
                        * self.args['C']
                        - self.args['B']
                        * self.args['B']
                    )
                )
            ),
            self.b,
        )

    def Li(
            self,
            h: float,
            i: int,
    ) -> float:
        """
        Приблизительный периметр i-го эллипса
        c расстояниями h между каждым
        :param h:
        :param i:
        :return:
        """
        return 4 * (
            pi
            * (self.a - h * i)
            * (self.b - h * i)
            + (self.a - self.b)
            * (self.a - self.b)
        ) / (
            self.a
            + self.b
            - 2 * h * i
        )

    def step2(self) -> List[float]:
        """
        Расчет трех коэффтцентов(?)
        :return:
        """
        K: List = []
        L0: float = self.Li(0, 0)
        for j in range(3):
            hj: float = self.b / (j + 1)
            SLi: float = L0
            for i in range(1 + j):
                SLi += self.Li(hj, i)
            # sin(60) * SLi / hj
            K.append(0.866025404 * SLi / hj)
        return K

    def step3(
            self,
            Kn: List[float],
    ) -> float:
        """
        Расчет оптиамьлного кол-ва концтрических эллипсов
        для данного кол-ва точек.
        :param Kn:
        :return:
        """
        Kf1 = ((Kn[2] - 2 * Kn[1] + Kn[0]) / 2)
        Kf2 = (Kn[1] - Kn[0] - 3 * Kf1)
        Kf3 = (Kn[0] - Kf1 - Kf2)
        K: float = (
            -Kf2
            + sqrt(
                (
                    Kf2 * Kf2
                    - 4 * Kf1 * (
                        Kf3 - self.args['N']
                    )
                )
            )
        ) / (2 * Kf1)
        return K

    def step4(
            self,
            K: int,
    ):
        """

        :param K: кол-во внутренних эллипсов
        :return:
        """
        try:
            h: float = self.b / K
        except ZeroDivisionError:
            h: float = 0
        aLi: List[float] = [self.Li(h, K)]
        for i in range(K-1, -1, -1):
            aLi.append(self.Li(h, i))
            self.create_dots_in_inner_ellipsis(
                N=int(aLi[K - i] / h),
                h=h,
                i=i,
            )
            yield from self.create_triangles_between_two_ellipsis(
                N1=int(aLi[K - i - 1] / h),
                N2=int(aLi[K - i] / h),
                h=h,
                i=i,
            )

    def create_dots_in_inner_ellipsis(
            self,
            N: int,
            h: float,
            i: int,
    ):
        """

        :param N: кол-во точек на внутреннем эллипсе
        :param h: расстояние между соседними концентрическими эллипсами
        :param i: порядковый номер внутреннего эллписа
        :return:
        """
        for j in range(N):
            x1: float = (self.a - h * i) * cos(j * 2 * pi / N)
            y1: float = (self.b - h * i) * sin(j * 2 * pi / N)
            self.create_rectangle(x1, y1, x1, y1, w=1, h=1)

    def create_triangles_between_two_ellipsis(
            self,
            N1,
            N2,
            h,
            i: int,
    ):
        i1: int = 0
        i2: int = 0
        x1: float = (self.a - h * i - h) * cos(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
        y1: float = (self.b - h * i - h) * sin(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
        x3: float = (self.a - h * i) * cos(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        y3: float = (self.b - h * i) * sin(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        i1 += 1
        i2 += 1
        while i1 < N1 or i2 < N2:
            if i1 / i2 > N1 / N2:
                if i2 <= N2:
                    x2: float = (self.a - h * i) * cos(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
                    y2: float = (self.b - h * i) * sin(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
                    i2 += 1
            else:
                if i1 <= N1:
                    x1 = (self.a - h * i - h) * cos(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
                    y1 = (self.b - h * i - h) * sin(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
                    i1 += 1

            self.create_line(x1, y1, x2, y2)
            yield
            self.create_line(x3, y3, x2, y2)
            yield
            self.create_line(x1, y1, x3, y3)
            yield

            if i1 / i2 > N1 / N2:
                x3 = x2
                y3 = y2
                print(f'p{i1:d}\tq{i2:d}\tq{i2 - 1:d}')
            else:
                x3 = x1
                y3 = x1
                print(f'p{i1 - 1:d}\tp{i1:d}\tq{i2:d}')
        print(f"===Triangulate {i:d}'s ellipse done!===")

    def draw(self):
        c = self.canvas
        self.a = int(sqrt(
            (2 * (
                sqrt(
                    (self.args['A'] - self.args['C'])
                    * (self.args['A'] - self.args['C'])
                    + self.args['B'] * self.args['B']
                )
                + self.args['A']
                + self.args['C']
            ))
            / (
                4 * self.args['A'] * self.args['C']
                - self.args['B'] * self.args['B']
              )
        ))
        self.b = int(sqrt(
            2 / (
                sqrt(
                    (self.args['A'] - self.args['C'])
                    * (self.args['A'] - self.args['C'])
                    + self.args['B'] * self.args['B']
                )
                + self.args['A']
                + self.args['C']
            )
        ))
        self.cc = sqrt(self.a * self.a - self.b * self.b)
        self.e = self.cc / self.a
        self.p = self.a * (1 - self.e * self.e)

        self.canvas.create_rectangle(
            5,
            5,
            self.mxSize[0],
            self.mxSize[1],
            fill="green",
        )

        if self.curentEntry == 'N':
            self.triangulate(self.args['N'])

    def draw_ellipse(self, event=None):
        self.draw()
        self.canvas.create_oval(
            int(self.mxSize[0] // 2 - self.a),
            int(self.mxSize[1] // 2 + self.b),
            int(self.mxSize[0] // 2 + self.a),
            int(self.mxSize[1] // 2 - self.b),
        )
        self.step1()

        self.draw__iter = self.step4(int(self.step3(self.step2())))

    def draw_ellipse3(self, event):
        N1 = 9
        N2 = 14
        h = self.b / 2
        i = 1

        if not hasattr(self, 'i1'):
            self.i1 = 0
        if not hasattr(self, 'i2'):
            self.i2 = 0

        self.x3 = (self.a - h * i) * cos(self.i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        self.y3 = (self.b - h * i) * sin(self.i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        self.x1 = (self.a - h * i - h) * cos(self.i1 * 2*pi/N1 + (i % 2) * 0.523259878)
        self.y1 = (self.b - h * i - h) * sin(self.i1 * 2*pi/N1 + (i % 2) * 0.523259878)
        self.i2 += 1
        self.i1 += 1

        if self.i1 / self.i2 > N1 / N2:
            if self.i2 <= N2:
                self.x2 = (self.a-h*i)*cos(self.i2*2*pi/N2  +((i+1)%2)*0.523259878)
                self.y2 = (self.b-h*i)*sin(self.i2*2*pi/N2  +((i+1)%2)*0.523259878)
                self.i2 += 1
        else:
            if self.i1 <= N1:
                self.x1=(self.a-h*i-h)*cos(self.i1*2*pi/N1  +(i%2)*0.523259878)
                self.y1=(self.b-h*i-h)*sin(self.i1*2*pi/N1  +(i%2)*0.523259878)
                self.i1+=1

        self.canvas.create_line(
            int(self.x1 + self.mxSize[0] // 2),
            int(self.y1 + self.mxSize[1] // 2),
            int(self.x2 + self.mxSize[0] // 2),
            int(self.y2 + self.mxSize[1] // 2),
        )

        self.canvas.create_line(
            int(self.x3 + self.mxSize[0] // 2),
            int(self.y3 + self.mxSize[1] // 2),
            int(self.x2 + self.mxSize[0] // 2),
            int(self.y2 + self.mxSize[1] // 2),
        )

        self.canvas.create_line(
            int(self.x1 + self.mxSize[0] // 2),
            int(self.y1 + self.mxSize[1] // 2),
            int(self.x3 + self.mxSize[0] // 2),
            int(self.y3 + self.mxSize[1] // 2),
        )

        if self.i1 / self.i2 > N1 / N2:
           self.x3 = self.x2
           self.y3 = self.y2
        else:
           self.x3 = self.x1
           self.y3 = self.x1
        print('%i,%i' % (self.i1, self.i2))

    def triangulate(self, n):
        #TODO
        return 0

    def ellipse(self, x, y):
        e = (
            self.args['A'] * x * x
            + self.args['B'] * x * y
            + self.args['C'] * y * y
        )
        return e < 1

    def quit(self, event):
        self.app.quit()

    class ellipse:
        a = None
        b = None


if __name__ == '__main__':
    a = App()
