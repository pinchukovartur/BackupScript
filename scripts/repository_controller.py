import subprocess
import os
import datetime
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
        raise NameError("ERROR!! git error number - " + str(p.returncode))
    else:
        print("good download repository - " + str(p.returncode))


# The method archives the specified folder
def archiving_folder(path, file_name):
    if os.path.exists(path):
        full_file_name = file_name + datetime.datetime.now().strftime(
            " %d %m %Y %H %M %S") + '.backup.zip'
        # create zip file in directory
        arch = zipfile.ZipFile(path + "\\" + full_file_name, 'w', zipfile.ZIP_DEFLATED)
        # add file in zip file
        lenDirPath = len(path)
        for root, dirs, files in os.walk(path + "\\" + file_name):
            for file in files:
                if file != '':
                    filePath = os.path.join(root, file)
                    arch.write(filePath, filePath[lenDirPath:])
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
