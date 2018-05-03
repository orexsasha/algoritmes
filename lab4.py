
from random import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
import copy

# Исходная функция:
def f(x, j):
    #return
    return pow(x, j)

# Функция для генерации таблицы с отклонениями:
def f_gen(x):
    #return sin(x)
    return x**3+x+12

# Генерация таблицы с отклонениями:
def generate_rand():
    f_add = open(input("Введите название файла для записи сгенерированной таблицы: ") + '.txt', "w")
    for i in range(20):
        x = -5 + i * 0.5
        # отклонения +-7%, вес всех точек 1:
        #print("{:0.4f} {:0.4f} {:0.4f}".format(x, f_gen(x) * (1 + (random() - 0.7) * 0.1), 1))
        f_add.write("{:0.4f} {:0.4f} {:0.4f}\n".format(x, f_gen(x) * (1 + (random() - 0.7) * 0.1), 1))
    return

# Вычисление ... (Дописать отсюда...)
def approximate(x, coefs):
    y = 0
    for j in range(n + 1):
        y += coefs[j] * f(x, j)
        
    return y

def nparray_to_list(a):
    a = list(a)
    for i in range(len(a)):
        a[i] = list(a[i])
    return a

def gauss_seidel(A, b, eps):
    n = len(A)  # размерность матрицы
    x = [0 for i in range(n)]  # инициализация вектора(приближение)

    converge = False  # сходимость
    while not converge:
        x_new = x.copy()   # предыдущее приближение
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        converge = sqrt(sum((x_new[i] - x[i]) ** 2 for i in range(n))) <= eps
        x = x_new
    return x

def solve():
    N = len(x)
    A = np.zeros((n + 1, n + 1))
    B = np.zeros((n + 1, 1))
    for j in range(n + 1):
        for k in range(n + 1):
            for i in range(N):
                A[j, k] += f(x[i], k + j) * p[i]
        for i in range(N):
            B[j] += y[i] * f(x[i], j) * p[i]

    det = np.linalg.det(A)
    
    nparray_to_list(A)
    nparray_to_list(B)
    
    print("Det:", det)
    if abs(det) <= 1e-7:# or abs(det) >= 1e15:
        print("\nОпределитель равен нулю, аппроксимация не определена!\n")
        #exit()

##    D = np.linalg.inv(A) # обратная матрица к А
##    D = np.matrix(D) # Преобразуем в матрицу
##    C = D * B # Умножим обратную матрицу на вектор значений
##    C = C.transpose() # Получим из вектор-столбца вектор-строку
##    ret = np.array(C.ravel()) # Получим одномерный массив по строкам
##    ret = nparray_to_list(ret)[0] # Преобразуем в массивы питона

    return gauss_seidel(A, B, 1e-4)


# ... (...до этого места)


# Инициализация массивов x, y и весов
x = []
y = []
p = []

#print("Предварительно сгенерировать точки? (1 - Да, 0 - Нет)")#
#print("(Иные числа будут интерпретированы как Нет)")#
#choice = int(input())#
choice = 0#
if (choice == 1):
    generate_rand()

# Считывание данных из файла:
#with open(input("Введите имя файла с набором данных: ") + ".txt", "r") as file:#
with open("123.txt", "r") as file:#
    for line in file.readlines():
        line = line.split()
        if len(line) != 3:
            continue
        else:
            x.append(float(line[0]))
            y.append(float(line[1]))
            p.append(float(line[2]))

if len(x) == 0:
    print("В таблице отсутствуют элементы, работа программы прервана")
    exit()
else:
    print("Исходная таблица, состоящая из", len(x), "элементов:")
    print('x          |       y    |          p')
    print('-'*40)
    for i in range(len(x)):
        print('{:>10.5f} | {:>10.5f} | {:>10.5f}'.format(x[i], y[i], p[i]))
    print()
    
n = int(input('Введите степень аппроксимации: '))

coefs = solve()

# Вывод графика:

x_show = [min(x) - (max(x) - min(x)) / 10 + i * 1.2 * (max(x) - min(x)) / 1000 for i in range(1000)]
plt.plot(x, y, 'ko')
plt.plot(x_show, [approximate(i, coefs) for i in x_show], '-r')

plt.show()
