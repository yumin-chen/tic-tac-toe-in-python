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
	address = raw_input('Please enter the address:');
	port_number = raw_input('Please enter the port:');

# Create the socket object, the first parameter AF_INET is for IPv4 networking, the second identifies the socket type, SOCK_STREAM is for TCP protocal
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Keep repeating connecting to the server
while True:

	try:

		print('Connecting to ' + address + "::" + port_number);

		# Connect to the specified host and port 
		client_socket.connect((address, int(port_number)));

		# Break the while loop if no error is caught
		break;

	except:

		# Caught an error
		print('There is an error when trying to connect to ' + address + "::" + port_number);

		# Ask the user what to do with the error
		choice = raw_input('[A]bort, [C]hange address and port, or [R]etry?');

		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			address = raw_input('Please enter the address:');
			port_number = raw_input('Please enter the port:');

while True:
	# Prompt the user to enter the message being sent
	message = raw_input('Please enter the message (q to quit):');

	# Print the message being sent onto the screen
	print(message);

	# Encode the message being sent
	data_out = message.encode();

	# Send the message to the server
	client_socket.send(data_out);

	# If the user enters q, then break the loop and disconnect
	if(message == 'q'):
		break;

	# Receive message from the server with message size being 1024 bytes
	data_in = client_socket.recv(1024);

	# Decode the message being received
	message = data_in.decode();

	# Print the message onto the screen
	print(message);

# Shut down the socket to prevent further sends/receives
client_socket.shutdown(socket.SHUT_RDWR);

# Close the socket
client_socket.close();