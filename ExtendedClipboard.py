#!/usr/bin/env python3

from pynput.keyboard import Key, Controller as keyboardController
import pyperclip
from pathlib import Path

class Clipboard:
    def __init__( self ):
        self.buffer = {}

    def get( self, id ):
        pyperclip.copy(self.buffer[id])

    def put( self, id ):
        self.buffer[id] = pyperclip.paste()

    def saveClipboard( self ):
        self.put('.clipboard')

    def restoreClipboard( self ):
        self.get('.clipboard')

    def buffers(self):
        print(self.buffer)

if __name__ == "__main__":
    #test code...
    clipboard = Clipboard()
    clipboard.saveClipboard()
    pyperclip.copy('Boo!')
    clipboard.restoreClipboard()
    print(pyperclip.paste())

    