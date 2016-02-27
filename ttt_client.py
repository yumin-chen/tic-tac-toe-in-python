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
		print("There is an error when trying to connect to ", address, "::", port_number);

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
	board_content = client_socket.recv(16).decode();

	# Get from the server whether it's my turn to move
	is_my_turn = client_socket.recv(4).decode();

	# If the assigned role is X
	if(is_my_turn == "Y"):

		# Print out the current board with " " converted to the position number
		print("Current board:\n" + formatBoard(convertEmptyBoardPosition(board_content)));

		while True:
			# Prompt the user to enter a position
			position = int(input('Please enter the position (1~9):'));

			if(position >= 1 and position <= 9):
				# If the user input is valid, break the loop
				break;
			# Else, loop until the user enters a valid value

		# Send the position back to the server
		client_socket.send(str(position).encode());

	else:
		# Print out the current board
		print("Current board:\n" + formatBoard(board_content));

		# This player waits the other player to make move
		print("Waiting for the other player to make a move...");


# Shut down the socket to prevent further sends/receives
client_socket.shutdown(socket.SHUT_RDWR);

# Close the socket
client_socket.close();