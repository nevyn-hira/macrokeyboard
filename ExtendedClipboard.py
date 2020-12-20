#!/usr/bin/env python3

# from pynput.keyboard import Key, Controller as keyboardController
import pyperclip
#from pathlib import Path

class Clipboard:
    def __init__( self ):
        self.buffer = {}

    def get( self, buff_id ):
        if buff_id in self.buffer:
            pyperclip.copy(self.buffer[buff_id])

    def put( self, buff_id ):
        self.buffer[buff_id] = pyperclip.paste()

    def saveClipboard( self ):
        self.put('.clipboard')

    def restoreClipboard( self ):
        self.get('.clipboard')

    # def copy(self, id, data):
    #     self._saveClipboard()
    #     pyperclip.copy(data)
    #     self._put(id)
    #     self._restoreClipboard()


if __name__ == "__main__":
    #test code...
    clipboard = Clipboard()
    # clipboard.copy('test','This is the data that never ends')
    print(clipboard.buffer)
    print(pyperclip.paste())