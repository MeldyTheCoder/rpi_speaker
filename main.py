from speak import Speaker
import time

sp = Speaker()

@sp.sound
def task1():
    for i in range(0, 20):
        print(i)
    time.sleep(5)


@sp.sound
def task2():
    for i in range(10, 60):
        if i == 59:
            raise KeyError



task1()
task2()
input('')