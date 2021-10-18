#+= imports =+#
try:
	import time
	import json
	import requests
	import webbrowser
	import os
	import sys
	import ctypes
	from pypresence import Presence
	from colorama import Fore, init
	os.system('cls' if os.name == 'nt' else 'clear')
	init(autoreset=True)  # auto reset color after every print
except ImportError as missingmod:
	print('[ERROR] Couldn\'t import everything')
	try:  # tries to print missing module's name, if it can't just print error
		print(f'Module \'{missingmod.name}\' is missing')
	except:
		print(f'[ERROR] Erorr message: {missingmod}')
	module = input('Would you like to install all of the modules? ')
	if module in ['yes', 'y']:
		print('Installing now...')
		try:
			os.system('py -m pip install --upgrade pip')
			os.system('py -m pip install pypresence')
			os.system('py -m pip install requests')
			os.system('py -m pip install colorama')
			print('Successfully installed all required modules! Please restart Switchence')
			time.sleep(600)
			sys.exit()
		except Exception as error:
			print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {error}')
			print('Please report this error on the Switchence GitHub issue page if this error happens consistently')
			time.sleep(5)
			webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
			time.sleep(600)
			sys.exit()
	else:
		print('Installation of required modules cancelled')
		time.sleep(600)
		sys.exit()
initializeTime = time.time()


#+= important functions =+#
class log:
	def __init__(self, text):
		self.text = text

	def error(text: str):
		changeWindowTitle('Error')
		clear()
		print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {text}')
		print('Please report this error on the Switchence GitHub issue page if this error happens consistently')
		time.sleep(5)
		webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
		time.sleep(600)
		sys.exit()

	def info(text: str):
		changeWindowTitle('Info')
		clear()
		print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}\nThis program will now close in 10 minutes')
		time.sleep(600)
		sys.exit()

	def loading(text: str):
		print(f'{Fore.LIGHTCYAN_EX}[Loading]{Fore.RESET} {text}')


class config:
	def update(self, changeto):  # self = setting being changed
		with open('config.json', 'r') as jsonfile:
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				details[self] = changeto
		with open('config.json', 'w') as jsonfile:
			json.dump(jsonFile, jsonfile, indent=4)

	@staticmethod
	def create(swcode):
		try:  # fucking global vars
			global sw, version, updatenotifier, configfname, showbutton, legacy, autoupdate
			configjson = {'config': [{
				'sw-code': swcode,
				'version': '1.8.0',
				'update-notifier': True,
				'fname': False,
				'show-button': True,
				'legacy': True,
				'auto-update': False
			}]}
			log.loading('Got settings to save, saving them...')
			with open('config.json', 'w') as jsonfile:
				json.dump(configjson, jsonfile, indent=4)
			log.loading('Saved settings!')
			with open('config.json', 'r') as jsonfile: # actually get the info lol
				log.loading('Setting config settings...')
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					sw = details['sw-code']
					version = details['version']
					updatenotifier = details['update-notifier']
					configfname = details['fname']
					showbutton = details['show-button']
					legacy = details['legacy']
					autoupdate = details['auto-update']
				log.loading('Config file settings set!')
		except Exception as error:
			log.error(f'Couldn\'t create config settings | {error}')

log.loading('Loading initial functions...')
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')  # *supposedly* multi platform supported clear
clear()

def changeWindowTitle(title):
	if os.name == 'nt': # hopefully multi platform support
		ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | {title}')
changeWindowTitle('Loading...')


def updateProgram(setting, onlineVer):
	if not setting:
		return
	changeWindowTitle(f'Updating to version {onlineVer}')
	log.loading(f'Updating to version {onlineVer}...')
	try:
		if os.path.isfile('Switchence.exe'):
			config.update('auto-update', False)  # fixes infinite error loop lol
			log.error('The exe file does not currently support auto updating')
		if not os.path.isfile('main.py'):
			log.error('File \'main.py\' not found, did you rename the file?')
		currentOnlineVersion = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/main.py')
		log.loading('Checking new version...')
		if currentOnlineVersion.status_code != 200:  # request to get raw code was not successful
			log.error(f'Status code is not 200, it is {currentOnlineVersion.status_code}, so the program will not update')
		log.loading('Successfully loaded new version! Getting new update...')
		onlineVersionBinary = currentOnlineVersion.content  # get binary version of raw code
		with open('main.py', 'wb') as file:  # thanks to https://stackoverflow.com/users/13155625/dawid-januszkiewicz for getting this to work!
			file.write(onlineVersionBinary)
		log.loading('Installed latest version! Updating local version...')
		config.update('version', onlineVer)
		changeWindowTitle(f'Updated to version {onlineVer}!')
		log.info(f'Finished updating to version {onlineVer}!')
	except Exception as error:
		log.error(f'Couldn\'t change version setting when updating | {error}')


#+= variables =+#
# just pre defining variables
beta = False  # if current build is a test build
version = None
oVersion = None  # online version
sw = None
updatenotifier = None
configfname = None
showbutton = None
legacy = None
autoupdate = None
gamenames = []
gamefnames = []
chosenOne = ''
updateAvailable = False
announcement = None

#+= loading config file =+#
log.loading('Checking for config file...')
if os.path.isfile('config.json'):
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
				legacy = details['legacy']
				autoupdate = details['auto-update']
			log.loading('Loaded config settings!')
	except KeyError:  # if some settings are missing, recreate the file while saving some settings
		if sw is None:  # in case an empty config folder is found
			sw = ''
		if version is None:
			version = '1.8.0'
		log.loading('Missing config settings found, creating them...')
		log.loading('This means some settings will be reset to default')
		config.create(sw)
elif os.path.isfile('config.json') is False:
	log.loading('Config file not found, attempting to create one...')
	sw = ''  # sw var is needed in function below, so it needs to be pre defined
	config.create(sw)

#+= game list =+#
log.loading('Attempting to load game list...')
gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json')  # auto update game list :)
if gamejson.status_code != 200:
	log.error(f'Failed to get game list with status code {gamejson.status_code}')
gamejsontext = gamejson.text
games = json.loads(gamejsontext)
oVersion = games['version']
announcement = games['announcement']
log.loading('Game list loaded!')

log.loading('Attempting to read game list info...')
for details in games['games']:
	gamenames.append(details['name'])
	gamefnames.append(details['fname'])
log.loading('Successfully read game list info!')

#+= checking version =+#
log.loading('Checking file version...')
if version in [None, '']: # checks your version
	log.loading('File version not found, attempting to create...')
	config.update('version', oVersion)
	log.loading('Successfully created file version!')
elif version != oVersion:
	updateAvailable = True

#+= rpc =+#
log.loading('Attempting to start Rich Presence...')
RPC = Presence('803309090696724554')
RPC.connect()
log.loading('Successfully started Rich Presence!')


#+= some more important functions =+#
def changePresence(swStatus, pName, pImg, pFname):
	start_time = time.time()
	string = time.strftime('%H:%M', time.localtime())
	if beta:  # set small image to indicate build ran by user is a beta build or not
		smallText = 'Switchence Beta'
		smallImg = 'gold_icon'
	else:
		smallText = f'Switchence v{version}'
		smallImg = 'switch_png'
	if swStatus is False:
		try:
			if showbutton:
				RPC.update(large_image=pImg, large_text=pFname, small_image=smallImg, small_text=smallText, details=pFname,
							buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
				print(f'Set game to {pFname} at {string}')
				changeWindowTitle(f'Playing {pFname}')
			elif showbutton is False:
				RPC.update(large_image=pImg, large_text=pFname, small_image=smallImg, small_text=smallText, details=pFname, start=start_time)
				print(f'Set game to {pFname} at {string}')
				changeWindowTitle(f'Playing {pFname}')
		except Exception as error:
			log.error(f'Couldn\'t set RPC(1) to {pName} | {error}')
	elif swStatus:
		try:
			if showbutton:
				RPC.update(large_image=pImg, large_text=pFname, small_image=smallImg, small_text=smallText, details=pFname,
							state=f'SW-{sw}', buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
				print(f'Set game to {pFname} at {string} with friend code \'SW-{sw}\' showing')
				changeWindowTitle(f'Playing {pFname}')
			elif showbutton is False:
				RPC.update(large_image=pImg, large_text=pFname, small_image=smallImg, small_text=smallText, details=pFname, state=f'SW-{sw}', start=start_time)
				print(f'Set game to {pFname} at {string} with friend code \'SW-{sw}\' showing')
				changeWindowTitle(f'Playing {pFname}')
		except Exception as error:
			log.error(f'Couldn\'t set RPC(2) to {pName} | {error}')

def changeUpdateNotifier():
	picked = input('What setting do you want the Update Notifier to be on (on or off)? ')
	picked = picked.lower()
	if picked in ['on', 'true', 't']: # why do you want this on tbh
		config.update('update-notifier', True)
		log.info(f'Update notifier set to {Fore.LIGHTGREEN_EX}TRUE{Fore.RESET}. Rerun the program to use it with the new settings')
	elif picked in ['off', 'off', 'f']:
		config.update('update-notifier', False)
		log.info(f'Update notifier set to {Fore.LIGHTRED_EX}FALSE{Fore.RESET}. Rerun the program to use it with the new settings')

def changeFNameSetting():
	length = 'short' if configfname is False else 'full'
	print(f'Your current setting is set to: {Fore.LIGHTGREEN_EX}{length}{Fore.RESET}')
	k = input('What do you want to change it to (\'full\' for full game names, \'short\' for shortened game names)? ')
	k = k.lower()
	if k in ['full', 'f']:
		config.update('fname', True)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Full{Fore.RESET}')
	elif k in ['short', 's']:
		config.update('fname', False)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Short{Fore.RESET}')

def changeAutoUpdate():
	print(f'Your current Auto Update setting is set to {Fore.LIGHTGREEN_EX}{autoupdate}{Fore.RESET}')
	ask = input('What would you like to change it to? On or off? ')
	ask = ask.lower()
	if ask == 'on':
		config.update('auto-update', True)
		log.info(f'Set Auto Update setting to {Fore.LIGHTGREEN_EX}True{Fore.RESET}')
	elif ask == 'off':
		config.update('auto-update', False)
		log.info(f'Set Auto Update setting to {Fore.LIGHTRED_EX}False{Fore.RESET}')
	else:
		log.error('Keeping auto update setting the same since you did not answer correctly')


#+= looking for game status before picking a game =+#
log.loading('Attempting to set looking for game status...')
startTime = time.time()
if showbutton:
	RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game',
				buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=startTime)
elif showbutton is False:
	RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', start=startTime)
log.loading('Successfully set looking for game status!')

#+= home page =+#
changeWindowTitle('Picking a game')
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

#+= handle announcement =+#
if announcement not in [None, '']:
	print(f'{Fore.LIGHTCYAN_EX}[ANNOUNCEMENT]{Fore.RESET} {announcement}\n')

#+= handle new update =+#
if updateAvailable:
	if autoupdate:
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} New update found, updating to latest version...')
		time.sleep(1)
		updateProgram(autoupdate, oVersion)
	if updatenotifier:  # this will show if auto updates aren't on
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} by turning on Auto Updates or by visiting the official GitHub page')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} If you wish to turn on auto updates type \'auto update\' below')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} If you wish to turn off update notifications, type \'update notifier\' below')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} If you want to visit the GitHub page to update to the latest version type \'github\' below')
		time.sleep(2)

#+= pick game =+#
print('Here are the current games: ')
if configfname is False:
	print(', '.join(gamenames))
else:
	print(', '.join(gamefnames))
initializeTime = time.time() - initializeTime
x = input('\nWhat game do you wanna play? ')
x = x.lower()

#+= input options =+#
if x in ['github', 'gh']:
	print('Opening GitHub page...')
	time.sleep(1)
	webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
	time.sleep(10)
	sys.exit()
elif x in ['update notifier', 'update-notifier', 'un', 'u-n']:
	changeUpdateNotifier()
elif x in ['change name', 'change-name', 'cn', 'c-n']:
	changeFNameSetting()
elif x in ['auto update', 'auto-update', 'au', 'a-u']:
	changeAutoUpdate()
elif x in ['initialize', 'i']:
	log.info(f'Time Switchence took to initialize: {initializeTime}')
elif x in ['options', 'o']:
	log.info(f'''The current options are:
\'github\' this will bring up the public GitHub repo
\'update notifier\' which toggles the built-in update notifier, this is set to {Fore.LIGHTCYAN_EX}{updatenotifier}{Fore.RESET}
\'change name\' this will toggle how game names are shown on the game select screen, this is set to {Fore.LIGHTCYAN_EX}{configfname}{Fore.RESET}
\'auto update\' which toggles the built-in auto updater, this is {Fore.LIGHTCYAN_EX}{autoupdate}{Fore.RESET}
\'initialize\' this will let you know how long it took Switchence to initialize
\'options\' this will bring up this page''')

#+= sw handling =+#
y = input(f'Do you want to show your friend code, SW-{sw} (you can change this by typing \'change\')? ')
y = y.lower()
if y in ['yes', 'y']:
	if sw in [None, '']:
		print('Friend code not set, continuing with setting set to off')
		y = 'n'
elif y in ['change', 'c']:
	c = input('What is your new friend code (just type the numbers)? ')
	b = input(f'Is \'SW-{c}\' correct? ')
	b = b.lower()
	if b in ['yes', 'y']:
		config.update('sw-code', c)
		sw = c
		print(f'Friend code changed to SW-{c}')
		y = 'y'
	else:
		print('Friend code not changed, continuing with setting set to off')
		y = 'n'

#+= search for game =+#
for n in games['games']:
	z = n['name']
	o = n['fname']
	if z.lower() == x:
		chosenOne = z
		break
	elif o.lower() == x:
		chosenOne = o
		break
else:
	log.info(f'The game you specified, {x}, is not in the current game list')

#+= send info to changePresence function about game picked =+#
for i in games['games']:
	if chosenOne in [i['name'], i['fname']]:
		name = i['name']
		img = i['img']
		fname = i['fname']
		if y in ['yes', 'y']:
			changePresence(True, name, img, fname)
			break
		changePresence(False, name, img, fname)  # sw code showing is no
		break

#+= just needed, trust me =+#
while True:
	time.sleep(15)
