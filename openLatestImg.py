#!/usr/bin/python3

import glob
import os
from Actioner import Actioner

listoffiles = glob.glob(os.path.expanduser('~')+'/Pictures/Screenshot*')
latest_file = max(listoffiles, key=os.path.getctime)
