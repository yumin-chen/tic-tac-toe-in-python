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
		# Bind to an address (localhost) with the designated port 
		server_socket.bind(("localhost", int(port_number)));
		print("Reserved port ", port_number);

		# Start listening to the binded address
		server_socket.listen(1);
		print("Listening to port ", port_number);

		# Break the while loop if no error is caught
		break;

	except:
		# Caught an error
		print("There is an error when trying to bind localhost::", port_number);

		# Ask the user what to do with the error
		choice = input("[A]bort, [C]hange port, or [R]etry?");

		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			port_number = input("Please enter the port:");

# Define the Player class
class Player:
	def sendMatchInfo(self):
		self.connection.send(("You are now matched with player " + str(self.match.id) + "\nGame is getting started!\nYou are the \"" + self.role + "\"").encode());


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

def gameThread(game):
	# Send both players the match info
	game.player1.sendMatchInfo();
	game.player2.sendMatchInfo();

	# Print the match info onto screen 
	print("Player " + str(game.player1.id) + " is matched with player " + str(game.player2.id) + "\n");

	if(game.player1.connection.recv(1024).decode() == "Ready" and game.player2.connection.recv(1024).decode() == "Ready"):
		print("New game started!");
	else:
		print("Error occured.");

	while True:
		# Send both players the current board content
		game.player1.connection.send(("".join(game.board_content)).encode());
		game.player2.connection.send(("".join(game.board_content)).encode());
		# Let player 1 to move first, Y stands for yes it's turn to move
		game.player1.connection.send("Y".encode());
		game.player2.connection.send("N".encode());
		# Receive the move from player 1
		move = int(game.player1.connection.recv(4).decode());
		# Write the "X" into the board
		game.board_content[move - 1] = "X";

		# Send both players the current board content
		game.player1.connection.send(("".join(game.board_content)).encode());
		game.player2.connection.send(("".join(game.board_content)).encode());
		# Let player 2 to move 
		game.player1.connection.send("N".encode());
		game.player2.connection.send("Y".encode());
		# Receive the move from player 1
		move = int(game.player2.connection.recv(4).decode());
		# Write the "X" into the board
		game.board_content[move - 1] = "O";


# The client thread for each player 
def clientThread(player):
	# Send the welcome message back to the client
	player.connection.send(("Welcome to Tic Tac Toe online, player " + str(player.id) + "\nPlease wait for another player to join the game...").encode());

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
				new_game.board_content = list("123456789");
				# This is for counting turns, as Tic Tac Toe is a turn-based game
				new_game.turns = 0;

				# This thread then deals with the game instead
				gameThread(new_game);

				# End this thread
				return;
		else:
			# If the player has already got matched, end this thread
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