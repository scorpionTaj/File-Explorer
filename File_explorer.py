from tkinter import *
from tkinter import filedialog
import os

# Function for opening the file explorer window
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files", "*.txt*"),
                                                     ("All files", "*.*")))
    if filename:
        label_current_directory.config(text="File Opened: " + filename)

# Function to open the selected item
def open_selected_item(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        item = widget.get(index)
        path = os.path.join(current_directory.get(), item)
        if os.path.isfile(path):
            os.startfile(path)
        elif os.path.isdir(path):
            current_directory.set(path)
            update_file_list()

# Function to navigate to the previous directory
def go_to_previous_directory():
    current_dir = current_directory.get()
    parent_dir = os.path.dirname(current_dir)
    if parent_dir:
        current_directory.set(parent_dir)
        update_file_list()

# Function to navigate to the next directory
def go_to_next_directory():
    current_dir = current_directory.get()
    if current_dir in directory_history:
        index = directory_history.index(current_dir)
        if index < len(directory_history) - 1:
            next_dir = directory_history[index + 1]
            current_directory.set(next_dir)
            update_file_list()

# Function to update the file list based on the selected directory
def update_file_list():
    directory = current_directory.get()
    if os.path.isdir(directory):
        file_list.delete(0, END)
        for item in os.listdir(directory):
            file_list.insert(END, item)

        # Update navigation history
        if directory not in directory_history:
            directory_history.append(directory)

# Create the root window
window = Tk()
window.title('File Explorer')
window.geometry("600x500")
window.config(background="white")

# Variable to store the current directory
current_directory = StringVar()

# Label to display the current directory
label_current_directory = Label(window, textvariable=current_directory, width=70, height=2, bg="lightgrey")

# Listbox to display the file list
file_list = Listbox(window, width=80, height=20, bg="white", selectmode=SINGLE)
file_list.bind('<Double-Button-1>', open_selected_item)

# Button to browse files
button_browse_files = Button(window, text="Browse Files", command=browse_files)

# Button to change directory to the previous directory
button_previous_directory = Button(window, text="Previous", command=go_to_previous_directory)

# Button to change directory to the next directory
button_next_directory = Button(window, text="Next", command=go_to_next_directory)

# Arrange widgets using grid layout
label_current_directory.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
file_list.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
button_browse_files.grid(row=2, column=0, padx=10, pady=10, sticky=W)
button_previous_directory.grid(row=2, column=1, padx=10, pady=10, sticky=W)
button_next_directory.grid(row=2, column=1, padx=10, pady=10, sticky=E)

# Initialize navigation history list
directory_history = []

# Start with the current directory set to the home directory
current_directory.set(os.path.expanduser("~"))
update_file_list()

# Run the Tkinter event loop
window.mainloop()
