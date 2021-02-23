from pypresence import Presence
import time
import json
import requests
import webbrowser
import os
import sys

class log:
    def error(text: str):
        print('[Error] {}\nPlease report this error on the Switchence GitHub issue page if this error happens consistently'.format(text))
        time.sleep(3)
        webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
        time.sleep(10)
        sys.exit()

version = None
if os.path.isfile('version.txt') == True:
    with open('version.txt', 'r') as vf:
        version = vf.read()
elif os.path.isfile('version.txt') == False:
    try:
        with open('version.txt', 'a'):
            pass
    except:
        log.error('Couldn\'t create version file')
else:
    log.error('Couldn\'t search for a file')
    time.sleep(2)
    webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
    time.sleep(10)
    sys.exit()

sw = ''
if os.path.isfile('sw-code.txt') == True:
    with open('sw-code.txt', 'r') as swc:
        sw = swc.read()
elif os.path.isfile('sw-code.txt') == False:
    try:
        with open('sw-code.txt', 'a'):
            pass
    except:
        log.error('Couldn\'t create sw-code file')
else:
    log.error('Couldn\'t search for a file')
    time.sleep(2)
    webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
    time.sleep(10)
    sys.exit()

game = ''
gamenames = []
gamefnames = []
chosenOne = ''
img = ''
fname = ''
try:
    gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json') # auto update list :)
    gamejsontext = gamejson.text
    games = json.loads(gamejsontext)
except:
    log.error('Couldn\'t load game list')
oVersion = games['version']

print("""
 .d8888b.                d8b 888             888                                          
d88P  Y88b               Y8P 888             888                                          
Y88b.                        888             888                                          
 "Y888b.   888  888  888 888 888888  .d8888b 88888b.   .d88b.  88888b.   .d8888b  .d88b.  
    "Y88b. 888  888  888 888 888    d88P"    888 "88b d8P  Y8b 888 "88b d88P"    d8P  Y8b 
      "888 888  888  888 888 888    888      888  888 88888888 888  888 888      88888888 
Y88b  d88P Y88b 888 d88P 888 Y88b.  Y88b.    888  888 Y8b.     888  888 Y88b.    Y8b.     
 "Y8888P"   "Y8888888P"  888  "Y888  "Y8888P 888  888  "Y8888  888  888  "Y8888P  "Y8888    
\n""")

if version == '' or version == None: # gets current version. if your current version doesn't equal the version online, it tells you that you can update your software and opens up the github page
    try:
        with open('version.txt', 'a') as vfile:
            vfile.write(oVersion)
    except:
        log.error('Couldn\'t write to the version file')
elif version != oVersion:
    print('Your current version of Switchence (v{}) is not up to date. You can update Switchence to the current version (v{}) on the official GitHub page or continue using the program as usual.\n'.format(version, oVersion))
    time.sleep(2)
    webbrowser.open('https://github.com/Aethese/Switchence', new=2, autoraise=True)
    time.sleep(3)

try:
    for details in games['games']:
        gamenames.append(details['name'])
        gamefnames.append(details['fname'])
except:
    log.error('Couldn\'t load game names from list')

id = '803309090696724554'
try:
    RPC = Presence(id)
    RPC.connect()
except:
    log.error('RPC couldn\'t connect')

def changePresence(swStatus, pName, pImg, pFname):
    start_time = time.time()
    local = time.localtime()
    string = time.strftime("%H:%M", local)
    if swStatus == False:
        try:
            RPC.update(large_image=pImg, large_text=pFname, details=pFname, start=start_time)
            print('Set game to {} at {}'.format(pFname, string))
        except:
            log.error('Couldn\'t set RPC to {} (1)'.format(pName))
    elif swStatus == True:
        try:
            RPC.update(large_image=pImg, large_text=pFname, details=pFname, state='SW-{}'.format(sw), start=start_time)
            print('Set game to {} at {} with friend code "SW-{}" showing'.format(pFname, string, sw))
        except:
            log.error('Couldn\'t set RPC to {} (2)'.format(pName))
    else:
        print('An error occured getting friend code status. If this error persists please create an issue on the Github page stating the issue and how you got to said issue')
        time.sleep(3)
        webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
        sys.exit()

print('Here are the current games: ')
print(', '.join(gamenames))
x = input('\nWhat game do you wanna play? ')
x = x.lower()

if x == 'help' or x == 'h': # help command to see full name of lists
    print('\nHere are the full name for the games specified above: ')
    print(', '.join(gamefnames))
    print('\nPlease rerun the program to select a game') # this is stupid, i need to redo all of the code lmao
    time.sleep(5)
    sys.exit()
elif x == 'github' or x == 'gh':
    print('i mean i guess')
    time.sleep(2)
    webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
    sys.exit()

y = input('Do you want to show your friend code "SW-{}" (you can change this by typing "change")? '.format(sw))
y = y.lower()

if y == 'yes' or y == 'y':
    if sw == '' or sw == None:
        print('Friend code not set. Rerun the program and change your friend code to your friend code')
        time.sleep(5)
        sys.exit()
elif y == 'change' or y == 'c':
    c = input('What is your new friend code (just type the numbers)? ')
    b = input('Is "SW-{}" correct? '.format(c))
    b = b.lower()
    if b == 'yes' or b == 'y':
        try:
            with open('sw-code.txt', 'w') as file:
                file.write(c)
            sw = c
            print('Friend code changed to SW-{}'.format(c))
            y = 'yes'
        except:
            log.error('Couldn\'t change sw-code')
    else:
        print('Friend code not changed')

try:
    for n in games['games']: # really need a backup plan for when things don't work out because if you type in a game that doesn't exist, it'll search FOREVER lol
        z = n['name']
        if z == x:
            chosenOne = z
            break
except:
    log.error('Can\'t find the game ({}) the user specified (1)'.format(x))

try:
    for i in games['games']:
        if i['name'] == chosenOne:
            img = i['img']
            fname = i['fname']
            if y == 'yes' or y == 'y':
                changePresence(True, chosenOne, img, fname)
                break
            elif y == 'no' or y == 'n':
                changePresence(False, chosenOne, img, fname)
                break
            else:
                changePresence(False, chosenOne, img, fname)
                break
except:
    log.error('Can\'t find the game ({}) specified (2)'.format(chosenOne))

while 1: # trust me, we need this
    time.sleep(15)