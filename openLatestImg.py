#!/usr/bin/python3

import glob
import os
from Actioner import Actioner

pictures_folder = os.path.expanduser('~')+'/Pictures/'

listoffiles = glob.glob( pictures_folder + "Screenshot*")
latest_file = max(listoffiles, key=os.path.getctime)
actioner = Actioner()
actioner.gotoLocation(pictures_folder)
actioner.keySequence('Key.enter|Key.ctrl+l|' + latest_file)