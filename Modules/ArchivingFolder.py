# -*- coding: utf8 -*-
# @author Pinchukov Artur
# The script archives the specified folder and sends it back
import os, zipfile, datetime


# The method archives the specified folder
def archiving_folder(path_folder, archive_name, path_made_archive):

    full_archive_name = path_made_archive + archive_name + datetime.datetime.now().strftime(" %d %m %Y %H %M") + '.zip'
    # create zip file in directory
    arch = zipfile.ZipFile(full_archive_name, 'w', zipfile.ZIP_DEFLATED)
    # add file in zip file
    for root, dirs, files in os.walk(path_folder):
        for tarfile in files:
            if tarfile != '':
                arch.write(root + '\\' + tarfile)
    arch.close()


# Example
# archiving_folder('D:\Projects\HeLSCRIPTS\Fog-Of-War', 'Fog-Of-War', 'D:\Projects\HeLSCRIPTS\\')
