import tkinter as tk
import tkinter.ttk as ttk
import time
#A standard message box


from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import numpy as np
import os
import serial

class DemoApp(object):
    """Layout demo."""

    def __init__(self, master=None, compartment_open = False):
        
            # Defining the master window for the GUI            
        self._master = master
        
            # Defining the window width and height (as given by the display)
        self._main_width = 800
        self._main_height = 480
        
            # Resizing the window geometry
        self._master.geometry(str(self._main_width)+"x"+str(self._main_height))
        
            # Changing the name of the window
        self._master.title("Smart Bin")
        
        self._state = "Main"
        self._user_accepted = 0
        self._rotation = tk.IntVar(0)
        
        
            # Start the function to create the images and load them in dictionaries
        #self.create_images()
        
            # Start the animation 
        #self.start_animation()
            
            # Create the main layout
        #self.create_main_layout()
        self.testing_display()
        

    def create_images(self):
        
            # Create dictionary to store the images
        self._images = {}
        
            # Load all the images in the images dictionary
        self.load_folder_images("C:/Users/javie/OneDrive - University College London/UCL/Year 4/MEng Capstone/Display/all")
        
            # Store all the gif images
        self._gif_start = self.load_gifs("C:/Users/javie/OneDrive - University College London/UCL/Year 4/MEng Capstone/Display/gifs/start.gif")
        self._gif_loading =  self.load_gifs("C:/Users/javie/OneDrive - University College London/UCL/Year 4/MEng Capstone/Display/gifs/loading.gif")
        self._gif_bin_top_open = self.load_gifs("C:/Users/javie/OneDrive - University College London/UCL/Year 4/MEng Capstone/Display/gifs/bin_top_open.gif")
        self._gif_cooking = self.load_gifs("C:/Users/javie/OneDrive - University College London/UCL/Year 4/MEng Capstone/Display/gifs/cooking.gif")
        
    def start_animation(self):
        
        self._state = "Loading Animation"
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
    
        self._start_canvas = tk.Label(self._main_frame)
        self._start_canvas.pack()
        
        for frame in range(1,len(self._gif_start)-3):
            self._start_canvas.configure(image=self._gif_start[frame])
            time.sleep(0.0001)
            self._start_canvas.update()
            
        #time.sleep(1)
        
    def testing_display(self):
        self._output = None
        self._state = "Testing"
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()

        self._dry_recyclables_button = tk.Button(self._main_frame, text = "General", command = self.send_signal_general)
        self._dry_recyclables_button.pack(side = tk.LEFT, expand = 1, fill =tk.BOTH)

        self._organic_button = tk.Button(self._main_frame, text = "Dry", command = self.send_signal_dry)
        self._organic_button.pack(side = tk.LEFT, expand = 1, fill =tk.BOTH)

        self._waste_button = tk.Button(self._main_frame, text = "Organic",  command = self.send_signal_organic)
        self._waste_button.pack(side = tk.LEFT, expand = 1, fill =tk.BOTH)

        self._other_recyclables_button = tk.Button(self._main_frame, text = "Paper", command = self.send_signal_paper)
        self._other_recyclables_button.pack(side = tk.LEFT, expand = 1, fill =tk.BOTH)
        

    def send_signal(self, output):
        
        #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        #ser.flush()
        #ser.write((output+"\n").encode('utf-8'))
        #line = ser.readline().decode('utf-8').rstrip()
        pass
        
    def send_signal_paper(self):
        self._output ="Paper"
        #return self._output

    
    
    def send_signal_organic(self):
        self._output ="Organic"

        
    def send_signal_dry(self):
        self._output = "Dry"
        
        
    def send_signal_general(self):
        self._output = "General"
        
        
    def create_main_layout(self):    
        
        self.destroy()   
        self._state = "Main"
        
        self._logo = tk.Label(self._master, width = 800, height = 100,image = self._images["logo"])
        self._logo.pack()
        
            # Create a frame and put some buttons in it
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        self._main_frame.pack_propagate(0)
        
    
        self._open_bin_button = ttk.Button(self._main_frame, text = "Open Bin", image = self._images["open"], compound = tk.TOP, command = self.open_bin)
        self._open_bin_button.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        self._open_bin_button.image = self._images["open"]
    
    
        self._cooking_mode_button = ttk.Button(self._main_frame, text="Cooking Mode",  image = self._images["cooking_mode"], compound = tk.TOP, command = self.cooking_mode)
        self._cooking_mode_button.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        self._cooking_mode_button.image = self._images["cooking_mode"]        
        
        
        self._cleaning_mode_button = ttk.Button(self._main_frame, text="Cleaning Mode",  image = self._images["cleaning_mode"], compound = tk.TOP, command = self.cleaning_mode)
        self._cleaning_mode_button.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        self._cleaning_mode_button.image = self._images["cleaning_mode"]        
        
       
        self._capacity_button = ttk.Button(self._main_frame, text="Check Capacity",  image = self._images["check_capacity"],  compound = tk.TOP,command = self.check_capacity)
        self._capacity_button.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        self._capacity_button.image = self._images["check_capacity"]
        
    
        

    def destroy(self):
        
        if self._state == "Main":
            self._logo.destroy()
            self._main_frame.destroy()
        
        elif self._state == "Capacity":
            self._frame_top.destroy()
            self._frame_med.destroy()
            self._frame_bottom.destroy()
            
        elif self._state == "Stop Bin":
            self._main_frame.destroy()
            
            
        elif self._state == "Bin Open":
            self._main_frame.destroy()
          
        elif self._state == "Warning Message":
            self._main_frame.destroy()
            
        elif self._state == "Loading Animation":
            self._main_frame.destroy()
            
        elif self._state == "Cooking":
            self._main_frame.destroy()
            
        elif self._state == "Cleaning":
            self._main_frame.destroy()
            
        elif self._state == "Testing":
            self._main_frame.destroy()
        
    def return_main(self):
        
        self.destroy()
        self.create_main_layout()
        
        
        
        
    def open_bin(self):
        
        self.destroy()
        self._state = "Bin Open"
        
        
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        
        
        self._loading_canvas = tk.Label(self._main_frame)
        self._loading_canvas.pack()
        
        for frame in range(1,len(self._gif_bin_top_open)):
            
            self._loading_canvas.configure(image=self._gif_bin_top_open[frame])
            time.sleep(0.01)
            self._loading_canvas.update()
            
        for frame in range(len(self._gif_bin_top_open),0,-1):
            
            
            self._loading_canvas.configure(image=self._gif_bin_top_open[frame])
            time.sleep(0.01)
            self._loading_canvas.update()
            
        self.return_main()    
        
        
    def cooking_mode(self):
        
        self.destroy()
        self._state = "Cooking"
        
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        
        self._return = tk.Button(self._main_frame , text="Return",bg='green', command = self.return_main)
        self._return.pack()
        
        self._cooking_canvas = tk.Label(self._main_frame)
        self._cooking_canvas.pack()
        
        
        while self._state == "Cooking":
            for frame in range(1,len(self._gif_cooking)):
                self._cooking_canvas.configure(image=self._gif_cooking[frame])
                time.sleep(0.02)
                self._cooking_canvas.update()
        

    def cleaning_mode(self):
        
        self.destroy()
        self._state = "Cleaning"
        
        
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        
        if self._rotation.get()%10 == 5:
            self._angle = tk.Label(self._main_frame, image = self._images["bin_open_45"])
            self._angle.pack()
        
        else:
            self._angle = tk.Label(self._main_frame, image = self._images["bin_open_0"])
            self._angle.pack()
            
        self._rotate_button = tk.Button(self._main_frame, text = "Rotate 45", command = self.rotate)
        self._rotate_button.pack()
        
        if self._rotation.get() == 360:
            self.return_main()
        
        
    def rotate(self):
        self._rotation.set(self._rotation.get() + 45)
        self.cleaning_mode()
        
       
    
    def check_capacity(self):
        
            # Destroy the main frame
        self.destroy()
        self._state = "Capacity"
        
            # Defining the height of the Capacity windows buttons
        self._capacity_layout_buttons_height = 100
        
            # Defining the height of the 4 frames for each bin            
        self._bin_frames_height = (self._main_height-self._capacity_layout_buttons_height)/2

            # Creating the capacity layout
        self.create_capacity_layout()
        
        
        
    def create_capacity_layout(self):
        
        self._frame_top = tk.Frame(self._master, width = self._main_width, height = self._bin_frames_height)
        self._frame_top.pack()
        
        self._frame_med = tk.Frame(self._master, width = self._main_width, height = self._bin_frames_height)
        self._frame_med.pack()
        
        self._frame_bottom = tk.Frame(self._master, width = self._main_width, height = self._capacity_layout_buttons_height)
        self._frame_bottom.pack()
        
        capacity_bin_1 = 50
        self._label_bin1 = tk.Label(self._frame_top,  width = self._main_width/2, height =  self._bin_frames_height, text = "Bin 1", compound = tk.TOP, image = self.create_bin_capacity_image(capacity_bin_1))
        self._label_bin1.pack(side = tk.LEFT)
        
        capacity_bin_2 = 30
        self._label_bin2 = tk.Label(self._frame_top,  width = self._main_width/2, height =  self._bin_frames_height, text = "Bin 2", compound = tk.TOP, image = self.create_bin_capacity_image(capacity_bin_2))
        self._label_bin2.pack(side = tk.LEFT)
        
        capacity_bin_3 = 0
        self._label_bin3 = tk.Label(self._frame_med,  width = self._main_width/2, height =  self._bin_frames_height, text = "Bin 3", compound = tk.TOP,image = self.create_bin_capacity_image(capacity_bin_3))
        self._label_bin3.pack(side = tk.LEFT)
        
        capacity_bin_4 = 75
        self._label_bin4 = tk.Label(self._frame_med,  width = self._main_width/2, height =  self._bin_frames_height, text = "Bin 4", compound = tk.TOP,image = self.create_bin_capacity_image(capacity_bin_4))
        self._label_bin4.pack(side = tk.LEFT)
        
        
        self._return = tk.Button(self._frame_bottom , text="Return",bg='green', command = self.return_main)
        self._return.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        
        self._return = tk.Button(self._frame_bottom , text="Stop Bin",bg='green' , command = self.stop_bin)
        self._return.pack(side = tk.LEFT, expand = 1)
        

        
    def stop_bin(self):
        self.destroy()
        self._state = "Stop Bin"
        
        
        self._main_frame = tk.Frame(self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        
        self._stop_label = tk.Label (self._main_frame, image = self._images["stop"])
        self._stop_label.pack()
        
        
        self._bin_restart = tk.Button(self._main_frame, text="Restart Bin", bg='green' , command = self.warning_message)
        self._bin_restart.pack()

    def create_bin_capacity_image(self, capacity):
        if capacity <25:
            return self._images["bin_0"]
        elif (capacity>=25) and (capacity<50):
            return self._images["bin_25"]
        elif (capacity>=50) and (capacity<75):
            return self._images["bin_75"]
        elif (capacity>=75) and (capacity<=100):
            return self._images["bin_100"]
    
    def load_folder_images(self,image_folder):
        
            # Obtain all images from a folder and save them in a dictionary        
        for filename in os.listdir(image_folder):
            
                # Obtain the path for each image                
            image_path = image_folder + "/" + filename
                # Opening the image
            pilImage = Image.open(image_path)
                # Converting it to tkinter Photo Object
            tk = ImageTk.PhotoImage(pilImage)
                # Delete file extension
            filename = filename[:-4]
                # Adding the file to the images dictionary
            self._images[filename] = tk
            
    def load_gifs(self, gif_path):
            
            # Function to return a dictionary containing all the frames for the .gif            
            
            # Create a sample dictionary
        sample_dict = {}
            # Open the gif file from the given path
        gif = Image.open(gif_path)
            # Obtaining the number of frames
        gif_frames = gif.n_frames
        item=0
            # For loop for all the frames            
        for frame in ImageSequence.Iterator(gif):
            item +=1
            gif_image = frame
            resized_gif = gif_image.resize((self._main_width,self._main_height))
            gif_tk  = ImageTk.PhotoImage(resized_gif)
            sample_dict[item] = gif_tk
            
            # Return the sample dictionary
        return sample_dict   
    
    def warning_message(self):
        self.destroy()
        self._status = "Warning Message"
        
        
        self._main_frame = tk.Frame (self._master, width = self._main_width, height = self._main_height)
        self._main_frame.pack()
        
        self._warning_label = tk.Label(self._main_frame, text = "Are you sure that you want to " + self._state +" ?")
        self._warning_label.pack()
        
        self._yes_button = tk.Button(self._main_frame, text = "Yes", command = self.create_main_layout)
        self._no_button = tk.Button(self._main_frame, text = "No", command = self.stop_bin)
        
        self._yes_button.pack()
        self._no_button.pack()



#root = tk.Tk()
#app = display.DemoApp(root)
#root.mainloop()
