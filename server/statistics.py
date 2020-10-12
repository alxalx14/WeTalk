# Settings up structure for keeping dynamically allocated inforamtion
stats = {
	"total_connections": 0,
	"total_messages": 0,
	"total_established": 0,
	"total_active": 0
}

# Getters
class Stats:
	def _get_messages():
		return stats["total_messages"]
	
	def _get_connections():
		return stats["total_connections"]
	
	def _get_users():
		return stats["total_active"]
	
	def _get_established():
		return stats["total_established"]

# Listeners
class StatsEvents:
	def _message(func):
		def wrapper(*args):
			stats["total_messages"] += 1
			return func(*args)
		return wrapper
	
	def _connect(func):
		def wrapper(*args):
			stats["total_connections"] += 1
			return func(*args)
		return wrapper
	
	def _establish(func):
		def wrapper(*args):
			stats["total_established"] += 1
			stats["total_active"] += 1
			return func(*args)
		return wrapper

	def _disconnect(func):
		def wrapper(*args):
			stats["total_active"] -= 1
			return func(*args)
		return wrapper