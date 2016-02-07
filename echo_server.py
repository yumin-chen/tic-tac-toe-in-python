# Import the socket module
import socket
# Import command line arguments
from sys import argv

# If there are more than 2 arguments 
if(len(argv) >= 2):
	# Set port number to argument 1
	port_number = argv[1];
else:
	# Ask the user to input port number
	port_number = raw_input('Please enter the port:');

# Create the socket object, the first parameter AF_INET is for IPv4 networking, the second identifies the socket type, SOCK_STREAM is for TCP protocal
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Keep repeating connecting to the server
while True:

	try:
		# Bind to an address (localhost) with the port being 6666
		server_socket.bind(('localhost', int(port_number)));
		print('Reserved port ' + port_number);

		# Start listening to the binded address
		server_socket.listen(1);
		print('Listening to port ' + port_number);

		# Break the while loop if no error is caught
		break;

	except:
		# Caught an error
		print("There is an error when trying to bind localhost::" + port_number);

		# Ask the user what to do with the error
		choice = raw_input('[A]bort, [C]hange port, or [R]etry?');

		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			port_number = raw_input('Please enter the port:');

# Accept a connection from a client
connection, client_address = server_socket.accept();
print('Received connection from ' + str(client_address));

while True:

	# Receive message from the connected client with message size being 1024 bytes
	data_in = connection.recv(1024);

	# Decode the message being received
	message = data_in.decode();

	# If the client sends 'q', then break the loop and disconnect
	if(message == 'q'):
		break;

	# Print the message onto the screen
	print('Received message:' + message);

	# Send the data back to the client
	connection.send(message.encode());

# Close the socket
server_socket.close();