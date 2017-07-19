# -*- coding: utf8 -*-
# @author Pinchukov Artur
# The script is moving a file to a directory
import shutil


# The main method that move file in directory
def moving_file_to_directory(directory_file, moving_point):
    try:
        shutil.move(directory_file, moving_point)
    except WindowsError:
        print("Locked when downloading a file to a folder " + moving_point)


# Example
# moving_file_to_directory('D:\Projects\HeLSCRIPTS\Fog-Of-War 19 07 2017 19 30.zip', 'D:\Projects\\')
