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
import slack
import slack.chat


# Main brain script
def main():
    # token slack messenger
    slack_token = 'xoxp-217741648471-216642605474-218678197590-5d0bb18202b703d2ac8e93d43ff4907b'
    # get list repository of config file
    list_repositories = get_all_repository()
    # work with all repository
    for set_repository in list_repositories:
        # check spelling repo data of config file
        check_config_file(set_repository)

        repository_name = set_repository["config_name"]
        url = set_repository['url']
        cloud_directory = set_repository['cloud_directory']
        cloning_directory = set_repository['cloning_directory']

        print("CHECK list pid\n")
        if check_list_pids(url):
            try:
                print("CREATE pid file\n")
                create_pid_file(url)

                print("DOWNLOAD repository\n")

                file_name = "\\" + repository_name + "-" + str(os.getpid())
                download_repository(url, cloning_directory + file_name)

                print("CHECK max size files and number\n")
                check_max_size_and_max_number(cloud_directory)

                print("ARCHIVED project\n")
                archiving_folder(cloning_directory + file_name, cloud_directory + repository_name)

                print("DELETE time folder\n")
                delete_folder(cloning_directory + file_name)

                print("DELETE lock file\n")
                os.remove(str(os.getpid()) + ".lock")
            except Exception as e:
                print(str(e))
            finally:
                print("SEND message\n")
                send_message_in_slack(url + " has be cloned", "#general", "backup bot", slack_token)

                print("SLEEP 10 sec\n")
                time.sleep(10)
        else:
            print("The process already in use")
            time.sleep(10)


# The method archives the specified folder
# path_folder - where is the folder to be archived
# path_made_archive - the path where the archive will be saved
def archiving_folder(path_folder, path_made_archive):
    full_archive_name = path_made_archive + datetime.datetime.now().strftime(
        " %d %m %Y %H %M %S") + '.backup.zip'
    # create zip file in directory
    print(full_archive_name)
    print(path_folder)
    print(path_made_archive)
    arch = zipfile.ZipFile(full_archive_name, 'w', zipfile.ZIP_DEFLATED)
    # add file in zip file
    for root, dirs, files in os.walk(path_folder):
        for tarfile in files:
            if tarfile != '':
                arch.write(root + '\\' + tarfile)
    arch.close()


# The method that downloads projects with github
# repository_url - network address of the repository
# file_path - the path where the project will be cloned
def download_repository(url, file_path):
    # create new process
    p = subprocess.Popen("git clone " + url + " " + file_path, shell=True,
                       stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print (line)
    p.communicate()
    # exit if process error
    if p.returncode != 0:
        print("ERROR!! download load repository, № err - " + str(p.returncode))
        sys.exit(p.returncode)
    else:
        print("good download repository - " + str(p.returncode))


# The method get all repository information of config.xml
def get_all_repository():
    repository_list = list()
    try:
        # pars file config
        tree = ET.parse(get_console_param())
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


# The method return console parameter(config name)
def get_console_param():
    # read console parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default='config.xml')
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.name


# Add info in log file
# inform - information to be saved
def add_info_in_log(inform):
    f = open("log_" + str(os.getpid()) + ".txt", 'a')
    f.write(inform + '\n')
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


# The method create file with pid info
# url - repository address
def create_pid_file(url):
    if url is not None:
        f = open(str(os.getpid()) + ".lock", 'w')
        text = '<?xml version="1.0"?>\n<data>\n<process>\n<url>' + url + \
               '</url>\n</process>\n</data>'
        f.write(text)
        f.close()


# The method checks if there is space in the folder and max size all files
# path - path to the folder you want to check
def check_max_size_and_max_number(path):
    # parsing config file
    tree = ET.parse(get_console_param())
    root = tree.getroot()

    max_file_number = 0
    max_files_size = 0
    size_expansion = 0

    # set param value of config file
    for param in root:
        if param.tag == 'max_file_number' and str(param.text) != "None":
            max_file_number = int(param.text)
        elif param.tag == 'max_files_size' and str(param.text) != "None":
            max_files_size = int(param.text)
        elif param.tag == 'size_expansion' and str(param.text) != "None":
            size_expansion = int(param.text)

    if max_files_size != 0 and max_file_number != 0 and 4 > size_expansion != 0:
        # check max files number
        if _get_number_file_in_direct(path) >= max_file_number:
            # delete last file
            _delete_file_with_last_time(path)
            # recursively check again the maximum size and number of files
            check_max_size_and_max_number(path)
        else:
            # check max files size
            if int(_get_size_file_in_direct(path)) >= int(max_files_size) * (1024**(size_expansion+1)):
                # delete last file
                _delete_file_with_last_time(path)
                # recursively check again the maximum size and number of files
                check_max_size_and_max_number(path)
    else:
        print("Warning!! check max_file_number and max_files_size attributes in config file")


# The method return file size in directory with .backup.zip expansion
# path - directory with files
def _get_size_file_in_direct(path):
    # get file in directory
    files_in_direct = os.listdir(path)
    # sort this files
    backup_files = filter(lambda x: x.endswith('.backup.zip'), files_in_direct)
    size = 0
    # and count their
    for file in backup_files:
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


# Sends a specific message to the slack
# message - message that is sent
# chanel - chanel to which the message will be sent
# username - the name of the message
def send_message_in_slack(message, chanel, username, slack_token):
    slack.chat.post_message(chanel, message, token=slack_token, username=username, icon_emoji=':robot_face:')


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


main()
