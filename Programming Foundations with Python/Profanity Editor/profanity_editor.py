__author__ = 'Maycon'

import urllib

def read_text():
    quotes = open("E:\Users\Maycon\Desktop\Maycon\Material Faculdade\Udacity\Programming Foundations with Python\Profanity Editor\movie_quotes.txt")
    contents_of_file = quotes.read()
    print(contents_of_file)
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(text_to_check):
    connection = urllib.urlopen("http://www.wdyl.com/profanity?q=" + text_to_check)
    output = connection.read()
    #print output
    connection.close()
    print("")
    if "true" in output:
        print("Profanity Alert")
    elif "false" in output:
        print("This document is alright")
    else:
        print("Problems reading the document")

read_text()