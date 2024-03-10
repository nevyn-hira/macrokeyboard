from pynput.keyboard import Key, Controller as keyboardController
import sys
import shlex
import subprocess
import magic
import os
from wmctrl import Window
from pynotifier import Notification
import pyperclip

class Actioner:
    def __init__(self):
        self.keyboardcontroller = keyboardController()
        self.launchnotifications = False
        self.launchicon = os.path.dirname(os.path.realpath(__file__)) + '/launch.png'

    def populateMimeLists(self, mimelists):
        self.mimelists = mimelists

    def setNotifications(self):
        self.launchnotifications = True

    def action(self, actioninfo):
        action = actioninfo['action']
        if action == 'chain':
            if "chain" in action:
                for a in sorted(actioninfo['chain']):
                    self.action( actioninfo['chain'][a] )
        elif action == 'switchto':
            executable = ""
            if "executable" in actioninfo:
                executable = actioninfo['executable']
            if( self.switchTo( actioninfo['classname'], executable )):
                if( self.launchnotifications ):
                    try:
                        Notification(
                            title = 'Launching',
                            description = os.path.basename( actioninfo['executable'] ),
                            icon_path = self.launchicon,
                            duration = 2,
                            urgency = "normal"
                        ).send()
                    except:
                        pass
        elif action == 'XF86Symbol':
            self.pressXF86Symbol(
                actioninfo['symbol'])
        elif action == 'unicode':
            self.typeUnicodeSymbol(
                actioninfo['code'])
        elif action == 'type':
            self.type(
                actioninfo['content'])
        elif action == 'run':
            self.execute(
                actioninfo['executable'],
                actioninfo['parameters'] if 'parameters' in actioninfo else [])
        elif action == "gotolocation":
            self.gotoLocation(actioninfo['location'])
        elif action == "keysequence":
            self.keySequence(actioninfo['sequence'])
            return(action)
        elif action == "altopen":
            if "mimelist" in actioninfo:
                self.openAlt(actioninfo["mimelist"])
        elif action == "sendkeypress":
            current_window = Window.get_active().wm_class
            if not self.switchTo(actioninfo["classname"], ''):
                self.keySequence(actioninfo["keypress"])
                self.switchTo(current_window, '')
        elif action =="holdandrelease":
            if "state" in actioninfo:
                if actioninfo["state"] == "hold":
                    self.action( actioninfo["onhold"] )
                elif actioninfo["state"] == "release":
                    self.action( actioninfo["onrelease"] )

    def openAlt(self, mimelist):
        self.keySequence('Key.ctrl+c')
        files = pyperclip.paste().split("\n")
        for file in files:
            fmimetype = magic.from_file(file, mime=True)
            if fmimetype in self.mimelists[mimelist]:
                subprocess.call(['gtk-launch', 
                    self.mimelists[mimelist][fmimetype], file])
            else:
                print(fmimetype)

    def keySequence(self, sequence):
        items = sequence.split('|')
        for item in items:
            i = item.split('+')
            pressList = []
            if len(i) > 1:
                for u in i:
                    if u.startswith('Key.'):
                        self.keyboardcontroller.press(eval(u))
                        pressList.append(u)
                    else:
                        self.keyboardcontroller.type(u)
                for key in pressList:
                    self.keyboardcontroller.release(eval(key))
            else:
                i = i[0]
                if i.startswith('Key.'):
                    self.keyboardcontroller.press(eval(i))
                    pressList.append(i)
                else:
                    self.keyboardcontroller.type(i)
                for key in pressList:
                    self.keyboardcontroller.release(eval(key))


    def execute(self, executable, parameters):
        if executable.startswith('addon/'):
            executable = executable.replace('addon/',os.getcwd()+'/')
        if(parameters):
            subprocess.call([executable] + shlex.split(parameters))
        else:
            subprocess.call([executable])

    def pressXF86Symbol(self, symbol):
        self.execute('xdotool','key ' + symbol)

    def typeUnicodeSymbol(self, code):
        self.keySequence('Key.ctrl+Key.shift+u|'+str(code)+"|Key.enter")

    def switchTo(self, classname, command):
        windows = ''
        try:
            windows = Window.by_class( classname )
        except ValueError:
            print(Window.list())
        if len(windows) > 0:
            windows[0].activate()
        else:
            if command != "":
                subprocess.Popen( command )
                return True
        return False

    def type(self, content):
        self.keyboardcontroller.type(str(content))

    def gotoLocation(self, location):
        self.keySequence('Key.ctrl+l|'+location+'|Key.enter')