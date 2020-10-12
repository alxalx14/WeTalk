import ujson
import hashlib

from ModifiedSocketServer import WebSocket, SimpleWebSocketServer
from statistics import StatsEvents
from Crypto.Random import get_random_bytes
from datetime import datetime
from time import sleep
from threading import Thread

connections = {}


def Serialize(data):
	return ujson.dumps(data)

def Deserialize(data):
	return ujson.loads(data)

def threaded(func):
    def wrapper(*args):
        thread = Thread(target=func, args=(*args, ))
        return thread.start()
    return wrapper

class Utils:
	def _date():
		return datetime.now().strftime("%d/%m/%y %H:%M")


	@StatsEvents._establish
	def _accept(identifier: str, username: str):
		conn = connections[identifier]["conn"]
		conn._username = username
		conn._joined = True
		connections[conn._id]["Username"] = username
		conn.sendMessage(Serialize({
			"Type": "check_username",
			"status": True,
			"message": "Welcome to the chat."
		}))


	def _is_available(username: str) -> bool:
		username = username.replace(" ", "").lower()
		for identifer in connections:
			if connections[identifer]["Username"].replace(" ", "").lower() == username:
				return False
		return True

	@threaded
	def _clean_close(identifier: str):
		try:
			sleep(1) # Sleeping to prevent interfering with client closing
			conn = connections[identifier]["conn"]
			if not conn.closed:
				conn.close()
			connections.pop(identifier)
		except KeyError:
			pass
		

class ChatEvents:
	@threaded
	def _user_joined(identifier: str, data: dict):
		username = data["Username"]
		if not Utils._is_available(username):
			conn = connections[identifier]["conn"]
			conn._duped_user = True
			conn.sendMessage(Serialize({
					"Type": "check_username", 
					"status": False, 
					"message": "Username already in use!"
				}))
			Utils._clean_close(identifier); return

		Utils._accept(identifier, username)
		serialized_data = Serialize({
					"Type": "user_joined",
					"Username": username
				})

		for _identifier in connections:
			connections[_identifier]["conn"].sendMessage(serialized_data)

	@threaded
	def _user_left(username: str):
		serialized_data = Serialize({
				"Type": "user_left",
				"Username": username
			})
		for _identifier in connections:
			connections[_identifier]["conn"].sendMessage(serialized_data)

	@threaded
	def _broadcast_message(identifier: str, data: dict):
		serialized_data = Serialize({
				"Type": "message_receive",
				"Author": data["Author"],
				"Message": data["Message"],
				"Timestamp": Utils._date()
			})
		for _identifier in connections:
			connections[_identifier]["conn"].sendMessage(serialized_data)


class ChatServer(WebSocket):
	@StatsEvents._message
	def handleMessage(self):
		data = Deserialize(self.data)
		return {
			"user_joined": ChatEvents._user_joined,
			"send_message": ChatEvents._broadcast_message
		}.get(data["Type"], lambda: None)(self._id, data)


	@StatsEvents._connect
	def handleConnected(self):
		self._id = hashlib.sha256(get_random_bytes(16)).hexdigest()
		self._join_date =  Utils._date()
		self._joined = False
		self._username = ""
		self._duped_user = False
		connections[self._id] = {
			"conn": self,
			"Username": "",
			"Joined": self._join_date
		}


	@StatsEvents._disconnect
	def handleClose(self):
		if not self._duped_user:
			Utils._clean_close(self._id)

		if self._joined:
			ChatEvents._user_left(self._username)
		
		
