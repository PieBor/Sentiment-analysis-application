import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import logic
import json

#loads models and vectorizer from file
models,vectorizer=logic.load_models_and_vectorizer()

# Create a new Tk root window
root = tk.Tk()
root.title("Sentia")

#Create a frame for model selection
model_Select=ttk.Frame(root)
model_Select.pack(side=tk.TOP, padx=10, pady=10)

#Creating label
label=ttk.Label(model_Select,text="Select your model:")
label.pack(side="left")

# Create a select box
model_names = ["svm", "logistic_regression", "nb", "k-neighbors", "random_forest"]

select_box = ttk.Combobox(model_Select, values=model_names, state="readonly",width=15)
select_box.current(0)  # Set the default selection
select_box.pack(side=tk.RIGHT)
selected_model=select_box.get()



# Create a frame to hold the label, text input, and analyse button
frame = ttk.Frame(root)
frame.pack()

# Create a Label
label = ttk.Label(frame, text="Text")
label.pack(side=tk.LEFT)

# Create an Entry for text input
text_input = tk.Entry(frame)
text_input.pack(side=tk.LEFT)

# Create an Analyse button
def analyse():
    text = text_input.get()
    selected_model = select_box.get()
    print(f"Analysing with {selected_model}: {text}")
    # analysis code here
    sentiment=logic.predict_single_sentiment(text,selected_model,models,vectorizer)
    # Insert the result into the next available position in the table
    next_index = len(table.get_children()) + 1
    table.insert('', 'end', values=(next_index, text, sentiment)) 
analyse_button = ttk.Button(frame, text="Analyse Sentiment", command=analyse)
analyse_button.pack(side=tk.LEFT)



# Create a progress bar
progress_bar = ttk.Progressbar(root, length=200)
progress_bar.pack()

# Create a button for file selection
def select_file():
    file_name = filedialog.askopenfilename()
    print(f"Selected file: {file_name}")

    # Load the JSON file
    with open(file_name, 'r') as file:
        data = json.load(file)

    # Determine the total number of entries in the JSON data
    total_entries = len(data)

    # Reset the progress bar
    progress_bar['value'] = 0
    progress_bar['maximum'] = total_entries

    # Process the entries in the JSON data
    for entry in data:
        #data processing
        sentiment=logic.predict_single_sentiment(entry['text'],selected_model,models,vectorizer)
        # Insert the values into the table
        table.insert('', 'end', values=(entry['index'], entry['text'], sentiment))

        # Update the progress bar
        progress_bar['value'] += 1
        root.update_idletasks()  # Force the GUI to update

button = ttk.Button(root, text="Select File", command=select_file)
button.pack()

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack()

# Create an Edit button
def edit_selected():
    # Get the selected item
    selected_item = table.selection()

    # Check if there is a selected item
    if selected_item:
        # Get the current values of the item
        values = table.item(selected_item, 'values')

        # Ask the user for the new text
        new_text = tk.simpledialog.askstring("Edit Text", "Enter new text:")

        # Check if the user entered some text
        if new_text is not None:
            # Update the text of the item
            table.item(selected_item, values=(values[0], new_text, values[2]))
    else:
        tk.messagebox.showerror("Error", "No row selected")

edit_button = ttk.Button(button_frame, text="Edit Row", command=edit_selected)
edit_button.pack(side=tk.LEFT)

# Create a Delete button
def delete_selected():
    # Get the selected item
    selected_item = table.selection()
    
    # Check if there is a selected item
    if selected_item:
        # Delete the selected item
        table.delete(selected_item)

        # Loop through the remaining items and reset the indices
        for i, item in enumerate(table.get_children(), start=1):
            # Get the current values of the item
            values = table.item(item, 'values')
            
            # Update the index of the item
            table.item(item, values=(i, values[1], values[2]))
    else:
        tk.messagebox.showerror("Error", "No row selected")

delete_button = ttk.Button(button_frame, text="Delete Row", command=delete_selected)
delete_button.pack(side=tk.LEFT)

# Create an Export button
def export_table():
    # Get all items in the table
    items = table.get_children()

     # Check if the table is empty
    if not items:
        tk.messagebox.showerror("Error", "The table is empty")
        return

    # Initialize a list to hold the data
    data = []

    # Loop through the items and add their values to the data list
    for item in items:
        values = table.item(item, 'values')
        data.append({
            'index': values[0],
            'text': values[1],
            'sentiment': values[2]
        })

    # Ask the user for a file name to save the data
    file_name = filedialog.asksaveasfilename(defaultextension=".json")

    # Save the data to a JSON file
    with open(file_name, 'w') as file:
        json.dump(data, file)

export_button = ttk.Button(button_frame, text="Export Table", command=export_table)
export_button.pack(side=tk.LEFT)

# Create a Clear Table button
def clear_table():
    # Ask for confirmation
    confirm = tk.messagebox.askyesno("Clear Table", "Are you sure you want to clear the table?")
    
    # Check if the user confirmed
    if confirm:
        # Get all items in the table
        items = table.get_children()

        # Delete all items in the table
        for item in items:
            table.delete(item)

clear_button = ttk.Button(button_frame, text="Clear Table", command=clear_table)
clear_button.pack(side=tk.RIGHT)  


# Create a frame for the table and scrollbar
table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Create a Treeview for the table
table = ttk.Treeview(table_frame)
table["columns"] = ("Index", "Text", "Sentiment")
table.column("#0", width=0, stretch=tk.NO)  # Hide the first column
table.column("Index", anchor=tk.W, width=40,stretch=tk.NO)
table.column("Text", anchor=tk.W,minwidth=35,stretch=tk.YES)
table.column("Sentiment", anchor=tk.W,minwidth=75, width=75,stretch=tk.NO)

table.heading("Index", text="Index", anchor=tk.W)
table.heading("Text", text="Text", anchor=tk.W)
table.heading("Sentiment", text="Sentiment", anchor=tk.W)

# Create a Scrollbar for the table
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the table to use the scrollbar
table.configure(yscrollcommand=scrollbar.set)

table.pack(fill=tk.BOTH, expand=True)  # Stretch the table

# Run the application
#root.mainloop()
