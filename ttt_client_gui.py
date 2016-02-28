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

	def __init__(self, canvas, x, y, button_text):
		self.canvas = canvas;
		# Generate a unique id for each button (for tags)
		self.id = str(CanvasButton.count);
		CanvasButton.count = CanvasButton.count + 1;

		# Create the rectangle background
		rect = canvas.create_rectangle(x - self.WIDTH/2 + self.HEIGHT/2, y - self.HEIGHT/2, x + self.WIDTH/2 - self.HEIGHT/2, y + self.HEIGHT/2, fill=C_COLOR_BLUE, outline="", tags=("btn_bg" + self.id, "rect" + self.id));
		# Create the two circles on both sides to create a rounded edge
		oval_l = canvas.create_oval(x - self.WIDTH/2, y - self.HEIGHT/2, x - self.WIDTH/2 + self.HEIGHT, y + self.HEIGHT/2, fill=C_COLOR_BLUE, outline="", tags=("btn_bg" + self.id, "oval_l" + self.id));
		oval_r = canvas.create_oval(x + self.WIDTH/2 - self.HEIGHT, y - self.HEIGHT/2, x + self.WIDTH/2, y + self.HEIGHT/2, fill=C_COLOR_BLUE, outline="", tags=("btn_bg" + self.id, "oval_r" + self.id));
		# Create the button text
		canvas.create_text(x, y, font="Helvetica 16 bold", text=button_text, fill=C_COLOR_BLUE_DARK);
		# Bind events
		canvas.tag_bind("rect" + self.id, "<Enter>", self.btn_on_enter_rect);
		canvas.tag_bind("oval_l" + self.id, "<Enter>", self.btn_on_enter_oval_l);
		canvas.tag_bind("oval_r" + self.id, "<Enter>", self.btn_on_enter_oval_r);
		canvas.tag_bind("btn_bg" + self.id, "<Leave>", self.btn_on_leave);
		canvas.tag_bind("rect" + self.id, "<Leave>", self.btn_on_leave_rect);
		canvas.tag_bind("oval_l" + self.id, "<Leave>", self.btn_on_leave_oval_l);
		canvas.tag_bind("oval_r" + self.id, "<Leave>", self.btn_on_leave_oval_r); 
		# Create a dictionary used to mark when a component is hovered 
		self.entered = {"rect" + self.id: False, "oval_l" + self.id: False, "oval_r" + self.id: False};

	def btn_on_enter(self, event):
		self.canvas.itemconfig("btn_bg" + self.id, fill=C_COLOR_BLUE_DARK);

	def btn_on_enter_rect(self, event):
		self.entered["rect" + self.id] = True;
		self.btn_on_enter(event);

	def btn_on_enter_oval_l(self, event):
		self.entered["oval_l" + self.id] = True;
		self.btn_on_enter(event);

	def btn_on_enter_oval_r(self, event):
		self.entered["oval_r" + self.id] = True;
		self.btn_on_enter(event);

	def btn_on_leave(self, event):
		if(self.entered["rect" + self.id] == False and self.entered["oval_l" + self.id] == False and self.entered["oval_r" + self.id] == False):
			self.canvas.itemconfig("btn_bg" + self.id, fill=C_COLOR_BLUE);

	def btn_on_leave_rect(self, event):
		self.entered["rect" + self.id] = False;
		self.btn_on_leave(event);

	def btn_on_leave_oval_l(self, event):
		self.entered["oval_l" + self.id] = False;
		self.btn_on_leave(event);

	def btn_on_leave_oval_r(self, event):
		self.entered["oval_r" + self.id] = False;
		self.btn_on_leave(event);

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
		self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 136, "Play");
		# Create the About button
		self.create_button(C_WINDOW_WIDTH/2, C_WINDOW_HEIGHT/2 + 192, "About");

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

	def create_button(self, x, y, button_text):
		return CanvasButton(self, x, y, button_text);

# Define a subclass of BaseScene for the about scene
class AboutScene(BaseScene):

	def __init__(self, parent):
		BaseScene.__init__(self, parent);

		# Create a blue arch at the bottom of the canvas
		self.create_arc((-64, C_WINDOW_HEIGHT - 192, C_WINDOW_WIDTH + 64, C_WINDOW_HEIGHT + 368), start=0, extent=180, fill=C_COLOR_BLUE, outline="");

		# Tag all of the drawn widgets for later reference
		self.addtag_all("all");

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
# Pack the about scene
about_scene.pack();
# Give a reference to the welcome scene for switching between scenes
welcome_scene.about_scene = about_scene;
    
# Main loop
root.mainloop();