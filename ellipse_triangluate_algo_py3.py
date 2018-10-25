import tkinter as tk
from math import (
    atan,
    cos,
    pi,
    sin,
    sqrt,
)
from time import sleep


class App:
    t = 0
    curentEntry = None
    args = {
        'A':0.00003,
        'B':0,
        'C':0.00008,
        'N':40,
    }
    a = int(
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
    b = int(
        sqrt(
            2 / (
                sqrt(
                    (args['A'] - args['C'])
                    *(args['A'] - args['C'])
                    + args['B'] * args['B']
                ) + args['A'] + args['C'])
        )
    )
    cc = sqrt(a * a - b * b)
    e = cc / a
    p = a * (1 - e * e)

    def __init__(self):
        self.app = tk.Tk()
        self.W = self.app.winfo_width()
        self.H = self.app.winfo_height()
        self.mxSize = self.app.wm_maxsize()
        self.mxSize = [self.mxSize[0] / 2, self.mxSize[1] / 2]
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
        for key in self.args.keys():
            self.app.bind(
                '<KeyPress-'+key.lower()+'>',
                self.edit_arg,
            ) #  lambda event: self.edit_arg(key))
          
        self.app.bind('<KeyPress-Return>', self.enter_arg2)
        self.app.bind('<Control-KeyPress-Return>', self.enter_arg)
        self.app.bind('<Control-KeyPress-q>', self.quit)
        
        #self.app.bind('<space>',self.draw_ellipse)
        self.draw()
        self.draw_ellipse(0)
        self.app.mainloop()

    def edit_arg(self, key):
        if (key.char.upper() in self.args.keys()):
            self.canvas.itemconfigure(self.cnvWindEntr, state=tk.NORMAL)
            self.curentEntry = key.char.upper()
            self.txt.set(self.args[key.char.upper()])
            self.entry.takefocus = 1
            c.focus(self.cnvWindEntr)

    def enter_arg2(self, event):
        self.args[self.curentEntry] = float(self.txt.get())
        self.canvas.itemconfigure(self.cnvWindEntr, state=tk.HIDDEN)

    def enter_arg(self, event):
        temp = self.args[self.curentEntry]
        self.args[self.curentEntry] = float(self.txt.get())
        if (self.args['A'] * self.args['C'] - self.args['B'] * self.args['B'] <= 0):
          #self.txt+=' args ERROR'
          print('args ERROR')
          self.args[self.curentEntry] = temp
        else:
          self.canvas.itemconfigure(self.cnvWindEntr, state=tk.HIDDEN)
          self.draw()

    def create_line(self, x1, y1, x2, y2):
        self.canvas.create_line(
          x1 + self.mxSize[0] / 2,
          y1 + self.mxSize[1] / 2,
          x2 + self.mxSize[0] / 2,
          y2 + self.mxSize[1] / 2,
        )

    def create_rectangle(self,x1,y1,x2,y2,w=0,h=0):
        self.canvas.create_rectangle(
            x1 + self.mxSize[0] / 2 + w,
            y1 + self.mxSize[1] / 2 + h,
            x1 + self.mxSize[0] / 2 - w,
            y1 + self.mxSize[1] / 2 - h,
        )

    def step1(self):
        vr = (
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

    def Li(self, h, i):
        return 4 * (
            pi
            * (self.a -h * i)
            * (self.b -h * i)
            + (self.a - self.b)
            * (self.a - self.b)
        ) / (
            self.a
            + self.b
            - 2 * h * i
        )

    def step2(self):
        K = []
        L0 = self.Li(0, 0)
        for j in range(3):
            hj = self.b / (j + 1) #####j
            SLi = L0
            for i in range(1 + j):
                SLi += self.Li(hj, i)
            K.append(0.866025404 * SLi / hj) #sin(60)*SLi/hj
        return K

    def step3(self, Kn):
        Kf = []
        Kf.append((Kn[2] - 2 * Kn[1] + Kn[0]) / 2)
        Kf.append(Kn[1] - Kn[0] - 3 * (Kf[0]))
        Kf.append(Kn[0] - Kf[0] - Kf[1])
        K = (
            -Kf[1]
            + sqrt(
                (
                    Kf[1]* Kf[1]
                    - 4 * Kf[0] * (
                        Kf[2] - self.args['N']
                    )
                )
            )
        ) / (2 * Kf[0])
        return K

    def step4(self, K): #  K:int
        try:
            h = self.b / K
        except ZeroDivisionError:
            h = 0
        self.aLi = [self.Li(h, K)]
        for i in range(K-1, -1, -1):
            self.aLi.append(self.Li(h, i))
            self.trn(int(self.aLi[K - i] / h), h, i)
            self.trnglt(
                int(self.aLi[K - i - 1] / h),
                int(self.aLi[K - i] / h),
                h,
                i,
            )

    def trn(self, N, h, i):
        for j in range(N):
            x1 = (self.a - h * i) * cos(j * 2 * pi / N)
            y1 = (self.b - h * i) * sin(j * 2 * pi / N)
            #  self.canvas.create_rectangle(x1+self.mxSize[0]/2+1,y1+self.mxSize[1]/2+1,x1+self.mxSize[0]/2-1,y1+self.mxSize[1]/2-1)
            self.create_rectangle(x1, y1, x1, y1, 1, 1)

    def trnglt(self, N1, N2, h, i):
    #    x1=(s.a-h*i-h)*cos(0*2*pi/N1+(i%2)*0.523259878)
    #    y1=(s.b-h*i-h)*sin(0*2*pi/N1+(i%2)*0.523259878)
    #    x2=(s.a-h*i)*cos(0*2*pi/N2+((i+1)%2)*0.523259878)
    #    y2=(s.b-h*i)*sin(0*2*pi/N2+((i+1)%2)*0.523259878)
    #    for j in range(N2+1):
    #      x1=(s.a-h*i-h)*cos(j*2*pi/N1+(i%2)*0.523259878)
    #      y1=(s.b-h*i-h)*sin(j*2*pi/N1+(i%2)*0.523259878)
        i1 = 0
        i2 = 0
        x1 = (self.a - h * i - h) * cos(0 * 2 * pi / N1 + (i % 2) * 0.523259878)
        y1 = (self.b - h * i - h) * sin(0 * 2 * pi / N1 + (i % 2) * 0.523259878)
        x3 = (self.a - h * i) * cos(0 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        y3 = (self.b - h * i) * sin(0 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
        i1 += 1
        i2 += 1
        while i1 < N1 or i2 < N2:
            if i1 / i2 > N1 / N2:
                if i2 <= N2:
                    x2 = (self.a -h * i) * cos(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
                    y2 = (self.b -h * i) * sin(i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
                    i2 += 1
            else:
                if i1 <= N1:
                    x1 = (self.a - h * i - h) * cos(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
                    y1 = (self.b - h * i - h) * sin(i1 * 2 * pi / N1 + (i % 2) * 0.523259878)
                    i1 += 1
                
            self.create_line(x1, y1, x2, y2)
            self.create_line(x3, y3, x2, y2)
            self.create_line(x1, y1, x3, y3)
            sleep(0.1)
            if i1 / i2 > N1 / N2:
                x3 = x2
                y3 = y2
                print('p%i\tq%i\tq%i' % (i1, i2, i2 - 1))
            else:
                x3 = x1
                y3 = x1
                print('p%i\tp%i\tq%i' % (i1 - 1, i1, i2))
        print('===Triangulate %i''s ellipse done!===' % i)

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

        #    c.create_rectangle(s.mxSize[0]/2-s.cc,s.mxSize[1]/2+p,s.mxSize[0]/2+cc,s.mxSize[1]/2-p)
        #    c.create_oval(s.mxSize[0]/2-a,s.mxSize[1]/2+b,s.mxSize[0]/2+a,s.mxSize[1]/2-b)
        '''
        for x in range(-a,a):#-s.mxSize[0]/2,s.mxSize[0]/2):
          bb=1
          for y in range(-b,b):#-s.mxSize[1]/2,s.mxSize[1]/2):
            be=s.ellipse(x,y)
            #if (not be):
            #  bb=1
            if (be and bb):
              c.create_rectangle(x+s.mxSize[0]/2,y+s.mxSize[1]/2,x+s.mxSize[0]/2,y+s.mxSize[1]/2,outline=None)
              bb=0
            if (not (be or bb)):
              c.create_rectangle(x-1+s.mxSize[0]/2,y+s.mxSize[1]/2,x-1+s.mxSize[0]/2,y+s.mxSize[1]/2,outline=None)
              bb=1
        '''
        if (self.curentEntry == 'N'):
            self.triangulate(self.args['N'])
        #c.create_ellipse()

    def draw_ellipse(self, event):
        self.canvas.create_oval(
            self.mxSize[0] / 2 - self.a,
            self.mxSize[1] / 2 + self.b,
            self.mxSize[0] / 2 + self.a,
            self.mxSize[1] / 2 - self.b,
        )
        self.step1()
        self.step4(int(self.step3(self.step2())))

    def draw_ellipse3(self, event):
        #    t=1
        #    mxS=0
        #    mxX=0
        #    mxT=0
        #    mxY=0

        N1 = 9
        N2 = 14
        h = self.b / 2
        i = 1
        try:
            self.i1 == 0
            self.i2 == 0
        except: #  AtributeError:
            self.i1 = 0
            self.i2 = 0

            self.x3 = (self.a - h * i) * cos(self.i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
            self.y3 = (self.b - h * i) * sin(self.i2 * 2 * pi / N2 + ((i + 1) % 2) * 0.523259878)
            self.x1 = (self.a - h * i - h) * cos(self.i1 * 2*pi/N1 + (i % 2) * 0.523259878)
            self.y1 = (self.b - h * i - h) * sin(self.i1 * 2*pi/N1 + (i % 2) * 0.523259878)
            self.i2 += 1
            self.i1 += 1
        if 1: #  while (i1<N1 or i2<N2):
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
                self.x1 + self.mxSize[0] / 2,
                self.y1 + self.mxSize[1] / 2,
                self.x2 + self.mxSize[0] / 2,
                self.y2 + self.mxSize[1] / 2,
            )
    #        s.canvas.create_rectangle(x1+s.mxSize[0]/2,y1+s.mxSize[1]/2,x1+s.mxSize[0]/2+2,y1+s.mxSize[1]/2+2)
            self.canvas.create_line(
                self.x3 + self.mxSize[0] / 2,
                self.y3 + self.mxSize[1] / 2,
                self.x2 + self.mxSize[0] / 2,
                self.y2 + self.mxSize[1] / 2,
            )
    #        s.canvas.create_rectangle(x2+s.mxSize[0]/2,y2+s.mxSize[1]/2,x2+s.mxSize[0]/2+2,y2+s.mxSize[1]/2+2)
            self.canvas.create_line(
                self.x1 + self.mxSize[0] / 2,
                self.y1 + self.mxSize[1] / 2,
                self.x3 + self.mxSize[0] / 2,
                self.y3 + self.mxSize[1] / 2,
            )
    #        s.canvas.create_rectangle(x3+s.mxSize[0]/2,y3+s.mxSize[1]/2,x3+s.mxSize[0]/2+2,y3+s.mxSize[1]/2+2)
            if self.i1 / self.i2 > N1 / N2:
               self.x3 = self.x2
               self.y3 = self.y2
            else:
               self.x3 = self.x1
               self.y3 = self.x1
            print('%i,%i' % (self.i1, self.i2))
        '''
        x2=(s.a-h*i)*cos(0*2*pi/N2+((i+1)%2)*0.523259878)
        y2=(s.a-h*i)*sin(0*2*pi/N2+((i+1)%2)*0.523259878)
      
        x2=(s.a-h*i)*cos(j*2*pi/N2+((i+1)%2)*0.523259878)
        y2=(s.a-h*i)*sin(j*2*pi/N2+((i+1)%2)*0.523259878)
          

        s.t+=1
        while t<(s.t+1):#12: 
          x=s.a*cos(t*2*pi/(s.t-1))
          y=s.b*sin(t*2*pi/(s.t-1))
          x1=s.mxSize[0]/2-x
          y1=s.mxSize[1]/2+y
          s.canvas.create_rectangle(x1-1,y1-1,x1+1,y1+1,fill='green',outline='green')#s.mxSize[0]/2-x,s.mxSize[1]/2+y,s.mxSize[0]/2-x,s.mxSize[1]/2+y)

          x=s.a*cos(t*2*pi/s.t)
          y=s.b*sin(t*2*pi/s.t)
          x1=s.mxSize[0]/2-x
          y1=s.mxSize[1]/2+y
          s.canvas.create_rectangle(x1-1,y1-1,x1+1,y1+1,fill='#'+hex(s.t*20*65536+s.t*20)[-6:],outline='#'+hex(s.t*20*65536+s.t*20)[-6:])#s.mxSize[0]/2-x,s.mxSize[1]/2+y,s.mxSize[0]/2-x,s.mxSize[1]/2+y)
          #s.canvas.create_rectangle(s.mxSize[0]/2-x,s.mxSize[1]/2+y,s.mxSize[0]/2-x,s.mxSize[1]/2+y)
          print('S='+str(x1*4*y1)+' %.2f, %.2f, %.2f'%(x1,y1,t))
          if (mxS<abs(x*4*y)):
            mxS=abs(x*4*y)
            mxT=t
            mxX=x
            mxY=y
        '''
        '''x=(s.a-51)*cos(t)
          y=(s.b-51)*sin(t)
          x2=s.mxSize[0]/2-x
          y2=s.mxSize[1]/2+y
          s.canvas.create_rectangle(x2,y2,x2,y2)#s.mxSize[0]/2-x,s.mxSize[1]/2+y,s.mxSize[0]/2-x,s.mxSize[1]/2+y)
          if (t>=17 and t<=17.2):
            s.canvas.create_line(x1,y1,x2,y2,fill='red')
    #        s.canvas.create_line(x2,y2,x2+3,y2+3,fill='red')
            print('%i'%(sqrt((x1-x2)**2+(y1-y2)**2)))
          if (t>=0 and t<=0.2):
            s.canvas.create_line(x1,y1,x2,y2,fill='red')
    #        s.canvas.create_rectangle(x2,y2,x2+3,y2+3,fill='red')
            print('%i'%(sqrt((x1-x2)**2+(y1-y2)**2)))
        '''
          #t+=1
        #print('max S='+str(mxS)+' %.2f, %.2f, %.2f'%(mxX,mxY,atan(mxY/mxX)*180))
        #print('foc S=%.2f %.2f, %.2f, %.2f'%(s.cc*s.p*4,s.cc,s.p,atan(s.p/s.cc)*180))
        #print('%.5f %.5f, %.5f'%(sqrt(mxS/(s.a*s.b*4)),mxX/s.a,mxY/s.b))
    #    s.canvas.create_rectangle(s.mxSize[0]/2-mxX+4,s.mxSize[1]/2+mxY+4,s.mxSize[0]/2+mxX-4,s.mxSize[1]/2-mxY-4,fill='red',outline='red')
        #s.canvas.create_rectangle(s.mxSize[0]/2-s.cc,s.mxSize[1]/2+s.p,s.mxSize[0]/2+s.cc,s.mxSize[1]/2-s.p,fill='gray')

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
