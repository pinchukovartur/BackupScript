# coding: utf8
# @author Pinchukov Artur
# The script downloads projects from the githab, archives them and sends them to the cloud
import argparse
import datetime
import os
import stat
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
#from slackclient import SlackClient
import slack
import slack.chat



# Main brain script
def main():
    list_repositories = get_all_repository()
    for set_repository in list_repositories:
        # checks the presence of the specified path
        print('checks folder')
        while True:
            if os.path.exists(set_repository['cloning_directory']) and os.path.exists(
                    set_repository['cloud_directory']):
                print("successful check")
                print("check list pid")
                if check_list_pids(set_repository['repository_name'], set_repository['username'],
                                   set_repository['branch']):
                    print("successful check")
                    try:
                        print("create pid file")
                        create_pid_file(set_repository['repository_name'], set_repository['username'],
                                    set_repository['branch'])
                        print("successful create")
                        print("download repository")

                        repository_url = 'https://github.com/' + set_repository['username'] + '/' \
                                     + set_repository['repository_name'] + '.git -b ' + set_repository['branch']

                        download_repository(repository_url, set_repository['cloning_directory'])
                        print("successful download")

                        print("check max size files and number")
                        check_max_size_and_max_number(set_repository['cloud_directory'])
                        print("successful check")

                        print("archived project")
                        archiving_folder(set_repository['cloning_directory'] + "\\" + set_repository['repository_name'],
                                     set_repository['cloud_directory'])
                        print("successful archived")

                        print("delete time folder")
                        delete_folder(set_repository['cloning_directory'] + "//" + set_repository['repository_name'])
                        print("successful deleted")
                        print(os.getpid())
                    except Exception as e:
                        print(e)
                    finally:
                        print("delete lock file")
                        os.remove(str(os.getpid()) + ".lock")
                        print("successful deleted")
                        print("sleep 10 sec")

                    send_message_in_slack(set_repository['repository_name'] + "has be cloned", "#general", "Backup "
                                                                                                           "System")
                    time.sleep(10)
                else:
                    print("The process already in use")
                    time.sleep(10)
            else:
                print("Folder not exist")
                break


# The method archives the specified folder
# path_folder - where is the folder to be archived
# path_made_archive - the path where the archive will be saved
def archiving_folder(path_folder, path_made_archive):
    full_archive_name = path_made_archive + datetime.datetime.now().strftime(
        " %d %m %Y %H %M %S") + '.backup.zip'
    # create zip file in directory
    arch = zipfile.ZipFile(full_archive_name, 'w', zipfile.ZIP_DEFLATED)
    # add file in zip file
    for root, dirs, files in os.walk(path_folder):
        for tarfile in files:
            if tarfile != '':
                print(tarfile)
                arch.write(root + '\\' + tarfile)
    arch.close()


# The method that downloads projects with github
# repository_url - network address of the repository
# file_path - the path where the project will be cloned
def download_repository(repository_url, file_path):
    # checks the presence of the specified path
    if os.path.exists(file_path):
        try:
            # arguments passed to run function
            comand = "cd /D  \"" + file_path + "\" && git clone " + repository_url
            # run process cloning repository
            subprocess.run(comand, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(e)
    else:
        print('The directory does not exist')


# The method get all repository information of config.xml
def get_all_repository():
    repository_list = list()
    tree = ET.parse(get_console_param())
    root = tree.getroot()
    print("reed config file")
    for repository in root:
        if repository.tag == "repository":
            repository_dict = dict()
            for attribute in repository:
                repository_dict[attribute.tag] = attribute.text
            repository_list.append(repository_dict)
    return repository_list


# The method return console parameter(config name)
def get_console_param():
    print("get config file")
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default='config.xml')
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.name


# Add info in log file
# inform - information to be saved
def add_info_in_log(inform):
    f = open("log.txt", 'a')
    f.write(inform + '\n')
    f.close


# Delete folder
# pth - path to folder
def delete_folder(pth):
    for root, dirs, files in os.walk(pth, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(pth)


# The method return information about PID all scripts
def _get_list_pids():
    list_pids = list()
    files = os.listdir('.')
    pid_files = filter(lambda x: x.endswith('.lock'), files)
    for file_name in pid_files:
        tree = ET.parse(file_name)
        root = tree.getroot()
        pid_dict = dict()
        for pid in root:
            for attribute in pid:
                pid_dict[attribute.tag] = attribute.text
        list_pids.append(pid_dict)
    return list_pids


# The method return true if process unique and false if not unique
# repository_name - check this repository in pid files
# username - check this username in pid files
# branch - check this branch in pid files
def check_list_pids(repository_name, username, branch):
    list_pids = _get_list_pids()
    if len(list_pids) == 0:
        return True
    for pid in list_pids:
        if pid['repository_name'] != repository_name or pid['username'] != username or pid['branch'] != branch:
            return True
        else:
            return False


# The method create file with pid info
# repository_name - save this repository info in pid files
# username - save this username info in pid files
# branch - save this branch info in pid files
def create_pid_file(repository_name, username, branch):
    f = open(str(os.getpid()) + ".lock", 'w')
    text = '<?xml version="1.0"?>\n<data>\n<process>\n<repository_name>' + repository_name + \
           '</repository_name>\n<username>' + username + '</username>\n<branch>' + branch + \
           '</branch>\n</process>\n</data>'
    f.write(text)
    f.close


# The method checks if there is space in the folder and max size all files
# path - path to the folder you want to check
def check_max_size_and_max_number(path):
    # parsing config file
    tree = ET.parse(get_console_param())
    root = tree.getroot()

    max_file_number = 0
    max_files_size = 0

    # set param value of config file
    for param in root:
        if param.tag == 'max_file_number':
            max_file_number = int(param.text)
        elif param.tag == 'max_files_size':
            max_files_size = int(param.text)

    if max_files_size != 0 and max_file_number != 0:
        # check max files number
        print(_get_size_file_in_direct(path))
        print(int(max_files_size) * 1024 * 1024)
        if _get_number_file_in_direct(path) >= max_file_number:
            print("File need delete (max_file_number > files in directory)")
            # delete last file
            _delete_file_with_last_time(path)
            # recursively check again the maximum size and number of files
            check_max_size_and_max_number(path)
        else:
            # check max files size
            if int(_get_size_file_in_direct(path)) >= int(max_files_size) * 1024 * 1024:  # byte in megabyte
                print("File need delete (max_file_number > files in directory)")
                # delete last file
                _delete_file_with_last_time(path)
                # recursively check again the maximum size and number of files
                check_max_size_and_max_number(path)
            else:
                return True
    else:
        print("Check config file")


# The method return file size in directory with .backup.zip expansion
# path - directory with files
def _get_size_file_in_direct(path):
    files_in_direct = os.listdir(path)
    backup_files = filter(lambda x: x.endswith('.backup.zip'), files_in_direct)
    size = 0
    for file in backup_files:
        if os.path.isfile(path + file):
            size += os.path.getsize(path + file)
    return size


# The method return number of file in directory with .backup.zip expansion
# - path where files are counter
def _get_number_file_in_direct(path):
    # get file with .backup.zip expansion
    files = os.listdir(path)
    backup_files = list(filter(lambda x: x.endswith('.backup.zip'), files))
    return len(backup_files)


# Delete the last file with .backup.zip expansion in directory
# path - directory wherein delete file
def _delete_file_with_last_time(path):
    # get file with .backup.zip expansion
    files = os.listdir(path)
    backup_files = filter(lambda x: x.endswith('.backup.zip'), files)

    # check file time
    file_time = 99 ** 99  # ГОВНА КОД ///////////////////////////////////////////////////////////////////////////////////////////////////
    file_name = ''
    for file in backup_files:
        # get the oldest file
        if os.path.getctime(path + "\\" + file) < file_time:
            file_time = os.path.getctime(path + "\\" + file)
            file_name = file
    # delete last file
    os.remove(path + "\\" + file_name)


# Sends a specific message to the slack
# message - message that is sent
# chanel - chanel to which the message will be sent
# username - the name of the message
def send_message_in_slack(message, chanel, username):
    slack.api_token = 'xoxp-217741648471-216642605474-216713481444-5d766c5d73469c073366b979ee4e37d5'
    slack.chat.post_message(chanel, message, username=username)



main()
# download_repository("https://github.com/pinchukovartur/BackupSystem", "F:\\")
#archiving_folder("D:\\", "test_arch", "G:\\")
#send_message_in_slack("hello bot", "#general", "Backup bot")