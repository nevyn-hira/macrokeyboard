#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import subprocess
import shlex
import re

class KeyLocks:
    def __init__(self):
        self.disablecaps = False
        self.forcenum = False

    def execute(self, executable, parameters):
        if(parameters):
            subprocess.call([executable] + shlex.split(parameters))
        else:
            subprocess.call([executable])

    def DisableCaps(self):
        self.disablecaps = True
        if self.IsCaps():
            self.__ToggleCapsLock()


    def ForceNum(self):
        self.forcenum = True
        if not self.IsNum():
            self.__ToggleNumLock()

    def __ToggleNumLock( self ):
        self.execute('xdotool','key Num_Lock')

    def __ToggleCapsLock( self ):
        self.execute('xdotool','key Caps_Lock')

    def getXSetOutput(self):
        return subprocess.getoutput('xset -q')


    def IsCaps(self, xsetOutput=""):
        if xsetOutput=="":
            out = self.getXSetOutput()
        else:
            out = xsetOutput
        m = re.search("Caps Lock: *(off|on)",out)
        if m:
            if m[0].find('on') >= 0:
                return True
        return False

    def IsNum(self, xsetOutput=""):
        if xsetOutput=="":
            out = self.getXSetOutput()
        else:
            out = xsetOutput
        m = re.search( 'Num Lock: *(off|on)', out )
        if m:
            if m[0].find('on') >= 0:
                return True
        return False
            
    def checkStates(self):
        out = self.getXSetOutput()
        if self.disablecaps and self.IsCaps(out):
            self.__ToggleCapsLock()
        if self.ForceNum and not self.IsNum(out):
            self.__ToggleNumLock()
