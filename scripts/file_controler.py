import os
import sys
import stat


# checks for a folder
def check_folder(folder_path, create_exception=False):
    # if folder not found False or Error
    if not os.path.exists(folder_path):
        if create_exception:
            raise NameError("ERROR!! not found folder - " + folder_path)
        else:
            return False
    return True


# checks for a file
def check_file(file_path, create_exception=False):
    # if file not found False or Error
    if not os.path.isfile(file_path):
        if create_exception:
            raise NameError("ERROR!! not found file - " + file_path)
        else:
            return False
    return True


# Delete folder in path
# pth - path to folder
def delete_folder(pth):
    # find folder in path
    for root, dirs, files in os.walk(pth, topdown=False):
        for name in files:
            # create full name file
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            # and remove him
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    # and remove empty folder
    os.rmdir(pth)


# The method return file size in directory
# path - directory with files
def get_size_file_in_direct(path):
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size


# The method checks if there is space in the folder and max size all files
# path - path to the folder you want to check
# size_project - max size project
# storage_size - size cloud
# max_file_number - max number file in directory
def check_max_size_and_max_number(path, size_project, storage_size, max_file_number):

    print("-- size project = " + str(float(size_project) / 10 ** 6))
    print("-- size storage = " + str(float(storage_size) / 10 ** 6))
    add_info_in_log("-- size project = " + str(float(size_project) / 10 ** 6))
    add_info_in_log("-- size project = " + str(float(size_project) / 10 ** 6))

    if int(size_project) > int(storage_size):
        raise NameError("ERROR!!! size project more storage size : size project -" + size_project + " size storage - " \
                        + str(storage_size))
    if storage_size != 0 and max_file_number != 0:
        # check max files number
        file_number = int(__get_number_file_in_direct(path))

        print("-- file number = " + str(file_number))
        add_info_in_log("-- file number = " + str(file_number))

        if int(file_number) >= int(max_file_number):
            # delete last file
            __delete_file_with_last_time(path)
            # recursively check again the maximum size and number of files
            check_max_size_and_max_number(path, size_project, storage_size, max_file_number)
        else:
            # check max files size
            size_file = int(get_size_file_in_direct(path))

            print("-- file size = " + str(float(size_file) / 10 ** 6))
            add_info_in_log("-- file size = " + str(float(size_file) / 10 ** 6))

            if size_file >= int(storage_size):
                # delete last file
                __delete_file_with_last_time(path)
                # recursively check again the maximum size and number of files
                check_max_size_and_max_number(path, size_project, storage_size, max_file_number)
    else:
        raise NameError("ERROR!! check max_file_number and max_files_size attributes in config file")


# The method return number of file in directory with .backup.zip expansion
# - path where files are counter
def __get_number_file_in_direct(path):
    # find folder in directory
    if os.path.exists(path):
        # get file with .backup.zip expansion
        files = os.listdir(path)
        backup_files = list(filter(lambda x: x.endswith('.backup.zip'), files))
        return len(backup_files)
    else:
        raise NameError("ERROR!!! Do not find path directory - check config file")


# Delete the last file with .backup.zip expansion in directory
# path - directory wherein delete file
def __delete_file_with_last_time(path):
    # get file with .backup.zip expansion
    files = os.listdir(path)
    backup_files = filter(lambda x: x.endswith('.backup.zip'), files)

    # check file time
    file_time = sys.maxsize
    file_name = ''
    for file in backup_files:
        # get the oldest file
        if os.path.getctime(path + "\\" + file) < file_time:
            file_time = os.path.getctime(path + "\\" + file)
            file_name = file
    # delete last file
    os.remove(path + "\\" + file_name)


# Add info in log file
def add_info_in_log(info):
    f = open("log_" + str(os.getpid()) + ".txt", "a")
    f.write(info + "\n")
    f.close()