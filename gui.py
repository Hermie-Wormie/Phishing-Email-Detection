import tkinter as tk
import re

def show_model():
    home_frame.pack_forget()
    model_frame.pack(fill='both', expand=True)

def show_home():
    model_frame.pack_forget()
    home_frame.pack(fill='both', expand=True)

def validate_URL_input(event=None):
    input_text = url_entry.get()
    if input_text.strip() == "":
        result_label.config(text="", fg='white')  # Clear the label if input is empty
        checkResults_button.grid(row=6, column=3, columnspan=2, pady=5)
        return
    url_pattern = re.compile(      
        r'^(?:https?://)?(?:www\.)'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
        r'(?:/\S*)?$',  
        re.IGNORECASE)

    if url_pattern.match(input_text):
        result_label.config(text="Valid URL", fg='green')
        checkResults_button.grid(row=6, column=3, columnspan=2, pady=5)  
    else:
        result_label.config(text="Invalid URL", fg='red')
        checkResults_button.grid_forget()  

def on_input_change(event):
    checkResults_button.grid_forget()
    validate_URL_input()

def check_phishing():
    print("phish")

# Create the main application window
root = tk.Tk()
root.geometry("800x600")
root.title("Phishing Email Detector")

# Create the title label
title_label = tk.Label(root, text="Phishing Email Detector", font=("system", 24, "bold"))
title_label.pack(pady=1)

# Create a frame to hold the home content
content_frame = tk.Frame(root)
content_frame.pack(fill='both', expand=True)

# Create the home frame
home_frame = tk.Frame(content_frame, bg='navy', borderwidth=2, relief='groove')
home_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Configure grid weights for centering
home_frame.grid_columnconfigure(0, weight=1)
home_frame.grid_columnconfigure(5, weight=1)
home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_rowconfigure(8, weight=1)

# Labels for the inputs
sender_label = tk.Label(home_frame, text="Enter the Sender:", bg='navy', fg='white')
sender_label.grid(row=1, column=2, padx=10, pady=5, sticky='e')

sender_entry = tk.Entry(home_frame)
sender_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

subject_label = tk.Label(home_frame, text="Enter the Subject:", bg='navy', fg='white')
subject_label.grid(row=2, column=2, padx=10, pady=5, sticky='e')

subject_entry = tk.Entry(home_frame)
subject_entry.grid(row=2, column=3, padx=10, pady=5, sticky='w')

content_label = tk.Label(home_frame, text="Enter the Content:", bg='navy', fg='white')
content_label.grid(row=3, column=2, padx=10, pady=5, sticky='e')

content_entry = tk.Entry(home_frame)
content_entry.grid(row=3, column=3, padx=10, pady=5, sticky='w')

url_label = tk.Label(home_frame, text="Enter URL (optional):", bg='navy', fg='white')
url_label.grid(row=4, column=2, padx=10, pady=10, sticky='e')

url_entry = tk.Entry(home_frame)
url_entry.grid(row=4, column=3, padx=10, pady=10, sticky='w')

# Bind the URL entry to detect changes
url_entry.bind('<KeyRelease>', on_input_change)

# Label to display validation results
result_label = tk.Label(home_frame, text="", bg='navy', fg='white')
result_label.grid(row=5, column=3, columnspan=2)

# Button to switch to the model
to_model_button = tk.Button(home_frame, text="See classification Model", command=show_model)
to_model_button.grid(row=8, column=2, columnspan=2, pady=5, sticky='s')

checkResults_button = tk.Button(home_frame, text="Check for Phishing", command=check_phishing)
checkResults_button.grid(row=6, column=3, columnspan=2, pady=5)

# Create the model frame
model_frame = tk.Frame(root)

# Button to switch back to the home frame
to_home_button = tk.Button(model_frame, text="Back to Home", command=show_home)
to_home_button.pack(pady=1)

# Show the home frame initially
home_frame.pack(fill='both', expand=True)

# Run the application
root.mainloop()