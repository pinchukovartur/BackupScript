import pycron
import time

b = True
while b:
    print(pycron.datetime.minute)
    if pycron.is_now('*/2 * * * *'):
        b = False
        print(b)
