# Import the socket module
import socket
# Import multi-threading module
import threading
# Import the time module
import time
# Import command line arguments
from sys import argv

# If there are more than 2 arguments 
if(len(argv) >= 2):
	# Set port number to argument 1
	port_number = argv[1];
else:
	# Ask the user to input port number
	port_number = input("Please enter the port:");

# Create the socket object, the first parameter AF_INET is for IPv4 networking, the second identifies the socket type, SOCK_STREAM is for TCP protocal
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Keep repeating connecting to the server
while True:
	try:
		# Bind to an address with the designated port, the empty string "" is a symbolic name meaning all available interfaces
		server_socket.bind(("", int(port_number)));
		print("Reserved port ", port_number);

		# Start listening to the binded address
		server_socket.listen(1);
		print("Listening to port ", port_number);

		# Break the while loop if no error is caught
		break;

	except:
		# Caught an error
		print("There is an error when trying to bind " + str(port_number));

		# Ask the user what to do with the error
		choice = input("[A]bort, [C]hange port, or [R]etry?");

		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			port_number = input("Please enter the port:");

# Define the Player class
class Player:

	def send(self, command_type, msg):
		# A 1 byte command_type character is put at the front of the message as a communication convention
		try:
			self.connection.send((command_type + msg).encode());
		except:
			# If any error occurred, the connection might be lost
			self.connection_lost();

	def recv(self, size, expected_type):
		try:
			msg = self.connection.recv(size).decode();
			# If received a quit signal from the client
			if(msg[0] == "q"):
				# Print why the quit signal
				print(msg[1:]);
				# Connection lost
				self.connection_lost();
			# If the message is not the expected type
			elif(msg[0] != expected_type):
				# Connection lost
				self.connection_lost();
			# If received an integer from the client
			elif(msg[0] == "i"):
				# Return the integer
				return int(msg[1:]);
			# In other case
			else:
				# Return the message
				return msg[1:];
			# Simply return the raw message if anything unexpected happended because it shouldn't matter any more
			return msg;
		except:
			# If any error occurred, the connection might be lost
			self.connection_lost();
		return None;

	def connection_lost(self):
		# This player has lost connection with the server
		print("Player " + str(self.id) + " connection lost.");
		# Tell the other player that the game is finished
		try:
			self.match.send("Q", "The other player has lost connection with the server.\nGame over.");
		except:
			pass;

	def send_match_info(self):
		# Sent to client the assigned role
		self.send("R", self.role);
		# Waiting for client to confirm
		if(self.recv(2,"c") != "2"):
			self.connection_lost();
		# Sent to client the matched player's ID
		self.send("I", str(self.match.id));
		# Waiting for client to confirm
		if(self.recv(2,"c") != "3"):
			self.connection_lost();

# Define the Game class
class Game:
	pass;

# Create an array object to store connected players
players = [];

# Use a simple lock to synchronize access
lock_matching = threading.Lock();
# This function is to match a player with another one
def matchingPlayer(player):
	# Try acquiring the lock
	lock_matching.acquire();
	try:
		# Loop through each player
		for p in players:
			# If another player is found waiting and its not the player itself
			if(p.isWaiting and p is not player):
				# Matched player with p
				# Set their match
				player.match = p;
				p.match = player;
				# Set their roles
				player.role = "X";
				p.role = "O";
				# Set the player is not waiting any more
				player.isWaiting = False;
				p.isWaiting = False;
				# Then return the player's ID
				return p;
	finally:
		# Release the lock
		lock_matching.release();
	# Return None if nothing is found
	return None;

# Check if the player wins the game. Return value - 1: Win; 0:Draw; -1:No result yet
def checkWinner(game, player):
	s = game.board_content;

	# Check columns
	if(len(set([s[0], s[1], s[2], player.role])) == 1):
		return 1;
	if(len(set([s[3], s[4], s[5], player.role])) == 1):
		return 1;
	if(len(set([s[6], s[7], s[8], player.role])) == 1):
		return 1;

	# Check rows
	if(len(set([s[0], s[3], s[6], player.role])) == 1):
		return 1;
	if(len(set([s[1], s[4], s[7], player.role])) == 1):
		return 1;
	if(len(set([s[2], s[5], s[8], player.role])) == 1):
		return 1;

	# Check diagonal
	if(len(set([s[0], s[4], s[8], player.role])) == 1):
		return 1;
	if(len(set([s[2], s[4], s[6], player.role])) == 1):
		return 1;

	# If there's no empty position left, draw
	if " " not in s:
		return 0;

	# The result cannot be determined yet
	return -1;

# Make a move
def gameMove(game, moving_player, waiting_player):
	# Send both players the current board content
	moving_player.send("B", ("".join(game.board_content)));
	waiting_player.send("B", ("".join(game.board_content)));
	# Let the moving player move, Y stands for yes it's turn to move, and N stands for no and waiting
	moving_player.send("C", "Y");
	waiting_player.send("C", "N");
	# Receive the move from the moving player
	move = int(moving_player.recv(2, "i"));
	# Send the move to the waiting player
	waiting_player.send("I", str(move));
	# Write the "X" into the board
	game.board_content[move - 1] = moving_player.role;
	# Check if this will result in a win
	result = checkWinner(game, moving_player);
	if(result != -1):
		if(result == 0):
			moving_player.send("B", ("".join(game.board_content)));
			waiting_player.send("B", ("".join(game.board_content)));
			moving_player.send("C", "D");
			waiting_player.send("C", "D");
			return True;
		if(result == 1):
			moving_player.send("B", ("".join(game.board_content)));
			waiting_player.send("B", ("".join(game.board_content)));
			moving_player.send("C", "W");
			waiting_player.send("C", "L");
			return True;
		return False;

def gameThread(game):
	# Wrap the whole game thread with a try and catch so that the server would not be affected even if a game messes up
	try:
		# Send both players the match info
		game.player1.send_match_info();
		game.player2.send_match_info();

		# Print the match info onto screen 
		print("Player " + str(game.player1.id) + " is matched with player " + str(game.player2.id));

		while True:
			# Player 1 move
			if(gameMove(game, game.player1, game.player2)):
				return;
			# Player 2 move
			if(gameMove(game, game.player2, game.player1)):
				return;
	except:
		print("Game between " + str(game.player1.id) + " and " + str(game.player2.id) + " is finished unexpectedly.");


# The client thread for each player 
def clientThread(player):
	# Wrap the whole client thread with a try and catch so that the server would not be affected even if a client messes up
	try:
		# Send the player's ID back to the client
		player.send("A", str(player.id));
		# Send the client didn't confirm the message
		if(player.recv(2, "c") != "1"):
			# An error happened
			print("Client didn't confirm the initial message.");
			# Finish 
			return;

		while True:
			# If the player is still waiting for another player to join
			if(player.isWaiting):
				# Try to match this player with other waiting players
				match_result = matchingPlayer(player);

				if(match_result is None):
					# If not matched, wait for a second (to keep CPU usage low) and keep trying
					time.sleep(1);
				else:
					# If matched with another player

					# Initialize a new Game object to store the game's infomation
					new_game = Game();
					# Assign both players
					new_game.player1 = player;
					new_game.player2 = match_result;
					# Create an empty string for empty board content
					new_game.board_content = list("         ");

					# This thread then deals with the game instead
					gameThread(new_game);

					# End this thread
					return;
			else:
				# If the player has already got matched, end this thread
				return;
	except:
		print("Player " + str(player.id) + " disconnected.");
		return;
		

		
# Loop to infinitely accept new clients
while True:
	# Accept a connection from a client
	connection, client_address = server_socket.accept();
	print("Received connection from ", client_address);

	# Initialize a new Player object to store all the client's infomation
	new_player = Player();
	# Generate an id for the client
	new_player.id = len(players) + 1;
	# Assign the corresponding connection 
	new_player.connection = connection;
	# Assign the corresponding client address 
	new_player.client_address = client_address;
	# Set the player waiting status to True
	new_player.isWaiting = True;
	# Push this new player object into the players array
	players.append(new_player);

	# Start a new thread to deal with this client
	threading.Thread(target=clientThread, args=(new_player,)).start();

# Close the socket
server_socket.close();