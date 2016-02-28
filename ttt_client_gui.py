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

# Define a subclass of Canvas for the welcome scene
class WelcomeScene(tkinter.Canvas):

	def __init__(self, parent):
		tkinter.Canvas.__init__(self, parent, bg=C_COLOR_BLUE_LIGHT, height=C_WINDOW_HEIGHT, width=C_WINDOW_WIDTH);
		self.bind("<Configure>", self.on_resize);
		self.width = C_WINDOW_WIDTH; 
		self.height = C_WINDOW_HEIGHT; 

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
		self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 136, "Play");
		# Create the About button
		self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 192, "About");

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

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

	def create_button(self, x, y, button_text):
		# Define constant width and height
		w = 196;
		h = 32;
		# Create the rectangle background
		self.create_rectangle(x - w/2 + h/2, y - h/2, x + w/2 - h/2, y + h/2, fill=C_COLOR_BLUE, outline="");
		# Create the two circles on both sides to create a rounded edge
		self.create_oval(x - w/2, y - h/2, x - w/2 + h, y + h/2, fill=C_COLOR_BLUE, outline="");
		self.create_oval(x + w/2 - h, y - h/2, x + w/2, y + h/2, fill=C_COLOR_BLUE, outline="");
		# Create the button text
		self.create_text(x, y, font="Helvetica 16 bold", text=button_text, fill=C_COLOR_BLUE_DARK);


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
    
# Main loop
root.mainloop();