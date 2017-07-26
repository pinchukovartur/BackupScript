# -*- coding: utf-8 -*-
import datetime
import os
import zipfile


# The method archives the specified folder
def archiving_folder(path, file_name, path_saved_arch):
    if os.path.exists(path):
        print(path)
        full_file_name = file_name + datetime.datetime.now().strftime(
            " %d %m %Y %H %M %S") + '.backup.zip'
        # create zip file in directory
        arch = zipfile.ZipFile(path_saved_arch + "\\" + full_file_name, 'w', zipfile.ZIP_DEFLATED)
        # add file in zip file
        lenDirPath = len(path)
        for root, dirs, files in os.walk(path + "\\" + file_name):
            for file in files:
                if file != '':
                    filePath = os.path.join(root, file)
                    arch.write(filePath, filePath[lenDirPath:])
        arch.close()
        __check_archive(path_saved_arch + "\\" + full_file_name)
    else:
        raise NameError("ERROR!!! not find clone path\n Check config file: clone directory")


# check arch size
def __check_archive(file_name):
    if int(os.path.getsize(file_name)) < 1024:
        os.remove(file_name)
        raise NameError("ERROR!!! archive size less  1kb\n Check config file: clone and cloud directory")