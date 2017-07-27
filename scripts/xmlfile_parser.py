import xml.etree.ElementTree as ET
import sys
import os


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
                # check for the correctness of the config file
                __check_config_file(repository_dict)
        return repository_list
    except ET.ParseError as e:
        print("ERROR!!! " + str(e) + "\n check config file")
        sys.exit(1)


# The method check spelling config file
# set_repository - dict with info about repository
def __check_config_file(set_repository):
    for keys_repo_set in set_repository.keys():
        if str(set_repository.get(keys_repo_set)) == "None":
            print("ERROR!!! " + keys_repo_set + " can't be NULL")
            sys.exit(1)
        if "url" != keys_repo_set and "cloud_directory" != keys_repo_set and "cloning_directory" != keys_repo_set \
                and "config_name" != keys_repo_set:
            print("ERROR!!! " + str(keys_repo_set) + " check spelling")
            sys.exit(1)


# The method get all slack config
def get_slack_config(config_file_name):
    try:
        # pars file config
        tree = ET.parse(config_file_name)
        root = tree.getroot()
        # get slack param
        for repository in root:
            if repository.tag == "slack":
                slack_dict = dict()
                for attribute in repository:
                    slack_dict[attribute.tag] = attribute.text
                return slack_dict
    except ET.ParseError as e:
        print("ERROR!!! " + str(e) + "\n check slack config file")
        sys.exit(1)


# return param max size of config file
def get_max_size(config_file_name):
    # pars file config
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
            if param.text[:-2].isdigit():
                storage_size = int(param.text[:-2])  # All symbols except the last two
            else:
                raise NameError("ERROR!!! storage size error, check config file")
            if param.text[-2:].isalpha():
                size_expansion = __get_max_size_expansion(param.text[-2:])  # Last two characters
            else:
                raise NameError("ERROR!!! size_expansion error, check config file")
    dict_max_size = {"storage_size": storage_size * (1000 ** (size_expansion + 1)), "max_file_number": max_file_number}
    return dict_max_size


# The method return true if process unique and false if not unique
# url - address repository
def check_list_pids(url):
    list_pids = __get_list_pids()
    if len(list_pids) == 0:
        return True

    for pid in list_pids:
        if pid['url'] != url:
            return True
        else:
            return False


# The method return information about PID all scripts
def __get_list_pids():
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


def __get_max_size_expansion(key_expansion):
    key = key_expansion.lower()
    if key == 'mb':
        return 1
    elif key == 'gb':
        return 2
    elif key == 'tb':
        return 3
    else:
        raise NameError("ERROR!!! Unknown expansion of the maximum value of the cloud directory")
