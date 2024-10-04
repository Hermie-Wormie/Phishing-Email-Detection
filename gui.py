import tkinter as tk
from tkinter import filedialog
import re
import webbrowser
from VirusTotal import *
from model_test import *
from model_train import *

#=========================== Functions ===========================

def show_home():
    model_frame.pack_forget()
    phishingResult_frame.pack_forget()
    home_frame.pack(fill='both', expand=True)

def show_model():
    #home_frame.pack_forget()
    #model_frame.pack(fill='both', expand=True)
    plot_confusion_matrix(y_test, y_pred)

def show_phishingResult():
    home_frame.pack_forget()
    phishingResult_frame.pack(fill='both', expand=True)

def validate_URL_input():
    input_text = url_entry.get().strip()
    if input_text == "":  
        result_label.config(text="", fg='white')
        return True  
    
    # URL validation RegEx pattern, HTTP:// HTTPS:// is optional
    url_pattern = re.compile(
        r'^(?:https?://)?(?:www\.)'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
        r'(?:/\S*)?$',  
        re.IGNORECASE)

    # Check if URL is valid
    if url_pattern.match(input_text):
        result_label.config(text="Valid URL", fg='green')
        return True  
    else:
        result_label.config(text="Invalid URL", fg='red')
        return False  

def on_input_change(event):
    checkResults_button.grid_forget()
    validate_URL_input()

def check_phishing():
    url = url_entry.get().strip()
    hash = hash_entry.get().strip()
    sender = sender_entry.get().strip()
    subject = subject_entry.get().strip()
    content = content_entry.get().strip()
    emailPositive = check_email(sender, subject, content)
    urlPositive = check_url(url)
    hashPositive = check_hash(hash)
    urlPositive_button.grid_forget()
    hashPositive_button.grid_forget()

    emailPositive_label.config(text=f"Based on our dataset, your email is likely to be a:     {emailPositive}")
    if isinstance(urlPositive, tuple):
        urlPositive_label.config(text=f"Number of positive results for malicious URL:           {urlPositive[0]}")
        urlPositive_button.grid(row=2, column=2, padx=5, pady=5, sticky='w')
    elif urlPositive == "Clean URL":
        urlPositive_label.config(text="Number of positive results for malicious URL:           Clean URL")
    elif urlPositive == "URL not found in VirusTotal database":
        urlPositive_label.config(text="Number of positive results for malicious URL:           URL not found in VirusTotal")
    else:
        urlPositive_label.config(text="Number of positive results for malicious URL:           No input provided")

    if isinstance(hashPositive, tuple):
        hashPositive_label.config(text=f"Number of positive results for malicious Hash:         {hashPositive[0]}")
        hashPositive_button.grid(row=3, column=2, padx=5, pady=5, sticky='w')
    elif hashPositive == "The file is clean.":
        hashPositive_label.config(text="Number of positive results for malicious Hash:         Clean File")
    elif hashPositive == "Hash of file not found in VirusTotal database.":
        hashPositive_label.config(text="Number of positive results for malicious Hash:         File Hash not found in VirusTotal")
    else:
        hashPositive_label.config(text="Number of positive results for malicious Hash:         No input provided")
    show_phishingResult()

def view_URL_positives():
    url = url_entry.get().strip()
    urlPositive = (check_url(url))
    hyperlink = urlPositive[1]
    webbrowser.open(hyperlink)

def view_hash_positives():
    hash = hash_entry.get().strip()
    hashPositive = (check_hash(hash))
    hyperlink = hashPositive[1]
    webbrowser.open(hyperlink)

def check_entries():
    sender = sender_entry.get().strip()
    subject = subject_entry.get().strip()
    content = content_entry.get().strip()

    # Email validation RegEx pattern
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if sender is a valid email
    if not re.match(email_pattern, sender):
        result_label.config(text="Invalid sender email!", fg='red')
        checkResults_button.grid_forget()
        return

    # Check if subject and content are non-empty
    if subject == "":
        result_label.config(text="Subject cannot be empty!", fg='red')
        checkResults_button.grid_forget()
        return

    if content == "":
        result_label.config(text="Content cannot be empty!", fg='red')
        checkResults_button.grid_forget()
        return

    # Call URL validation and store the result
    url_is_valid = validate_URL_input()

    # Only show the check button if all fields are valid
    if url_is_valid:
        checkResults_button.grid(row=7, column=2, pady=5, padx=15, sticky='w')  # Show the check button
    else:
        checkResults_button.grid_forget()  # Hide the check button if URL is invalid

def bind_entries():
    sender_entry.bind('<KeyRelease>', lambda event: check_entries())
    subject_entry.bind('<KeyRelease>', lambda event: check_entries())
    content_entry.bind('<KeyRelease>', lambda event: check_entries())
    url_entry.bind('<KeyRelease>', lambda event: check_entries())

def upload_file():
    file_path = filedialog.askopenfilename()
    
    if file_path:
        hash = file_to_hash(file_path)
        hash_entry.delete(0, tk.END)  # Clear any existing text in the entry
        hash_entry.insert(0, hash)  # Insert "12345" into the hash_entry

# Create the main application window
root = tk.Tk()
root.geometry("800x600")
root.title("Phishing Email Detector") # Title of GUI
root.resizable(False, False)

# Create the title label
title_label = tk.Label(root, text="Phishing Email Detector", font=("system", 24, "bold"))
title_label.pack(pady=1)

#=========================== Home Page Content ===========================

# Create a frame to hold the home content
content_frame = tk.Frame(root)
content_frame.pack(fill='both', expand=True)

# Create the home frame
home_frame = tk.Frame(content_frame, bg='navy', borderwidth=2, relief='solid')

# Show the home frame initially
home_frame.pack(fill='both', expand=True)

# Configure grid weights for centering
home_frame.grid_columnconfigure(0, weight=1)
home_frame.grid_columnconfigure(1, weight=1)
home_frame.grid_columnconfigure(5, weight=1)
home_frame.grid_columnconfigure(2, weight=1)
home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_rowconfigure(7, weight=1)
home_frame.grid_rowconfigure(8, weight=1)

# Labels and entries for the inputs
sender_label = tk.Label(home_frame, text="Enter the Sender:", bg='navy', fg='white')
sender_label.grid(row=1, column=1, padx=10, pady=5, sticky='e')
sender_entry = tk.Entry(home_frame, width=45)
sender_entry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

subject_label = tk.Label(home_frame, text="Enter the Subject:", bg='navy', fg='white')
subject_label.grid(row=2, column=1, padx=10, pady=5, sticky='e')
subject_entry = tk.Entry(home_frame, width=45)
subject_entry.grid(row=2, column=2, padx=10, pady=5, sticky='w')

content_label = tk.Label(home_frame, text="Enter the Content:", bg='navy', fg='white')
content_label.grid(row=3, column=1, padx=10, pady=5, sticky='e')
content_entry = tk.Entry(home_frame, width=45)
content_entry.grid(row=3, column=2, padx=10, pady=5, sticky='w')

url_label = tk.Label(home_frame, text="Enter URL (optional):", bg='navy', fg='white')
url_label.grid(row=4, column=1, padx=10, pady=10, sticky='e')
url_entry = tk.Entry(home_frame, width=45)
url_entry.grid(row=4, column=2, padx=10, pady=10, sticky='w')

hash_label = tk.Label(home_frame, text="Enter Hash (optional):", bg='navy', fg='white')
hash_label.grid(row=5, column=1, padx=10, pady=5, sticky='e')

hash_entry = tk.Entry(home_frame, width=45)
hash_entry.grid(row=5, column=2, padx=10, pady=5, sticky='w')

# File upload section
upload_button = tk.Button(home_frame, text="Upload File to get Hash", command=upload_file)
upload_button.grid(row=7, column=1, sticky='e')  # Positioned in the right column

checkResults_button = tk.Button(home_frame, text="Check for Phishing", command=check_phishing, width=35)


# Bind the URL entry to detect changes
url_entry.bind('<KeyRelease>', on_input_change)

# Label to display validation results
result_label = tk.Label(home_frame, text="", bg='navy', fg='white', anchor='w', width=20)
result_label.grid(row=7, column=2, pady=5, padx=9, sticky='nw', columnspan=2)

# Button to switch to the model
to_model_button = tk.Button(home_frame, text="See classification Model", command=show_model)
to_model_button.grid(row=10, column=1, columnspan=3, pady=5, sticky='s')

#=========================== Model Page Content ===========================

# Create the model frame
model_frame = tk.Frame(content_frame, bg='navy', borderwidth=2, relief='solid')


# Button to switch back to the home frame
to_home_button = tk.Button(model_frame, text="Back to Home Page", command=show_home)
to_home_button.grid(pady=10, padx=10)




#=========================== Phishing Results Page Content ===========================
# Phishing Results page
phishingResult_frame = tk.Frame(content_frame, bg='navy', borderwidth=2, relief='solid')
emailPositive_label = tk.Label(phishingResult_frame, bg='navy', fg='white', text="Based on our dataset, your email is likely to be: ")
emailPositive_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')

urlPositive_label = tk.Label(phishingResult_frame, bg='navy', fg='white', text="Number of positive results for malicious URL: ")
urlPositive_label.grid(row=2, column=1, padx=5, pady=5, sticky='w')
urlPositive_button = tk.Button(phishingResult_frame, text="View malicious URL Flags", command=view_URL_positives)
urlPositive_button.grid(row=2, column=2, padx=5, pady=5, sticky='w')

hashPositive_label = tk.Label(phishingResult_frame, bg='navy', fg='white', text="Number of positive results for malicious Hash: ")
hashPositive_label.grid(row=3, column=1, padx=5, pady=5, sticky='w')
hashPositive_button = tk.Button(phishingResult_frame, text="View malicious Hash Flags", command=view_hash_positives)
hashPositive_button.grid(row=3, column=2, padx=5, pady=5, sticky='w')

to_home_button = tk.Button(phishingResult_frame, text="Back to Home Page", command=show_home)
to_home_button.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

phishingResult_frame.grid_columnconfigure(0, weight=1)
phishingResult_frame.grid_columnconfigure(1, weight=1)
phishingResult_frame.grid_columnconfigure(3, weight=1)
phishingResult_frame.grid_columnconfigure(4, weight=1)
phishingResult_frame.grid_rowconfigure(0, weight=1)
phishingResult_frame.grid_rowconfigure(4, weight=1)

# Bind entry validation
bind_entries()

# Run the application
root.mainloop()
