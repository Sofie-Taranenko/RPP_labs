 #Задание 1.4
x = 0
y = 0
z = int(input("Введите последовательность (закончить - 0)"))
while z != 0:
        x+= z
        y+= 1
        z = int(input("Введите последовательность (закончить - 0)"))
        print("Сумма чисел =", x)
        print("Количество чисел", y)