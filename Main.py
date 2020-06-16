from time import sleep
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
from math import cos, sin, radians

def Read_files():
    file1 = open('Points.txt', 'r')
    p = [x.strip().split(' ')+[1.0] for x in file1]
    file1.close()
    file2 = open('Connections.txt', 'r')
    c = [x.strip().split(' ') for x in file2]
    file2.close()
    return p,c
    pass

points, connetctions = Read_files()
points = np.array([[float(i[0]),float(i[1]), float(i[2]), 1.0] for i in points])
connetctions = np.array([[int(i[0]),int(i[1])] for i in connetctions])-1
dx, dy, dz, k = 0, 0, 0, 0

def vokrug_X():
    global points, dx
    a = dx
    matr = np.array([[1,0,0,0],[0, cos(a), -sin(a), 0], [0, sin(a), cos(a), 0], [0,0,0,1]])
    points = np.dot(points, matr)

def vokrug_Y():
    global points, dy
    a = dy
    matr = np.array([[cos(a),0,-sin(a),0],[0,1,0,0],[sin(a),0,cos(a),0],[0,0,0,1]])
    points = np.dot(points, matr)

def vokrug_Z():
    global points, dz
    a = dz
    matr = np.array([[cos(a),-sin(a),0,0],[sin(a),cos(a),0,0],[0,0,1,0],[0,0,0,1]])
    points = np.dot(points,matr)

def Draw():
    global points
    can.delete("all")
    # Center()
    for i in connetctions:
        x0, y0 = points[i[0]][0], points[i[0]][1]
        x1, y1 = points[i[1]][0], points[i[1]][1]
        can.create_line(x0, y0, x1, y1)
        pass
    pass

def For_all(k1=0,k2=0,k3=0):
    global points
    matr = np.array([[1, 0, 0, k1], [0, 1, 0, k2], [0, 0, 1, k3],[0, 0, 0, 1]])
    points = np.dot(points, matr)
    print('Two ',points)
    if k1!=0:
        for i in points:
            i[1] /= i[-1]
            i[2] /= i[-1]
            i[-1] /= i[-1]
            pass
    elif k2!=0:
        for i in points:
            i[0] /= i[-1]
            i[2] /= i[-1]
            i[-1] /= i[-1]
            pass
    elif k3!=0:
        for i in points:
            i[0] /= i[-1]
            i[1] /= i[-1]
            i[-1] /= i[-1]
            pass
    pass

def Perspectiva():#Одноточечное проективное преобразование
    global points
    print('One ', points)
    k1, k2, k3 = kx.get(), ky.get(), kz.get()
    k1 = 0 if k1 == '' or k1 == 0 else -1/float(k1)
    k2 = 0 if k2 == '' or k2 == 0 else -1/float(k2)
    k3 = 0 if k3 == '' or k3 == 0 else -1/float(k3)
    For_all(k1 = k1)
    For_all(k2 = k2)
    For_all(k3 = k3)
    print('Three ',points)
    Scale()
    Draw()
    pass


def Scale():
    global points, k
    max = 1
    for i, val1 in enumerate(points):
        for j in range(i+1, len(points)):
            raz = ((val1[0] - points[j][0])**2 + (val1[1] - points[j][1])**2 + (val1[2] - points[j][2])**2)**0.5
            if raz > max:
                max = raz
        pass
    k = 710/max
    matr = np.array([[k,0,0,0],[0,k,0,0],[0,0,k,0],[0,0,0,1]])
    points = np.dot(points, matr)

def Sdvig(xa, ya, za = 0):
    global points
    matr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[xa,ya,za,1]])
    points = np.dot(points, matr)

def Center():
    global points
    left, top, right, down = 1e20, 1e20, 0, 0
    for i in connetctions:
        x0, y0 = points[i[0]][0], points[i[0]][1]
        x1, y1 = points[i[1]][0], points[i[1]][1]
        if x0 < left: left = x0
        if x1 < left: left = x1
        if y0 < top: top = y0
        if y1 < top: top = y1

        if x0 > right: right = x0
        if x1 > right: right = x1
        if y0 > down: down = y0
        if y1 > down: down = y1
        pass
    MAIN_MIDL_X = 500
    MAIN_MIDL_Y = 360
    midl_x = left + (right - left)/2
    midl_y = top + (down - top)/2
    xa = MAIN_MIDL_X - midl_x
    ya = MAIN_MIDL_Y - midl_y
    Sdvig(xa, ya)

def CLick():
    global points, dx, dy, dz
    dx, dy, dz = x.get(), y.get(), z.get()
    dx = 0 if dx == '' else radians(float(dx))
    dy = 0 if dy == '' else radians(float(dy))
    dz = 0 if dz == '' else radians(float(dz))
    vokrug_X()
    vokrug_Y()
    vokrug_Z()
    Draw()
    pass

f = False

def Default():
    global points, connetctions, dx, dy, dz
    points, connetctions = Read_files()
    points = np.array([[float(i[0]), float(i[1]), float(i[2]), 1.0] for i in points])
    connetctions = np.array([[int(i[0]), int(i[1])] for i in connetctions]) - 1
    dx, dy, dz = 0, 0, 0
    Scale()
    Draw()

def Dvij():
    global f, dx, dy, dz
    f = not f
    if f:
        dx, dy, dz = spin_x.get(), spin_y.get(), spin_z.get()
        dx = 0 if dx == '' else radians(float(dx))
        dy = 0 if dy == '' else radians(float(dy))
        dz = 0 if dz == '' else radians(float(dz))
        bt2['text'] = 'стоп'
    else:
        dx, dy, dz = 0, 0, 0
        bt2['text'] = 'Начать'
    while f:
        vokrug_X()
        vokrug_Y()
        vokrug_Z()
        Draw()
        can.update()
        sleep(0.1)
    pass

def Smeshenie():
    global points, k
    kind = combo.get()
    match = last.get()
    S = {'xy':0, 'yx':0,'xz':0,'zx':0,'yz':0,'zy':0}
    S[kind] = float(match)/k
    matr = np.array([[1,S['yx'],S['zx'],0],[S['xy'],1,S['zy'],0],[S['xz'],S['yz'],1,0],[0,0,0,1]])
    points = np.dot(points,matr)
    Scale()
    Draw()
    pass

def Vpis():
    global points
    left, top, right, down = 1e20, 1e20, 0, 0
    for i in connetctions:
        x0, y0 = points[i[0]][0], points[i[0]][1]
        x1, y1 = points[i[1]][0], points[i[1]][1]
        if x0 < left: left = x0
        if x1 < left: left = x1
        if y0 < top: top = y0
        if y1 < top: top = y1

        if x0 > right: right = x0
        if x1 > right: right = x1
        if y0 > down: down = y0
        if y1 > down: down = y1
        pass
    kk = min(710/(down - top), 990/(right - left))
    matr = np.array([[kk, 0, 0, 0], [0, kk, 0, 0], [0, 0, kk, 0], [0, 0, 0, 1]])
    points = np.dot(points, matr)
    Center()
    Draw()
    pass

def Perenos():
    global points, dx, dy, dz
    dx, dy, dz = x.get(), y.get(), z.get()
    dx = 0 if dx == '' else radians(float(dx))
    dy = 0 if dy == '' else radians(float(dy))
    dz = 0 if dz == '' else radians(float(dz))
    matr = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])
    points = np.dot(points, matr)
    Scale()
    Draw()
    pass



windows = Tk()
can = Canvas(windows, width = 1000, height = 720, bg = 'white')
can.grid(column = 0, row = 0)
windows.title('Компьютерная графика')
windows.geometry('1280x720+320+180')
lbl = Label(windows, text='Перенос и поворот на\nзаданный угол',justify = CENTER, font = ('Bold', 15))
lbl.place(relx = .8, rely = .04)
pom = Label(windows, text='x              y              z',font = ('Bold', 12))
pom.place(relx = 0.833, rely = 0.11)

x = Entry(windows, width = 5)
x.place(relx = 0.825, rely = 0.15)

y = Entry(windows, width = 5)
y.place(relx = 0.875, rely = 0.15)

z = Entry(windows, width = 5)
z.place(relx = 0.925, rely = 0.15)

bt = Button(windows, text = 'Поворот', command = CLick)
bt.place(relx = 0.875, rely = 0.18)

flex = Label(text = 'Флекс', font = ('Bold',15))
flex.place(relx = 0.867,rely = 0.24)

pom_pom = Label(windows, text='x              y              z',font = ('Bold', 12))
pom_pom.place(relx = 0.833, rely = 0.28)

spin_x = Spinbox(windows, from_ = 0, to = 10, width = 5)
spin_x.place(relx = 0.825,rely = 0.32)
spin_y = Spinbox(windows, from_ = 0, to = 10, width = 5)
spin_y.place(relx = 0.875, rely = 0.32)
spin_z = Spinbox(windows, from_ = 0, to = 10, width = 5)
spin_z.place(relx = 0.925, rely = 0.32)

bt2 = Button(windows, text = 'Начать', command = Dvij)
bt2.place(relx = 0.85,rely = 0.35)

for_default = Button(windows, text = 'обратно', command = Default, width = 20)
for_default.place(relx = 0.83, rely = .0)

Perspect = Label(windows, text = 'Перспектива', font = ('Bold', 15))
Perspect.place(relx = 0.82, rely = 0.42)
pom_pom_pom = Label(windows, text='x              y              z',font = ('Bold', 12))
pom_pom_pom.place(relx = 0.83, rely = 0.46)

kx = Entry(windows, width = 5)
kx.place(relx = 0.825, rely = 0.49)

ky = Entry(windows, width = 5)
ky.place(relx = 0.875, rely = 0.49)

kz = Entry(windows, width = 5)
kz.place(relx = 0.925, rely = 0.49)

kbt = Button(windows, text = 'начинай', command = Perspective)
kbt.place(relx = 0.834, rely = 0.52)

sdv = Label(windows, text = 'Косой сдвиг', font = ('Bold', 15))
sdv.place(relx = 0.836, rely = 0.57)
S = Label(windows, text = 'Выберите вариант косого сдвига\nИ введите значение', font = ('Bold', 10))
S.place(relx = 0.785, rely = 0.62)

last = Entry(windows, width = 7)
last.place(relx = 0.85, rely = 0.68)
last.insert(0,'Тут')

bt_last = Button(windows, text = 'Сдвинуть', command = Smeshenie)
bt_last.place(relx = 0.8, rely = 0.71)

combo = Combobox(windows, values = ('xy', 'yx','xz','zx','yz','zy'), width = 5)
combo.current(0)
combo.place(relx = 0.95, rely = 0.625)

l = Label(windows, text = "Вписывание в экран", font = ('Bold', 15))
l.place(relx = .8, rely = .8)

b = Button(windows, text = "Клик", command = Vpis)
b.place(relx = .82, rely = .85)

b_per = Button(windows, text = "Перенеос", command = Perenos)
b_per.place(relx = .81, rely =.18)

Scale()
Center()
Draw()
windows.mainloop()