import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import pyautogui
import time
import json
import re

def save_code():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename:
        with open(filename, "w") as file:
            text = text_box.get("1.0", "end-1c")  # Get the text from the text box
            file.write(text)


def load_code():
    filename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename:
        with open(filename, "r") as file:
            text = file.read()
            text_box.delete("1.0", "end")  # Clear the current text
            text_box.insert("1.0", text)  # Insert the loaded text


default_keys = ("C", "F", "H", "J", "K", "M", "N", "P", "Q", "R", "S",
                "T", "W", "X", "Y", "0", "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "@", "&", "-", "#", "%", "+", "=")


def export_mapping():
    target_file = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=(("Json Files", "*.json"), ("All Files", "*.*")))

    try:
        with open("positions.json", "rb") as src, open(target_file, "wb") as tgt:
            tgt.write(src.read())
        print(f"File cloned: {target_file}")
    except IOError as e:
        print(f"Error cloning file: {e}")


def import_mapping():
    source_file = filedialog.askopenfilename(filetypes=(("Json Files", "*.json"), ("All Files", "*.*")))

    try:
        with open(source_file, "rb") as src, open("positions.json", "wb") as tgt:
            tgt.write(src.read())
        print(f"File cloned: {source_file}")
    except IOError as e:
        print(f"Error cloning file: {e}")


def countdown(root, keys=default_keys):
    # initiate the dictionary with the positions
    pos_dict = {}

    def next_key(index):
        if index < len(keys):
            timer = 3
            label.config(text=keys[index] + ": " + str(timer))
            root.after(1000, lambda: update_countdown(index, timer))

        # if there are no more keys to map it saves the dictionary to a json file
        else:
            with open("positions.json", "w") as file:
                json.dump(pos_dict, file)

    def update_countdown(index, timer):
        # Update the label with the current key and countdown value
        label.config(text=keys[index] + ": " + str(timer))
        if timer > 0:
            # Decrement the countdown time and schedule the next update
            timer -= 1
            root.after(1000, lambda: update_countdown(index, timer))
        else:
            # Countdown finished
            label.config(text="Done")

            # Absolute coordinates of the current key
            point = pyautogui.position()
            pos_dict[keys[index]] = (point[0], point[1])

            # Next key to map
            root.after(1000, lambda: next_key(index + 1))


    # Create a Toplevel window for displaying the countdown
    countdown_window = tk.Toplevel()
    countdown_window.title("Countdown")
    countdown_window.geometry("200x100")
    countdown_window.resizable(False, False)
    countdown_window.attributes("-topmost", True)

    # Create a label for displaying the countdown
    label = tk.Label(countdown_window, font=("Arial", 36))
    label.pack(pady=20)

    # start the mapping loop
    update_countdown(index=0, timer=5)


def type_code(code):
    """
        code: a string containing the code you want to paste

        Pastes the wondermail code, you have 2 seconds to change to your emulator window
        The optimal way is to put the emulator in fullscreen, then map, and afterwards always
        paste the codes in fullscreen, that way u can make sure that the keys are in the
        same place as last time.
    """

    with open("positions.json", "r") as file:
        pos_dict = json.load(file)

    code = re.sub(r"[\n\t\s]*", "", code)

    time.sleep(2)
    for word in code:
        pyautogui.moveTo(pos_dict[word][0], pos_dict[word][1])
        pyautogui.mouseDown()
        pyautogui.mouseUp()

def clear_box():
    text_box.delete(1.0, tk.END)


# Create the main window
root = tk.Tk()
root.title("GUI with Relative Positioning")

# Set the minimum and maximum dimensions of the window
root.minsize(800, 500)
root.maxsize(1200, 630)

# Convert the image to PhotoImage
background_image = ImageTk.PhotoImage(
    Image.open("29c953e9-6b99-403d-abbd-4a64d97d74c5-3623719-pokemon-mystery-dungeon-dx-thumb.jpg"))

# Set the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for the content
content_frame = ttk.Frame(root)
content_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

# Create a button
type_button = ttk.Button(content_frame, text="Auto Type", command=lambda: (type_code(text_box.get("1.0", "end-1c")), clear_box() ))
type_button.place(relx=0.4, rely=0.1)

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
file_menu.add_command(label="Save Code", command=save_code)
# Add "Load" option to the "File" menu
file_menu.add_command(label="Load Code", command=load_code)

# Create the "Setup" menu
setup_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Setup", menu=setup_menu)
# Add "Map Keys"
setup_menu.add_command(label="Map Keys", command=lambda: countdown(root=root, keys=(default_keys)))
# Add "Export Mapping"
setup_menu.add_command(label="Export Mapping", command=export_mapping)
# Add "Import Mapping"
setup_menu.add_command(label="Import Mapping", command=import_mapping)

# Run the main loop
root.mainloop()
