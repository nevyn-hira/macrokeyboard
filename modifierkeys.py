class Modifierkey:
    def __init__( self, key ):
        self.key = key
        self.status = False

class Modifierkeys:
    def __init__( self, keys ):
        self.modifierkeys = []
        keys=keys.split(',')
        for key in keys:
            self.modifierkeys.append(Modifierkey(key))

    def findModifier( self, key ):
        for index, modifier in enumerate(self.modifierkeys):
            if modifier.key == key:
                return index
        return -1

    def keydown( self, key ):
        i = self.findModifier( key )
        if i != -1:
            self.modifierkeys[i].status = True
            return True
        return False

    def keyup( self, key ):
        i = self.findModifier( key )
        if i != -1:
            self.modifierkeys[i].status = False
            return True
        return False

    def isModifiers( self ):
        return any( x.status for x in self.modifierkeys )

    def checkmodifiers( self, keys ):
        for modifier in self.modifierkeys:
            if (modifier.key in keys) and (not modifier.status):
                return False
            elif (modifier.key not in keys) and modifier.status == True:
                return False
        return True