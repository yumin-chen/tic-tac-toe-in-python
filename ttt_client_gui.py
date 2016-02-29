# Import the GUI library Tkinter
import tkinter
# Import the messagebox module explicitly
from tkinter import messagebox
# Import the webbroswer module for opening a link
import webbrowser

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

	def set_clickable(self, clickable):
		if(clickable):
			self.canvas.tag_bind(self.tag_name, "<Button-1>", self.on_click);
		else:
			self.canvas.tag_unbind(self.tag_name);

	def on_click(self, event):
		try:
			self.command();
		except:
			print("Error: " + self.__class__.__name__ + " " + self.id + " does not have a command");

	def config(self, **args):
		return self.canvas.itemconfig(self.tag_name, **args);

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

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 128, C_WINDOW_WIDTH + 128, C_WINDOW_HEIGHT + 368), 
			start=0, extent=180, fill=C_COLOR_BLUE, outline="");

		# Create the return button
		return_btn = self.create_button(C_WINDOW_WIDTH - 128, 32, "Go back");
		return_btn.command = self.on_return_clicked;

		# Draw the board
		board_line_width = 4; # Line width 
		board_width = 256; # Board takes 256x256 pixels
		board_grid_size = 3; # Draw a 3x3 board
		for i in range(1, board_grid_size):
			# Draw the board at the center of the screeen

			# Draw horizontal lines
			self.create_line((C_WINDOW_WIDTH - board_width)/2, 
				(C_WINDOW_HEIGHT - board_width)/2 + board_width/board_grid_size * i, 
				(C_WINDOW_WIDTH + board_width)/2, 
				(C_WINDOW_HEIGHT - board_width)/2 + board_width/board_grid_size * i, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);

			# Draw vertical lines
			self.create_line((C_WINDOW_WIDTH - board_width)/2 + board_width/board_grid_size * i, 
				(C_WINDOW_HEIGHT - board_width)/2, 
				(C_WINDOW_WIDTH - board_width)/2 + board_width/board_grid_size * i, 
				(C_WINDOW_HEIGHT + board_width)/2, 
				fill=C_COLOR_BLUE_DARK, width=board_line_width);

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def on_return_clicked(self):
		self.pack_forget();
		self.welcome_scene.pack();

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