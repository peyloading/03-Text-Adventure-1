import sys, logging, json

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def render(game,current):
    '''display the current location'''
    r = game['rooms']
    c = r[current]

    print('\n\nYou are in the {name}'.format(name=c['name']))
    print(c['desc'])
    return True

def update(response, game, current):
    '''update location if possible'''
    for e in game['rooms'][current]['exits']:
        if e ['verb'] == response:
            current = e['target']
    return current

def checkInput():
    '''get user input'''
    response = input('What would you like to do?') .upper() .strip()
    return response


def main():
    game = {}
    with open('zork.json') as json_file:
        game = json.load(json_file)
    # Your game goes here!

    current = 'LOC2'

    quit = False
    while not quit:
        render(game,current)
        response = checkInput()
        current = update(response, game, current)
        return True



#if we are running this from the command line, run main
if __name__ == '__main__':
	main()