# -*- coding: utf-8 -*-
# from CloneScript import *
# from ArchiveScript import *
# from SlackScript import *
import shutil
import pycron
import time
from scripts.console_parser import *
from scripts.xmlfile_parser import *
from scripts.slack_controller import *
from scripts.file_controler import *
from scripts.repository_controller import *

# read console parameter
parameters_console = get_console_param()
cron_cmd = parameters_console["cron_cmd"]
config_name = parameters_console["config_name"]
config_slack = parameters_console["config_slack"]

while True:
    if pycron.is_now(cron_cmd):
        print("GET List repository of config file")
        list_repositories = get_all_repository(config_name)

        print("CHECK Console param")
        check_file(config_name, create_exception=True)
        check_file(config_slack, create_exception=True)

        for set_repository in list_repositories:

            print("GET Param from config file")
            name_config = set_repository["config_name"]
            url_repository = set_repository['url']
            cloning_directory = set_repository['cloning_directory']
            cloud_directory = set_repository['cloud_directory']

            print("GET Slack config")
            slack_config = get_slack_config(config_slack)
            slack_channel = slack_config["channel"]
            slack_username = slack_config["username"]
            icon_name = slack_config["icon_name"]

            print("SEND Slack message - start clone")
            send_message_in_slack(slack_channel, "bot has be started", "backup repository - " + name_config,
                                  slack_username, icon_name, SLACK_BLUE)

            print("CREATE temporary name - " + name_config + "-" + str(os.getpid()))
            temporary_name = name_config + "-" + str(os.getpid())

            if check_list_pids(url_repository):

                print("CREATE pid file")
                create_pid_file(url_repository)
                try:
                    print("DOWNLOAD repository")
                    download_repository(url_repository, cloning_directory + "\\" + temporary_name)

                    print("ARCHIVE repository")
                    archive_name = archiving_folder(cloning_directory, temporary_name)

                    print("CHECK SIZE AND NUMBER FILES")
                    project_size = os.path.getsize(cloning_directory + "\\" + archive_name)

                    max_size = get_max_size(parameters_console["config_name"])

                    check_max_size_and_max_number(cloud_directory, project_size, max_size["storage_size"],
                                                  max_size["max_file_number"])
                    print("MOVE archive")
                    shutil.copy(cloning_directory + "\\" + archive_name, cloud_directory)
                    print("final")
                except Exception as e:
                    print(e)
                    send_message_in_slack(slack_channel, "ERROR!!!", str(e), slack_username, icon_name, SLACK_RED)
                    sys.exit(1)
                finally:
                    # if log file exist delete him
                    if check_file(str(os.getpid()) + ".lock"):
                        os.remove(str(os.getpid()) + ".lock")
                    # if cloned project folder exist delete her
                    if check_folder(cloning_directory + "\\" + temporary_name):
                        delete_folder(cloning_directory + "\\" + temporary_name)
                    if check_file(cloning_directory + "\\" + archive_name):
                        os.remove(cloning_directory + "\\" + archive_name)

                send_message_in_slack(slack_channel, "good clone!!!", "good", slack_username, icon_name, SLACK_GREEN)
            else:
                print("The process already in use")

        print("WAIT one minute")
        time.sleep(60)  # wait one minute, so that there is no re-cloning if the repository is very small
