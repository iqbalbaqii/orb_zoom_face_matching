from notifypy import Notify

class Alert:

	# Toast like in JS but hit to OS

	def __init__(self):
		self.notification = Notify()
		
	def send(self, title:str, body:str):
		self.notification.title = title
		self.notification.message = body
		self.notification.send(block=False)

