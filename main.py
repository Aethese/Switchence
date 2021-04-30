try:
    import time, json, requests, webbrowser, os, sys, colorama, ctypes
    from pypresence import Presence
    from colorama import Fore, init
    init(autoreset=True)
    ctypes.windll.kernel32.SetConsoleTitleW('Switchence')
except Exception as error:
    print(f'Couldn\'t import everything | {error}')

class log:
    def error(text: str):
        clear()
        print(f'{Fore.RED}[Error]{Fore.RESET} {text}\nPlease report this error on the Switchence GitHub issue page if this error happens consistently')
        time.sleep(5)
        webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
        time.sleep(600)
        sys.exit()

    def info(text: str):
        clear()
        print(f'{Fore.GREEN}[Info]{Fore.RESET} {text}\nThis program will now close in 1 minute')
        time.sleep(60)
        sys.exit()
    
    def warning(text: str):
        print(f'\n{Fore.YELLOW}[WARNING]{Fore.RESET} {text}\n')

    def loading(text: str):
        print(f'{Fore.LIGHTCYAN_EX}[Loading]{Fore.RESET} {text}')

def clear():
    os.system('cls' if os.name =='nt' else 'clear')
clear()

id = '803309090696724554'
version = None
sw = None
updatenotifier = None
configfname = None
showbutton = None
gamenames = []
gamefnames = []
chosenOne = ''
img = ''
fname = ''

log.loading('Checking for config file...')
if os.path.isfile('config.json') == True:
    log.loading('Found config file, attempting to read contents...')
    try:
        with open('config.json', 'r') as jsonfile:
            log.loading('Reading config file\'s content...')
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                sw = details['sw-code']
                version = details['version']
                updatenotifier = details['update-notifier']
                configfname = details['fname']
                showbutton = details['show-button']
                log.loading('Loaded config settings!')
    except Exception as error:
        log.error(f'Couldn\'t load config file (1) | {error}')
elif os.path.isfile('config.json') == False:
    log.loading('Config file not found, attempting to create one...')
    try:
        configjson = {}
        configjson['config'] = [{
            'sw-code': '',
            'version': '1.3.0',
            'update-notifier': True,
            'fname': False,
            'show-button': True
        }]
        with open('config.json', 'w') as jsonfile:
            json.dump(configjson, jsonfile, indent=4)
            log.loading('Config file created!')
        with open('config.json', 'r') as jsonfile: # actually get the info lol
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                sw = details['sw-code']
                version = details['version']
                updatenotifier = details['update-notifier']
                configfname = details['fname']
                showbutton = details['show-button']
    except Exception as error:
        log.error(f'Couldn\'t load config file (2) | {error}')
else:
    log.error('Couldn\'t load config settings')

log.loading('Attempting to load game list...')
try:
    gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json') # auto update list :)
    gamejsontext = gamejson.text
    games = json.loads(gamejsontext)
    log.loading('Game list loaded!')
except Exception as error:
    log.error(f'Couldn\'t load game list | {error}')

oVersion = games['version']

log.loading('Checking file version...')
if version == '' or version == None: # checks your version
    log.loading('File version not found, attempting to create...')
    try:
        with open('config.json', 'r') as jsonfile:
            jsonFile = json.load(jsonfile)
            for details in jsonFile['config']:
                details['version'] = oVersion
        with open('config.json', 'w') as jsonfile:
            json.dump(jsonFile, jsonfile, indent=4)
        log.loading('Succesfully created file version!')
    except Exception as error:
        log.error(f'Couldn\'t write to the version file | {error}')
elif version != oVersion:
    if updatenotifier == True:
        print(f'{Fore.RED}[INFO]{Fore.RESET} Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date')
        print(f'{Fore.RED}[INFO]{Fore.RESET} You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} on the official GitHub page or continue using the program as usual')
        print(f'{Fore.RED}[INFO]{Fore.RESET} If you wish to turn off update notifications, type \'update notifier\' in the game selection input\n')
        print(f'{Fore.LIGHTYELLOW_EX}The program will return to normal in 5 seconds.')
        time.sleep(2)
        webbrowser.open('https://github.com/Aethese/Switchence', new=2, autoraise=True)
        time.sleep(5)

log.loading('Attempting to read game list info...')
try:
    for details in games['games']:
        gamenames.append(details['name'])
        gamefnames.append(details['fname'])
    log.loading('Succesfully read game list info!')
except Exception as error:
    log.error(f'Couldn\'t load game names from list | {error}')

log.loading('Attempting to start Rich Presence...')
try:
    RPC = Presence(id)
    RPC.connect()
    log.loading('Succesfully started Rich Presence!')
except Exception as error:
    log.error(f'RPC couldn\'t connect | {error}')

def changePresence(swStatus, pName, pImg, pFname):
    start_time = time.time()
    local = time.localtime()
    string = time.strftime('%H:%M', local)
    if swStatus == False:
        try:
            if showbutton == True:
                RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text='Switchence', details=pFname, 
                           buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
                print(f'Set game to {pFname} at {string}')
                ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | Playing {pFname}')
            elif showbutton == False:
                RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text='Switchence', details=pFname, start=start_time)
                print(f'Set game to {pFname} at {string}')
                ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | Playing {pFname}')
            else:
                log.error('Couldn\'t get button info (1)')
        except Exception as error:
            log.error(f'Couldn\'t set RPC(1) to {pName} | {error}')
    elif swStatus == True:
        try:
            if showbutton == True:
                RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text='Switchence', details=pFname, 
                           state=f'SW-{sw}', buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
                print(f'Set game to {pFname} at {string} with friend code "SW-{sw}" showing')
                ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | Playing {pFname}')
            elif showbutton == False:
                RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text='Switchence', details=pFname, state=f'SW-{sw}', start=start_time)
                print(f'Set game to {pFname} at {string} with friend code "SW-{sw}" showing')
                ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | Playing {pFname}')
            else:
                log.error('Couldn\'t get button info (2)')
        except Exception as error:
            log.error(f'Couldn\'t set RPC(2) to {pName} | {error}')
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
            log.error(f'Couldn\'t change update-notifier setting | {error}')
        log.info('Update notifier set to {Fore.GREEN}TRUE{Fore.RESET}. Rerun the program to use it with the new settings')
    elif picked == 'off' or picked == 'false' or picked == 'f':
        try:
            with open('config.json', 'r') as jsonfile: # very weird/hacky way to do this lol
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['update-notifier'] = False
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
        except Exception as error:
            log.error(f'Couldn\'t change update-notifier setting | {error}')
        log.info('Update notifier set to {Fore.YELLOW}FALSE{Fore.RESET}. Rerun the program to use it with the new settings')

def changeFNameSetting():
    if configfname == False:
        l = 'short'
    elif configfname == True:
        l = 'full'
    else:
        log.error('Couldn\'t get config name setting')

    k = input(f'Your current setting is set to: {Fore.LIGHTGREEN_EX}{l}{Fore.RESET}. What do you want to change it to ("full" for full game names, "short" for shortened game names)? ')
    if k == 'full' or k == 'f':
        try:
            with open('config.json', 'r') as jsonfile: # man i can use this anywhere lol
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['fname'] = True
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
            log.info(f'Set game name to {Fore.YELLOW}Full{Fore.RESET}')
        except Exception as error:
            log.error(f'Couldn\'t change fname setting | {error}')
    elif k == 'short' or k == 's':
        try:
            with open('config.json', 'r') as jsonfile:
                jsonFile = json.load(jsonfile)
                for details in jsonFile['config']:
                    details['fname'] = False
            with open('config.json', 'w') as jsonfile:
                json.dump(jsonFile, jsonfile, indent=4)
            log.info(f'Set game name to {Fore.YELLOW}Short{Fore.RESET}')
        except Exception as error:
            log.error(f'Couldn\'t change fname setting | {error}')

clear()
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

y = input(f'Do you want to show your friend code "SW-{sw}" (you can change this by typing "change")? ')
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
            log.error(f'Couldn\'t change sw-code | {error}')
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
    log.error(f'Can\'t find the game ({x}) the user specified (1) | {error}')

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
    log.error(f'Can\'t find the game ({chosenOne}) specified (2) | {error}')

while 1: # trust me, we need this
    time.sleep(15)
