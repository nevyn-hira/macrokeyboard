from pynput.keyboard import Key, Controller as keyboardController
import sys
import shlex
import subprocess
import magic
from wmctrl import Window
import pyperclip
import notify2 as notify

class Actioner:
    def __init__( self ):
        self.keyboardcontroller = keyboardController()
    def populateMimeLists(self, mimelists):
        self.mimelists = mimelists
        print(self.mimelists)

    def setNotifications( self ):
        self.launchnotifications = True
        notify.init("Macro Keyboard")

    def action( self, actioninfo ):
        action = actioninfo['action']
        if action == 'switchto':
            if( self.switchTo(
                actioninfo['classname'],
                actioninfo['executable'] )):
                if( self.launchnotifications ):
                    n = notify.Notification("Launching", str(actioninfo['executable']), "notification-message-im")
                    n.show()
                    
        elif action == 'XF86Symbol':
            self.pressXF86Symbol(
                actioninfo['symbol'] )
        elif action == 'unicode':
            self.typeUnicodeSymbol(
                actioninfo['code'] )
        elif action == 'quit':
            sys.exit(0)
        elif action == 'type':
            self.type(
                actioninfo['content'] )
        elif action == 'run':
            if 'parameters' in actioninfo:
                parameters = actioninfo['parameters']
            else:
                parameters = []
            self.execute(actioninfo['executable'],parameters)
        elif action == "gotolocation":
            self.gotoLocation( actioninfo['location'] )
        elif action == "keysequence":
            self.keySequence( actioninfo['sequence'] )
            return(action)
        elif action == "altopen":
            self.openAlt(actioninfo["mimelist"])

    def openAlt(self, mimelist):
        list = self.mimelists[mimelist]
        self.execute("xdotool","key ctrl+c")
        files = pyperclip.paste().split("\n")
        for file in files:
            fmimetype = magic.from_file( file, mime=True )
            if fmimetype in self.mimelists[mimelist]:
                subprocess.call(['gtk-launch',self.mimelists[mimelist][fmimetype],file])
            else:
                print(fmimetype)

    def keySequence(self, sequence):
        items = sequence.split('|')
        for item in items:
            i = item.split('+')
            pressList = []
            if len(i)>1:
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
        if(parameters):
            subprocess.call([executable] + shlex.split(parameters))
        else:
            subprocess.call([executable])

    def pressXF86Symbol(self, symbol):
        self.execute('xdotool','key ' + symbol)

    def typeUnicodeSymbol( self, code ):
        self.keySequence('Key.ctrl+Key.shift+u|'+str(code)+"|Key.enter")

    def switchTo( self, classname, command ):
        for window in Window.list():
            if( window.wm_class == classname ):
                window.activate()
        if (Window.get_active()):
            if( Window.get_active().wm_class != classname ):
                subprocess.Popen( command )
                return True
        return False

    def type( self, content ):
        self.keyboardcontroller.type(str(content))

    def gotoLocation( self, location ):
        self.keySequence('Key.ctrl+l|'+location+'|Key.enter')

