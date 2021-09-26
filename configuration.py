import os
import sys
import json
from modifierkeys import Modifierkeys

class Configuration:
    def __init__( self, configFile ):
        self.keyIndex = {}
        self.config_file = configFile
        self.readConfiguration()
        self.keyIndex = {}

        for ikey in self.config['keys']:
            keys = ikey.split('+',1)
            if keys[0] not in self.keyIndex:
                self.keyIndex[keys[0]] = []
            self.keyIndex[keys[0]].append(self.config['keys'][ikey])
            if len(keys) > 1:
                self.keyIndex[keys[0]][len(self.keyIndex[keys[0]]) -1 ]["modifiers"] = keys[1]

    def find( self, key ):
        if key in self.keyIndex:
            return self.keyIndex[key]
        else:
            return False

    def readConfiguration( self ):
        self.config = []
        if not os.path.exists(self.config_file):
            sys.exit('Configuration file not found.')
            sys.exit(1)
        with open(self.config_file) as json_file:
            self.config = json.load(json_file)
        if( not 'device' in self.config ):
            sys.exit('No device defined.')
        else:
            for ikey in self.config['keys']:
                keys = ikey.split('+',1)
                if keys[0] not in self.keyIndex:
                    self.keyIndex[keys[0]] = []
                self.keyIndex[keys[0]].append(self.config['keys'][ikey])
                if len(keys) > 1:
                    self.keyIndex[keys[0]][len(self.keyIndex[keys[0]]) -1 ]["modifiers"] = keys[1]
            self.device = self.config['device']
            self.modifierkeys = Modifierkeys(self.config['modifier_keys'])