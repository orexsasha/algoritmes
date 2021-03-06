# Шибанова Дарья, ИУ7-42
# Лабораторная работа №1
# Построить полином Ньютона на заданной таблице.
# Часть первая:
# пользователем вводятся степень полинома и координата по оси абсцисс.
# Вывести результат интерполяции/экстраполяции и точное значение функции.
# Часть вторая:
# Используя интерполяцию, найти корень функции
# (функция постоянная и возвращающася).

from math import *

# Исходная функция для первой части задания:
def f1(x):
    return x**2 / 2

# Функция для второй части задания:
def f2(x):
    return (x - 3)**2 - 4 # корни 1 и 5, возрастает на [3; +бескон.)

# Рекурсивно строим таблицу:
def y(lst):
    # Если у нас больше двух точек, найдём 2 подтаблицы:
    if (len(lst) > 2):
        delt_y = y(lst[:len(lst)-1]) - y(lst[1:])
    # Если две точки, найдём разность игреков
    elif (len(lst) == 2):
        delt_y = lst[0][1] - lst[1][1]
    else:
        return 0

    # Вернём разность игреков, делённую на разность иксов
    return delt_y / (lst[0][0] - lst[len(lst)-1][0])

# Функция для выполнения интерполяции:
def approx(lst, x0, n):
    # Берём ординату первой точки:
    res = lst[0][1]
    multi = 1
    # Для всех точек, кроме двух:
    for i in range(2, n + 2):
        # Вычисляем коэффициент воздействия (на основании расстояния до текущей точки):
        multi *= x0 - lst[i-2][0]
        # Учитывая коэффициент, изменим итоговую ординату:
        res += multi * y(lst[:i])    
    return res

# Функция выбора точек для построения полинома:
def find(lst, x0, n):
    buf = 0
    # Определяем последнюю точку промежутка интерполяции:
    for i in range(len(lst)):
        # Если интерполируемое значение x0 уже имеется среди точек, вернём его y:
        if lst[i][0] == x0:
            return lst[i][1]
        # В иных случаях:
        if lst[i][0] < x0:
            buf = i
        if lst[i][0] > x0:
            break
    # Если справа от x0 меньше n точек:
    if ((buf + 1) + n) > len(lst):
        buf = len(lst) - (n + 1)

    # Запуск алгоритма интерполяции:
    # передаём список из n+1 точек, начиная с индекса buf, а также x0 и степень:
    res = approx(lst[buf:buf + n + 1], x0, n)
    return res

# Функция обращения координат абсцисс и ординат в списке для второго задания:
def reverse(lst):
    # Создаём пустой список:
    rev_list = []
    # Идя в цикле, меняем местами координаты столбцов таблицы:
    for i in lst:
        rev_list.append([i[1],i[0]])
    return rev_list

# Функция, обрезающая список lst по заданным границам start и end:
def cut(lst, start, end):
    # Создаём пустой список:
    new_list = []
    # Идя в цикле, проверяем, входит ли координата в нужный отрезок (да - добавляем):
    for i in lst:
        if (i[0] >= start and i[0] <= end):
            new_list.append(i)
    return new_list

# Функция нахождения корня для второй части задания:
def root_sec_t(lst, start, end, n):
    rev_list = []
    new_list = cut(lst, start, end)
    rev_list = reverse(new_list)
    root = find(rev_list, 0, n)
    return root

# Функция задания таблицы:
def create_list(f, start, end, step):
    list_sec_t = []
    i = start
    delt = 1e-5
    while (i <= end):
        rec = [i, f(i)] # i = x / f(i)
        if (i >= -1*delt and i <= delt ):
            rec = [0, f(0)]
        list_sec_t.append(rec)
        i = i + step
    return list_sec_t

# Ввод данных (границы таблицы и степень полинома):
x1, x2 = map(float, input('Введите границы интервала \
для построения таблицы: ').split())
h = float(input('Введите шаг таблицы: '))
# построение таблицы значений по введённым границам и её вывод:
lst = create_list(f1, x1, x2, h)
print()
print('Исходная функция: y = x*x / 2')
print()
# вывод таблицы
print('Таблица значений:')
print('x          |       y')
print('-'*25)
for i in range(len(lst)):
    print('{:>10.5f} | {:>10.5f}'.format(lst[i][0],lst[i][1]))
print()
n = int(input('Введите степень для построения полинома: '))
if n > (len(lst) - 1):
    print('Степень превысила максимально возможную (недостаточно точек).')
elif n < 0:
    print('Степень меньше минимально возможной.')
else:
    # Работа с функцией:
    # 1) ввод координаты по оси абсцисс
    x0 = float(input('Введите абсциссу для аппроксимации: '))
    # 2) выполнение интерполяции/экстраполяции с проверкой,
    #    интерполяция или экстраполяция производится:
    res = find(lst, x0, n)
    if x0 > x2:
        print()
        print('Произошла экстраполяция с правой стороны границ.')
        print()
        cy0 = f1(x0)
        print('Точное значение функции: {:10.4f}'.format(cy0))
        print()
        print('Значение функции в результате построения полинома: {:10.4f}'.format(res))
    elif x0 < x1:
        print()
        print('Произошла экстраполяция с левой стороны границ.')
        print()
        cy0 = f1(x0)
        print('Точное значение функции: {:10.4f}'.format(cy0))
        print()
        print('Значение функции в результате построения полинома: {:10.4f}'.format(res))
    else:
        print()
        print('Произошла интерполяция.')
        print()
        cy0 = f1(x0)
        print('Точное значение функции: {:10.4f}'.format(cy0))
        print()
        print('Значение функции в результате построения полинома: {:10.4f}'.format(res))
print()
print('Нахождение корня: ')
print()
print('Исходная функция: y = (x - 3)*(x - 3) - 4')
print()
lst = create_list(f2, 0, 10, 0.7)
print('Таблица имеющихся значений: ')
print('x          |       y')
print('-'*25)
for i in range(len(lst)):
    print('{:>10.5f} | {:>10.5f}'.format(lst[i][0],lst[i][1]))
print()
print('Данная функция монотонно возрастает на промежутке [3; +бесконечность),')
print('поэтому возьмём отрезок [3; 10] исходной таблицы.')
print('Точный корень на отрезке [3; 10]: 5')
n = int(input('Введите степень полинома для нахождения корня: '))
if (n >= len(cut(lst, 3, 10))):
    print('Слишком большая степень, невозможно построить полином.')
elif (n < 0):
    print('Слишком маленькая степень, невозможно построить полином.')
else:
    root = root_sec_t(lst, 3, 10, n)
    print('Полученный корень: {:10.4f}'.format(root))
