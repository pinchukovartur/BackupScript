# -*- coding: utf8 -*-
# @author Pinchukov Artur
# The script is responsible for downloading the repositories
import subprocess, os


# The main method that downloads projects with github
def download_repository(repository_url, file_path):
    if check_folder(file_path):
        try:
            # arguments passed to run function
            a = "cd /D " + file_path + " && git clone " + repository_url
            # run process cloning repository
            p = subprocess.run(a, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("There was an error when the script tried to clone the project - " + repository_url)
    else:
        print('The directory does not exist')


# The method checks the presence of the specified path
def check_folder(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

# Example
# download_repository('https://github.com/pinchukovartur/Fog-Of-War.git', 'D:\Projects\HeLSCRIPTS')
