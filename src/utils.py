'''small functions that can be fit here to make `main.py` smaller and more readable'''
import ctypes
import os
import sys
import time
import webbrowser
from colorama import Fore, init
from src.config import config
from src.logger import logger
init()

CURRENT_VERSION = '1.10.0-b9'
BETA_BUILD = True  # forcefully sets Discord Presence to show user is using a beta build
IS_EXE = False


def add_favorite(favorites: list):
	'''
	allows the user to add or remove games from their favorite list

	Parameters
	----------
	favorites : list
		list of user's favorite games
	'''
	if input('Would you like to add or remove a favorite? ').lower().startswith('r'):
		if not favorites:
			logger.info('Your favorite list is currently empty', True)
		remove_ask = input('What game would you like to remove from your favorites? ')
		if remove_ask not in favorites:
			logger.info(f'{remove_ask} is currently not in your favorite list', True)
		favorites.remove(remove_ask)
		config.update('favorites', favorites)
		logger.info(f'Successfully removed {remove_ask} from your favorite list', True)
	else:
		add_ask = input('What game would you like to add to your favorites? ')
		favorites.append(add_ask)
		config.update('favorites', favorites)
		logger.info(f'Successfully added {add_ask} to your favorite list', True)


def change_setting(setting_full_name: str, setting_short_name: str, setting_var: bool) -> bool:
	'''
	change a setting based on multiple variables. made to be used in multiple different ways
	
	Parameters
	----------
	setting_full_name : str
		full name of the setting
	setting_short_name : str
		short name of the setting. used to change the config file
	setting_var : bool
		the variable for the setting. says if the setting is enabled or disabled
	'''
	print(f'\nYour current {setting_full_name} setting is set to {Fore.LIGHTGREEN_EX}{setting_var}{Fore.RESET}')
	ask = input('What would you like to change it to, on or off? ').lower()
	if ask == 'on':
		config.update(setting_short_name, True)
		logger.info(f'Set {setting_full_name} setting to {Fore.LIGHTGREEN_EX}True{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	elif ask == 'off':
		config.update(setting_short_name, False)
		logger.info(f'Set {setting_full_name} setting to {Fore.LIGHTRED_EX}False{Fore.RESET}. Switchence will now restart shortly...', False)
		time.sleep(3)
		reopen()
	else:
		logger.error(f'Keeping {setting_full_name} setting the same since you did not answer correctly')


def change_window_title(title: str):
	'''
	changes the terminal window title
	'''
	if os.name == 'nt':
		ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | {title}')


def clear():
	'''
	just clears the terminal screen
	'''
	os.system('cls' if os.name == 'nt' else 'clear')


def form():
	'''
	opens the survey form
	'''
	logger.info('Opening the form...', False)
	webbrowser.open('https://forms.gle/ofCZ8QXQYxPvTcDE7', new=2, autoraise=True)
	logger.info('Form is now open! Thanks for being willing to fill out the form!', True)


def reopen():
	'''
	reopens Switchence
	'''
	logger.add_log('Attempting to reopen Switchence :/')
	file_name = os.path.basename(__file__)
	if os.path.isfile('Switchence.exe'):  # TODO: add support for if they changed file name lol
		logger.add_log('EXE file found, exiting')
		sys.exit(1)  # TODO: actually reopen exe file lol
	elif '.py' in file_name:  # even exe files are considered .py files :/
		logger.add_log('Attempting to reopen Switchence with python3')
		os.system('python3 main.py')
		logger.add_log('Attempting to reopen Switchence with python')
		os.system('python main.py')  # just in case option above failed
	else:
		logger.add_log('Unknown error while trying to reopen Switchence')
		sys.exit(1)


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
	logger.error('You don\'t have that many favorites in your favorite list. Use the \'shortcut\' command to figure out how shortcuts work')


def yes_no_input(prompt: str) -> bool:
	'''
	given the passed in prompt, it will ask the user for a yes or no answer.
	if the answer starts with a y, returns True. False is returned in any other
	situation
	'''
	return input(prompt).lower().startswith('y')
