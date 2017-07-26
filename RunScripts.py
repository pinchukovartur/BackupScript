# -*- coding: utf-8 -*-
from CloneScript import *
from ArchiveScript import *
from SlackScript import *
import argparse
import pycron

SLACK_CHANNEL = "#general"
SLACK_NAME = "Backup Bot"
SLACK_ICON = ":flag-by:"
SLACK_BLUE = "#0000FF"
SLACK_RED = "#FF4500"
SLACK_GREEN = "#00FF00"

# read console parameter
parser = argparse.ArgumentParser()
parser.add_argument('g', nargs='?', default='configs/config.xml')
parser.add_argument('c', nargs='?', default='*/32 * * * *')
config_file = parser.parse_args(sys.argv[1:])
cron_cmd = parser.parse_args(sys.argv[2:])

print(config_file.g)
print(cron_cmd.c)

while True:
    if pycron.is_now(cron_cmd.c.replace("_", " ")):
        # get list repository of config file
        list_repositories = get_all_repository(config_file.g)

        # work with all repository
        for set_repository in list_repositories:
            # check spelling repo data of config file
            check_config_file(set_repository)

            name_config = set_repository["config_name"]
            url = set_repository['url']
            cloning_directory = set_repository['cloning_directory']
            cloud_directory = set_repository['cloud_directory']

            send_message_in_slack(SLACK_CHANNEL, "Start clone " + name_config, "backup bot started...", SLACK_NAME,
                                  SLACK_ICON, SLACK_BLUE)

            print("\n CHECK list pid")
            if check_list_pids(url):

                print("\n CREATE pid file")
                create_pid_file(url)
                # CLONE REPOSITORY
                try:
                    print("\n DOWNLOAD repository")
                    file_name = name_config + "-" + str(os.getpid())
                    download_repository(url, cloning_directory + "\\" + file_name)
                    # CHECK SIZE AND NUMBER FILES
                    size_project = get_size_file_in_direct(cloning_directory + "\\" + file_name)
                    check_max_size_and_max_number(cloning_directory, size_project, config_file.g)
                except Exception as e:
                    print(e)
                    send_message_in_slack(SLACK_CHANNEL, "ERROR!!! clone repository " + name_config,
                                          "qwe", SLACK_NAME, SLACK_ICON, SLACK_RED)
                    sys.exit(1)
                finally:
                    print("DELETE lock file\n")
                    os.remove(str(os.getpid()) + ".lock")

                # ARCHIVE REPOSITORY
                try:
                    print("ARCHIVE repository\n")
                    archiving_folder(cloning_directory, file_name, cloud_directory)
                except Exception as e:
                    print(e)
                    send_message_in_slack(SLACK_CHANNEL, "ERROR!!! archived repository " + name_config,
                                          str(e), SLACK_NAME, SLACK_ICON, SLACK_RED)
                    sys.exit(2)
                finally:
                    print("DELETE folder\n")
                    delete_folder(cloning_directory + "\\" + file_name)

                send_message_in_slack(SLACK_CHANNEL, "Successful " + name_config,
                                      "Successful backup files", SLACK_NAME, SLACK_ICON, SLACK_GREEN)
            else:
                print("The process already in use")
