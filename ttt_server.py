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
	pass;

# Create an array object to store connected players
players = [];

# Use a simple lock to synchronize access
lock_matching = threading.Lock();
# This function is to match a player with another one
def matchingPlayer(player):
	lock_matching.acquire();
	try:
		# Loop through each player
		for p in players:
			# If another player is found waiting and its not the player itself
			if(p.isWaiting and p.id != player.id):
				# Matched player with p
				# Set the player's the match
				player.match = p;
				p.match = player;
				# Set the player is not waiting any more
				player.isWaiting = False;
				p.isWaiting = False;
				# Then return the player's ID
				return p;
	finally:
		lock_matching.release();
	# Return None if nothing is found
	return None;

# The client thread for each player 
def clientThread(player):
	# Send the welcome message back to the client
	player.connection.send("Welcome to Tic Tac Toe online\nPlease wait for another player to join the game...".encode());

	while True:
		# If the player is still waiting for another player to join
		if(player.isWaiting):
			# Try to match this player with other waiting players
			match_result = matchingPlayer(player);

			if(match_result is None):
				# If not matched, wait for a second (to keep CPU usage low) and keep trying
				time.sleep(1);
			else:
				# If matched with another player, send both players message to notify that game is starting
				player.connection.send(("You are now matched with player " + str(match_result.id) + "\nGame is getting started!\n").encode());
				match_result.connection.send(("You are now matched with player " + str(player.id) + "\nGame is getting started!\n").encode());


		
# Loop to infinitely accept new clients
while True:
	# Accept a connection from a client
	connection, client_address = server_socket.accept();
	print("Received connection from ", client_address);

	# Initialize a new Player object to store all the client's infomation
	new_player = Player();
	# Generate an id for the client
	new_player.id = 10000 + len(players);
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