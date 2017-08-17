import datetime
import os
import subprocess
import sys
import zipfile


# The method that downloads projects with github
# repository_url - network address of the repository
# file_path - the path where the project will be cloned
def download_repository(repository_url, file_path):
    # if os.path.exists(file_path):
    # create new process
    p = subprocess.run("git clone " + repository_url + " " + file_path, shell=True)
    # exit if process error
    if p.returncode != 0:
        raise NameError("ERROR!! git error code - " + str(p.returncode))
    else:
        print("Successful download repository - " + str(p.returncode))


# The method archives the specified folder
# path - path folder where need archived
# file_name - project name
# folder_name - folder which need archived
def archiving_folder(path, file_name, folder_name):
    if os.path.exists(path):
        full_file_name = file_name + datetime.datetime.now().strftime(
            " %d-%m-%Y %H_%M_%S") + '.backup.zip'
        # create zip file in directory
        arch = zipfile.ZipFile(path + "\\" + full_file_name, 'w', zipfile.ZIP_DEFLATED)
        # add file in zip file
        lenDirPath = len(path)

        # set process bar size
        toolbar_width = 100
        tb_now = 0
        file_number = 1
        number_of_file = __get_number_file_in_direct(path + "\\" + folder_name)

        # setup toolbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

        for root, dirs, files in os.walk(path + "\\" + folder_name):
            for file in files:
                if file != '':
                    # get % toolbar
                    tb_must_be = int(file_number / number_of_file * 100)
                    while True:
                        if tb_now < tb_must_be:
                            sys.stdout.write("#")
                            sys.stdout.flush()
                            tb_now = tb_now + 1
                        else:
                            break
                    file_number = file_number + 1
                    # update the bar

                    filePath = os.path.join(root, file)
                    arch.write(filePath, filePath[lenDirPath:])

        sys.stdout.write("\n")

        arch.close()
        __check_archive(path + "\\" + full_file_name)
        return full_file_name
    else:
        raise NameError("ERROR!!! not find clone path\n Check config file: clone directory")


# check arch size
def __check_archive(file_name):
    # if arch file < 1 kb = error
    if int(os.path.getsize(file_name)) < 1024:
        os.remove(file_name)
        raise NameError("ERROR!!! archive size less  1kb\n Check config file: clone and cloud directory")


# The method return number of file in directory
# - path where files are counter
def __get_number_file_in_direct(path):
    # find folder in directory
    if os.path.exists(path):
        number = 0
        # get file with .backup.zip expansion
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != '':
                    number = number + 1

        return number
    else:
        raise NameError("ERROR!!! Do not find path directory - check config file")
