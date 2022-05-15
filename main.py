#+= imports =+#
import sys
import os
if sys.version_info < (3, 8):  # Switchence officially supports version 3.8 and higher
	os.system('cls' if os.name == 'nt' else 'clear')
	print('[Warning] Your version of Python is lower than the recommended Python version')
	print('Switchence officially supports Python version 3.8 and higher')
	vInput = input('Do you wish to continue (Y/N)? ')
	if vInput.lower() in ['no', 'n']:
		sys.exit(0)
import ctypes
import json
import random
import time
import webbrowser

try:  # only try for the modules that need to be installed
	from colorama import Fore, init
	from pypresence import Presence
	import requests
	init()
	os.system('cls' if os.name == 'nt' else 'clear')
except ImportError as missing_module:
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'[Error] Module \'{missing_module.name}\' is missing')
	install_modules = input('Would you like to install all of the required modules? ')
	if install_modules in ['yes', 'y']:
		print('[Info] Installing now...')
		try:
			os.system('pip install --upgrade pip')
			os.system('pip install pypresence')
			os.system('pip install requests')
			os.system('pip install colorama')
			print('\n[Info] Successfully installed all of the required modules! Please restart Switchence')
			sys.exit(0)
		except Exception as error:
			print('Error in installing required modules automatically. Please install them manually. Error below')
			print(error)
			sys.exit(1)
	else:
		print('[Info] Installation of required modules cancelled')
		sys.exit(0)
initialize_time = time.time()
CURRENT_VERSION = '1.9.4'


#+= important functions =+#
class log:
	'''
	custom logging function to log error, info and loading texts

	Parameters
	----------
	text : str
		the text within the logged message
	'''
	def __init__(self, text: str, color: str):
		self.text = text
		self.color = color

	def error(text: str):
		change_window_title('Error')
		clear()
		print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {text}')
		print('Please report this error on the Switchence GitHub issue page if this error happens consistently')
		time.sleep(1)
		webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
		sys.exit(1)

	def info(text: str, close: bool):  # second param is for if i want switchence to close after printing info
		'''
		Parameters
		----------
		close : bool
			decides if the program closes or not after logging the message
		'''
		change_window_title('Info')
		print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
		if close:
			clear()
			print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
			sys.exit(0)

	def loading(text: str, color: str):  # color is the color of the loading text
		'''
		Parameters
		----------
		color : str
			can pick between green, yellow or red as the logged color text
		'''
		if color == 'green':
			color = Fore.LIGHTGREEN_EX
		elif color == 'yellow':
			color = Fore.LIGHTYELLOW_EX
		else:
			color = Fore.LIGHTRED_EX
		print(f'{Fore.LIGHTCYAN_EX}[Loading] {color}{text}{Fore.RESET}')


class config:
	'''
	config file handler class. used for updating the config file, and creating a new config file
	'''
	def update(setting_changed: str, change_to):
		'''
		updates the config file by changing one value

		Parameters
		----------
		setting_changed : str
			the setting that's being changed, such as version
		change_to : any
			what the new setting is being changed to. can be a string, bool, updated list, and prob more
		'''
		with open('config.json', 'r') as jfile:
			jFile = json.load(jfile)
			for i in jFile['config']:
				i[setting_changed] = change_to
		with open('config.json', 'w') as jfile:
			json.dump(jFile, jfile, indent=4)

	@staticmethod
	def create(swcode: str, saved_favorites: list = [], current_version: str = CURRENT_VERSION):
		'''
		creates a blank config file

		Parameters
		----------
		swcode : str
			used to set the sw code (or friend code) for the new config file. can be empty if sw code is not found
		saved_favorites : list
			used to set the new game list for new config file. can be empty if favorite list not found.
			doesn't need to be passed all the time if config file not found
		current_version : str
			used to set new version for new config file. will default to current build version if version isn't found
		'''
		# load up all the vars from the global scale
		global sw, version, updatenotifier, configfname, showbutton, autoupdate, favorites
		# create settings to save to config file
		configjson = {'config': [{
			'sw-code': swcode,
			'version': current_version,
			'update-notifier': True,
			'fname': False,
			'show-button': True,
			'auto-update': False,
			'favorites': saved_favorites
		}]}

		log.loading('Loaded settings to save, saving them...', 'yellow')
		# save settings to file
		with open('config.json', 'w') as jsonfile:
			json.dump(configjson, jsonfile, indent=4)

		# reopen config file then save the settings within it
		with open('config.json', 'r') as jsonfile:
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				sw = details['sw-code']
				version = details['version']
				updatenotifier = details['update-notifier']
				configfname = details['fname']
				showbutton = details['show-button']
				autoupdate = details['auto-update']
				favorites = details['favorites']
			log.loading('Config file settings set!', 'green')


log.loading('Loading initial functions...', 'yellow')
def clear():
	'''
	just clears the terminal screen
	'''
	os.system('cls' if os.name == 'nt' else 'clear')
clear()


def change_window_title(title: str):
	'''
	changes the terminal window type. only works on windows lol
	'''
	if os.name == 'nt':
		ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | {title}')
change_window_title('Loading...')


def reopen():
	'''
	reopens Switchence
	'''
	file_name = os.path.basename(__file__)
	if os.path.isfile('Switchence.exe'):  # TODO: add support for if they changed file name lol
		sys.exit(1)  # TODO: actually reopen exe file lol
	elif '.py' in file_name:  # even exe files are considered .py files :/
		os.system(f'python3 {file_name}')
	else:
		sys.exit(1)


def update_program(online_ver: str):
	'''
	automatically updates Switchence by pulling the latest raw file from GitHub to update to

	Parameters
	----------
	online_ver : str
		the newest version number
	'''
	change_window_title(f'Updating to version {online_ver}')
	log.info(f'Updating to version {online_ver}...', False)

	# get the path location of file
	current_file = os.path.basename(__file__)
	if os.path.isfile('Switchence.exe'):
		config.update('auto-update', False)
		log.info('The exe file does not currently support auto updating', True)

	# request up-to-date file from github
	current_online_version = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/main.py')
	if current_online_version.status_code != 200:
		log.error(f'Status code is not 200, it is {current_online_version.status_code}, so the program will not update')
	elif current_online_version.status_code == 429:  # being rate limited
		log.info('Woah, slow down! You\'re being rate limited!', True)

	# get binary version of raw code
	online_version_binary = current_online_version.content
	with open(current_file, 'wb') as file:  # thanks to https://stackoverflow.com/users/13155625/dawid-januszkiewicz
		file.write(online_version_binary)  # for getting this to work!
	config.update('version', online_ver)
	change_window_title(f'Updated to version {online_ver}')
	reopen_prompt = input('Would you like to reopen Switchence? ')
	if reopen_prompt in ['yes', 'y']:
		reopen()
	log.info(f'Finished updating to version {online_ver}', True)


#+= variables =+#
# everything except beta is pulled from either the config file or online files
beta = False  # if current build is a beta build
version = None
oVersion = None  # online version
sw = None
updatenotifier = None
configfname = None
showbutton = None
autoupdate = None
gamenames = []
gamefnames = []
update_available = False
announcement = None
favorites = None
tips = None

#+= loading config file =+#
log.loading('Checking for config file...', 'yellow')
if os.path.isfile('config.json'):
	log.loading('Found config file, attempting to read contents...', 'yellow')
	try:
		with open('config.json', 'r') as json_file:
			json_File = json.load(json_file)
			for details in json_File['config']:
				sw = details['sw-code']
				version = details['version']
				updatenotifier = details['update-notifier']
				configfname = details['fname']
				showbutton = details['show-button']
				autoupdate = details['auto-update']
				favorites = details['favorites']
			log.loading('Loaded config settings!', 'green')
	except Exception:  # if some settings are missing, recreate the file while saving some settings
		try:  # attempt to save sw-code
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					sw = i['sw-code']
		except KeyError:
			sw = ''

		try:  # attempt to save version
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					version = i['version']
					break
		except KeyError:
			version = CURRENT_VERSION

		try:  # attempt to save favorite list
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					favorites = i['favorites']
					break
		except KeyError:
			favorites = []

		log.loading('Missing config settings found, creating them...', 'red')
		log.loading('This means some settings will be reset to default', 'red')
		config.create(sw, favorites, version)
else:  # config file can't be found
	log.loading('Config file not found, attempting to create one...', 'yellow')
	sw = ''  # sw var is needed in function below, so it needs to be pre defined
	config.create(sw)

#+= game list =+#
log.loading('Attempting to load game list...', 'yellow')
gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json')  # auto update game list :)
if gamejson.status_code != 200:
	log.error(f'Failed to get game list with status code {gamejson.status_code}')
elif gamejson.status_code == 429:
	log.info('Woah, slow down! You\'re being rate limited!', True)

# use the online data and make it readable for the program
gamejsontext = gamejson.text  # get text content from request (just json file)
games = json.loads(gamejsontext)  # load the text content from request
oVersion = games['version']
announcement = games['announcement']
tips = games['tips']
log.loading('Game list loaded!', 'green')

log.loading('Attempting to read game list info...', 'yellow')
for details in games['games']:
	gamenames.append(details['name'])
	gamefnames.append(details['fname'])
log.loading('Successfully read game list info!', 'green')

#+= checking version =+#
log.loading('Checking file version...', 'yellow')
if version in [None, '']:  # checks your version
	log.loading('File version not found, attempting to create...', 'red')
	config.update('version', oVersion)
	log.loading('Successfully created file version!', 'green')
elif version != oVersion:
	update_available = True

#+= rpc =+#
log.loading('Attempting to start Rich Presence...', 'yellow')
RPC = Presence('802943733045526588')
RPC.connect()
log.loading('Successfully started Rich Presence!', 'green')


#+= some more important functions =+#
def change_presence(swstatus: bool, gameimg: str, gamefname: str):
	'''
	changes the presence for Switchence. changes how it updates the RPC depending on if the user wants to show friend code and if they want to show a
	button that will lead anyone to the public GitHub page if they click on it

	Parameters
	----------
	swstatus : bool
		if the friend code is being shown
	gameimg : str
		name of the image to show on discord
	gamefname : str
		full name of the game the user wants to play
	'''
	start_time = time.time()
	current_time_formatted = time.strftime('%H:%M', time.localtime())
	# set small image to indicate build ran by user is a beta build or not
	if beta:
		small_text = 'Switchence Beta'
		small_img = 'gold_icon'
	else:
		small_text = f'Switchence v{version}'
		small_img = 'switch_png'

	if showbutton:
		button = [{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}]
	else:
		button = None
	
	if swstatus:
		sw_code = f'SW-{sw}'
	else:
		sw_code = None

	RPC.update(large_image=gameimg, large_text=gamefname, small_image=small_img, small_text=small_text, details=gamefname,
		state=sw_code, buttons=button, start=start_time)
	print(f'Set game to {Fore.LIGHTGREEN_EX}{gamefname}{Fore.RESET} at {current_time_formatted}')
	change_window_title(f'Playing {gamefname}')


def change_update_notifier():
	'''
	changes setting for the new update notifications
	'''
	picked = input('\nWhat setting do you want the Update Notifier to be set to, on or off? ')
	picked = picked.lower()
	if picked in ['on', 'true', 't']:  # why do you want this on tbh
		config.update('update-notifier', True)
		log.info(f'Update notifier set to {Fore.LIGHTGREEN_EX}TRUE{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	elif picked in ['off', 'false', 'f']:
		config.update('update-notifier', False)
		log.info(f'Update notifier set to {Fore.LIGHTRED_EX}FALSE{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()


def change_FName_setting():
	'''
	changes setting for if the user wants to show the full game name for the games or not
	'''
	length = 'short' if configfname is False else 'full'
	print(f'\nYour current setting is set to: {Fore.LIGHTGREEN_EX}{length}{Fore.RESET}')
	k = input('What do you want to change it setting to? \'Full\' for full game names or \'short\' for shortened game names ')
	k = k.lower()
	if k in ['full', 'f']:
		config.update('fname', True)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Full{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	elif k in ['short', 's']:
		config.update('fname', False)
		log.info(f'Set game name to {Fore.LIGHTGREEN_EX}Short{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()


def change_auto_update():
	'''
	changes setting for the auto updater
	'''
	print(f'\nYour current Auto Update setting is set to {Fore.LIGHTGREEN_EX}{autoupdate}{Fore.RESET}')
	ask = input('What would you like to change it to? On or off? ')
	ask = ask.lower()
	if ask == 'on':
		config.update('auto-update', True)
		log.info(f'Set Auto Update setting to {Fore.LIGHTGREEN_EX}True{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	elif ask == 'off':
		config.update('auto-update', False)
		log.info(f'Set Auto Update setting to {Fore.LIGHTRED_EX}False{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	else:
		log.error('Keeping auto update setting the same since you did not answer correctly')


def add_favorite():
	'''
	allows the user to add or remove games from their favorite list
	'''
	favask = input('Would you like to add or remove a favorite? ')
	if favask in ['remove', 'r']:
		if not favorites:
			log.info('Your favorite list is currently empty', True)
		remove_ask = input('What game would you like to remove from your favorites? ')
		if remove_ask not in favorites:
			log.info(f'{remove_ask} is currently not in your favorite list', True)
		favorites.remove(remove_ask)
		config.update('favorites', favorites)
		log.info(f'Successfully removed {remove_ask} from your favorite list', True)
	else:
		add_ask = input('What game would you like to add to your favorites? ')
		favorites.append(add_ask)
		config.update('favorites', favorites)
		log.info(f'Successfully added {add_ask} to your favorite list', True)


def form():
	'''
	opens the survey form
	'''
	log.info('Opening the form...', False)
	webbrowser.open('https://forms.gle/ofCZ8QXQYxPvTcDE7', new=2, autoraise=True)
	log.info('Form is now open! Thanks for being willing to fill out the form!', True)


def shortcut(chosen_game: int, favs: list) -> int:
	'''
	gets the selected game from the list from an int from user

	Parameters
	----------
	chosen_game : int
		the game in the list the user wants to play
	favs : list
		the current favorite list of the user
	
	Returns
	-------
	favs[i] : str
		returns the favorite game name corresponding with the option the user selected
	'''
	for i in range(len(favs)):
		if i + 1 == chosen_game:
			return favs[i]
	log.error('You don\'t have that many favorites in your favorite list. Use the \'shortcut\' command to figure out how shortcuts work')


#+= looking for game status before picking a game =+#
log.loading('Attempting to set looking for game status...', 'yellow')
start_time = time.time()
if showbutton:
	button = [{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}]
else:
	button = None
RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', buttons=button, start=start_time)
log.loading('Successfully set looking for game status!', 'green')

#+= home page =+#
change_window_title('Picking a game')
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
Made by: Aethese
''')

#+= handle announcement and tips =+#
if announcement not in [None, '']:
	print(f'{Fore.LIGHTCYAN_EX}[Announcement]{Fore.RESET} {announcement}')
print(f'{Fore.LIGHTCYAN_EX}[Tip]{Fore.RESET} {random.choice(tips)}\n')

#+= handle new update =+#
if update_available:
	if autoupdate:
		log.info('New update found, updating to latest version...', False)
		time.sleep(1)
		update_program(oVersion)
	if updatenotifier:  # this will only show if auto updates aren't on
		log.info(f'Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date', False)
		log.info(f'You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} by turning on Auto Updates or by visiting the official GitHub page', False)
		log.info('If you wish to turn on auto updates type \'auto update\' below', False)
		log.info('If you wish to turn off update notifications, type \'update notifier\' below', False)
		log.info('If you want to visit the GitHub page to update to the latest version type \'github\' below\n', False)
		time.sleep(1)

#+= pick game =+#
print('Here are the current games:')
if favorites:
	favorites.sort()  # sort alphabetically
	print(Fore.LIGHTYELLOW_EX+', '.join(favorites))
if configfname:  # if user wants to show full game names
	# Fore.WHITE to reset yellow color from above
	print(Fore.WHITE+', '.join(gamefnames))
else:
	print(Fore.WHITE+', '.join(gamenames))
initialize_time = time.time() - initialize_time
game_input = input('\nWhat game do you wanna play? ')
game_input = game_input.lower()

#+= input options =+#
if game_input in ['github', 'gh', 'g']:
	log.info('Opening GitHub page...', False)
	time.sleep(1)
	webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
	log.info('GitHub page opened', True)
elif game_input in ['update notifier', 'update-notifier', 'un', 'u-n']:
	change_update_notifier()
elif game_input in ['change name', 'change-name', 'cn', 'c-n']:
	change_FName_setting()
elif game_input in ['auto update', 'auto-update', 'au', 'a-u']:
	change_auto_update()
elif game_input in ['initialize', 'init', 'i']:
	log.info(f'Time Switchence took to initialize: {initialize_time}', True)
elif game_input in ['favorite', 'f']:
	add_favorite()
elif game_input == 'form':
	form()
elif game_input in ['shortcut', 'shortcuts', 's']:
	log.info(f'''You currently have {Fore.LIGHTRED_EX}{len(favorites)}{Fore.RESET} favorite(s) in your favorite list
Let\'s say you want to pick the first one, just type {Fore.LIGHTRED_EX}1{Fore.RESET} to pick your first favorite''', True)
elif game_input in ['discord', 'd']:
	log.info('Opening Discord server link...', False)
	webbrowser.open('https://discord.gg/238heBqmZb', new=2, autoraise=True)
	log.info('Discord server link opened!', True)
elif game_input in ['options', 'o']:
	log.info(f'''The current options are:
\'github\' this will bring up the public GitHub repo
\'discord\' this will bring up the public Discord server
\'update notifier\' which toggles the built-in update notifier, this is set to {Fore.LIGHTCYAN_EX}{updatenotifier}{Fore.RESET}
\'change name\' this will toggle how game names are shown on the game select screen, this is set to {Fore.LIGHTCYAN_EX}{configfname}{Fore.RESET}
\'auto update\' which toggles the built-in auto updater, this is {Fore.LIGHTCYAN_EX}{autoupdate}{Fore.RESET}
\'initialize\' this will let you know how long it took Switchence to initialize
\'favorite\' this will let you favorite a game show it shows up 
\'form\' this will bring up the Google form that has questions related to Switchence (please fill it out!)
\'shortcut\' this will tell you how shortcuts work
\'options\' this will bring up this page :P''', True)

#+= sw handling =+#
show_sw_code = input(f'Do you want to show your friend code, SW-{sw} (you can change this by typing \'change\')? ')
show_sw_code = show_sw_code.lower()
if show_sw_code in ['yes', 'y']:
	if sw in [None, '']:
		log.info('Friend code not set, continuing with setting set to off', False)
		show_sw_code = 'n'
elif show_sw_code in ['change', 'c']:
	new_sw_code = input('What is your new friend code (just type the numbers)? ')
	confirm_new_code = input(f'Is \'SW-{new_sw_code}\' correct? ')
	confirm_new_code = confirm_new_code.lower()
	if confirm_new_code in ['yes', 'y']:
		config.update('sw-code', new_sw_code)
		sw = new_sw_code
		log.info(f'Friend code changed to SW-{new_sw_code}', False)
		show_sw_code = 'y'
	else:
		log.info('Friend code not changed, continuing with setting set to off', False)
		show_sw_code = 'n'

#+= search for game =+#
# attempt to change game_input to int to see if the user wants to pick a favorite
try:
	game_input_int = int(game_input)
except ValueError:
	game_input_int = None
if isinstance(game_input_int, int):  # for shortcuts
	game_input = shortcut(game_input_int, favorites)

for details in games['games']:
	details_name = details['name']
	details_fname = details['fname']  # if user has full game name being shown
	if details_name.lower() == game_input:
		chosen_game = details_name
		break
	elif details_fname.lower() == game_input:
		chosen_game = details_fname
		break
else:
	log.info(f'The game you specified, {Fore.LIGHTGREEN_EX}{game_input}{Fore.RESET}, is not in the current game list', True)

#+= send info to changePresence function about game picked =+#
for i in games['games']:
	if chosen_game in [i['name'], i['fname']]:
		img = i['name']  # the short game name is the same as the img name
		fname = i['fname']
		if show_sw_code in ['yes', 'y']:
			change_presence(True, img, fname)
			break
		change_presence(False, img, fname)
		break

#+= needed to keep program running in background =+#
while True:
	time.sleep(15)
