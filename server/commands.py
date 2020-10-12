import colorama
import os

from ModifiedSocketServer import SimpleWebSocketServer, WebSocket
from threading import Thread
from sys import stdout
from server import ChatServer, connections
from statistics import Stats
from prettytable import PrettyTable

COMMANDS = {}

colorama.init()

ServerApplication: SimpleWebSocketServer
ServerStatus: bool = False


def command(**kwargs):
	def wrapper(func):
		COMMANDS[func.__name__] = {
			"function": func,
			"usage": kwargs["usage"],
			"description": kwargs["description"]
		}
		return func
	return wrapper

class Log:
	def __init__(self, name):
		self.name = name

	def Info(self, message):
		stdout.write(f"\n[{colorama.Fore.GREEN}INFO{colorama.Fore.WHITE}] {colorama.Fore.CYAN}{message} {colorama.Fore.WHITE}| {colorama.Fore.CYAN}Function{colorama.Fore.WHITE}: {colorama.Fore.MAGENTA} {self.name}\n\n")

	def Warning(self, message):
		stdout.write(f"\n[{colorama.Fore.YELLOW}WARNING{colorama.Fore.WHITE}] {colorama.Fore.CYAN}{message} {colorama.Fore.WHITE}| {colorama.Fore.CYAN}Function{colorama.Fore.WHITE}: {colorama.Fore.MAGENTA} {self.name}\n\n")

	def Error(self, message):
		stdout.write(f"\n[{colorama.Fore.RED}ERROR{colorama.Fore.WHITE}] {colorama.Fore.CYAN}{message} {colorama.Fore.WHITE}| {colorama.Fore.CYAN}Function{colorama.Fore.WHITE}: {colorama.Fore.MAGENTA} {self.name}\n\n")


@command(
	usage="clear",
	description=f"{colorama.Fore.CYAN}Clears the screen{colorama.Fore.WHITE}."
)
def clear():
	if os.name == "nt":
		os.system("cls"); return
	os.system("clear")

@command(
	usage=f"start_server {colorama.Fore.WHITE}[{colorama.Fore.GREEN}IP{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.GREEN}PORT{colorama.Fore.WHITE}]",
	description=f"{colorama.Fore.CYAN}Starts the chat server on the given port and IP{colorama.Fore.WHITE}."
)
def start_server(host, port):
	log = Log(start_server.__name__)
	try:
		port = int(port)
	except ValueError:
		log.Error(f"Port is not a number{colorama.Fore.WHITE}."); return

	if port > 65535 or port < 1:
		log.Error(f"Port is out of range{colorama.Fore.WHITE}."); return
	try:
		global ServerApplication, ServerStatus
		if ServerStatus:
			log.Error(f"The server is already running{colorama.Fore.WHITE}."); return
		ServerApplication = SimpleWebSocketServer(host, port, ChatServer)
		Thread(target=ServerApplication.serveforever).start()
		ServerStatus = True
	except PermissionError:
		log.Error(f"Could not bind to that port, try again with elevated privileges{colorama.Fore.WHITE}."); return
	except OSError:
		log.Error(f"Could not bind to that IP, check for any typos{colorama.Fore.WHITE}."); return
	except ValueError:
		pass

	log.Info("Server started successfully on: %s:%d" % (host, port))

@command(
	usage="stop_server",
	description=f"{colorama.Fore.CYAN}Stops the chat server and disconnects all clients{colorama.Fore.WHITE}."
)
def stop_server():
	global ServerApplication, ServerStatus
	log = Log(stop_server.__name__)
	if not ServerStatus: 
		log.Error(f"The server is not running{colorama.Fore.WHITE}."); return
	
	ServerApplication.close()
	log.Info(f"Server stopped successfully{colorama.Fore.WHITE}!{colorama.Fore.CYAN}")

@command(
	usage="get_online",
	description=f"{colorama.Fore.CYAN}Displays all active users{colorama.Fore.WHITE}."
)
def get_online():
	user_table = PrettyTable(["Username", "Online since"])
	if len(connections) == 0:
		stdout.write(f"There are no active users at the moment{colorama.Fore.WHITE}.\n")
		return
	for _identifier in connections:
		username = connections[_identifier]["Username"]
		join_date = connections[_identifier]["Joined"]
		user_table.add_row([username, join_date])
	stdout.write(f"""\n{user_table}\n\n""")


@command(
	usage="get_stats",
	description=f"{colorama.Fore.CYAN}Displays all stats of the chat server since it got started{colorama.Fore.WHITE}."
)
def get_stats():
	stdout.write(f"""
			\rTotal connections: {Stats._get_connections()} 
			\rTotal established connections: {Stats._get_established()}
			\rTotal messages: {Stats._get_messages()}
			\rActive users: {Stats._get_users()}
		\n""")


@command(
	usage=f"help {colorama.Fore.WHITE}[{colorama.Fore.GREEN}COMMAND{colorama.Fore.WHITE}](optional)",
	description=f"{colorama.Fore.CYAN}Displays all commands if no argument is supplied{colorama.Fore.WHITE}."
)
def help(command=None):
	if command is None:
		command_table = PrettyTable(["Command", "Usage", "Description"])
		for cmd in COMMANDS:
			this_cmd = COMMANDS[cmd]
			command_table.add_row([f"{colorama.Fore.MAGENTA}{cmd}{colorama.Fore.WHITE}", this_cmd["usage"], this_cmd["description"]])
		stdout.write(f"\n{command_table}\n\n")
		return

	stdout.write(f"""
			\rCommand: {command}
			\rUsage: {COMMANDS[command]["usage"]}
			\rDescription: {COMMANDS[command]["description"]}
		\n""")