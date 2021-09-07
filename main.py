import random
import sys, threading
import time


def printt(n):
    x = random.randint(1, 100)
    time.sleep(x/100)
    print(n)

def printts(n):
    time.sleep(3)
    print(n, ' отработал')


if __name__ == '__main__':
    for i in range(10):
        my_thread = threading.Thread(target=printt(i))
        my_thread1 = threading.Thread(target=printts(i))
        my_thread.start()



