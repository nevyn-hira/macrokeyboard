from pynput.keyboard import Key, Controller as keyboardController
import sys
import shlex
import subprocess
from wmctrl import Window

class Actioner:
    def __init__( self ):
        self.keyboardcontroller = keyboardController()

    def action( self, actioninfo ):
        action = actioninfo['action']
        if action == 'switchto':
            self.switchTo( 
                actioninfo['classname'],
                actioninfo['executable'] )
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
        
    def type( self, content ):
        self.keyboardcontroller.type(str(content))
    
    def gotoLocation( self, location ):
        self.keySequence('Key.ctrl+l|'+location+'|Key.enter')