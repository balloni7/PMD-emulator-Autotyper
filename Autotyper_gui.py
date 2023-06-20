import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

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

# Run the main loop
root.mainloop()