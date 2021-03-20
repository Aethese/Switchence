from pypresence import Presence
import time, json, requests, webbrowser, os, sys

class log:
    def error(text: str):
        clear()
        print('\n[Error] {}\nPlease report this error on the Switchence GitHub issue page if this error happens consistently'.format(text))
        time.sleep(5)
        webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
        time.sleep(600)
        sys.exit()

    def info(text: str):
        clear()
        print('[Info] {}\nThis program will now close in 1 minute'.format(text))
        time.sleep(60)
        sys.exit()
    
    def warning(text: str):
        print('\n[WARNING] {}\n'.format(text))

def clear():
    os.system('cls' if os.name =='nt' else 'clear')
clear()

id = '803309090696724554'
version = None
sw = None
updatenotifier = None
configfname = None
gamenames = []
gamefnames = []
chosenOne = ''
img = ''
fname = ''

if os.path.isfile('config.json') == True:
    try:
        with open('config.json', 'r') as jsonfile:
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                sw = details['sw-code']
                version = details['version']
                updatenotifier = details['update-notifier']
                configfname = details['fname']
    except Exception as error:
        log.error('Couldn\'t load config file (1) | {}'.format(error))
elif os.path.isfile('config.json') == False:
    try:
        configjson = {}
        configjson['config'] = [{
            "sw-code": "",
            "version": "1.1.2",
            "update-notifier": True,
            "fname": False
        }]
        with open('config.json', 'w') as jsonfile:
            json.dump(configjson, jsonfile, indent=4)
        with open('config.json', 'r') as jsonfile: # actually get the info lol
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                sw = details['sw-code']
                version = details['version']
                updatenotifier = details['update-notifier']
                configfname = details['fname']
    except Exception as error:
        log.error('Couldn\'t load config file (2) | {}'.format(error))
else:
    log.error('Couldn\'t load config settings | {}'.format(error))

try:
    gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json') # auto update list :)
    gamejsontext = gamejson.text
    games = json.loads(gamejsontext)
except Exception as error:
    log.error('Couldn\'t load game list | {}'.format(error))

oVersion = games['version']

print('''
 .d8888b.                d8b 888             888                                          
d88P  Y88b               Y8P 888             888                                          
Y88b.                        888             888                                          
 "Y888b.   888  888  888 888 888888  .d8888b 88888b.   .d88b.  88888b.   .d8888b  .d88b.  
    "Y88b. 888  888  888 888 888    d88P"    888 "88b d8P  Y8b 888 "88b d88P"    d8P  Y8b 
      "888 888  888  888 888 888    888      888  888 88888888 888  888 888      88888888 
Y88b  d88P Y88b 888 d88P 888 Y88b.  Y88b.    888  888 Y8b.     888  888 Y88b.    Y8b.     
 "Y8888P"   "Y8888888P"  888  "Y888  "Y8888P 888  888  "Y8888  888  888  "Y8888P  "Y8888    
Made by: Aethese#1337
''')

if version == '' or version == None: # checks your version
    try:
        with open('config.json', 'r') as jsonfile:
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                details['version'] = oVersion
        with open('config.json', 'w') as jsonfile:
            json.dump(jsonFile, jsonfile, indent=4)
    except Exception as error:
        log.error('Couldn\'t write to the version file | {}'.format(error))
elif version != oVersion:
    if updatenotifier == True:
        print('Your current version of Switchence (v{}) is not up to date'.format(version))
        print('You can update Switchence to the current version (v{}) on the official GitHub page or continue using the program as usual'.format(oVersion))
        print('If you wish to turn off update notifications, type \'update notifier\' in the game selection input\n')
        time.sleep(2)
        webbrowser.open('https://github.com/Aethese/Switchence', new=2, autoraise=True)
        time.sleep(3)
    else:
        pass

try:
    for details in games['games']:
        gamenames.append(details['name'])
        gamefnames.append(details['fname'])
except Exception as error:
    log.error('Couldn\'t load game names from list | {}'.format(error))

try:
    RPC = Presence(id)
    RPC.connect()
except Exception as error:
    log.error('RPC couldn\'t connect | {}'.format(error))

def changePresence(swStatus, pName, pImg, pFname):
    start_time = time.time()
    local = time.localtime()
    string = time.strftime("%H:%M", local)
    if swStatus == False:
        try:
            RPC.update(large_image=pImg, large_text=pFname, details=pFname, start=start_time)
            print('Set game to {} at {}'.format(pFname, string))
        except Exception as error:
            log.error('Couldn\'t set RPC(1) to {} | {}'.format(pName, error))
    elif swStatus == True:
        try:
            RPC.update(large_image=pImg, large_text=pFname, details=pFname, state='SW-{}'.format(sw), start=start_time)
            print('Set game to {} at {} with friend code "SW-{}" showing'.format(pFname, string, sw))
        except Exception as error:
            log.error('Couldn\'t set RPC(2) to {} | {}'.format(pName, error))
    else:
        log.error('Couldn\'t get friend code status')

def changeUpdateNotifier():
    picked = input('What setting do you want the Update Notifier to be on (on or off)? ')
    picked = picked.lower()
    if picked == 'on' or picked == 'true' or picked == 't': # why do you want this on tbh
        try:
            with open('config.json', 'r') as jsonfile: # very weird/hacky way to do this lol, but it does work tho
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['update-notifier'] = True
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
        except Exception as error:
            log.error('Couldn\'t change update-notifier setting | {}'.format(error))
        log.info('Update notifier set to TRUE. Rerun the program to use it with the new settings')
    elif picked == 'off' or picked == 'false' or picked == 'f':
        try:
            with open('config.json', 'r') as jsonfile: # very weird/hacky way to do this lol
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['update-notifier'] = False
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
        except Exception as error:
            log.error('Couldn\'t change update-notifier setting | {}'.format(error))
        log.info('Update notifier set to FALSE. Rerun the program to use it with the new settings')

def changeFNameSetting():
    k = input('Your current setting is set to: {}. What do you want to change it to ("full" for full game names, "short" for shortened game names)? '.format(configfname))
    if k == 'full' or k == 'f':
        try:
            with open('config.json', 'r') as jsonfile: # man i can use this anywhere lol
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['fname'] = True
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
            log.info('Set game name to "Full"')
        except Exception as error:
            log.error('Couldn\'t change fname setting | {}'.format(error))
    elif k == 'short' or k == 's':
        try:
            with open('config.json', 'r') as jsonfile:
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['fname'] = False
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
            log.info('Set game name to "Short"')
        except Exception as error:
            log.error('Couldn\'t change fname setting | {}'.format(error))

print('Here are the current games: ')
if configfname == False:
    print(', '.join(gamenames))
elif configfname == True:
    print(', '.join(gamefnames))
else:
    log.error('Couldn\'t print game names')
x = input('\nWhat game do you wanna play? ')
x = x.lower()

if x == 'help' or x == 'h': # help command to see full name of lists, only shows if you have fnames set to false in config file
    if configfname == False:
        print('\nHere are the full names for the games specified above: ')
        print(', '.join(gamefnames))
        log.info('Please rerun the program to select a game') # this is stupid, i need to redo all of the code lmao
    else:
        log.info('You already have game full names showing')
elif x == 'github' or x == 'gh':
    print('i mean i guess')
    time.sleep(3)
    webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
    sys.exit()
elif x == 'update notifier' or x == 'update-notifier' or x == 'un' or x == 'u-n':
    changeUpdateNotifier()
elif x == 'change-name' or x =='change name' or x == 'c-n' or x == 'cn':
    changeFNameSetting()

y = input('Do you want to show your friend code "SW-{}" (you can change this by typing "change")? '.format(sw))
y = y.lower()

if y == 'yes' or y == 'y':
    if sw == '' or sw == None:
        log.info('Friend code not set. Rerun the program and change your friend code to your friend code')
elif y == 'change' or y == 'c':
    c = input('What is your new friend code (just type the numbers)? ')
    b = input('Is "SW-{}" correct? '.format(c))
    b = b.lower()
    if b == 'yes' or b == 'y':
        try:
            with open('config.json', 'r') as jsonfile: # i use this because it works, don't judge me
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['sw-code'] = c
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
            sw = c
            print('Friend code changed to SW-{}'.format(c))
            y = 'yes'
        except Exception as error:
            log.error('Couldn\'t change sw-code | {}'.format(error))
    else:
        print('Friend code not changed')

try:
    for n in games['games']:
        z = n['name']
        o = n['fname']
        if z == x:
            chosenOne = z
            break
        elif o.lower() == x:
            chosenOne = o
            break
    else:
        log.info('The game you specified is not in the current game list')
except Exception as error:
    log.error('Can\'t find the game ({}) the user specified (1) | {}'.format(x, error))

try:
    for i in games['games']:
        if i['name'] == chosenOne or i['fname'] == chosenOne:
            name = i['name']
            img = i['img']
            fname = i['fname']
            if y == 'yes' or y == 'y':
                changePresence(True, name, img, fname)
                break
            else:
                changePresence(False, name, img, fname)
                break
except Exception as error:
    log.error('Can\'t find the game ({}) specified (2) | {}'.format(chosenOne, error))

while 1: # trust me, we need this
    time.sleep(15)
