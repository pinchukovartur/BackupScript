import sys
import argparse


# the method return console parameters
def get_console_param():
    # read console parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('g', nargs='?', default='')
    parser.add_argument('c', nargs='?', default='* * * * *')
    parser.add_argument('s', nargs='?', default='')
    name_space = parser.parse_args(sys.argv[1:])
    # create dict
    parameters = {"config_name": name_space.g, "cron_cmd": name_space.c, "config_slack": name_space.s}
    return parameters
