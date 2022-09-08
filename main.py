#+= imports =+#
import sys
import os

# Switchence officially supports version 3.8 and higher
if sys.version_info < (3, 8):
	os.system('cls' if os.name == 'nt' else 'clear')
	print('[Warning] Your version of Python is lower than the recommended Python version')
	print('Switchence officially supports Python version 3.8 and higher')
	if input('Do you wish to continue? (Y/N) ')[0] in 'Nn':
		sys.exit(0)

import json
import time
import webbrowser
from random import choice as random_choice

try:  # only try for the modules that need to be installed
	from colorama import Fore, init
	import requests
	init()
except ImportError as missing_module:
	print(f'[Error] Module \'{missing_module.name}\' is missing')
	if input('Would you like to install all of the required modules? ')[0] in 'Yy':
		print('[Info] Installing now...')
		try:
			os.system('pip3 install --upgrade pip')
			os.system('pip3 install pypresence')
			os.system('pip3 install requests')
			os.system('pip3 install colorama')
			print('\n[Info] Successfully installed all of the required modules! Please restart Switchence')
			sys.exit(0)
		except Exception as error:
			print('Error in installing required modules automatically. Please install them manually. Error below:')
			print(error)
			sys.exit(1)
	else:
		print('[Info] Installation of required modules canceled')
		sys.exit(0)

# import src files after checking to see if all modules are installed
from src import utils
utils.clear()
from src import presence, updater
from src.config import config
from src.logger import logger

# init stuff
logger.loading('Initializing...', 'yellow')
initialize_time = time.time()

#+= variables =+#
# config settings
version = None
sw = None
updatenotifier = None
configfname = None
showbutton = None
autoupdate = None
gamenames = []
gamefnames = []
hide_all_except_favs = None
favorites = None
# in debug mode Switchence uses a local version of the games.json file
debug = False

# different vars used by Switchence
oVersion = None  # online version
update_available = False
announcement = None
tips = None

#+= loading config file =+#
logger.loading('Checking for config file...', 'yellow')
if os.path.isfile('config.json'):
	logger.loading('Found config file, attempting to read contents...', 'yellow')
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
				hide_all_except_favs = details['hide-all-except-favs']
				favorites = details['favorites']

		# test to see if in debug mode. what's in debug mode is stated where the debug var is stated
		try:
			with open('config.json', 'r') as test_debug:
				test_debug = json.load(test_debug)
				for i in test_debug['config']:
					debug = i['debug']
					break
		except:
			pass
		
		logger.loading('Loaded config settings!', 'green')
		logger.add_log(f'Version: {version}')
		logger.add_log(f'Built-in: {utils.CURRENT_VERSION}')
		logger.add_log(f'Auto updater: {autoupdate}')
		logger.add_log(f'Update notifier: {updatenotifier}')
		logger.add_log(f'Beta: {utils.BETA_BUILD}')
		logger.add_log(f'Debug mode: {debug}')
	except Exception:  # if some settings are missing, recreate the file while saving some settings
		try:  # attempt to save sw-code
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					sw = i['sw-code']
					break
		except KeyError:
			sw = ''

		try:  # attempt to save version
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					version = i['version']
					break
		except KeyError:
			version = utils.CURRENT_VERSION

		try:  # attempt to save favorite list
			with open('config.json', 'r') as json_file:
				json_File = json.load(json_file)
				for i in json_File['config']:
					favorites = i['favorites']
					break
		except KeyError:
			favorites = []

		logger.loading('Missing config settings found, creating them...', 'red')
		logger.loading('This means some settings will be reset to default', 'red')
		if input('Would you like to overwrite your current config file? (Y/N) ')[0] in 'Nn':
			logger.info('Ok, will not overwrite current config file and now exiting', True)
		sw, version, updatenotifier, configfname, showbutton, autoupdate, hide_all_except_favs, favorites = config.create(sw, favorites, version)
else:  # config file can't be found
	logger.loading('Config file not found, attempting to create one...', 'yellow')
	sw = ''  # sw var is needed in function below, so it needs to be pre defined
	sw, version, updatenotifier, configfname, showbutton, autoupdate, hide_all_except_favs, favorites = config.create(sw, [], utils.CURRENT_VERSION)

#+= game list =+#
logger.loading('Attempting to load game list...', 'yellow')
if debug:
	with open('games.json', 'r') as gamesjson:
		games = json.load(gamesjson)
else:
	gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json')  # auto update game list :)
	if gamejson.status_code != 200:
		logger.error(f'Failed to get game list with status code {gamejson.status_code}')

	# use the online data and make it readable for the program
	gamejsontext = gamejson.text  # get text content from request (just json file)
	games = json.loads(gamejsontext)  # load the text content from request

oVersion = games['version']
announcement = games['announcement']
tips = games['tips']
logger.loading('Game list loaded!', 'green')

logger.loading('Attempting to read game list info...', 'yellow')
for details in games['games']:
	gamenames.append(details['name'])
	gamefnames.append(details['fname'])
logger.loading('Successfully read game list info!', 'green')

#+= checking version =+#
logger.loading('Checking file version...', 'yellow')
if version in [None, '']:  # checks your version
	logger.loading('File version not found, attempting to create...', 'red')
	config.update('version', oVersion)
	logger.loading('Successfully created file version!', 'green')
elif version != oVersion:
	update_available = True

#+= home page =+#
presence.looking_for_game(showbutton)
utils.clear()
print('''
 .d8888b.                d8b 888             888                                          
d88P  Y88b               Y8P 888             888                                          
Y88b.                        888             888                                          
 "Y888b.   888  888  888 888 888888  .d8888b 88888b.   .d88b.  88888b.   .d8888b  .d88b.  
    "Y88b. 888  888  888 888 888    d88P"    888 "88b d8P  Y8b 888 "88b d88P"    d8P  Y8b 
      "888 888  888  888 888 888    888      888  888 88888888 888  888 888      88888888 
Y88b  d88P Y88b 888 d88P 888 Y88b.  Y88b.    888  888 Y8b.     888  888 Y88b.    Y8b.     
 "Y8888P"   "Y8888888P"  888  "Y888  "Y8888P 888  888  "Y8888  888  888  "Y8888P  "Y8888    
Made by Aethese
''')
logger.add_log('Printed logo')

#+= handle announcement, tips, and print if in debug mode =+#
if announcement != '':
	print(f'{Fore.LIGHTCYAN_EX}[Announcement]{Fore.RESET} {announcement}')
print(f'{Fore.LIGHTCYAN_EX}[Tip]{Fore.RESET} {random_choice(tips)}')

if debug:  # if in debug mode print at the top that you're in debug mode
	print(f'{Fore.LIGHTCYAN_EX}[Debug]{Fore.RESET} Debug mode is currently {Fore.LIGHTGREEN_EX}enabled{Fore.RESET}')
print(Fore.RESET)  # just add an empty space after tips and reset color

#+= handle new update =+#
if update_available:
	if autoupdate:
		logger.info('New update found, updating to latest version...', False)
		time.sleep(1)
		updater.update_program(oVersion, os.path.basename(__file__), debug)
	if updatenotifier:  # this will only show if auto updates aren't on
		logger.info(f'Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date', False)
		logger.info(f'You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} by turning on Auto Updates or by visiting the official GitHub page', False)
		logger.info('If you wish to turn on auto updates type \'auto update\' below', False)
		logger.info('If you wish to turn off update notifications, type \'update notifier\' below', False)
		logger.info('If you want to visit the GitHub page to update to the latest version type \'github\' below\n', False)
		time.sleep(0.75)

#+= pick game =+#
print('Here are the current games:')
if favorites:
	favorites.sort()  # sort alphabetically
	print(Fore.LIGHTYELLOW_EX+', '.join(favorites))

# prints the entire game list unless user doesn't want them to
if not hide_all_except_favs:
	if configfname:  # if user wants to show full game names
		print(Fore.RESET+', '.join(gamefnames))  # Fore.WHITE to reset yellow color from above
	else:
		print(Fore.RESET+', '.join(gamenames))
else:
	print(Fore.RESET+'Game list is hidden, to change type \'hide games\' to try to change')

initialize_time = time.time() - initialize_time
game_input = input('\nWhat game do you wanna play or what command do you want to use? ')
game_input = game_input.lower()

#+= input options =+#
# sorry :(
if game_input in ['github', 'gh', 'g']:
	logger.info('Opening GitHub page...', False)
	time.sleep(1)
	webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
	logger.info('GitHub page opened', True)
elif game_input in ['update notifier', 'update-notifier', 'un', 'u-n']:
	utils.change_setting('Update Notifier', 'update-notifier', updatenotifier)
elif game_input in ['change name', 'change-name', 'cn', 'c-n']:
	utils.change_setting('Show Full Game Names', 'fname', configfname)
elif game_input in ['auto update', 'auto-update', 'au', 'a-u']:
	utils.change_setting('Auto Update', 'auto-update', autoupdate)
elif game_input in ['initialize', 'init', 'i']:
	logger.info(f'Time Switchence took to initialize: {initialize_time}', True)
elif game_input in ['favorite', 'favourite']:
	utils.add_favorite(favorites)
elif game_input == 'form':
	utils.form()
elif game_input in ['shortcut', 'shortcuts']:
	logger.info(f'''You currently have {Fore.LIGHTRED_EX}{len(favorites)}{Fore.RESET} favorite(s) in your favorite list
Let\'s say you want to pick the first one, just type {Fore.LIGHTRED_EX}1{Fore.RESET} to pick your first favorite''', True)
elif game_input in ['discord', 'd']:
	logger.info('Opening Discord server link...', False)
	webbrowser.open('https://discord.gg/238heBqmZb', new=2, autoraise=True)
	logger.info('Discord server link opened!', True)
elif game_input in ['hide games', 'hide-games', 'h g', 'h-g']:
	utils.change_setting('Hide Games', 'hide-all-except-favs', hide_all_except_favs)
elif game_input in ['options', 'o']:
	logger.info(f'''The current options are:
\'github\' this will bring up the public GitHub repo
\'discord\' this will bring up the public Discord server
\'update notifier\' which toggles the built-in update notifier, this is set to {Fore.LIGHTCYAN_EX}{updatenotifier}{Fore.RESET}
\'change name\' this will toggle how game names are shown on the game select screen, this is set to {Fore.LIGHTCYAN_EX}{configfname}{Fore.RESET}
\'auto update\' which toggles the built-in auto updater, this is {Fore.LIGHTCYAN_EX}{autoupdate}{Fore.RESET}
\'initialize\' this will let you know how long it took Switchence to initialize
\'favorite\' this will let you favorite a game show it shows up 
\'form\' this will bring up the Google form that has questions related to Switchence (please fill it out!)
\'shortcut\' this will tell you how shortcuts work
\'hide games\' this will toggle if the game list will be shown or not, this is set to {Fore.LIGHTCYAN_EX}{hide_all_except_favs}{Fore.RESET}
\'options\' this will bring up this page :P''', True)

#+= sw handling =+#
show_sw_code = input(f'Do you want to show your friend code, SW-{sw} (you can change this by typing \'change\')? ')
show_sw_code = show_sw_code.lower()
if show_sw_code in ['yes', 'y']:
	if sw == '':
		logger.info('Friend code not set, continuing with setting set to off', False)
		show_sw_code = 'n'
elif show_sw_code in ['change', 'c']:
	new_sw_code = input('What is your new friend code (just type the numbers)? ')
	if input(f'Is \'SW-{new_sw_code}\' correct? ')[0] in 'Yy':
		config.update('sw-code', new_sw_code)
		sw = new_sw_code
		logger.info(f'Friend code changed to SW-{new_sw_code}', False)
		show_sw_code = 'y'
	else:
		logger.info('Friend code not changed, continuing with setting set to off', False)
		show_sw_code = 'n'

#+= search for game =+#
# attempt to change game_input to int to see if the user wants to pick a favorite
logger.add_log('Checking to see if user wants to play favorite...')
try:
	game_input_int = int(game_input)
except ValueError:
	logger.add_log('User didn\'t pick favorite game')
	game_input_int = None
if isinstance(game_input_int, int):  # for shortcuts
	logger.add_log('User did pick favorite game')
	game_input = utils.shortcut(game_input_int, favorites)

for details in games['games']:
	details_name = details['name']
	details_fname = details['fname']  # if user has full game name being shown
	if details_name.lower() == game_input:
		logger.add_log('Found game through small game name')
		chosen_game = details_name
		break
	elif details_fname.lower() == game_input:
		logger.add_log('Found game through full game name')
		chosen_game = details_fname
		break
else:
	logger.info(f'The game you specified, {Fore.LIGHTGREEN_EX}{game_input}{Fore.RESET}, is not in the current game list', True)

#+= send info to changePresence function about game picked =+#
for i in games['games']:
	if chosen_game in [i['name'], i['fname']]:
		img = i['name']  # the short game name is the same as the img name
		fname = i['fname']
		if show_sw_code in ['yes', 'y']:
			presence.change_presence(True, img, fname, debug, version, showbutton, sw)
			break
		presence.change_presence(False, img, fname, debug, version, showbutton, sw)
		break


#+= needed to keep program running in background =+#
while True:
	time.sleep(15)
