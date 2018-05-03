# Лабораторная работа №2
# Провести "трёхмерную" интерполяцию на основе функции z = f(x,y).
# Пользователем вводятся параметры x, y и степени интерполяции по x и y.

from math import *

# Исходная функция:
def f(x, y):
    return x*x + y*y
    #return x*x/2 + y*y/2

# Функция, вычисляющая y для модели вида x,y:
def g(lst):
    # Если больше двух точек, найдём две подтаблицы:
    if (len(lst) > 2):
        delt_z = g(lst[:len(lst)-1]) - g(lst[1:])
    # В иных случаях:
    else:
        delt_z = lst[0][1] - lst[1][1]
    return delt_z / (lst[0][0] - lst[len(lst)-1][0])

# Функция для выполнения интерполяции:
def approx(lst, x0, n):
    # Берём ординату первой точки:
    res = lst[0][1]
    multi = 1
    # Для всех точек, кроме двух:
    for i in range(2, n + 2):
        # Вычислим коэффициент воздействия:
        multi *= x0 - lst[i-2][0]
        res += multi * g(lst[:i])
    return res

# Функция выбора точек для построения полинома:
def find(lst, x0, n):
    buf = 0
    # Определим последнюю точку промежутка интерполяции:
    for i in range(len(lst)):
        # Если интерполируемое значение уже есть среди точек,
        # вернём соответствующее ему значение:
        if lst[i][0] == x0:
            return lst[i][1]
        # В ином случае:
        if lst[i][0] < x0:
            buf = i
    # Если справа от x0 меньше нужного числа точек:
    if ((buf + 1) + n) > len(lst):
        buf = len(lst) - (n + 1)
    # Выполним алгоритм интерполяции:
    res = approx(lst[buf:buf + n + 1], x0, n)
    return res

# Функция, которая возвращает массив х и у,
# которые представляют из себя все значения х и у соответственно в диапазоне с шагом:
def get_range(start_x, end_x, hx, start_y, end_y, hy):
    a = start_x
    b = start_y
    r_x = []
    r_y = []
    while (a <= end_x):
        r_x.append(a)
        a = a + hx
    while (b <= end_y):
        r_y.append(b)
        b = b + hy    
    return r_x,r_y

# Функция создания таблицы, возвращает массив z на участке с шагом:
def create_table(f, start_x, end_x, hx, start_y, end_y, hy):
    a = start_x
    b = start_y
    table = []
    while (a <= end_x):
        rec = []
        while (b <= end_y):
            rec.append(f(a,b))
            b = b + hy
        table.append(rec)  
        a = a + hx
        b = start_y
    return table

# Функция вывода таблицы:
def print_data(x, y, z):
    print('       ',end = '')
    # Выводим все ординаты:
    for i in range(len(y)):
        print('{:7.3f} '.format(y[i]),end='')
    print()
    j = 0
    r = 0
    # Выводим абсциссы и значения функции, пока не закончился массив:
    for i in range(len(x)):
        print('{:7.3f}'.format(x[i]),end='')
        for j in range(len(y)):
            print('{:7.3f} '.format(z[i][j]),end = '')
        print('')

# Функция, склеивающая строки:
def concat(a, b):
    # Создаём список:
    new_lst = []
    # Идя в цикле, добавляем данные:
    for i in range(len(a)):
        new_lst.append([a[i],b[i]])
    return new_lst

# Функция нахождения значения функции,
# в которой находим сначала точку от которой считать,
# после чего считаем необходимое число полиномов,
# на основе которых считаем значение z:
def find_new(x1, y1, n_x, n_y, x, y, z):
    for_x = []
    i_y = 0
    i_x = 0
    for i in range(len(y)):
        if y1 == y[i]:
            i_y = i
            break
        elif y1 < y[i]:
            i_y = i - 1
            break
        else:
            i_y += 1
    for i in range(len(x)):
        if x1 == x[i]:
            i_x = i
            break
        elif x1 < x[i]:
            i_x = i - 1
            break
        else:
            i_x += 1

    while (i_y + n_y +1>= len(y)):
        i_y -= 1

    while (i_x + n_x +1>= len(y)):
        i_x -= 1   
        
    tmp_y = y[i_y:i_y + n_y + 1]
    for j in range(n_x + 1):
        tmp_z = z[i_x + j][i_y:i_y + 1 + n_y]
        tmp_l = concat(tmp_y, tmp_z)
        p = find(tmp_l, y1, n_y)
        for_x.append(p)
    tmp_x = x[i_x:i_x + n_x + 1]
    l = concat(tmp_x, for_x)
    p = find(l, x1, n_x)
    return p

fx, lx, hx = map(float, input('Введите границы интервала по x и шаг: ').split())
fy, ly, hy = map(float, input('Введите границы интервала по y и шаг: ').split())
x, y = get_range(fx, lx, hx, fy, ly, hy)
z = create_table(f, fx, lx, hx, fy, ly, hy)
print_data(x, y, z)
x1, y1 = map(float, input("Введите x и y, для которых ищем значение функции: ").split())
n_x = -1
n_y = -1
while ((n_x < 0 or n_y < 0) or (n_x > len(x)) or (n_y > len(y))):
    n_x,n_y = map(int, input("Введите степени по х и по у: ").split())
    if (n_x < 0 or n_y < 0):
        print('Введена отрицательная степень полинома (должна быть не меньше 0).\
Пожалуйста, введите заново.')
    if (n_x > len(x)) or (n_y > len(y)):
        print('Введена слишком маленькая степень, невозможно построить полином.')
res = find_new(x1, y1, n_x, n_y, x, y, z)
print('Точное значение функции: {:7.3f}'.format(f(x1,y1)))
print('Значение функции, полученное в результате построения полинома: {:7.3f}'.format(res))
