from art import *
from time import sleep
import os
text = text2art('Welcome, \n{}  :)'.format(os.getlogin()))

for line in text.split('\n'):
    print(line)
    sleep(0.01)
