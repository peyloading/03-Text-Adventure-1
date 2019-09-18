#!/usr/bin/env python3
import sys, logging, os, json
import textwrap
import cmd
import time
from time import sleep



#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class player():
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage
    def is_alive(self):
        return self.hp > 0
class Item():
    ''' The base class for items'''
    def __init__ (self, name, desc):
        self.name = name
        self.desc = desc
    def __str__(self):
        return "{}\n{}".format(self.name,self.desc)

class weapon(Item):
    def __init__(self,name,desc,damage):
        self.damage = damage
        super().__init__ (name,desc)


class enemy():
    def __init__ (self, name, desc, hp, damage):
        self.name = name
        self.desc = desc
        self.hp = hp
        self.damage = damage
    def is_alive(self):
        return self.hp > 0

# Game loop functions
def render(game,current):
    ''' Displays the current room, moves, and points '''
    r = game['rooms']
    c = r[current]
    print('\n\nyou are in the {name}.'.format(name=c['name']))
    print(c['desc'])
    if len(c['inventory']):
        print('you see the following items:')
        for i in c['inventory']:
            print('\t{i}'.format(i=i))


def getInput(game,current,verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list 
of commands '''
    toReturn = input('\nwhat would you like to do?').strip().lower().split()
    if (len(toReturn)):
        #assume the first word is the verb
        toReturn[0] = normalizeVerb(toReturn[0],verbs)
    return toReturn


def update(selection,game,current,inventory):
    ''' Process the input and update the state of the world '''

    if selection == 'pick up key' and "key" in game['rooms'][current]["inventory"]:
        game['rooms'][current]['inventory'] = []
        inventory.append("key")

    s = list(selection)[0]  #We assume the verb is the first thing typed
    if s == "":
        print("\nSorry, I don't understand.")
        return current
    elif s == 'EXITS':
        printExits(game,current)
        return current
    else:
        for e in game['rooms'][current]['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']
    print("\nyou can't go that way!")
    
    return current


# Helper functions
def printExits(game,current):
    e = ", ".join(str(x['verb']) for x in game['rooms'][current]['exits'])
    print('\nyou can go the following directions: {directions}'.format(directions =
e))

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def escape(selection,inventory,game,current):
    if selection=='unlock' and "key" in game['rooms'][current]['inventory']:
        print('you escaped!')
        return 
        
def main():
    gameFile = 'AVARICE.json'
    game = {'AVARICE'}
    with open(gameFile) as json_file:
        game = json.load(json_file)
    current = 'START'


    inventory = []

    while True:
        render(game,current)

        selection = getInput(game,current,game['verbs'])
        if selection == 'quit':
            break
        
        current = update(selection,game,current,inventory)


#if we are running this from the command line, run main
if __name__ == '__main__':
	main()