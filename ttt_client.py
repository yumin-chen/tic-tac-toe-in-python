# Import the socket module
import socket
# Import command line arguments
from sys import argv

class TTTClient:
	"""TTTClient deals with networking and communication with the TTTServer."""

	def __init__(self):
		"""Initializes the client and create a client socket."""
		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	def connect(self, address, port_number):
		"""Keeps repeating connecting to the server and returns True if 
		connected successfully."""
		while True:
			try:
				print("Connecting to the game server...");
				# Connect to the specified host and port 
				self.client_socket.connect((address, int(port_number)));
				# Return True if connected successfully
				return True;
			except:
				# Caught an error
				print("There is an error when trying to connect to " + 
					str(address) + "::" + str(port_number));
				self.__connect_failed__();
		return False;

	def __connect_failed__(self):
		"""(Private) This function will be called when the attempt to connect
		failed. This function might be overridden by the GUI program."""
		# Ask the user what to do with the error
		choice = input("[A]bort, [C]hange address and port, or [R]etry?");
		if(choice.lower() == "a"):
			exit();
		elif(choice.lower() == "c"):
			address = input("Please enter the address:");
			port_number = input("Please enter the port:");

	def s_send(self, command_type, msg):
		"""Sends a message to the server with an agreed command type token 
		to ensure the message is delivered safely."""
		# A 1 byte command_type character is put at the front of the message
		# as a communication convention
		try:
			self.client_socket.send((command_type + msg).encode());
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost();

	def s_recv(self, size, expected_type):
		"""Receives a packet with specified size from the server and check 
		its integrity by comparing its command type token with the expected
		one."""
		try:
			msg = self.client_socket.recv(size).decode();
			# If received a quit signal from the server
			if(msg[0] == "Q"):
				why_quit = "";
				try:
					# Try receiving the whole reason why quit
					why_quit = self.client_socket.recv(1024).decode();
				except:
					pass;
				# Print the resaon
				print(msg[1:] + why_quit);
				# Throw an error
				raise Exception;
			# If the command type token is not the expected type
			elif(msg[0] != expected_type):
				# Connection lost
				self.__connection_lost();
			# If received an integer from the server
			elif(msg[0] == "I"):
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

	def __connection_lost(self):
		"""(Private) This function will be called when the connection is lost."""
		print("Error: connection lost.");
		try:
			# Try and send a message back to the server to notify connection lost
			self.client_socket.send("q".encode());
		except:
			pass;
		# Raise an error to finish 
		raise Exception;

	def close(self):	
		"""Shut down the socket and close it"""
		# Shut down the socket to prevent further sends/receives
		self.client_socket.shutdown(socket.SHUT_RDWR);
		# Close the socket
		self.client_socket.close();

class TTTClientGame(TTTClient):
	"""TTTClientGame deals with the game logic on the client side."""

	def __init__(self):
		"""Initializes the client game object."""
		TTTClient.__init__(self);

	def start_game(self):
		"""Starts the game and gets basic game information from the server."""
		# Receive the player's ID from the server
		self.player_id = int(self.s_recv(128, "A"));
		# Confirm the ID has been received
		self.s_send("c","1");

		print("Welcome to Tic Tac Toe online, player " + str(self.player_id) 
			+ "\nPlease wait for another player to join the game...");

		# Receive the assigned role from the server
		self.role = str(self.s_recv(2, "R"));
		# Confirm the assigned role has been received
		self.s_send("c","2");

		# Receive the mactched player's ID from the server
		self.match_id = int(self.s_recv(128, "I"));
		# Confirm the mactched player's ID has been received
		self.s_send("c","3");

		print(("You are now matched with player " + str(self.match_id) 
			+ "\nYou are the \"" + self.role + "\""));

		# Call the __game_started() function, which might be implemented by
		# the GUI program to interact with the user interface.
		self.__game_started__();

		# Start the main loop
		self.__main_loop();

	def __game_started__(self):
		"""(Private) This function is called when the game is getting started."""
		# This is a virtual function
		# The actual implementation is in the subclass (the GUI program)
		return;

	def __main_loop(self):
		"""The main game loop."""
		while True:
			# Get the board content from the server
			board_content = self.s_recv(10, "B");
			# Get the command from the server 
			command = self.s_recv(2, "C");
			# Update the board
			self.__update_board__(command, board_content);

			if(command == "Y"):
				# If it's this player's turn to move
				self.__player_move__();
			elif(command == "N"):
				# If the player needs to just wait
				print("Waiting for the other player to make a move...");
				# Get the move the other player made from the server 
				move = self.s_recv(2, "I");
				print("Your opponent took up number " + str(move));
			elif(command == "D"):
				# If the result is a draw
				print("It's a draw.");
				break;
			elif(command == "W"):
				# If this player wins
				print("You WIN!");
				# Break the loop and finish
				break;
			elif(command == "L"):
				# If this player loses
				print("You lose.");
				# Break the loop and finish
				break;
			else:
				# If the server sends back anything unrecognizable
				# Simply print it
				print("Error: unknown message was sent from the server");
				# And finish
				break;


	def __update_board__(self, command, board_string):
		"""(Private) Updates the board. This function might be overridden by
		the GUI program."""
		if(command == "Y"):
			# If it's this player's turn to move, print out the current 
			# board with " " converted to the corresponding position number
			print("Current board:\n" + TTTClientGame.format_board(
				TTTClientGame.show_board_pos(board_string)));
		else:
			# Print out the current board
			print("Current board:\n" + TTTClientGame.format_board(
				board_string));

	def __player_move__(self):
		"""(Private) Lets the user input the move and sends it back to the
		server. This function might be overridden by the GUI program."""
		while True:
			# Prompt the user to enter a position
			try:
				position = int(input('Please enter the position (1~9):'));
			except:
				print("Invalid input.");
				continue;

			# Ensure user-input data is valid
			if(position >= 1 and position <= 9):
				# If the position is between 1 and 9
				if(board_content[position - 1] != " "):
					# If the position is already been taken,
					# Print out a warning
					print("That position has already been taken." + 
						"Please choose another one.");
				else:
					# If the user input is valid, break the loop
					break;
			else:
				print("Please enter a value between 1 and 9 that" + 
					"corresponds to the position on the grid board.");
			# Loop until the user enters a valid value

		# Send the position back to the server
		self.s_send("i", str(position));
		return;

	def show_board_pos(s):
		"""(Static) Converts the empty positions " " (a space) in the board 
		string to its corresponding position index number."""

		new_s = list("123456789");
		for i in range(0, 8):
			if(s[i] != " "):
				new_s[i] = s[i];
		return "".join(new_s);

	def format_board(s):
		"""(Static) Formats the grid board."""

		# If the length of the string is not 9
		if(len(s) != 9):
			# Then print out an error message
			print("Error: there should be 9 symbols.");
			# Throw an error 
			raise Exception;

		# Draw the grid board
		#print("|1|2|3|");
		#print("|4|5|6|");
		#print("|7|8|9|");
		return("|" + s[0] + "|" + s[1]  + "|" + s[2] + "|\n" 
			+ "|" + s[3] + "|" + s[4]  + "|" + s[5] + "|\n" 
			+ "|" + s[6] + "|" + s[7]  + "|" + s[8] + "|\n");

# Define the main program
def main():
	# If there are more than 3 arguments 
	if(len(argv) >= 3):
		# Set the address to argument 1, and port number to argument 2
		address = argv[1];
		port_number = argv[2];
	else:
		# Ask the user to input the address and port number
		address = input("Please enter the address:");
		port_number = input("Please enter the port:");

	# Initialize the client object
	client = TTTClientGame();
	# Connect to the server
	client.connect(address, port_number);
	try:
		# Start the game
		client.start_game();
	except:
		print(("Game finished unexpectedly!"));
		raise;
	finally:
		# Close the client
		client.close();

if __name__ == "__main__":
	# If this script is running as a standalone program,
	# start the main program.
	main();