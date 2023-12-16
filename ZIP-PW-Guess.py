import zipfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox

txt_paths = []  # file paths of TXT files

def test_pass(zip_file, password, password_entry):
    """try to guess password."""
    try:
        zip_file.extractall(pwd=password.encode())
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)  # insert the password in the entry
        messagebox.showinfo("Password Found", f"Password found: {password}")
        return password
    except Exception as ex:
        print("An error occurred: %s" % (ex))
        return None

def browse_zip_file():
    """select ZIP file."""
    file_path = filedialog.askopenfilename(filetypes=[("Zip File", "*.zip")])
    return file_path

def browse_txt_files():
    """select TXT files."""
    global txt_paths
    txt_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    return txt_paths

# function to Guess password
def crack_password(zip_path, txt_paths, password_entry):
    """ guess password."""
    if not zip_path:
        messagebox.showwarning("No ZIP File Selected", "Please select a ZIP file.")
        return
    
    if not txt_paths:
        messagebox.showwarning("No TXT Files Selected", "Please select TXT files containing passwords.")
        return
    
    zip_obj = zipfile.ZipFile(zip_path)
    for txt_path in txt_paths:
        if os.path.exists(txt_path):
            with open(txt_path, "r") as filepass:
                for word in filepass.readlines():
                    password = word.strip() 
                    guess_password = test_pass(zip_obj, password, password_entry)
                    if guess_password:
                        return
        else:
            messagebox.showwarning("File Not Found", f"File {txt_path} not found.")
    
    messagebox.showinfo("No Password Found", "No password found in the specified TXT files.")

def create_gui():
    """ Creates a GUI for the ZIP PW Guess application."""
    root = tk.Tk()
    root.title("ZIP PW Guess")  # name of the application
    
    # set window position
    window_width = 250
    window_height = 180
    root.geometry(f"{window_width}x{window_height}+{root.winfo_screenwidth() // 2 - window_width // 2}+{root.winfo_screenheight() // 2 - window_height // 2}")

    root.resizable(False, False)  # fix window size

    # frames
    frame1 = tk.Frame(root)
    frame1.pack(pady=10)

    def browse_txt_and_display():
        global txt_paths
        txt_paths = browse_txt_files()
        if txt_paths:
            txt_files_label.config(text=", ".join(os.path.basename(path) for path in txt_paths))

    browse_txt_button = tk.Button(frame1, text="Select TXT Files", command=browse_txt_and_display)
    browse_txt_button.grid(row=0, column=0, padx=10)

    txt_files_label = tk.Label(frame1, text="", width=30, anchor='w')
    txt_files_label.grid(row=0, column=1)

    frame2 = tk.Frame(root)
    frame2.pack(pady=10)

    browse_zip_button = tk.Button(frame2, text="Select ZIP File", command=lambda: crack_password(browse_zip_file(), txt_paths, password_entry))
    browse_zip_button.grid(row=0, column=0, padx=10, pady=10)

    password_label = tk.Label(frame2, text="Password")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password_entry = tk.Entry(frame2, show='')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

#copyright
    copyright_font = ("Segoe UI", 6)
    copyright_label = tk.Label(frame2, text="Copyright © 2023,\n Coded by Rami Dalati", font=copyright_font)
    copyright_label.grid(row=2, column=0, padx=0, pady=0, sticky='sw')
    root.mainloop()  # Run the GUI

if __name__ == '__main__':
    create_gui()
