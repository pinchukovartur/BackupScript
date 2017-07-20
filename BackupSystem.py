# coding: utf8
# @author Pinchukov Artur
# The script downloads projects from the githab, archives them and sends them to the cloud
import subprocess, os, zipfile, datetime, shutil, argparse, sys, time, stat
import xml.etree.ElementTree as ET


# Main brain script
def main():
    list_repositories = get_all_repository()
    for set_repository in list_repositories:
        # checks the presence of the specified path
        add_info_in_log('checks folder')
        while True:
            if os.path.exists(set_repository['cloning_directory']):
                add_info_in_log("successful check")
                add_info_in_log("download repository")
                repository_url = 'https://github.com/' + set_repository['username'] + '/' \
                             + set_repository['repository_name'] + '.git -b ' + set_repository['branch']
                download_repository(repository_url, set_repository['cloning_directory'])
                archiving_folder(set_repository['cloning_directory'], set_repository['repository_name'],
                             set_repository['cloud_directory'])
                delete_folder(set_repository['cloning_directory'] + set_repository['repository_name'])
                print(os.getpid())
                time.sleep(5)


# The method archives the specified folder
# path_folder - where is the folder to be archived
# archive_name - name of the future archive
# path_made_archive - the path where the archive will be saved
def archiving_folder(path_folder, archive_name, path_made_archive):
    full_archive_name = path_made_archive + '/' + archive_name + datetime.datetime.now().strftime(" %d %m %Y %H %M") + '.zip'
    # create zip file in directory
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
def download_repository(repository_url, file_path):
    # checks the presence of the specified path
    if os.path.exists(file_path):
        try:
            # arguments passed to run function
            a = "cd /D  \"" + file_path + "\" && git clone " + repository_url
            # run process cloning repository
            subprocess.run(a, shell=True, check=True)
            add_info_in_log("successful downloads")
        except subprocess.CalledProcessError:
            add_info_in_log("There was an error when the script tried to clone the project - " + repository_url)
    else:
        add_info_in_log('The directory does not exist')


# The method get all repository information of config.xml
def get_all_repository():
    repository_list = list()
    tree = ET.parse(get_console_param())
    root = tree.getroot()
    add_info_in_log("reed config file")
    for repository in root:
        repository_dict = dict()
        for attribute in repository:
            repository_dict[attribute.tag] = attribute.text
        repository_list.append(repository_dict)
    return repository_list


# The method return console parameter(config name)
def get_console_param():
    add_info_in_log("get config file")
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

main()