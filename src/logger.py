'''logging functions for Switchence'''
import time
import sys
import webbrowser
from colorama import Fore, init
from src import utils
init()

# var to hold logs until ready to save to file
logs = []


class logger:
	'''
	custom logging class to log error logs, info logs, loading logs, and saves logs to file
	'''
	def __init__(self, text: str, color: str):
		self.text = text
		self.color = color

	@staticmethod
	def return_logs():
		'''
		returns the logs in a formatted way. just newline after every log lol
		'''

		return '\n'.join(logs)

	@staticmethod
	def save_logs():
		'''
		saves current logs to file when terminal closes
		'''

		with open('logs.switchence', 'w') as log_file:
			all_logs = logger.return_logs()
			log_file.write(all_logs)

	def add_log(log_to_add: str):
		'''
		adds to local logs variable the newly added log

		Parameters
		----------
		log_to_add : str
			the log message that will be formatted then logged
		'''

		current_time = time.strftime('%H:%M:%S', time.localtime())
		# format looks like this: TIME(15:15:15) - LOG_MESSAGE
		log_message = f'{current_time} - {log_to_add} - [{len(logs)}]'
		logs.append(log_message)

		logger.save_logs()  # sadly have to run this every after every log

	def error(text: str):
		'''
		Parameters
		----------
		text : str
			the text that is printed when logged
		'''

		utils.change_window_title('Error')
		utils.clear()
		error_text_plain = f'[Error] {text}'
		logger.add_log(error_text_plain)
		print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {text}')
		print('Please report this error on the Switchence GitHub issue page if this error happens consistently')
		time.sleep(1)
		webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
		sys.exit(1)

	def info(text: str, close: bool):  # second param is for if i want switchence to close after printing info
		'''
		Parameters
		----------
		text : str
			the text that is printed when logged
		close : bool
			decides if the program closes or not after logging the message
		'''

		utils.change_window_title('Info')
		info_text_plain = f'[Info] {text}'
		logger.add_log(info_text_plain)
		print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
		if close:
			utils.clear()
			print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
			sys.exit(0)

	def loading(text: str, color: str):  # color is the color of the loading text
		'''
		Parameters
		----------
		text : str
			the text that is printed when logged
		color : str
			can pick between green, yellow or red as the logged color text
		'''

		if color == 'green':
			color = Fore.LIGHTGREEN_EX
		elif color == 'yellow':
			color = Fore.LIGHTYELLOW_EX
		else:
			color = Fore.LIGHTRED_EX
		loading_text_plain = f'[Loading] {text}'
		logger.add_log(loading_text_plain)
		print(f'{Fore.LIGHTCYAN_EX}[Loading] {color}{text}{Fore.RESET}')

logger.add_log('Switchence Logger initialized')
