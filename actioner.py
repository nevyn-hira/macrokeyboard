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
        elif action =='reload':
            return True
        elif action == 'type':
            self.type(
                actioninfo['content'] )
        elif action == 'run':
            if 'parameters' in actioninfo:
                parameters = actioninfo['parameters']
            else:
                parameters = []
            self.execute(actioninfo['executable'],parameters)
        return False

    def execute(self, executable, parameters):
        if(parameters):
            subprocess.call([executable] + shlex.split(parameters))
        else:
            subprocess.call([executable])

    def pressXF86Symbol(self, symbol):
        self.execute('xdotool','key ' + symbol)
        # subprocess.call(['xdotool','key',symbol])

    def typeUnicodeSymbol( self, code ):
        self.keyboardcontroller.press(Key.ctrl)
        self.keyboardcontroller.press(Key.shift)
        self.keyboardcontroller.press('u')
        self.keyboardcontroller.release(Key.shift)
        self.keyboardcontroller.release(Key.ctrl)
        self.keyboardcontroller.type(str(code)+' ')
    
    def switchTo( self, classname, command ):
        for window in Window.list():
            if( window.wm_class == classname ):
                window.activate()
        if (Window.get_active()):
            if( Window.get_active().wm_class != classname ):
                subprocess.Popen( command )
        
    def type( self, content ):
        self.keyboardcontroller.type(str(content))