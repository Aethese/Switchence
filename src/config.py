import json
from src.logger import logger

class config:
	'''
	config file handler class. used for updating the config file, and creating a new config file
	'''

	def update(self, change_to):
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
				i[self] = change_to
		with open('config.json', 'w') as jfile:
			json.dump(jFile, jfile, indent=4)

	@staticmethod
	def create(swcode: str, saved_favorites: list, current_version: str):
		'''
		creates a blank config file. returns all of the new changes variables

		Parameters
		----------
		swcode : str
			used to set the sw code (or friend code) for the new config file. can be empty if sw code is not found
		saved_favorites : list
			used to set the new game list for new config file. can be empty if favorite list not found.
			when function is called the variable is either passed as an empty list or current favorite list
		current_version : str
			used to set new version for new config file. will default to current build version if version isn't found.
			when function is called the variable is either passed as the new version or the current build version
		
		Returns
		-------
		sw : str
			friend code
		version : str
			saved local current Switchence version
		updatenotifier : bool
			if the new update triggers a notification on program open
		configfname : bool
			if game full names are printed or not
		showbutton : bool
			setting that enables or disables the button on Discord that promotes Switchence
		autoupdate : bool
			setting to see if the auto update setting is enabled
		hide_all_except_favs : bool
			setting that decides if the entire game list is hidden except favorites or not
		favorites : list
			list of all of the user's saved favorites, or empty if no saved favorites
		'''

		# create settings to save to config file
		configjson = {'config': [{
			'sw-code': swcode,
			'version': current_version,
			'update-notifier': True,
			'fname': False,
			'show-button': True,
			'auto-update': False,
			'hide-all-except-favs': False,
			'favorites': saved_favorites
		}]}

		logger.loading('Loaded settings to save, saving them...', 'yellow')
		# save settings to file
		with open('config.json', 'w') as jsonfile:
			json.dump(configjson, jsonfile, indent=4)
		logger.add_log('Saved settings to file')

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
				hide_all_except_favs = details['hide-all-except-favs']
				favorites = details['favorites']
		logger.loading('Config file settings set! Returning new variables', 'green')

		# return all of the new changes variables
		return sw, version, updatenotifier, configfname, showbutton, autoupdate, hide_all_except_favs, favorites
