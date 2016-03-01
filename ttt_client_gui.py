# Import the GUI library Tkinter
import tkinter
# Import the messagebox module explicitly
from tkinter import messagebox
# Import the webbroswer module for opening a link
import webbrowser
# Import the client module
from ttt_client import TTTClientGame
# Import multi-threading module
import threading

# Constants 
C_WINDOW_WIDTH = 640;
C_WINDOW_HEIGHT = 480;
C_WINDOW_MIN_WIDTH = 480;
C_WINDOW_MIN_HEIGHT = 360;
C_COLOR_BLUE_LIGHT = "#e4f1fe";
C_COLOR_BLUE_DARK = "#304e62";
C_COLOR_BLUE = "#a8d4f2";

class CanvasWidget:
	"""(Abstract) The base class for all the canvas widgets."""

	__count = 0; # Count the number of widgets initialized

	def __init__(self, canvas):
		"""Initializes the widget."""
		self.canvas = canvas;
		# Generate a unique id for each widget (for tags)
		self.id = str(CanvasWidget.__count);
		CanvasWidget.__count = CanvasWidget.__count + 1;
		# Generate a unique tag for each widget
		self.tag_name = self.__class__.__name__ + self.id;
		# Initialize instance variables
		self.__disabled__ = False;
		# Set default colors
		self.normal_color = C_COLOR_BLUE; 
		self.hovered_color = C_COLOR_BLUE_DARK;

	def set_clickable(self, clickable):
		"""Sets if the widget can be clicked."""
		if(clickable):
			self.canvas.tag_bind(self.tag_name, "<Button-1>", 
				self.__on_click__);
		else:
			self.canvas.tag_unbind(self.tag_name, "<Button-1>");

	def __on_click__(self, event):
		"""(Private) This function will be called when the user clicks on 
		the widget."""
		if(self.__disabled__):
			return False;
		try:
			self.command();
			return True;
		except AttributeError:
			print("Error: " + self.__class__.__name__ + " " + 
				self.id + " does not have a command");
			raise;
		return False;

	def set_hoverable(self, hoverable):
		"""Sets if the widget can be hovered."""
		if(hoverable):
			self.canvas.tag_bind(self.tag_name, "<Enter>", 
				self.__on_enter__);
			self.canvas.tag_bind(self.tag_name, "<Leave>", 
				self.__on_leave__);
		else:
			self.canvas.tag_unbind(self.tag_name, "<Enter>");
			self.canvas.tag_unbind(self.tag_name, "<Leave>");

	def __on_enter__(self, event):
		"""(Private) This function will be called when the mouse enters
		into the widget."""
		if(self.__disabled__):
			return False;
		self.canvas.itemconfig(self.tag_name, fill=self.hovered_color);
		return True;

	def __on_leave__(self, event):
		"""(Private) This function will be called when the mouse leaves
		the widget."""
		if(self.__disabled__):
			return False;
		self.canvas.itemconfig(self.tag_name, fill=self.normal_color);
		return True;

	def disable(self):
		"""Disables the widget so it won't respond to any events."""
		self.__disabled__ = True;

	def enable(self):
		"""Enables the widget so it starts to respond to events."""
		self.__disabled__ = False;

	def is_enabled(self):
		"""Returns True if the widget is disabled."""
		return self.__disabled__;

	def config(self, **kwargs):
		"""Configures the widget's options."""
		return self.canvas.itemconfig(self.tag_name, **kwargs);

class CanvasClickableLabel(CanvasWidget):
	"""A clickable label that shows text and can respond to user 
	click events."""

	def __init__(self, canvas, x, y, label_text, normal_color, 
		hovered_color):
		"""Initializes the clickable label object."""

		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_color = normal_color;
		self.hovered_color = hovered_color;
		
		# Create the clickable label text
		canvas.create_text(x, y, font="Helvetica 14 underline", 
			text=label_text, fill=self.normal_color, tags=(self.tag_name));
		
		# Bind events
		self.set_hoverable(True);
		self.set_clickable(True);

class CanvasButton(CanvasWidget):
	"""A button that responds to mouse clicks."""

	# Define constant width and height
	WIDTH = 196;
	HEIGHT = 32;

	def __init__(self, canvas, x, y, button_text, normal_color, 
		hovered_color, normal_text_color, hovered_text_color):
		"""Initialize the button object."""

		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_color = normal_color;
		self.hovered_color = hovered_color;
		self.normal_text_color = normal_text_color;
		self.hovered_text_color = hovered_text_color;

		# Create the rectangle background
		canvas.create_rectangle(x - self.WIDTH/2 + self.HEIGHT/2, 
			y - self.HEIGHT/2, x + self.WIDTH/2 - self.HEIGHT/2, 
			y + self.HEIGHT/2, fill=self.normal_color, outline="", 
			tags=(self.tag_name, "rect" + self.id));

		# Create the two circles on both sides to create a rounded edge
		canvas.create_oval(x - self.WIDTH/2, y - self.HEIGHT/2, 
			x - self.WIDTH/2 + self.HEIGHT, y + self.HEIGHT/2, 
			fill=self.normal_color, outline="", 
			tags=(self.tag_name, "oval_l" + self.id));

		canvas.create_oval(x + self.WIDTH/2 - self.HEIGHT, 
			y - self.HEIGHT/2, x + self.WIDTH/2, y + self.HEIGHT/2,
			fill=self.normal_color, outline="", 
			tags=(self.tag_name, "oval_r" + self.id));

		# Create the button text
		canvas.create_text(x, y, font="Helvetica 16 bold", 
			text=button_text, fill=self.normal_text_color, 
			tags=(self.tag_name, "text" + self.id));

		# Bind events
		self.set_hoverable(True);
		self.set_clickable(True);

	def __on_enter__(self, event):
		"""(Override) Change the text to a different color when the 
		enter event is triggered."""
		if(super().__on_enter__(event)):
			self.canvas.itemconfig("text" + self.id, 
				fill=self.hovered_text_color);

	def __on_leave__(self, event):
		"""(Override) Change the text to a different color when the 
		leave event is triggered."""
		if(super().__on_leave__(event)):
			self.canvas.itemconfig("text" + self.id, 
				fill=self.normal_text_color);

class CanvasSquare(CanvasWidget):
	"""A square that responds to mouse click event. This is for the grid
	board."""

	def __init__(self, canvas, x, y, width, normal_color, hovered_color, 
		disabled_color):
		"""Initialize the square object."""

		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_color = normal_color;
		self.hovered_color = hovered_color;
		self.disabled_color = disabled_color;

		# Create the circle background
		canvas.create_rectangle(x - width/2, y - width/2, x + width/2, 
			y + width/2, fill=self.normal_color, outline="", 
			tags=(self.tag_name, "oval" + self.id));

		# Bind events
		self.set_hoverable(True);
		self.set_clickable(True);

	def disable(self):
		"""(Override) Change the color when the square is disabled."""
		super().disable();
		self.canvas.itemconfig(self.tag_name, fill=self.disabled_color);

	def enable(self):
		"""(Override) Change the color back to normal when the square 
		is disabled."""
		super().enable();
		self.canvas.itemconfig(self.tag_name, fill=self.normal_color);

class BaseScene(tkinter.Canvas):
	"""(Abstract) The base class for all scenes. BaseScene deals with
	general widgets and handles window resizing event."""

	def __init__(self, parent):
		"""Initializes the scene."""

		# Initialize the superclass Canvas
		tkinter.Canvas.__init__(self, parent, bg=C_COLOR_BLUE_LIGHT, 
			width=C_WINDOW_WIDTH, height=C_WINDOW_HEIGHT);

		# Bind the window-resizing event
		self.bind("<Configure>", self.__on_resize__);

		# Set self.width and self.height for later use
		self.width = C_WINDOW_WIDTH; 
		self.height = C_WINDOW_HEIGHT; 

	def __on_resize__(self, event):
		"""(Private) This function is called when the window is being
		resied."""

		# Determine the ratio of old width/height to new width/height
		self.wscale = float(event.width)/self.width;
		self.hscale = float(event.height)/self.height;
		self.width = event.width;
		self.height = event.height;

		# Resize the canvas 
		self.config(width=self.width, height=self.height);

		# Rescale all the objects tagged with the "all" tag
		self.scale("all", 0, 0, self.wscale, self.hscale);

	def create_button(self, x, y, button_text, 
		normal_color=C_COLOR_BLUE, hovered_color=C_COLOR_BLUE_DARK, 
		normal_text_color=C_COLOR_BLUE_DARK, 
		hovered_text_color=C_COLOR_BLUE_LIGHT):
		"""Creates a button widget and returns it. Note this will
		return a CanvasButton object, not the ID as other standard 
		Tkinter canvas widgets usually returns."""

		return CanvasButton(self, x, y, button_text, 
			normal_color, hovered_color, 
			normal_text_color, hovered_text_color);

	def create_square(self, x, y, width,
		normal_color=C_COLOR_BLUE, hovered_color=C_COLOR_BLUE_DARK, 
		disabled_color=C_COLOR_BLUE_LIGHT):
		"""Creates a square widget and returns it. Note this will
		return a CanvasSquare object, not the ID as other standard 
		Tkinter canvas widgets usually returns."""

		return CanvasSquare(self, x, y, width,
			normal_color, hovered_color, disabled_color);

	def create_clickable_label(self, x, y, button_text, 
		normal_color=C_COLOR_BLUE_DARK, hovered_color=C_COLOR_BLUE_LIGHT):
		"""Creates a clickable label widget and returns it. Note this
		will return a CanvasClickableLabel object, not the ID as other 
		standard Tkinter canvas widgets usually returns."""

		return CanvasClickableLabel(self, x, y, button_text, 
			normal_color, hovered_color);

class WelcomeScene(BaseScene):
	"""WelcomeScene is the first scene to show when the GUI starts."""

	def __init__(self, parent):
		"""Initializes the welcome scene."""

		# Initialize BaseScene
		super().__init__(parent);

		# Create a blue arch at the top of the canvas
		self.create_arc((-64, -368, C_WINDOW_WIDTH + 64, 192), 
			start=0, extent=-180, fill=C_COLOR_BLUE, outline="");

		try:
			# From the logo image file create a PhotoImage object 
			self.logo_image = tkinter.PhotoImage(file="res/icon.png");
			# Create the logo image at the center of the canvas
			logo = self.create_image((C_WINDOW_WIDTH/2, 
				C_WINDOW_HEIGHT/2 - 96), image=self.logo_image);
			# From the title image file create a PhotoImage object 
			self.title_image = tkinter.PhotoImage(file="res/title.png");
			# Create the logo image at the center of the canvas
			title = self.create_image((C_WINDOW_WIDTH/2, 
				C_WINDOW_HEIGHT/2 + 48), image=self.title_image);
		except:	
			# An error has been caught when creating the logo image
			tkinter.messagebox.showerror("Error", "Can't create images.\n" +
				"Please make sure the res folder is in the same directory" + 
				" as this script.");

		# Create the Play button
		play_btn = self.create_button(C_WINDOW_WIDTH/2, 
			C_WINDOW_HEIGHT/2 + 136, "Play");
		play_btn.command = self.__on_play_clicked__;
		# Create the About button
		about_btn = self.create_button(C_WINDOW_WIDTH/2, 
			C_WINDOW_HEIGHT/2 + 192, "About");
		about_btn.command = self.__on_about_clicked__;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def __on_play_clicked__(self):
		"""(Private) Switches to the main game scene when the play
		button is clicked."""
		self.pack_forget();
		self.main_game_scene.pack();

	def __on_about_clicked__(self):
		"""(Private) Switches to the about scene when the about	button 
		is clicked."""
		self.pack_forget();
		self.about_scene.pack();

class AboutScene(BaseScene):
	"""AboutScene shows the developer and copyright information."""

	def __init__(self, parent):
		"""Initializes the about scene object."""

		# Initialize the base scene
		super().__init__(parent);

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 128, 
			C_WINDOW_WIDTH + 128, C_WINDOW_HEIGHT + 368), 
			start=0, extent=180, fill=C_COLOR_BLUE, outline="");

		try:
			# From the Charmy image file create a PhotoImage object 
			self.charmy_image = tkinter.PhotoImage(file="res/charmy.png");
			# Create the logo image on the left of the canvas
			logo = self.create_image((C_WINDOW_WIDTH/2 - 192, 
				C_WINDOW_HEIGHT/2 - 48), image=self.charmy_image);
			# From the title image file create a PhotoImage object 
			self.title_image = tkinter.PhotoImage(file="res/title.png");
			# Resize the image to make it smaller
			self.title_image = self.title_image.subsample(2, 2);
			# Create the logo image at the center of the canvas
			title = self.create_image((C_WINDOW_WIDTH/2 + 64, 
				C_WINDOW_HEIGHT/2 - 160), image=self.title_image);
		except:	
			# An error has been caught when creating the logo image
			tkinter.messagebox.showerror("Error", "Can't create images.\n" +
				"Please make sure the res folder is in the same directory" + 
				" as this script.");
		
		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2 - 96, 
			font="Helvetica 14", text="Developed by Charlie Chen", 
			anchor="w", fill=C_COLOR_BLUE_DARK);
		
		link_charmysoft = self.create_clickable_label(C_WINDOW_WIDTH/2 - 80, 
			C_WINDOW_HEIGHT/2 - 64, "http://CharmySoft.com", 
			"#0B0080", "#CC2200");
		link_charmysoft.config(anchor="w");
		link_charmysoft.command = self.__on_charmysoft_clicked__;

		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2, 
			anchor="w", font="Helvetica 14", fill=C_COLOR_BLUE_DARK, 
			text="Tic Tac Toe Online in Python is \n" + 
			"open source under the MIT license");
		
		link_project = self.create_clickable_label(C_WINDOW_WIDTH/2 - 80, 
			C_WINDOW_HEIGHT/2 + 40, "http://CharmySoft.com/app/ttt-python.htm", 
			"#0B0080", "#CC2200");
		link_project.config(anchor="w");
		link_project.command = self.__on_project_link_clicked__;

		self.create_text(C_WINDOW_WIDTH/2 + 64, C_WINDOW_HEIGHT/2 + 96, 
			font="Helvetica 16", text="Copyright (c) 2016 CharmySoft", 
			fill=C_COLOR_BLUE_DARK);
		
		# Create the OK button
		ok_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 160, 
			"OK", C_COLOR_BLUE_DARK, C_COLOR_BLUE_LIGHT, C_COLOR_BLUE_LIGHT, 
			C_COLOR_BLUE_DARK);
		ok_btn.command = self.__on_ok_clicked__;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def __on_ok_clicked__(self):
		"""(Private) Switches back to the welcome scene when the ok button
		is clicked."""
		self.pack_forget();
		self.welcome_scene.pack();

	def __on_charmysoft_clicked__(self):
		"""(Private) Opens CharmySoft.com in the system default browser 
		when the CharmySoft.com link is clicked."""
		webbrowser.open("http://www.CharmySoft.com/about.htm");

	def __on_project_link_clicked__(self):
		"""(Private) Opens the project link in the system default browser 
		when it is clicked."""
		webbrowser.open("http://www.CharmySoft.com/ttt-python.htm");

class MainGameScene(BaseScene):
	"""MainGameScene deals with the game logic."""

	def __init__(self, parent):
		"""Initializes the main game scene object."""

		# Initialize the base scene
		super().__init__(parent);

		# Initialize instance variables
		self.board_grids_power = 3; # Make it a 3x3 grid board
		self.board_width = 256; # The board is 256x256 wide

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 64, C_WINDOW_WIDTH + 128, 
			C_WINDOW_HEIGHT + 368), start=0, extent=180, fill=C_COLOR_BLUE, 
			outline="");

		# Create the return button
		return_btn = self.create_button(C_WINDOW_WIDTH - 128, 32, "Go back");
		return_btn.command = self.__on_return_clicked__;

		self.draw_board();

		# Draw the player_self_text
		player_self_text = self.create_text(96, 128, font="Helvetica 16", 
			fill=C_COLOR_BLUE_DARK, tags=("player_self_text"));
		# Draw the player_match_text
		player_match_text = self.create_text(C_WINDOW_WIDTH - 96, 128, 
			font="Helvetica 16", fill=C_COLOR_BLUE_DARK, 
			tags=("player_match_text"));

		# Draw the notif text
		notif_text = self.create_text(8, C_WINDOW_HEIGHT-64, anchor="w",
			font="Helvetica 16", fill=C_COLOR_BLUE_DARK, tags=("notif_text"));

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def pack(self):
		"""(Override) When the scene packs, start the client thread."""
		super().pack();
		# Start a new thread to deal with the client communication
		threading.Thread(target=self.__start_client__).start();

	def draw_board(self, board_line_width = 4):
		"""Draws the board at the center of the screen, parameter 
		board_line_width determines the border line width."""

		# Create squares for the grid board
		self.squares = [None] * self.board_grids_power * self.board_grids_power;
		for i in range(0, self.board_grids_power):
			for j in range(0, self.board_grids_power):
				self.squares[i+j*3] = self.create_square(
					(C_WINDOW_WIDTH - self.board_width)/2 + 
					self.board_width/self.board_grids_power * i + 
					self.board_width / self.board_grids_power / 2,
					(C_WINDOW_HEIGHT - self.board_width)/2 + 
					self.board_width/self.board_grids_power * j + 
					self.board_width / self.board_grids_power / 2,
					self.board_width / self.board_grids_power);
				# Disable those squares to make them unclickable
				self.squares[i+j*3].disable();

		# Draw the border lines
		for i in range(1, self.board_grids_power):
			# Draw horizontal lines
			self.create_line((C_WINDOW_WIDTH - self.board_width)/2, 
				(C_WINDOW_HEIGHT - self.board_width)/2 + 
				self.board_width/self.board_grids_power * i, 
				(C_WINDOW_WIDTH + self.board_width)/2, 
				(C_WINDOW_HEIGHT - self.board_width)/2 + 
				self.board_width/self.board_grids_power * i, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);
			# Draw vertical lines
			self.create_line((C_WINDOW_WIDTH - self.board_width)/2 + 
				self.board_width/self.board_grids_power * i, 
				(C_WINDOW_HEIGHT - self.board_width)/2, 
				(C_WINDOW_WIDTH - self.board_width)/2 + 
				self.board_width/self.board_grids_power * i, 
				(C_WINDOW_HEIGHT + self.board_width)/2, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);

	def __start_client__(self):
		"""(Private) Starts the client side."""
		# Initialize the client object
		self.client = TTTClientGameGUI();
		# Gives the client a reference to self 
		self.client.canvas = self;
		# Set the notif text
		self.set_notif_text("Connecting to the game server...");
		# Connect to the server
		if(self.client.connect("localhost", "8080")):
			# If connected to the server
			self.set_notif_text("Server connected. \n" +
				"Waiting for other players to join...");
			# Start the game
			self.client.start_game();
			# Close the client
			self.client.close();

	def __on_return_clicked__(self):
		"""(Private) Switches back to the welcome scene when the return 
		button is clicked."""
		self.pack_forget();
		self.welcome_scene.pack();

	def set_notif_text(self, text):
		"""Sets the notification text."""
		self.itemconfig("notif_text", text=text);

	def update_board_content(self, board_string):
		"""Redraws the board content with new board_string."""
		if(len(board_string) != 
			self.board_grids_power * self.board_grids_power):
			# If board_string is in valid
			print("The board string should be " + 
				str(self.board_grids_power * self.board_grids_power) 
				+ " characters long.");
			# Throw an error
			raise Exception;

		# Delete everything on the board
		self.delete("board_content");

		p = 16; # Padding

		# Draw the board content
		for i in range(0, self.board_grids_power):
			for j in range(0, self.board_grids_power):

				if(board_string[i+j*3] == "O"):
					# If this is an "O"
					self.create_oval(
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * i + p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * j + p,
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (i + 1) - p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (j + 1) - p,
						fill="", outline=C_COLOR_BLUE_DARK, width=4,
						tags="board_content");
				elif(board_string[i+j*3] == "X"):
					# If this is an "X"
					self.create_line(
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * i + p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * j + p,
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (i + 1) - p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (j + 1) - p,
						fill=C_COLOR_BLUE_DARK, width=4,
						tags="board_content");
					self.create_line(
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (i + 1) - p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * j + p,
						(C_WINDOW_WIDTH - self.board_width)/2 + 
						self.board_width/self.board_grids_power * i + p,
						(C_WINDOW_HEIGHT - self.board_width)/2 + 
						self.board_width/self.board_grids_power * (j + 1) - p,
						fill=C_COLOR_BLUE_DARK, width=4,
						tags="board_content");


class TTTClientGameGUI(TTTClientGame):
	"""The client implemented with GUI."""

	def __connect_failed__(self):
		"""(Override) Updates the GUI to notify the user that the connection
		couldn't be established"""
		# Write the notif text
		self.canvas.set_notif_text("Can't connect to the game server.\n" + 
			"Plase check your connection.");
		# Throw an error and finish the client thread
		raise Exception;

	def __game_started__(self):
		"""(Override) Updates the GUI to notify the user that the game is
		getting started"""
		self.canvas.set_notif_text("Game started. " + 
			"You are the \"" + self.role + "\"");
		self.canvas.itemconfig("player_self_text", 
			text="Player " + str(self.player_id));
		self.canvas.itemconfig("player_match_text", 
			text="Player " + str(self.match_id));

	def __update_board__(self, command, board_string):
		"""(Override) Updates the board."""
		self.canvas.update_board_content(board_string);
		if(command == "D"):
			# If the result is a draw
			self.canvas.set_notif_text("It's a draw.");
		elif(command == "W"):
			# If this player wins
			self.canvas.set_notif_text("You WIN!");
		elif(command == "L"):
			# If this player loses
			self.canvas.set_notif_text("You lose.");

	def __player_move__(self):
		"""(Override) Lets the user to make a move and sends it back to the
		server. """
		for i in range(0, self.canvas.board_grids_power * 
			self.canvas.board_grids_power):
			# Enable those squares to make them clickable
			self.canvas.squares[i].enable();
			# Bind their commands
			self.canvas.squares[i].command = (lambda self=self, i=i: 
				self.__move_made__(i));

		while self.canvas.squares[0].is_enabled():
			# Wait until the user has clicked on something
			pass;

	def __move_made__(self, index):
		"""(Private) This function is called when the user clicks on the 
		board to make a move."""

		print("User chose " + str(index + 1));

		# Send the position back to the server
		self.s_send("i", str(index + 1));

		for i in range(0, self.canvas.board_grids_power * 
			self.canvas.board_grids_power):
			# Disable those squares to make them unclickable
			self.canvas.squares[i].disable();
			# Remove their commands
			self.canvas.squares[i].command = None;

		
# Define the main program
def main():
	# Create a Tkinter object
	root = tkinter.Tk();
	# Set window title
	root.title("Tic Tac Toe");
	# Set window minimun size
	root.minsize(C_WINDOW_MIN_WIDTH, C_WINDOW_MIN_HEIGHT);
	# Set window size
	root.geometry(str(C_WINDOW_WIDTH) + "x" + str(C_WINDOW_HEIGHT));

	try:
		# Set window icon
		root.iconbitmap("res/icon.ico");
	except:	
		# An error has been caught when setting the icon
		tkinter.messagebox.showerror("Error", "Can't set the window icon.");

	# Initialize the welcome scene
	welcome_scene = WelcomeScene(root);
	# Initialize the about scene
	about_scene = AboutScene(root);
	# Initialize the main game scene
	main_game_scene = MainGameScene(root);

	# Give a reference for switching between scenes
	welcome_scene.about_scene = about_scene;
	welcome_scene.main_game_scene = main_game_scene; 
	about_scene.welcome_scene = welcome_scene;
	main_game_scene.welcome_scene = welcome_scene;

	# Start showing the welcome scene
	welcome_scene.pack();
	    
	# Main loop
	root.mainloop();

if __name__ == "__main__":
	# If this script is running as a standalone program,
	# start the main program.
	main();