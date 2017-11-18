import Tkinter as tk
from math import sqrt,cos,sin,atan,pi

class App:
	t=0
	curentEntry=None
	args={	'A':0.00003,
			'B':0,
			'C':0.00008,
			'N':40}
	a=int(sqrt((2*(sqrt((args['A']-args['C'])*(args['A']-args['C'])+args['B']*args['B'])+args['A']+args['C']))/(4*args['A']*args['C']-args['B']*args['B'])))
	b=int(sqrt(2/(sqrt((args['A']-args['C'])*(args['A']-args['C'])+args['B']*args['B'])+args['A']+args['C'])))
	cc=sqrt(a*a-b*b)
	e=cc/a
	p=a*(1-e*e)

	def __init__(s):
		s.app=tk.Tk()
		s.W=s.app.winfo_width()
		s.H=s.app.winfo_height()
		s.mxSize=s.app.wm_maxsize()
		s.mxSize=[s.mxSize[0]/2,s.mxSize[1]/2]
		s.app.wm_geometry('%ix%i+%i+%i'%(s.mxSize[0],s.mxSize[1],-7,0))
		s.canvas=tk.Canvas(s.app,width=s.mxSize[0],height=s.mxSize[1]*2)
		s.app.grid()
		s.canvas.grid(column=0,row=0,sticky=tk.NE)
		print('app w=%i,h=%i'%(s.W,s.H))
		print('cnv w=%i,h=%i'%(s.mxSize[0],s.mxSize[1]))
		s.txt=tk.StringVar(s.canvas)
		s.entry=tk.Entry(s.canvas,textvariable=s.txt,width=5,font='Courier 8')
		s.cnvWindEntr=s.canvas.create_window(25,25,window=s.entry,state=tk.HIDDEN,tag='entry')
		for key in s.args.keys():
			s.app.bind('<KeyPress-'+key.lower()+'>',s.edit_arg)#lambda event: s.edit_arg(key))
			
		s.app.bind('<KeyPress-Return>', s.enter_arg2)
		s.app.bind('<Control-KeyPress-Return>', s.enter_arg)
		s.app.bind('<Control-KeyPress-q>',s.quit)
		
		s.app.bind('<space>',s.draw_ellipse)
		
		s.draw()
		s.app.mainloop()
	def edit_arg(s,key):
		if (key.char.upper() in s.args.keys()):
			s.canvas.itemconfigure(s.cnvWindEntr,state=tk.NORMAL)
			s.curentEntry=key.char.upper()
			s.txt.set(s.args[key.char.upper()])
			s.entry.takefocus=1
			c.focus(s.cnvWindEntr)
			#print(key)
#			print(dir(event))
	def enter_arg2(s,event):
		s.args[s.curentEntry]=float(s.txt.get())
		s.canvas.itemconfigure(s.cnvWindEntr,state=tk.HIDDEN)
		
	def enter_arg(s,event):
		temp=s.args[s.curentEntry]
		s.args[s.curentEntry]=float(s.txt.get())
		if (s.args['A']*s.args['C']-s.args['B']*s.args['B']<=0):
			#s.txt+=' args ERROR'
			print('args ERROR')
			s.args[s.curentEntry]=temp
		else:
			s.canvas.itemconfigure(s.cnvWindEntr,state=tk.HIDDEN)
			s.draw()
		
	def step1(s):
		vr=(sqrt((s.args['A']-s.args['C'])*(s.args['A']-s.args['C'])+s.args['B']*s.args['B'])+s.args['A']+s.args['C'])
		s.a=int(sqrt((2*vr)/(4*s.args['A']*s.args['C']-s.args['B']*s.args['B'])))
		s.b=min(int(sqrt(2/vr)),s.a)
		s.a=max(int(sqrt((2*vr)/(4*s.args['A']*s.args['C']-s.args['B']*s.args['B']))),s.b)
		
	def Li(s,h,i):
		return 4*(pi*(s.a-h*i)*(s.b-h*i)+(s.a-s.b)*(s.a-s.b))/(s.a+s.b-2*h*i)
	def step2(s):
		K=[]
		L0=s.Li(0,0)
		for j in range(3):
			hj=s.b/(j+1) #####j
			SLi=L0
			for i in range(1+j):
				SLi+=s.Li(hj,i)
			K.append(0.866025404*SLi/hj) #sin(60)*SLi/hj
		return K
	
	def step3(s,Kn):
		Kf=[]
		Kf.append((Kn[2]-2*Kn[1]+Kn[0])/2)
		Kf.append(Kn[1]-Kn[0]-3*(Kf[0]))
		Kf.append(Kn[0]-Kf[0]-Kf[1])
		K=(-Kf[1]+sqrt((Kf[1]*Kf[1]-4*Kf[0]*(Kf[2]-s.args['N']))))/(2*Kf[0])
		return K
	
	def step4(s,K): ##K:int
		try:
			h=s.b/K
		except:
			h=0
		s.aLi=[]
		for i in range(K,-1,-1):
			s.aLi.append(s.Li(h,i))
			s.trn(int(s.aLi[K-i]/h),h,i)
			
	def trn(s,N,h,i):
		for j in range(N):
			x1=(s.a-h*i)*cos(j*2*pi/N)
			y1=(s.b-h*i)*sin(j*2*pi/N)
			s.canvas.create_rectangle(x1+s.mxSize[0]/2+1,y1+s.mxSize[1]/2+1,x1+s.mxSize[0]/2-1,y1+s.mxSize[1]/2-1)
	
	def trnglt(s,N1,N2,h,i):
		x1=(s.a-h*i-h)*cos(0*2*pi/N1+(i%2)*0.523259878)
		y1=(s.b-h*i-h)*sin(0*2*pi/N1+(i%2)*0.523259878)
		x2=(s.a-h*i)*cos(0*2*pi/N2+((i+1)%2)*0.523259878)
		y2=(s.b-h*i)*sin(0*2*pi/N2+((i+1)%2)*0.523259878)
		for j in range(N2+1):
			x1=(s.a-h*i-h)*cos(j*2*pi/N1+(i%2)*0.523259878)
			y1=(s.b-h*i-h)*sin(j*2*pi/N1+(i%2)*0.523259878)
			
			
	
	def draw(s):
		c=s.canvas
		s.a=int(sqrt((2*(sqrt((s.args['A']-s.args['C'])*(s.args['A']-s.args['C'])+s.args['B']*s.args['B'])+s.args['A']+s.args['C']))/(4*s.args['A']*s.args['C']-s.args['B']*s.args['B'])))
		s.b=int(sqrt(2/(sqrt((s.args['A']-s.args['C'])*(s.args['A']-s.args['C'])+s.args['B']*s.args['B'])+s.args['A']+s.args['C'])))
		s.cc=sqrt(s.a*s.a-s.b*s.b)
		s.e=s.cc/s.a
		s.p=s.a*(1-s.e*s.e)

		s.canvas.create_rectangle(5,5,s.mxSize[0],s.mxSize[1],fill="green")
		
#		c.create_rectangle(s.mxSize[0]/2-s.cc,s.mxSize[1]/2+p,s.mxSize[0]/2+cc,s.mxSize[1]/2-p)
#		c.create_oval(s.mxSize[0]/2-a,s.mxSize[1]/2+b,s.mxSize[0]/2+a,s.mxSize[1]/2-b)
		'''
		for x in range(-a,a):#-s.mxSize[0]/2,s.mxSize[0]/2):
			bb=1
			for y in range(-b,b):#-s.mxSize[1]/2,s.mxSize[1]/2):
				be=s.ellipse(x,y)
				#if (not be):
				#	bb=1
				if (be and bb):
					c.create_rectangle(x+s.mxSize[0]/2,y+s.mxSize[1]/2,x+s.mxSize[0]/2,y+s.mxSize[1]/2,outline=None)
					bb=0
				if (not (be or bb)):
					c.create_rectangle(x-1+s.mxSize[0]/2,y+s.mxSize[1]/2,x-1+s.mxSize[0]/2,y+s.mxSize[1]/2,outline=None)
					bb=1
		'''
		if (s.curentEntry=='N'):
			s.triangulate(s.args['N'])
		#c.create_ellipse()
	
	def draw_ellipse3(s,event):
		s.canvas.create_oval(s.mxSize[0]/2-s.a,s.mxSize[1]/2+s.b,s.mxSize[0]/2+s.a,s.mxSize[1]/2-s.b)
		s.step1()
		s.step4(int(s.step3(s.step2())))
		
	def draw_ellipse(s,event):
#		t=1
#		mxS=0
#		mxX=0
#		mxT=0
#		mxY=0
#
		N1=9
		N2=14
		h=s.b/2
		i=0
		try:
			s.i1==0
			s.i2==0
		except:# AtributeError:
			s.i1=0
			s.i2=0
		
		x3=(s.a-h*i)*cos(s.i2*2*pi/N2	)#+((i+1)%2)*0.523259878)
		y3=(s.b-h*i)*sin(s.i2*2*pi/N2	)#+((i+1)%2)*0.523259878)
		x1=(s.a-h*i-h)*cos(s.i1*2*pi/N1	)#+(i%2)*0.523259878)
		y1=(s.b-h*i-h)*sin(s.i1*2*pi/N1	)#+(i%2)*0.523259878)
		s.i2+=1
		s.i1+=1
		if(1):#while (i1<N1 or i2<N2):
			if (s.i1/s.i2>=N1/N2):
				if(s.i2<=N2):
					x2=(s.a-h*i)*cos(s.i2*2*pi/N2	)#+((i+1)%2)*0.523259878)
					y2=(s.b-h*i)*sin(s.i2*2*pi/N2	)#+((i+1)%2)*0.523259878)
					s.i2+=1
			else:
				if (s.i1<=N1):  
					x1=(s.a-h*i-h)*cos(s.i1*2*pi/N1	)#+(i%2)*0.523259878)
					y1=(s.b-h*i-h)*sin(s.i1*2*pi/N1	)#+(i%2)*0.523259878)
					s.i1+=1
			s.canvas.create_line(x1+s.mxSize[0]/2,y1+s.mxSize[1]/2,x2+s.mxSize[0]/2,y2+s.mxSize[1]/2)
#			s.canvas.create_rectangle(x1+s.mxSize[0]/2,y1+s.mxSize[1]/2,x1+s.mxSize[0]/2+2,y1+s.mxSize[1]/2+2)
			s.canvas.create_line(x3+s.mxSize[0]/2,y3+s.mxSize[1]/2,x2+s.mxSize[0]/2,y2+s.mxSize[1]/2)
#			s.canvas.create_rectangle(x2+s.mxSize[0]/2,y2+s.mxSize[1]/2,x2+s.mxSize[0]/2+2,y2+s.mxSize[1]/2+2)
			s.canvas.create_line(x1+s.mxSize[0]/2,y1+s.mxSize[1]/2,x3+s.mxSize[0]/2,y3+s.mxSize[1]/2)
#			s.canvas.create_rectangle(x3+s.mxSize[0]/2,y3+s.mxSize[1]/2,x3+s.mxSize[0]/2+2,y3+s.mxSize[1]/2+2)
			if (s.i1/s.i2>=N1/N2):
				x3=x1
				y3=y1
			else:
				x3=x2
				y3=x2
			print('%i,%i'%(s.i1,s.i2))
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
#				s.canvas.create_line(x2,y2,x2+3,y2+3,fill='red')
				print('%i'%(sqrt((x1-x2)**2+(y1-y2)**2)))
			if (t>=0 and t<=0.2):
				s.canvas.create_line(x1,y1,x2,y2,fill='red')
#				s.canvas.create_rectangle(x2,y2,x2+3,y2+3,fill='red')
				print('%i'%(sqrt((x1-x2)**2+(y1-y2)**2)))'''
			#t+=1
		#print('max S='+str(mxS)+' %.2f, %.2f, %.2f'%(mxX,mxY,atan(mxY/mxX)*180))
		#print('foc S=%.2f %.2f, %.2f, %.2f'%(s.cc*s.p*4,s.cc,s.p,atan(s.p/s.cc)*180))
		#print('%.5f %.5f, %.5f'%(sqrt(mxS/(s.a*s.b*4)),mxX/s.a,mxY/s.b))
#		s.canvas.create_rectangle(s.mxSize[0]/2-mxX+4,s.mxSize[1]/2+mxY+4,s.mxSize[0]/2+mxX-4,s.mxSize[1]/2-mxY-4,fill='red',outline='red')
		#s.canvas.create_rectangle(s.mxSize[0]/2-s.cc,s.mxSize[1]/2+s.p,s.mxSize[0]/2+s.cc,s.mxSize[1]/2-s.p,fill='gray')

	def triangulate(s,n):
		#TODO
		return 0
	def ellipse(s,x,y):

		e=s.args['A']*x*x+s.args['B']*x*y+s.args['C']*y*y
		return e<1
	def quit(s,event):
		s.app.quit()
	
	class ellipse:
		a=None
		b=None
		
if __name__=='__main__':
	a=App()
