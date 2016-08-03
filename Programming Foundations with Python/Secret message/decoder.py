__author__ = 'Maycon'

import os

def rename_files():
    # (1) get file names from a folder
    file_list = os.listdir(r"E:\Users\Maycon\Desktop\Maycon\Material Faculdade\Udacity\Programming Foundations with Python\Secret message\prank")
    print file_list
    working_dir = os.getcwd()
    print ("Current Working Directory is " + working_dir)
    os.chdir(r"E:\Users\Maycon\Desktop\Maycon\Material Faculdade\Udacity\Programming Foundations with Python\Secret message\prank")

    # (2) for each file, rename file
    for file_name in file_list:
        print ("Old file's name " + file_name)
        os.rename(file_name, file_name.translate(None, "0123456789"))
        print ("New file's name " + file_name)

rename_files()