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


# differentiating damage taken from damage received???
class Player():
    def __init__(self,hp,damage):
        self.hp = hp
        self.damage = damage
        self.inventory = []

        
    def game_over(self): #when player hp reaches 0, game ends 
        if self.hp == 0:
            print('you died! game over.')
            return True
        return False
    

    def take(self,item):#pick up items and put in inventory
            if item not in self.inventory:
                self.inventory.append(item)
    
    def attack(self,selection):
        if selection == 'attack':
            print('you attacked the monster.')
        return self.damage
    def damageReceived(self,d):
        self.hp = self.hp - d   #??????





# differentiating damage taken from damage received??? 
class Enemy():
    def __init__ (self, name, desc, hp, damage):
        self.name = name
        self.desc = desc
        self.hp = hp
        self.damage = damage
    def is_alive(self):
        return self.hp > 0
    def attack(self):
        return self.damage
    def damageReceived(self,d):    #?????
        self.hp -= d




# Game loop functions
def render(game,current,enemy):
    ''' Displays the current room, moves, and points '''
    r = game['rooms']
    c = r[current]
    n = c['enemy']
    print('\n\nyou are in the {name}.'.format(name=c['name']))
    print(c['desc'])
    
    if len(n): #print json stuff about enemy
        print('you see a monster. it looms above you, guarding a key.')
    
    if len(c['inventory']):
        print('you see the following items:')
        for i in c['inventory']:
            print('\t{i}'.format(i=i))





def getInput(game,current,verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list 
of commands '''
    selection = input('\nwhat would you like to do?').strip().lower().split()
    if (len(selection)):
        #assume the first word is the verb
        selection[0] = normalizeVerb(selection[0],verbs)
    return selection


def update(selection,game,current,player,enemy):
    ''' Process the input and update the state of the world '''


    s = list(selection)[0]  #We assume the verb is the first thing typed

    if s == 'take' and "key" in game['rooms'][current]['inventory']:
        game['rooms'][current]['inventory'] = []
        player.take("key")
        print('\n\nyou have picked up the key.')


    if s == 'take' and "weapon" in game['rooms'][current]['inventory']:
        game['rooms'][current]['inventory'] = []
        player.take("weapon")
        print('\n\nyou have picked up the weapon.')

    if s == 'attack' and "weapon" in game['rooms'][current]['inventory'] and "monster" in game['rooms'][current]['enemy']:
        enemy.damage(player.attack())
        player.damage(enemy.attack())
        print('you attack the monster.')

    
    
    if s == "":
        print("\nSorry, I don't understand.")
        return current
    elif s == 'exits':
        printExits(game,current)
        return current

    elif s== 'unlock':
        escape(selection,game,current, player)
        print('you escaped!')
        return selection

    else:
        for e in game['rooms'][current]['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']
    print("\nyou can't go that way!")

    return current


def escape(selection,game,current,player):
    r = selection
    if r =='unlock' and "key" in player.inventory():
        print('you escaped!')
        return True
    return False





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




#main game functions    
def main():
    gameFile = 'AVARICE.json'
    game = {'AVARICE'}
    with open(gameFile) as json_file:
        game = json.load(json_file)
    current = 'START'


    player = Player(100,10)
    enemy = Enemy("","",100, 10)



    while True:
        render(game,current,enemy)

        selection = getInput(game, current, game['verbs']) #player input

        if selection[0] == 'quit':
            break
        
        current = update(selection,game,current,player,enemy) #depends on current 
        
        if player.game_over():  
            break
        
        if escape(selection,game,current,player):
            break


#if we are running this from the command line, run main
if __name__ == '__main__':
	main()