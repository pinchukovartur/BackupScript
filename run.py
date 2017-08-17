# -*- coding: utf-8 -*-
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

# if config file null, return user help
if config_name == "":
    print(open("README.md").read())
    exit(1)

print("start script every " + cron_cmd)

while True:
    # start cron script
    if pycron.is_now(cron_cmd.replace("_", " ")):

        print("CHECK Console param")

        check_file(config_name, create_exception=True)
        if config_slack != "":
            check_file(config_slack, create_exception=True)
            print("GET Slack config")

            slack_config = get_slack_config(config_slack)
            slack_url = slack_config["url"]
            slack_channel = slack_config["channel"]
            slack_username = slack_config["username"]
            icon_name = slack_config["icon_name"]

        print("GET List repository of config file")
        list_repositories = get_all_repository(config_name)

        for set_repository in list_repositories:

            print("GET Param from config file")

            name_config = set_repository["config_name"]
            url_repository = set_repository['url']
            cloning_directory = set_repository['cloning_directory']
            cloud_directory = set_repository['cloud_directory']

            # check directory in config
            check_folder(cloning_directory, create_exception=True)
            check_folder(cloud_directory, create_exception=True)

            print("SEND Slack message - start clone")

            if config_slack != "":
                slack_header = "Start cloning of the project - " + name_config
                slack_message = "Time to start the script - " + \
                                str(datetime.datetime.now().strftime(" %d-%m-%Y %H_%M_%S"))
                print(slack_header)
                print(slack_message)
                send_message_in_slack(slack_url, slack_channel, slack_header, slack_message,
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
                    archive_name = archiving_folder(cloning_directory, name_config, temporary_name)

                    print("CHECK SIZE AND NUMBER FILES")

                    project_size = os.path.getsize(cloning_directory + "\\" + archive_name)

                    max_size = get_max_size(parameters_console["config_name"])

                    check_max_size_and_max_number(cloud_directory, project_size, max_size["storage_size"],
                                                  max_size["max_file_number"])
                    print("MOVE archive")
                    if cloning_directory + "\\" + archive_name != cloud_directory + "\\" + archive_name:
                        shutil.copy(cloning_directory + "\\" + archive_name, cloud_directory)
                except Exception as e:
                    print(e)

                    if config_slack != "":
                        slack_header = "An ERROR occurred while running the script"
                        send_message_in_slack(slack_url, slack_channel, slack_header, str(e), slack_username, icon_name, SLACK_RED)
                    sys.exit(1)
                finally:
                    # if lock file exist delete him
                    if check_file(str(os.getpid()) + ".lock"):
                        os.remove(str(os.getpid()) + ".lock")
                    # if cloned project folder exist delete her
                    if check_folder(cloning_directory + "\\" + temporary_name):
                        delete_folder(cloning_directory + "\\" + temporary_name)
                    if cloning_directory + "\\" + archive_name != cloud_directory + "\\" + archive_name:
                        if check_file(cloning_directory + "\\" + archive_name):
                            os.remove(cloning_directory + "\\" + archive_name)

                # If the script has successfully worked, then delete the log file
                if check_file("log_" + str(os.getpid()) + ".txt"):
                    os.remove("log_" + str(os.getpid()) + ".txt")

                if config_slack != "":
                    slack_header = "The project " + name_config + " was successfully cloned"
                    slack_message = "Time to end the script - " + str(
                        datetime.datetime.now().strftime(" %d-%m-%Y %H_%M_%S"))
                    send_message_in_slack(slack_url, slack_channel, slack_header,
                                          slack_message, slack_username, icon_name, SLACK_GREEN)
            else:
                print("The process already in use")

        print("WAIT one minute")
        time.sleep(60)  # wait one minute, so that there is no re-cloning if the repository is very small
