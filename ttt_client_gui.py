# Import the GUI library Tkinter
import tkinter
# Import the messagebox module explicitly
from tkinter import messagebox

# Constants 
C_WINDOW_WIDTH = 640;
C_WINDOW_HEIGHT = 480;
C_WINDOW_MIN_WIDTH = 480;
C_WINDOW_MIN_HEIGHT = 360;
C_COLOR_BLUE_LIGHT = "#e4f1fe";
C_COLOR_BLUE_DARK = "#304e62";
C_COLOR_BLUE = "#a8d4f2";

class CanvasButton:

	# Define constant width and height
	WIDTH = 196;
	HEIGHT = 32;

	# Count the number of buttons objects initialized
	count = 0;

	def __init__(self, canvas, x, y, button_text, normal_background, hovered_background, normal_foreground, hovered_foreground):
		self.canvas = canvas;
		# Generate a unique id for each button (for tags)
		self.id = str(CanvasButton.count);
		CanvasButton.count = CanvasButton.count + 1;
		# Set color scheme for different states
		self.normal_background = normal_background;
		self.hovered_background = hovered_background;
		self.normal_foreground = normal_foreground;
		self.hovered_foreground = hovered_foreground;

		# Create the rectangle background
		canvas.create_rectangle(x - self.WIDTH/2 + self.HEIGHT/2, y - self.HEIGHT/2, x + self.WIDTH/2 - self.HEIGHT/2, y + self.HEIGHT/2, fill=self.normal_background, outline="", tags=("btn" + self.id, "rect" + self.id));
		# Create the two circles on both sides to create a rounded edge
		canvas.create_oval(x - self.WIDTH/2, y - self.HEIGHT/2, x - self.WIDTH/2 + self.HEIGHT, y + self.HEIGHT/2, fill=self.normal_background, outline="", tags=("btn" + self.id, "oval_l" + self.id));
		canvas.create_oval(x + self.WIDTH/2 - self.HEIGHT, y - self.HEIGHT/2, x + self.WIDTH/2, y + self.HEIGHT/2, fill=self.normal_background, outline="", tags=("btn" + self.id, "oval_r" + self.id));
		# Create the button text
		canvas.create_text(x, y, font="Helvetica 16 bold", text=button_text, fill=self.normal_foreground, tags=("btn" + self.id, "text" + self.id));
		# Bind events
		canvas.tag_bind("btn" + self.id, "<Enter>", self.on_enter);
		canvas.tag_bind("btn" + self.id, "<Leave>", self.on_leave);
		canvas.tag_bind("btn" + self.id, "<Button-1>", self.on_click);

	def on_enter(self, event):
		self.canvas.itemconfig("btn" + self.id, fill=self.hovered_background);
		self.canvas.itemconfig("text" + self.id, fill=self.hovered_foreground);

	def on_leave(self, event):
		self.canvas.itemconfig("btn" + self.id, fill=self.normal_background);
		self.canvas.itemconfig("text" + self.id, fill=self.normal_foreground);

	def on_click(self, event):
		try:
			self.command();
		except:
			print("Error: CanvasButton " + self.id + " does not have a command");

# Define a subclass of Canvas as an abstract base scene class
class BaseScene(tkinter.Canvas):

	def __init__(self, parent):
		tkinter.Canvas.__init__(self, parent, bg=C_COLOR_BLUE_LIGHT, height=C_WINDOW_HEIGHT, width=C_WINDOW_WIDTH);
		self.bind("<Configure>", self.on_resize);
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


	def create_button(self, x, y, button_text, normal_background=C_COLOR_BLUE, hovered_background=C_COLOR_BLUE_DARK, normal_foreground=C_COLOR_BLUE_DARK, hovered_foreground=C_COLOR_BLUE_LIGHT):
		return CanvasButton(self, x, y, button_text, normal_background, hovered_background, normal_foreground, hovered_foreground);


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
			tkinter.messagebox.showerror("Error", "Can't create images.\nPlease make sure the res folder is in the same directory as this script.");

		# Create the Play button
		play_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 136, "Play");
		play_btn.command = self.on_play_clicked;
		# Create the About button
		about_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 192, "About");
		about_btn.command = self.on_about_clicked;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def on_play_clicked(self):
		return;

	def on_about_clicked(self):
		self.pack_forget();
		self.about_scene.pack();


# Define a subclass of BaseScene for the about scene
class AboutScene(BaseScene):

	def __init__(self, parent):
		BaseScene.__init__(self, parent);

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-128, C_WINDOW_HEIGHT - 128, C_WINDOW_WIDTH + 128, C_WINDOW_HEIGHT + 368), start=0, extent=180, fill=C_COLOR_BLUE, outline="");

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
			tkinter.messagebox.showerror("Error", "Can't create images.\nPlease make sure the res folder is in the same directory as this script.");
		
		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2 - 96, anchor="w", font="Helvetica 14", text="Developed by Charlie Chen", fill=C_COLOR_BLUE_DARK);
		
		self.create_text(C_WINDOW_WIDTH/2 - 80, C_WINDOW_HEIGHT/2, anchor="w", font="Helvetica 14", text="Tic Tac Toe Online in Python is \nopen source under the MIT license", fill=C_COLOR_BLUE_DARK);
		
		self.create_text(C_WINDOW_WIDTH/2 + 64, C_WINDOW_HEIGHT/2 + 96, font="Helvetica 16", text="Copyright (c) 2016 CharmySoft", fill=C_COLOR_BLUE_DARK);
		
		# Create the Play button
		ok_btn = self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 160, "OK", C_COLOR_BLUE_DARK, C_COLOR_BLUE_LIGHT, C_COLOR_BLUE_LIGHT, C_COLOR_BLUE_DARK);
		ok_btn.command = self.on_ok_clicked;

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def on_ok_clicked(self):
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
# Pack the welcome scene
welcome_scene.pack();

# Initialize the about scene
about_scene = AboutScene(root);
# Give a reference for switching between scenes
welcome_scene.about_scene = about_scene;
about_scene.welcome_scene = welcome_scene;
    
# Main loop
root.mainloop();