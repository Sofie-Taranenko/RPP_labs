# Задание 3.5
import sys

a = []
for arg in sys.argv[1:]:
    a.append(arg)

print(a)

for i, v in enumerate(a):
    if int(v) < 0:
        if i + 1 <= len(a) and int(a[i + 1]) < 0:
            print(v, a[i + 1])

inst_list = list(set(a))
print(inst_list)