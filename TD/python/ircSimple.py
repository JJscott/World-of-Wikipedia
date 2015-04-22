irc_user = "imabot"
irc_real_name = "Mr. Bottington"
irc_channels = ["#en.wikipedia"]

import asyncore, socket, threading, time, re, inspect, queue
from collections import deque
import re

message_regex = re.compile(r'(?:\:[a-zA-Z0-9\.]+)*\s(?P<command>[a-zA-Z0-9]+)\s(?P<params>.+)')
magic_regex = re.compile(r'\[\[(?P<title>.*)\]\].*(?P<url>http\://\S+)\s\*\s(?P<user>\S+)\s\*\s.*')
# magic_regex = re.compile(ur'\:14\[\[07(?P<title>.+)14\]\]4.+03(?P<user>.+)\s5')

"""Store data from an event received from our IRC watcher."""
re_color = re.compile("\x03([0-9]{1,2}(,[0-9]{1,2})?)?")

crlf = "\r\n"

class IRC(asyncore.dispatcher):
	class IRCcommands(object):
		def ping(self, irc, params, msg):
			print("ping!")

		# This is probably going to be the reply
		def auth(self, irc, params, msg):
			pass

		def notice(self, irc, params, msg):
			# https://tools.ietf.org/html/rfc2812#section-3.3.2
			pass

		# These could be handy for confirming you're actually
		# in the channel, or tracking other users in the channel
		def join(self, irc, params, msg):
			pass
		def quit(self, irc, params, msg):
			pass

		# The money-shot. Enjoy.
		def privmsg(self, irc, params, msg):
			# """Parse a recent change event into some variables."""
			# # Strip IRC color codes; we don't want or need 'em:
			msg = re_color.sub("", params).strip()
			# magic

			# The magic
			magic = re.search(magic_regex, msg)
			if magic != None:
				title = magic.group("title")
				user = magic.group("user")
				irc.on_msg_recv(user, title)
				# print title, ' ', userx
			# else :
				# print "could not match: '{0}' against '{1}'".format(magic_regex, params)


		# https://tools.ietf.org/html/rfc2812#section-5.1 - aka hell
		# these are all command responses.
		# we can basically ignore all these.
		def r_001(self, irc, params, msg):
			pass
		def r_002(self, irc, params, msg):
			pass
		def r_003(self, irc, params, msg):
			pass
		def r_004(self, irc, params, msg):
			pass
		def r_005(self, irc, params, msg):
			pass
		def r_250(self, irc, params, msg):
			pass
		def r_251(self, irc, params, msg):
			pass
		def r_252(self, irc, params, msg):
			pass
		def r_253(self, irc, params, msg):
			pass
		def r_254(self, irc, params, msg):
			pass
		def r_255(self, irc, params, msg):
			pass
		def r_256(self, irc, params, msg):
			pass
		def r_256(self, irc, params, msg):
			pass
		def r_265(self, irc, params, msg):
			pass
		def r_266(self, irc, params, msg):
			pass
		def r_353(self, irc, params, msg):
			pass
		def r_366(self, irc, params, msg):
			pass
		def r_372(self, irc, params, msg):
			pass
		def r_375(self, irc, params, msg):
			pass

		# MOTD
		# We use this command response to know we're good to go.
		def r_376(self, irc, params, msg):
			irc.command_ready = True

	irc_commands = IRCcommands()
	commands = {}
	for n, v in inspect.getmembers(irc_commands, inspect.ismethod):
		commands[n] = v

	buffer = deque()
	socket_ready = False
	command_ready = False

	message_buffer = ""

	on_msg_recv = None

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, port) )

	def handle_connect(self):
		self.socket_ready = True

	def handle_close(self):
		self.close()

	def handle_read(self):
		t_msg = self.recv(8192)
		self.message_buffer += t_msg

		while crlf in self.message_buffer:
			splits = self.message_buffer.split(crlf, 1)

			self.message_buffer = splits[1]

			msg = splits[0]

			# print "Msg: {0}".format(msg)

			match = re.search(message_regex, msg)
			if match == None:
				return

			command = match.group("command").lower()
			params = match.group("params")

			if command[0].isdigit():
				command = "r_" + command

			if command in self.commands:
				self.commands[command](self, params, msg)
			else:
				print("Unknown command: {0}".format(command))
				# print "Message: {0}".format(msg)

	def writable(self):
		return len(self.buffer) > 0

	def handle_write(self):
		msg = self.buffer.popleft()
		sent = self.send(msg)
		# print "2> Wrote {0} bytes".format(sent)
		msg = msg[sent:]

		if len(msg) > 0:
			self.buffer.appendleft(msg)

	def enqueue_send(self, msg):
		if len(msg) > 0:
			self.buffer.append("{0}\r\n".format(msg))

	def stop(self):
		self.close()

class IRCrecv(object):
	def __init__(self):
		self.to_process = queue.Queue()

	def msg_recv(self, user, title):
		# print "msg: {0},{1}".format(user, title)
		self.to_process.put((user, title))

	def stop(self):
		self.irc.stop()
		self.thread.join()

	def start(self):
		self.irc = IRC('irc.wikimedia.org', 6667)

		#TODO: You should start a proper thread, and put some exception
		# handling around the call to asyncore.loop.
		self.thread = threading.Thread(target=asyncore.loop,kwargs = {'timeout':1} )
		self.thread.start()

		while self.irc.socket_ready == False:
			time.sleep(1)

		self.irc.enqueue_send("PASS *")
		self.irc.enqueue_send("NICK {0}".format(irc_user))
		self.irc.enqueue_send("USER {0} 8 * :{1}".format(irc_user, irc_real_name))

		while self.irc.command_ready == False:
			time.sleep(1)

		for channel in irc_channels:
			self.irc.enqueue_send("JOIN {0}".format(channel))

		self.irc.on_msg_recv = self.msg_recv

		# while True:
		#     if len(self.to_process) == 0:
		#         time.sleep(1)

		#     # grab one and get to work I guess.
		#     # this is happening on a different thread.

		# self.irc.stop()

	def getLatest(self):
		latest = []
		while not self.to_process.empty():
			latest.append(self.to_process.get())
		return latest

def newBot():
	return IRCrecv()

# client = IRCrecv()
# client.start()
# client.stop()