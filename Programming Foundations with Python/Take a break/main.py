__author__ = 'Maycon'

import time
import webbrowser

totalBreaks = 3
breakCount = 0

print ("Esse programa iniciou em " + time.ctime())
while breakCount < totalBreaks:
    time.sleep(10)
    webbrowser.open("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
    breakCount += 1
    print("Descanso numero " + breakCount)
#webbrowser.open("http://www.youtube.com/watch?v=5CxdZpGaVco")