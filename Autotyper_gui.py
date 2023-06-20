import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
from collections import defaultdict
import pyautogui
import time
import re

def save_text():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename:
        with open(filename, "w") as file:
            text = text_box.get("1.0", "end-1c")  # Get the text from the text box
            file.write(text)

def load_text():
    filename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename:
        with open(filename, "r") as file:
            text = file.read()
            text_box.delete("1.0", "end")  # Clear the current text
            text_box.insert("1.0", text)  # Insert the loaded text


default_keys = ("C", "F", "H", "J", "K", "M", "N", "P", "Q", "R", "S",
                "T", "W", "X","Y", "0","1","2", "3", "4", "5", "6", "7",
                "8", "9", "@", "&", "-", "#", "%", "+", "=")

def map_key_positions(keys=default_keys):
    """ keys: list of all the keys you want to map
        filename: name of the file to save the mapping

        saves the mapping as a dictionary to a txt file
    """
    for i in range(5, -1, -1):
        print(f"{i}", end="\r", flush=True)
        time.sleep(1)

    pos_dict = {}

    for i in range(len(keys)):
        print(keys[i], end="\r")
        time.sleep(2)
        point = pyautogui.position()
        pos_dict[keys[i]] = (point[0], point[1])

    f = open("key_map.txt", "w")
    f.write(str(pos_dict))
    f.close()


default_keys = ("C", "F", "H", "J", "K", "M", "N", "P", "Q", "R", "S",
                "T", "W", "X","Y", "0","1","2", "3", "4", "5", "6", "7",
                "8", "9", "@", "&", "-", "#", "%", "+", "=")
def countdown(root, keys = default_keys):

    def next_key(index):
        timer = 5
        label.config(text=keys[index+1] + " - " + str(timer))
        update_countdown(index+1, timer)

    def update_countdown(index, timer):
        # Update the label with the current key and countdown value
        label.config(text=keys[index] + " - " + str(timer))
        if timer > 0:
            # Decrement the countdown time and schedule the next update
            timer -= 1
            root.after(1000, lambda: update_countdown(index, timer))
        else:
            # Countdown finished
            label.config(text="Done")
            root.after(1000, next_key(index))
            # Perform any action related to the countdown completion

    # Create a Toplevel window for displaying the countdown
    countdown_window = tk.Toplevel()
    countdown_window.title("Countdown")
    countdown_window.geometry("200x100")
    countdown_window.resizable(False, False)

    # Create a label for displaying the countdown
    label = tk.Label(countdown_window, font=("Arial", 36))
    label.pack(pady=20)

    label.config(text=keys[0] + " - " + "5")
    update_countdown(index=0, timer=5)



# Create the main window
root = tk.Tk()
root.title("GUI with Relative Positioning")

# Set the minimum and maximum dimensions of the window
root.minsize(800, 500)
root.maxsize(1200, 630)

# Convert the image to PhotoImage
background_image = ImageTk.PhotoImage(Image.open("29c953e9-6b99-403d-abbd-4a64d97d74c5-3623719-pokemon-mystery-dungeon-dx-thumb.jpg"))

# Set the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for the content
content_frame = ttk.Frame(root)
content_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

# Create a button
button = ttk.Button(content_frame, text="Click Me!")
button.place(relx=0.4, rely=0.1)

# Create a text box
text_box = tk.Text(content_frame)
text_box.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.4)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
# Add "Save" option to the "File" menu
file_menu.add_command(label="Save", command=save_text)
# Add "Load" option to the "File" menu
file_menu.add_command(label="Load", command=load_text)

# Create the "Setup" menu
setup_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Setup", menu=setup_menu)
#Add "Map Keys"
setup_menu.add_command(label="Map Keys", command= lambda:countdown(root=root,keys=default_keys))
#Add "Export Mapping"
setup_menu.add_command(label="Export Mapping")
#Add "Import Mapping"
setup_menu.add_command(label="Import Mapping")


# Run the main loop
root.mainloop()