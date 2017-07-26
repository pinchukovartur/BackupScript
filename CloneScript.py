import os
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET


# The method that downloads projects with github
# repository_url - network address of the repository
# file_path - the path where the project will be cloned
def download_repository(url, file_path):
    # create new process
    p = subprocess.run("git clone " + url + " " + file_path, shell=True)
    # exit if process error
    if p.returncode != 0:
        raise NameError("ERROR!! git error number - " + str(p.returncode))
    else:
        print("good download repository - " + str(p.returncode))


# The method get all repository information of config.xml
def get_all_repository(config_file_name):
    repository_list = list()
    try:
        # pars file config
        tree = ET.parse(config_file_name)
        root = tree.getroot()
        # get repository param
        for repository in root:
            if repository.tag == "repository":
                repository_dict = dict()
                for attribute in repository:
                    repository_dict[attribute.tag] = attribute.text
                repository_list.append(repository_dict)
        return repository_list
    except ET.ParseError as e:
        print("ERROR!!! " + str(e) + "\n check config file")
        sys.exit(1)


# The method check spelling config file
# set_repository - dict with info about repository
def check_config_file(set_repository):
    for keys_repo_set in set_repository.keys():
        if str(set_repository.get(keys_repo_set)) == "None":
            print("ERROR!!! " + keys_repo_set + " can't be NULL")
            sys.exit(1)
        if "url" != keys_repo_set and "cloud_directory" != keys_repo_set and "cloning_directory" != keys_repo_set \
                and "config_name" != keys_repo_set:
            print("ERROR!!! " + str(keys_repo_set) + " check spelling")
            sys.exit(1)


# The method return true if process unique and false if not unique
# url - address repository
def check_list_pids(url):
    list_pids = _get_list_pids()
    if len(list_pids) == 0:
        return True

    for pid in list_pids:
        if pid['url'] != url:
            return True
        else:
            return False


# The method return information about PID all scripts
def _get_list_pids():
    list_pids = list()
    # get all files, where is project
    files = os.listdir('.')
    # sort there files
    pid_files = filter(lambda x: x.endswith('.lock'), files)
    # and get full data in them
    for file_name in pid_files:
        tree = ET.parse(file_name)
        root = tree.getroot()
        pid_dict = dict()
        for pid in root:
            for attribute in pid:
                pid_dict[attribute.tag] = attribute.text
        list_pids.append(pid_dict)
    return list_pids


# The method create file with pid info
# url - repository address
def create_pid_file(url):
    if url is not None:
        f = open(str(os.getpid()) + ".lock", 'w')
        text = '<?xml version="1.0"?>\n<data>\n<process>\n<url>' + url + \
               '</url>\n</process>\n</data>'
        f.write(text)
        f.close()


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


# The method checks if there is space in the folder and max size all files
# path - path to the folder you want to check
def check_max_size_and_max_number(path, size_project, config_file_name):
    # parsing config file
    tree = ET.parse(config_file_name)
    root = tree.getroot()

    max_file_number = 0
    storage_size = 0
    size_expansion = 0

    # set param value of config file
    for param in root:
        if param.tag == 'max_file_number' and str(param.text) != "None":
            max_file_number = int(param.text)
        elif param.tag == 'storage_size' and str(param.text) != "None":
            storage_size = int(param.text[:-2])  # All symbols except the last two
            size_expansion = get_max_size_expansion(param.text[-2:])  # Last two characters

    if size_project > storage_size:
        raise NameError("ERROR!!! size project more storage size")

    if storage_size != 0 and max_file_number != 0 and 4 > size_expansion != 0:
        # check max files number
        if _get_number_file_in_direct(path) >= max_file_number:
            # delete last file
            _delete_file_with_last_time(path)
            # recursively check again the maximum size and number of files
            check_max_size_and_max_number(path, size_project, config_file_name)
        else:
            # check max files size
            if int(get_size_file_in_direct(path)) >= int(storage_size) * (1024 ** (size_expansion + 1)):
                # delete last file
                _delete_file_with_last_time(path)
                # recursively check again the maximum size and number of files
                check_max_size_and_max_number(path, size_project, config_file_name)
    else:
        print("Warning!! check max_file_number and max_files_size attributes in config file")


def get_max_size_expansion(key_expansion):
    key = key_expansion.lower()
    if key == 'mb':
        return 1
    elif key == 'gb':
        return 2
    elif key == 'tb':
        return 3
    else:
        raise NameError("ERROR!!! Unknown expansion of the maximum value of the cloud directory")


# The method return file size in directory with .backup.zip expansion
# path - directory with files
def get_size_file_in_direct(path):
    # get file in directory
    files_in_direct = os.listdir(path)
    size = 0
    # and count their
    for file in files_in_direct:
        if os.path.isfile(path + file):
            size += os.path.getsize(path + file)
    return size


# The method return number of file in directory with .backup.zip expansion
# - path where files are counter
def _get_number_file_in_direct(path):
    # find folder in directory
    if os.path.exists(path):
        # get file with .backup.zip expansion
        files = os.listdir(path)
        backup_files = list(filter(lambda x: x.endswith('.backup.zip'), files))
        return len(backup_files)
    else:
        print("ERROR!!! Don't find path cloud directory")
        sys.exit(1)


# Delete the last file with .backup.zip expansion in directory
# path - directory wherein delete file
def _delete_file_with_last_time(path):
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
