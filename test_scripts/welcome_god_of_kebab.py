from art import *
from time import sleep
text = text2art('Welcome, \nGod  Of  Kebab  :)')

for line in text.split('\n'):
    print(line)
    sleep(0.05)
