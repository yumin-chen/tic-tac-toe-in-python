# Import the socket module
import socket
# Import command line arguments
from sys import argv

# If there are more than 3 arguments 
if(len(argv) >= 3):
	# Set the address to argument 1, and port number to argument 2
	address = argv[1];
	port_number = argv[2];
else:
	# Ask the user to input the address and port number
	address = input("Please enter the address:");
	port_number = input("Please enter the port:");

# Create the socket object, the first parameter AF_INET is for IPv4 networking, the second identifies the socket type, SOCK_STREAM is for TCP protocal
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Keep repeating connecting to the server
while True:
	try:
		print("Connecting to the game server...");

		# Connect to the specified host and port 
		client_socket.connect((address, int(port_number)));

		# Break the while loop if no error is caught
		break;

	except:
		# Caught an error
		print("There is an error when trying to connect to " + str(address) + "::" + str(port_number));

		# Ask the user what to do with the error
		choice = input("[A]bort, [C]hange address and port, or [R]etry?");

		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			address = input("Please enter the address:");
			port_number = input("Please enter the port:");

# Connection lost
def connection_lost():
	print("Error: connection lost.");
	try:
		# Try and send a message back to the server to notify connection lost
		client_socket.send("q".encode());
	except:
		raise;

# Safe communication convention to send message
def s_send(command_type, msg):
	# A 1 byte command_type character is put at the front of the message as a communication convention
	try:
		client_socket.send((command_type + msg).encode());
	except:
		# If any error occurred, the connection might be lost
		connection_lost();

# Safe communication convention to receive message
def s_recv(size, expected_type):
	try:
		msg = client_socket.recv(size).decode();
		# If received a quit signal from the server
		if(msg[0] == "Q"):
			# Print the resaon
			print(msg[1:]);
			# Connection lost
			connection_lost();
		# If the message is not the expected type
		elif(msg[0] != expected_type):
			# Connection lost
			connection_lost();
		# If received an integer from the server
		elif(msg[0] == "I"):
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
		connection_lost();
	return None;

# Receive the player's ID from the server
player_id = int(s_recv(128, "A"));
# Confirm the ID has been received
s_send("c","1");

print("Welcome to Tic Tac Toe online, player " + str(player_id) + "\nPlease wait for another player to join the game...");

# Receive the assigned role from the server
role = str(s_recv(2, "R"));
# Confirm the assigned role has been received
s_send("c","2");

# Receive the mactched player's ID from the server
match_id = int(s_recv(128, "I"));
# Confirm the mactched player's ID has been received
s_send("c","3");

print(("You are now matched with player " + str(match_id) + "\nGame is getting started!\nYou are the \"" + role + "\""));

# This functon converts empty board position " " to its corresponding position index
def convertEmptyBoardPosition(s):
	new_s = list("123456789");
	for i in range(0, 8):
		if(s[i] != " "):
			new_s[i] = s[i];
	return "".join(new_s);

# Format the Grid Board
def formatBoard(s):
	# If the length of the string is not 9
	if(len(s) != 9):
		# Then print out an error message
		print("Error: there should be 9 symbols.");
		return "";

	# Draw the grid board
	#print("|1|2|3|");
	#print("|4|5|6|");
	#print("|7|8|9|");
	return "|" + s[0] + "|" + s[1]  + "|" + s[2] + "|\n" + "|" + s[3] + "|" + s[4]  + "|" + s[5] + "|\n" + "|" + s[6] + "|" + s[7]  + "|" + s[8] + "|\n";

while True:

	# Get the board content from the server
	board_content = s_recv(10, "B");
	# Get the command from the server 
	command = s_recv(2, "C");

	# If it's this player's turn to move
	if(command == "Y"):
		# Print out the current board with " " converted to the position number
		print("Current board:\n" + formatBoard(convertEmptyBoardPosition(board_content)));
	else:
		# Print out the current board
		print("Current board:\n" + formatBoard(board_content));

	# If it's this player's turn to move
	if(command == "Y"):
		while True:
			# Prompt the user to enter a position
			position = int(input('Please enter the position (1~9):'));

			if(position >= 1 and position <= 9):

				if(board_content[position - 1] != " "):
					# If the position is already been taken, print out a warning
					print("That position has already been taken. Please choose another one.");

				else:
					# If the user input is valid, break the loop
					break;
			else:
				print("Please enter a value between 1 and 9 that corresponds to the position on the grid board.");
			# Else, loop until the user enters a valid value

		# Send the position back to the server
		s_send("i", str(position));

	# If the player needs to just wait
	elif(command == "N"):

		# This player waits the other player to make move
		print("Waiting for the other player to make a move...");

		# Get the move that the other player made from the server 
		move = s_recv(2, "I");
		print("Your opponent took up number " + str(move));

	# If the result is a draw
	elif(command == "D"):
		print("It's a draw.");
		break;

	# If this player wins
	elif(command == "W"):
		print("You WIN!");
		# Break the loop and finish
		break;

	# If this player loses
	elif(command == "L"):
		print("You lose.");
		# Break the loop and finish
		break;

	# If the server sends back anything unrecognizable
	else:
		# Simply print it
		print("Error: unknown message was sent from the server");
		# And finish
		break;


# Shut down the socket to prevent further sends/receives
client_socket.shutdown(socket.SHUT_RDWR);

# Close the socket
client_socket.close();