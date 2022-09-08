import os
import requests
from src import utils
from src.config import config
from src.logger import logger

def update_program(online_ver: str, current_file: str, in_debug_mode: bool):
	'''
	automatically updates Switchence by pulling the latest raw file from GitHub to update to

	Parameters
	----------
	online_ver : str
		the newest version number
	current_file : str
		the path to the current file
	in_debug_mode : bool
		if the program is in debug mode. if in debug mode it stops the update
	'''

	utils.change_window_title(f'Updating to version {online_ver}')
	logger.info(f'Updating to version {online_ver}...', False)

	if utils.BETA_BUILD or in_debug_mode:
		logger.info('Canceled auto updater because in beta or in debug, skipping update', False)
		return

	# look in the parent folder to see if the exe file exists
	if os.path.isfile('Switchence.exe'):
		config.update('auto-update', False)
		logger.info('The exe file does not currently support auto updating', True)

	# request the up-to-date files from GitHub
	logger.info('Getting online files...', False)
	# online files
	beginning_link = 'https://raw.githubusercontent.com/Aethese/Switchence/main/'
	online_main = requests.get(f'{beginning_link}main.py')
	online_config = requests.get(f'{beginning_link}src/config.py')
	online_log = requests.get(f'{beginning_link}src/log.py')
	online_presence = requests.get(f'{beginning_link}src/presence.py')
	online_utils = requests.get(f'{beginning_link}src/utils.py')
	logger.info('Online files obtained', False)

	status_codes = [
		online_main.status_code,
		online_config.status_code,
		online_log.status_code,
		online_presence.status_code,
		online_utils.status_code,
	]

	# check the status codes to see if any are not 200
	for status_code in status_codes:
		if status_code != 200:
			logger.add_log(f'Current status code: {status_code}')
			logger.error(f'Status code is not 200, it is {status_code}, so the program will not update')

	# get binary version of raw code
	# thanks to https://stackoverflow.com/users/13155625/dawid-januszkiewicz
	# for getting this to work!
	logger.info('Getting binary version of online files...', False)
	online_main_binary = online_main.content
	online_config_binary = online_config.content
	online_log_binary = online_log.content
	online_presence_binary = online_presence.content
	online_utils_binary = online_utils.content
	logger.info('Binary files obtained, updating files...', False)

	# update all of the files
	with open(current_file, 'wb') as main_file:
		main_file.write(online_main_binary)

	with open('src/config.py', 'wb') as config_file:
		config_file.write(online_config_binary)

	with open('src/log.py', 'wb') as log_file:
		log_file.write(online_log_binary)

	with open('src/presence.py', 'wb') as presence_file:
		presence_file.write(online_presence_binary)

	with open('src/utils.py', 'wb') as utils_file:
		utils_file.write(online_utils_binary)
	logger.info('Updated all of the files', False)

	# update files and prompt to reopen Switchence
	config.update('version', online_ver)
	utils.change_window_title(f'Updated to version {online_ver}')
	if input('Would you like to reopen Switchence? ')[0] in 'Yy':
		utils.reopen()
	logger.info(f'Finished updating to version {online_ver}', True)