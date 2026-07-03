import pygame as py
from math import *
py.init()
R=400
screen=py.display.set_mode((R,R))
clock=py.time.Clock()
running=True
gravity=0.03
TBal=5
Z=0;T=TBal*2
L=ceil((R+100)/T)
minX=-50;minY=-50;fps=120
font=py.font.SysFont("Calibri",20,bold=True)
Bal=[];RES=[]
Rplace=[]
contrainte="C"
def getgrid():
    grid=[[[]for i in range(L)]for w in range(L)]
    for b in Bal:
        Px,Py=int(b.x-minX)//T,int(b.y-minY)//T
        grid[Py][Px]+=[b.Z]
    return grid
grid=getgrid()
F=1;ADD=1
class particle():
    def __init__(self,x,y,r,c,Z,move):
        self.x=x;self.y=y;self.r=r;self.c=c;self.Z=Z
        self.x1,self.y1=x,y
        self.immobile=move
    def depla(self):
        if self.immobile:
            self.x,self.y=self.x1,self.y1
            return
        self.x,self.y,self.x1,self.y1=(1+F)*self.x-F*self.x1,self.y*(1+F)-F*self.y1+gravity,self.x,self.y
    def draw(self):
        py.draw.circle(screen,self.c,(self.x,self.y),self.r)
    def contrainteC(self):
        if self.immobile:return
        dx,dy=self.x-R/2,self.y-R/2
        d=sqrt(dx**2+dy**2)
        if d>R/2-self.r:
            delta=(R/2-self.r)/d
            Dx=R/2+delta*dx;Dy=R/2+delta*dy
            self.x=Dx
            self.y=Dy
    def contrainteR(self):
        if self.immobile:return
        self.x=min(max(0,self.x),R)
        self.y=min(max(0,self.y),R)
    def solver(self):
        if self.immobile:return
        cx,cy=int(self.x-minX)//T,int(self.y-minY)//T
        Bt=[]
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                Bt+=grid[cy+dy][cx+dx]
        for www in Bt:
            b=Bal[www]
            if b.Z!=self.Z:
                dx,dy=self.x-b.x,self.y-b.y
                d=sqrt(dx**2+dy**2)
                sumR=b.r+self.r
                w=sumR-d
                if 0<w and d!=0:
                    delta=w/(2*d)
                    self.x+=dx*delta
                    self.y+=dy*delta
                    b.x-=dx*delta
                    b.y-=dy*delta

def pr():
    if contrainte=="C":py.draw.circle(screen,(255,255,255),(R/2,R/2),R/2,5)
    for b in Bal:
        b.draw()
    for l in RES:
        b0,b1=Bal[l[0]],Bal[l[1]]
        py.draw.line(screen,(100,100,100),(b0.x,b0.y),(b1.x,b1.y),2)
    screen.blit(font.render(str(fps),True,(255,255,255)),(5,5))
    screen.blit(font.render(str(len(Bal)),True,(255,255,255)),(5,20))
def simulate():
    for b in Bal:
        b.depla()
    for b in Bal:
        b.solver()
    k=-1
    for i1,i2,d in RES:
        b1,b2=Bal[i1],Bal[i2]
        dx,dy=b2.x-b1.x,b2.y-b1.y
        Ad=sqrt(dx**2+dy**2)
        Dd=k*(d-Ad)/(2*Ad)
        Dx=Dd*dx;Dy=Dd*dy
        b1.x+=Dx;b1.y+=Dy
        b2.x-=Dx;b2.y-=Dy
    if contrainte=="C":
        for b in Bal:
            b.contrainteC()
    else:
        for b in Bal:
            b.contrainteR()
while running:
    xs,ys=py.mouse.get_pos()
    for event in py.event.get():
        if event.type==py.QUIT:
            running=False
        if event.type==py.MOUSEBUTTONDOWN:
            cx,cy=int(xs-minX)//T,int(ys-minY)//T
            Bt=[]
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    Bt+=grid[cy+dy][cx+dx]
            for k in Bt:
                b=Bal[k]
                d=(xs-b.x)**2+(ys-b.y)**2
                if d<b.r**2:
                    ADD=0
                    Rplace.append(k)
                    print(0)
            if Rplace:
                if len(Rplace)>1:
                    if Rplace[0]!=Rplace[1]:
                        b0=Bal[Rplace[0]];b1=Bal[Rplace[1]]
                        d=(b0.x-b1.x)**2+(b0.y-b1.y)**2
                        RES.append(Rplace[:2]+[sqrt(d)])
                    Rplace=[]
        if event.type==py.MOUSEBUTTONUP:
            ADD=1
    screen.fill("black")
    pr()
    py.display.flip()
    grid=getgrid()
    simulate()
    if py.mouse.get_pressed()[0] and ADD:
        Bal+=[particle(xs,ys,TBal,(255,255,255),Z,0)]
        Z+=1
    clock.tick(60)
    fps=round(clock.get_fps(),1)
py.quit()
