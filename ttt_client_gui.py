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
	# Count the number of widgets initialized
	count = 0;

	def __init__(self, canvas):
		self.canvas = canvas;

		# Generate a unique id for each widget (for tags)
		self.id = str(CanvasWidget.count);
		CanvasWidget.count = CanvasWidget.count + 1;

		# Generate a unique tag for each widget
		self.tag_name = self.__class__.__name__ + self.id;

		# Initialize instance variables
		self.__disabled__ = False;

	def set_clickable(self, clickable):
		if(clickable):
			self.canvas.tag_bind(self.tag_name, "<Button-1>", self.on_click);
		else:
			self.canvas.tag_unbind(self.tag_name);

	def on_click(self, event):
		if(self.__disabled__):
			return False;
		try:
			self.command();
			return True;
		except AttributeError:
			print("Error: " + self.__class__.__name__ + " " + self.id + " does not have a command");
			raise;
		return False;

	def disable(self):
		self.__disabled__ = True;

	def enable(self):
		self.__disabled__ = False;

	def is_enabled(self):
		return self.__disabled__;

	def config(self, **kwargs):
		return self.canvas.itemconfig(self.tag_name, **kwargs);

class CanvasClickableLabel(CanvasWidget):

	def __init__(self, canvas, x, y, label_text, normal_foreground, hovered_foreground):
		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_foreground = normal_foreground;
		self.hovered_foreground = hovered_foreground;
		
		# Create the clickable label text
		canvas.create_text(x, y, font="Helvetica 14 underline", text=label_text, 
			fill=self.normal_foreground, tags=(self.tag_name));
		
		# Bind events
		canvas.tag_bind(self.tag_name, "<Enter>", self.on_enter);
		canvas.tag_bind(self.tag_name, "<Leave>", self.on_leave);
		self.set_clickable(True);

	def on_enter(self, event):
		self.canvas.itemconfig(self.tag_name, fill=self.hovered_foreground);

	def on_leave(self, event):
		self.canvas.itemconfig(self.tag_name, fill=self.normal_foreground);


class CanvasButton(CanvasWidget):
	# Define constant width and height
	WIDTH = 196;
	HEIGHT = 32;

	def __init__(self, canvas, x, y, button_text, normal_background, hovered_background, 
		normal_foreground, hovered_foreground):

		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_background = normal_background;
		self.hovered_background = hovered_background;
		self.normal_foreground = normal_foreground;
		self.hovered_foreground = hovered_foreground;

		# Create the rectangle background
		canvas.create_rectangle(x - self.WIDTH/2 + self.HEIGHT/2, y - self.HEIGHT/2, 
			x + self.WIDTH/2 - self.HEIGHT/2, y + self.HEIGHT/2, 
			fill=self.normal_background, outline="", tags=(self.tag_name, "rect" + self.id));
		# Create the two circles on both sides to create a rounded edge
		canvas.create_oval(x - self.WIDTH/2, y - self.HEIGHT/2, 
			x - self.WIDTH/2 + self.HEIGHT, y + self.HEIGHT/2, 
			fill=self.normal_background, outline="", tags=(self.tag_name, "oval_l" + self.id));

		canvas.create_oval(x + self.WIDTH/2 - self.HEIGHT, y - self.HEIGHT/2, 
			x + self.WIDTH/2, y + self.HEIGHT/2, 
			fill=self.normal_background, outline="", tags=(self.tag_name, "oval_r" + self.id));

		# Create the button text
		canvas.create_text(x, y, font="Helvetica 16 bold", text=button_text, 
			fill=self.normal_foreground, tags=(self.tag_name, "text" + self.id));

		# Bind events
		canvas.tag_bind(self.tag_name, "<Enter>", self.on_enter);
		canvas.tag_bind(self.tag_name, "<Leave>", self.on_leave);
		self.set_clickable(True);

	def on_enter(self, event):
		self.canvas.itemconfig(self.tag_name, fill=self.hovered_background);
		self.canvas.itemconfig("text" + self.id, fill=self.hovered_foreground);

	def on_leave(self, event):
		self.canvas.itemconfig(self.tag_name, fill=self.normal_background);
		self.canvas.itemconfig("text" + self.id, fill=self.normal_foreground);

class CanvasSquare(CanvasWidget):

	def __init__(self, canvas, x, y, width, normal_background, hovered_background, 
		disabled_background):

		# Initialize super class
		CanvasWidget.__init__(self, canvas);

		# Set color scheme for different states
		self.normal_background = normal_background;
		self.hovered_background = hovered_background;
		self.disabled_background = disabled_background;

		# Create the circle background
		canvas.create_rectangle(x - width/2, y - width/2, x + width/2, y + width/2, 
			fill=self.normal_background, outline="", tags=(self.tag_name, "oval" + self.id));

		# Bind events
		canvas.tag_bind(self.tag_name, "<Enter>", self.on_enter);
		canvas.tag_bind(self.tag_name, "<Leave>", self.on_leave);
		self.set_clickable(True);

	def on_enter(self, event):
		if(self.__disabled__):
			return False;
		self.canvas.itemconfig(self.tag_name, fill=self.hovered_background);

	def on_leave(self, event):
		if(self.__disabled__):
			return False;
		self.canvas.itemconfig(self.tag_name, fill=self.normal_background);

	def disable(self):
		super().disable();
		self.canvas.itemconfig(self.tag_name, fill=self.disabled_background);

	def enable(self):
		super().enable();
		self.canvas.itemconfig(self.tag_name, fill=self.normal_background);

# Define a subclass of Canvas as an abstract base scene class
class BaseScene(tkinter.Canvas):

	def __init__(self, parent):
		# Initialize the superclass Canvas
		tkinter.Canvas.__init__(self, parent, bg=C_COLOR_BLUE_LIGHT, 
			width=C_WINDOW_WIDTH, height=C_WINDOW_HEIGHT);

		# Bind the window-resizing event
		self.bind("<Configure>", self.on_resize);

		# Set self.width and self.height for later use
		self.width = C_WINDOW_WIDTH; 
		self.height = C_WINDOW_HEIGHT; 

	def on_resize(self, event):
		# Determine the ratio of old width/height to new width/height
		wscale = float(event.width)/self.width;
		hscale = float(event.height)/self.height;
		self.width = event.width;
		self.height = event.height;

		# Resize the canvas 
		self.config(width=self.width, height=self.height);

		# Rescale all the objects tagged with the "all" tag
		self.scale("all", 0, 0, wscale, hscale);

	def create_button(self, x, y, button_text, 
		normal_background=C_COLOR_BLUE, hovered_background=C_COLOR_BLUE_DARK, 
		normal_foreground=C_COLOR_BLUE_DARK, hovered_foreground=C_COLOR_BLUE_LIGHT):

		return CanvasButton(self, x, y, button_text, 
			normal_background, hovered_background, normal_foreground, hovered_foreground);

	def create_square(self, x, y, width,
		normal_background=C_COLOR_BLUE, hovered_background=C_COLOR_BLUE_DARK, 
		disabled_background=C_COLOR_BLUE_LIGHT):

		return CanvasSquare(self, x, y, width,
			normal_background, hovered_background, disabled_background);

	def create_clickable_label(self, x, y, button_text, 
		normal_foreground=C_COLOR_BLUE_DARK, hovered_foreground=C_COLOR_BLUE_LIGHT):

		return CanvasClickableLabel(self, x, y, button_text, 
			normal_foreground, hovered_foreground);

# Define a subclass of BaseScene for the welcome scene
class WelcomeScene(BaseScene):

	def __init__(self, parent):
		BaseScene.__init__(self, parent);

		# Create a blue arch at the top of the canvas
		self.create_arc((-64, -368, C_WINDOW_WIDTH + 64, 192), start=0, extent=-180, fill=C_COLOR_BLUE, outline="");

		try:
			# From the logo image file create a PhotoImage object 
			self.logo_image = tkinter.PhotoImage(file="res/icon.png");
			# Create the logo image at the center of the canvas
			logo = self.create_image((C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 - 96), image=self.logo_image);
			# From the title image file create a PhotoImage object 
			self.title_image = tkinter.PhotoImage(file="res/title.png");
			# Create the logo image at the center of the canvas
			title = self.create_image((C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 48), image=self.title_image);
		except:	
			# An error has been caught when creating the logo image
			tkinter.messagebox.showerror("Error", "Can't create images.\n" +
				"Please make sure the res folder is in the same directory as this script.");

		# Create the Play button
		play_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 136, "Play");
		play_btn.command = self.on_play_clicked;
		# Create the About button
		about_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 192, "About");
		about_btn.command = self.on_about_clicked;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def on_play_clicked(self):
		self.pack_forget();
		self.main_game_scene.pack();

	def on_about_clicked(self):
		self.pack_forget();
		self.about_scene.pack();

# Define a subclass of BaseScene for the about scene
class AboutScene(BaseScene):

	def __init__(self, parent):
		BaseScene.__init__(self, parent);

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 128, C_WINDOW_WIDTH + 128, C_WINDOW_HEIGHT + 368), 
			start=0, extent=180, fill=C_COLOR_BLUE, outline="");

		try:
			# From the Charmy image file create a PhotoImage object 
			self.charmy_image = tkinter.PhotoImage(file="res/charmy.png");
			# Create the logo image on the left of the canvas
			logo = self.create_image((C_WINDOW_WIDTH/2 - 192, C_WINDOW_HEIGHT/2 - 48), image=self.charmy_image);
			# From the title image file create a PhotoImage object 
			self.title_image = tkinter.PhotoImage(file="res/title.png");
			# Resize the image to make it smaller
			self.title_image = self.title_image.subsample(2, 2);
			# Create the logo image at the center of the canvas
			title = self.create_image((C_WINDOW_WIDTH/2 + 64, C_WINDOW_HEIGHT/2 - 160), image=self.title_image);
		except:	
			# An error has been caught when creating the logo image
			tkinter.messagebox.showerror("Error", "Can't create images.\n" +
				"Please make sure the res folder is in the same directory as this script.");
		
		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2 - 96, anchor="w", 
			font="Helvetica 14", text="Developed by Charlie Chen", fill=C_COLOR_BLUE_DARK);
		
		link_charmysoft = self.create_clickable_label(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2 - 64, 
			"http://CharmySoft.com", "#0B0080", "#CC2200");
		link_charmysoft.config(anchor="w");
		link_charmysoft.command = self.on_charmysoft_clicked;

		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2, anchor="w", font="Helvetica 14", 
			text="Tic Tac Toe Online in Python is \nopen source under the MIT license", fill=C_COLOR_BLUE_DARK);
		
		link_project = self.create_clickable_label(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2 + 40, 
			"http://CharmySoft.com/app/ttt-python.htm", "#0B0080", "#CC2200");
		link_project.config(anchor="w");
		link_project.command = self.on_project_link_clicked;

		self.create_text(C_WINDOW_WIDTH/2 + 64, C_WINDOW_HEIGHT/2 + 96, font="Helvetica 16", 
			text="Copyright (c) 2016 CharmySoft", fill=C_COLOR_BLUE_DARK);
		
		# Create the OK button
		ok_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 160, "OK", 
			C_COLOR_BLUE_DARK, C_COLOR_BLUE_LIGHT, C_COLOR_BLUE_LIGHT, C_COLOR_BLUE_DARK);
		ok_btn.command = self.on_ok_clicked;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def on_ok_clicked(self):
		self.pack_forget();
		self.welcome_scene.pack();

	def on_charmysoft_clicked(self):
		webbrowser.open("http://www.CharmySoft.com/about.htm");

	def on_project_link_clicked(self):
		webbrowser.open("http://www.CharmySoft.com/ttt-python.htm");

# Define a subclass of BaseScene for the main game scene
class MainGameScene(BaseScene):

	def __init__(self, parent):
		BaseScene.__init__(self, parent);

		# Initialize instance variables
		self.board_grids_power = 3; # Make it a 3x3 grid board

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 64, C_WINDOW_WIDTH + 128, C_WINDOW_HEIGHT + 368), 
			start=0, extent=180, fill=C_COLOR_BLUE, outline="");

		# Create the return button
		return_btn = self.create_button(C_WINDOW_WIDTH - 128, 32, "Go back");
		return_btn.command = self.on_return_clicked;

		self.draw_board(256);

		# Draw the player_self_text
		player_self_text = self.create_text(96, 128, font="Helvetica 16", fill=C_COLOR_BLUE_DARK, tags=("player_self_text"));
		# Draw the player_match_text
		player_match_text = self.create_text(C_WINDOW_WIDTH - 96, 128, font="Helvetica 16", fill=C_COLOR_BLUE_DARK, tags=("player_match_text"));

		# Draw the notif text
		notif_text = self.create_text(8, C_WINDOW_HEIGHT-64, font="Helvetica 16", fill=C_COLOR_BLUE_DARK, tags=("notif_text"), anchor="w");

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def pack(self):
		super().pack();
		# Start a new thread to deal with the client communication
		threading.Thread(target=self.__start_client).start();

	def draw_board(self, board_width, board_line_width = 4):
		"""Draws the board at the center of the screen, parameter board_width 
		determines the size of the board, e.g. 256 would mean the board is 256x256. 
		board_line_width determines the border line width."""

		# Create squares for the grid board
		self.squares = [None] * self.board_grids_power * self.board_grids_power;
		for i in range(0, self.board_grids_power):
			for j in range(0, self.board_grids_power):
				self.squares[i+j*3] = self.create_square((C_WINDOW_WIDTH - board_width)/2 + 
					board_width/self.board_grids_power * i + board_width / self.board_grids_power / 2,
					(C_WINDOW_HEIGHT - board_width)/2 + 
					board_width/self.board_grids_power * j + board_width / self.board_grids_power / 2,
					board_width / self.board_grids_power);
				# Disable those squares to make them unclickable
				self.squares[i+j*3].disable();

		# Draw the border lines
		for i in range(1, self.board_grids_power):
			# Draw horizontal lines
			self.create_line((C_WINDOW_WIDTH - board_width)/2, 
				(C_WINDOW_HEIGHT - board_width)/2 + board_width/self.board_grids_power * i, 
				(C_WINDOW_WIDTH + board_width)/2, 
				(C_WINDOW_HEIGHT - board_width)/2 + board_width/self.board_grids_power * i, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);
			# Draw vertical lines
			self.create_line((C_WINDOW_WIDTH - board_width)/2 + board_width/self.board_grids_power * i, 
				(C_WINDOW_HEIGHT - board_width)/2, 
				(C_WINDOW_WIDTH - board_width)/2 + board_width/self.board_grids_power * i, 
				(C_WINDOW_HEIGHT + board_width)/2, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);

	def __start_client(self):
		# Initialize the client object
		self.client = TTTClientGameGUI();
		# Gives the client a reference to self 
		self.client.canvas = self;
		# Set the notif text
		self.set_notif_text("Connecting to the game server...");
		# Connect to the server
		if(self.client.connect("localhost", "8080")):
			# If connected to the server
			self.set_notif_text("Server connected.");
			# Start the game
			self.client.start_game();
			# Close the client
			self.client.close();

	def set_notif_text(self, text):
		self.itemconfig("notif_text", text=text);

	def on_return_clicked(self):
		self.pack_forget();
		self.welcome_scene.pack();

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
		self.canvas.set_notif_text("Game started. You are the \"" + self.role + "\"");
		self.canvas.itemconfig("player_self_text", text="Player " + str(self.player_id));
		self.canvas.itemconfig("player_match_text", text="Player " + str(self.match_id));

	def __player_move__(self):
		"""(Override) Lets the user to make a move and sends it back to the
		server. This function might be overridden by the GUI program."""
		for i in range(0, self.canvas.board_grids_power * 
			self.canvas.board_grids_power):
			# Enable those squares to make them clickable
			self.canvas.squares[i].enable();
			# Bind their commands
			self.canvas.squares[i].command = lambda self=self, i=i: self.__move_made(i);

		while self.canvas.squares[0].is_enabled():
			# Wait until the user has clicked on something
			pass;

	def __move_made(self, index):
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