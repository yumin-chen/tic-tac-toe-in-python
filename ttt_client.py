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

# Print the welcome message from the server
print(client_socket.recv(1024).decode());
# Print the match info from the server
print(client_socket.recv(1024).decode());
# Confirm to the server that this player is ready to start
client_socket.send("Ready".encode());

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
	board_content = client_socket.recv(9).decode();
	# Get the command from the server 
	command = client_socket.recv(1).decode();

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
		client_socket.send(str(position).encode());

	# If the player needs to just wait
	elif(command == "N"):

		# This player waits the other player to make move
		print("Waiting for the other player to make a move...");

		# Get the move that the other player made from the server 
		move = client_socket.recv(1).decode();
		print("Your opponent took up number " + move);

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

	# If the other player lost connection
	elif(command == "Q"):
		print("The other player has lost connection with the server.\nGame over.");
		# Break the loop and finish
		break;

	# If the server sends back anything unrecognizable
	else:
		# Simply print it
		print("Error: unknown message was sent from the server");


# Shut down the socket to prevent further sends/receives
client_socket.shutdown(socket.SHUT_RDWR);

# Close the socket
client_socket.close();