#! /usr/bin/python3

# Import the socket module
import socket
# Import multi-threading module
import threading
# Import the time module
import time
# Import command line arguments
from sys import argv
# Import logging
import logging


# Set up logging to file 
logging.basicConfig(level=logging.DEBUG,
	format='[%(asctime)s] %(levelname)s: %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	filename='ttt_server.log');
# Define a Handler which writes INFO messages or higher to the sys.stderr
# This will print all the INFO messages or higer at the same time
console = logging.StreamHandler();
console.setLevel(logging.INFO);
# Add the handler to the root logger
logging.getLogger('').addHandler(console);

class TTTServer:
	"""TTTServer deals with networking and communication with the TTTClient."""

	def __init__(self):
		"""Initializes the server object with a server socket."""
		# Create a TCP/IP socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	def bind(self, port_number):
		"""Binds the server with the designated port and start listening to
		the binded address."""
		while True:
			try:
				# Bind to an address with the designated port
				# The empty string "" is a symbolic name 
				# meaning all available interfaces
				self.server_socket.bind(("", int(port_number)));
				logging.info("Reserved port " + str(port_number));
				# Start listening to the binded address
				self.server_socket.listen(1);
				logging.info("Listening to port " + str(port_number));
				# Break the while loop if no error is caught
				break;
			except:
				# Caught an error
				logging.warning("There is an error when trying to bind " + 
					str(port_number));
				# Ask the user what to do with the error
				choice = input("[A]bort, [C]hange port, or [R]etry?");
				if(choice.lower() == "a"):
					exit();
				elif(choice.lower() == "c"):
					port_number = input("Please enter the port:");

	def close(self):
		# Close the socket
		self.server_socket.close();

class TTTServerGame(TTTServer):
	"""TTTServerGame deals with the game logic on the server side."""

	def __init__(self):
		"""Initializes the server game object."""
		TTTServer.__init__(self);

	def start(self):
		"""Starts the server and let it accept clients."""
		# Create an array object to store connected players
		self.waiting_players = [];
		# Use a simple lock to synchronize access when matching players
		self.lock_matching = threading.Lock();
		# Start the main loop
		self.__main_loop();

	def __main_loop(self):
		"""(Private) The main loop."""
		# Loop to infinitely accept new clients
		while True:
			# Accept a connection from a client
			connection, client_address = self.server_socket.accept();
			logging.info("Received connection from " + str(client_address));

			# Initialize a new Player object to store all the client's infomation
			new_player = Player(connection);
			# Push this new player object into the players array
			self.waiting_players.append(new_player);

			try:
				# Start a new thread to deal with this client
				threading.Thread(target=self.__client_thread, 
					args=(new_player,)).start();
			except:
				logging.error("Failed to create thread.");

	def __client_thread(self, player):
		"""(Private) This is the client thread."""
		# Wrap the whole client thread with a try and catch so that the 
		# server would not be affected even if a client messes up
		try:
			# Send the player's ID back to the client
			player.send("A", str(player.id));
			# Send the client didn't confirm the message
			if(player.recv(2, "c") != "1"):
				# An error happened
				logging.warning("Client " + str(player.id) + 
					" didn't confirm the initial message.");
				# Finish 
				return;

			while player.is_waiting:
				# If the player is still waiting for another player to join
				# Try to match this player with other waiting players
				match_result = self.matching_player(player);

				if(match_result is None):
					# If not matched, wait for a second (to keep CPU usage low) 
					time.sleep(1);
					# Check if the player is still connected
					player.check_connection();
				else:
					# If matched with another player

					# Initialize a new Game object to store the game's infomation
					new_game = Game();
					# Assign both players
					new_game.player1 = player;
					new_game.player2 = match_result;
					# Create an empty string for empty board content
					new_game.board_content = list("         ");

					try:
						# Game starts
						new_game.start();
					except:
						logging.warning("Game between " + str(new_game.player1.id) + 
							" and " + str(new_game.player2.id) + 
							" is finished unexpectedly.");
					# End this thread
					return;
		except:
			print("Player " + str(player.id) + " disconnected.");
		finally:
			# Remove the player from the waiting list
			self.waiting_players.remove(player);

	def matching_player(self, player):
		"""Goes through the players list and try to match the player with 
		another player who is also waiting to play. Returns any matched 
		player if found."""
		# Try acquiring the lock
		self.lock_matching.acquire();
		try:
			# Loop through each player
			for p in self.waiting_players:
				# If another player is found waiting and its not the player itself
				if(p.is_waiting and p is not player):
					# Matched player with p
					# Set their match
					player.match = p;
					p.match = player;
					# Set their roles
					player.role = "X";
					p.role = "O";
					# Set the player is not waiting any more
					player.is_waiting = False;
					p.is_waiting = False;
					# Then return the player's ID
					return p;
		finally:
			# Release the lock
			self.lock_matching.release();
		# Return None if nothing is found
		return None;

class Player:
	"""Player class describes a client with connection to the server and
	as a player in the tic tac toe game."""

	# Count the players (for generating unique IDs)
	count = 0;

	def __init__(self, connection):
		"""Initialize a player with its connection to the server"""
		# Generate a unique id for this player
		Player.count = Player.count + 1
		self.id = Player.count;
		# Assign the corresponding connection 
		self.connection = connection;
		# Set the player waiting status to True
		self.is_waiting = True;	

	def send(self, command_type, msg):
		"""Sends a message to the client with an agreed command type token 
		to ensure the message is delivered safely."""
		# A 1 byte command_type character is put at the front of the message
		# as a communication convention
		try:
			self.connection.send((command_type + msg).encode());
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost();

	def recv(self, size, expected_type):
		"""Receives a packet with specified size from the client and check 
		its integrity by comparing its command type token with the expected
		one."""
		try:
			msg = self.connection.recv(size).decode();
			# If received a quit signal from the client
			if(msg[0] == "q"):
				# Print why the quit signal
				logging.info(msg[1:]);
				# Connection lost
				self.__connection_lost();
			# If the message is not the expected type
			elif(msg[0] != expected_type):
				# Connection lost
				self.__connection_lost();
			# If received an integer from the client
			elif(msg[0] == "i"):
				# Return the integer
				return int(msg[1:]);
			# In other case
			else:
				# Return the message
				return msg[1:];
			# Simply return the raw message if anything unexpected happended 
			# because it shouldn't matter any more
			return msg;
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost();
		return None;

	def check_connection(self):
		"""Sends a meesage to check if the client is still properly connected."""
		# Send the client an echo signal to ask it to repeat back
		self.send("E", "z");
		# Check if "e" gets sent back
		if(self.recv(2, "e") != "z"):
			# If the client didn't confirm, the connection might be lost
			self.__connection_lost();

	def send_match_info(self):
		"""Sends a the matched information to the client, which includes
		the assigned role and the matched player."""
		# Send to client the assigned role
		self.send("R", self.role);
		# Waiting for client to confirm
		if(self.recv(2,"c") != "2"):
			self.__connection_lost();
		# Sent to client the matched player's ID
		self.send("I", str(self.match.id));
		# Waiting for client to confirm
		if(self.recv(2,"c") != "3"):
			self.__connection_lost();

	def __connection_lost(self):
		"""(Private) This function will be called when the connection is lost."""
		# This player has lost connection with the server
		logging.warning("Player " + str(self.id) + " connection lost.");
		# Tell the other player that the game is finished
		try:
			self.match.send("Q", "The other player has lost connection" + 
				" with the server.\nGame over.");
		except:
			pass;
		# Raise an error so that the client thread can finish
		raise Exception;

class Game:
	"""Game class describes a game with two different players."""

	def start(self):
		"""Starts the game."""
		# Send both players the match info
		self.player1.send_match_info();
		self.player2.send_match_info();

		# Print the match info onto screen 
		logging.info("Player " + str(self.player1.id) + 
			" is matched with player " + str(self.player2.id));

		while True:
			# Player 1 move
			if(self.move(self.player1, self.player2)):
				return;
			# Player 2 move
			if(self.move(self.player2, self.player1)):
				return;

	def move(self, moving_player, waiting_player):
		"""Lets a player make a move."""
		# Send both players the current board content
		moving_player.send("B", ("".join(self.board_content)));
		waiting_player.send("B", ("".join(self.board_content)));
		# Let the moving player move, Y stands for yes it's turn to move, 
		# and N stands for no and waiting
		moving_player.send("C", "Y");
		waiting_player.send("C", "N");
		# Receive the move from the moving player
		move = int(moving_player.recv(2, "i"));
		# Send the move to the waiting player
		waiting_player.send("I", str(move));
		# Check if the position is empty
		if(self.board_content[move - 1] == " "):
			# Write the it into the board
		 	self.board_content[move - 1] = moving_player.role;
		else:
			logging.warning("Player " + str(moving_player.id) + 
				" is attempting to take a position that's already " + 
				"been taken.");
		# 	# This player is attempting to take a position that's already
		# 	# taken. HE IS CHEATING, KILL HIM!
		# 	moving_player.send("Q", "Please don't cheat!\n" + 
		# 		"You are running a modified client program.");
		# 	waiting_player.send("Q", "The other playing is caught" + 
		# 		"cheating. You win!");
		# 	# Throw an error to finish this game
		# 	raise Exception;

		# Check if this will result in a win
		result, winning_path = self.check_winner(moving_player);
		if(result >= 0):
			# If there is a result
			# Send back the latest board content
			moving_player.send("B", ("".join(self.board_content)));
			waiting_player.send("B", ("".join(self.board_content)));

			if(result == 0):
				# If this game ends with a draw
				# Send the players the result
				moving_player.send("C", "D");
				waiting_player.send("C", "D");
				print("Game between player " + str(self.player1.id) + " and player " 
					+ str(self.player2.id) + " ends with a draw.");
				return True;
			if(result == 1):
				# If this player wins the game
				# Send the players the result
				moving_player.send("C", "W");
				waiting_player.send("C", "L");
				# Send the players the winning path
				moving_player.send("P", winning_path);
				waiting_player.send("P", winning_path);
				print("Player " + str(self.player1.id) + " beats player " 
					+ str(self.player2.id) + " and finishes the game.");
				return True;
			return False;

	def check_winner(self, player):
		"""Checks if the player wins the game. Returns 1 if wins, 
		0 if it's a draw, -1 if there's no result yet."""
		s = self.board_content;

		# Check columns
		if(len(set([s[0], s[1], s[2], player.role])) == 1):
			return 1, "012";
		if(len(set([s[3], s[4], s[5], player.role])) == 1):
			return 1, "345";
		if(len(set([s[6], s[7], s[8], player.role])) == 1):
			return 1, "678";

		# Check rows
		if(len(set([s[0], s[3], s[6], player.role])) == 1):
			return 1, "036";
		if(len(set([s[1], s[4], s[7], player.role])) == 1):
			return 1, "147";
		if(len(set([s[2], s[5], s[8], player.role])) == 1):
			return 1, "258";

		# Check diagonal
		if(len(set([s[0], s[4], s[8], player.role])) == 1):
			return 1, "048";
		if(len(set([s[2], s[4], s[6], player.role])) == 1):
			return 1, "246";

		# If there's no empty position left, draw
		if " " not in s:
			return 0, "";

		# The result cannot be determined yet
		return -1, "";

# Define the main program
def main():
	# If there are more than 2 arguments 
	if(len(argv) >= 2):
		# Set port number to argument 1
		port_number = argv[1];
	else:
		# Ask the user to input port number
		port_number = input("Please enter the port:");

	try:
		# Initialize the server object
		server = TTTServerGame();
		# Bind the server with the port 
		server.bind(port_number);
		# Start the server
		server.start();
		# Close the server
		server.close();
	except BaseException as e:
		logging.critical("Server critical failure.\n" + str(e));

if __name__ == "__main__":
	# If this script is running as a standalone program,
	# start the main program.
	main();

