import os
import sys
import time
from src import utils
from src.logger import logger
from colorama import Fore, init
init()

try:
	from pypresence import Presence
except ImportError as missing_module:
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'[Error] Module \'{missing_module.name}\' is missing')
	if utils.yes_no_input('Would you like to install all of the required modules? '):
		print('[Info] Installing now...')
		try:
			os.system('pip install --upgrade pip')
			os.system('pip install pypresence')
			os.system('pip install requests')
			os.system('pip install colorama')
			print('\n[Info] Successfully installed all of the required modules! Please restart Switchence')
			sys.exit(0)
		except Exception as error:
			print('Error in installing required modules automatically. Please install them manually. Error below:')
			print(error)
			sys.exit(1)
	else:
		print('[Info] Installation of required modules canceled')
		sys.exit(0)

logger.loading('Attempting to start Rich Presence...', 'yellow')
RPC = Presence('803309090696724554')
RPC.connect()
logger.loading('Successfully started Rich Presence!', 'green')


def looking_for_game(showbutton: bool):
	'''
	sets looking for game status before the user picks a game

	Parameters
	----------
	showbutton : bool
		if the user wants to show a button linking to the GitHub page for Switchence
	'''
	logger.loading('Attempting to set looking for game status...', 'yellow')
	utils.change_window_title('Picking a game')

	start_time = time.time()
	button = [{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}] if showbutton else None
	RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', buttons=button, start=start_time)
	logger.loading('Successfully set looking for game status!', 'green')


def change_presence(swstatus: bool, gameimg: str, gamefname: str, debug: bool, version: str, showbutton: bool, sw: str):
	'''
	changes the presence for Switchence. changes how it updates the RPC depending on if the user wants to
	show friend code and if they want to show a button that will lead anyone to the public GitHub page if they click on it

	Parameters
	----------
	swstatus : bool
		if the friend code is being shown
	gameimg : str
		name of the image to show on discord
	gamefname : str
		full name of the game the user wants to play
	debug : bool
		if debug mode is enabled
	version : str
		local version of Switchence that is installed
	showbutton : bool
		setting for `showbutton` to see
	'''
	start_time = time.time()
	current_time_formatted = time.strftime('%H:%M', time.localtime())

	# set small image to indicate build ran by user is a beta build or not
	if debug or utils.BETA_BUILD:
		small_text = 'Switchence Beta'
		small_img = 'gold_icon'
		logger.add_log('User is running a beta build')
	else:
		small_text = f'Switchence v{version}'
		small_img = 'switch_png'
		logger.add_log('User is not running a beta build')

	button = [{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}] if showbutton else None
	sw_code = f'SW-{sw}' if swstatus else None

	RPC.update(large_image=gameimg, large_text=gamefname, small_image=small_img, small_text=small_text,
		details=gamefname, state=sw_code, buttons=button, start=start_time)
	print(f'Set game to {Fore.LIGHTGREEN_EX}{gamefname}{Fore.RESET} at {current_time_formatted}')

	logger.add_log(f'Set game to {gamefname} at {current_time_formatted}')
	utils.change_window_title(f'Playing {gamefname}')
