import os
import sys

if sys.platform.startswith('win32'):
    os.system('cls')
else:
    os.system('clear')

while True:
    os.system('python bot.py')