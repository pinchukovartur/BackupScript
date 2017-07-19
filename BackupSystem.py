# -*- coding: utf8 -*-
# export PYTHONPATH=.
# @author Pinchukov Artur
# The script downloads projects from the githab, archives them and sends them to the cloud
import subprocess, os

from Modules import CloningFromTheRepository


def main():
    CloningFromTheRepository.ownload_repository('https://github.com/pinchukovartur/Fog-Of-War.git', 'D:\Projects\HeLSCRIPTS')