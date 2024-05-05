import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox


class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        # Create a frame to hold the login form
        self.login_frame = tk.Frame(self.master, padx=20, pady=20)
        self.login_frame.pack(expand=True, fill='both')

        # Create the username label and entry
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the password label and entry
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = tk.Entry(self.login_frame, width=30, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create the login and clear buttons
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky='w')
        self.clear_button = tk.Button(self.login_frame, text="Clear", command=self.clear_inputs)
        self.clear_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky='e')

        # Bind the Enter key event to the display_text function
        self.master.bind('<Return>', lambda event: self.login())

    def login(self):
        # Get the username and password from the entry widgets
        username = self.username_entry.get()
        password = self.password_entry.get()

            # Connect to the SQLite database
        conn = sqlite3.connect('_internal/internal/chatrooms.db')
        cursor = conn.cursor()
    
        # Query the members table to find a row with the given username and password
        cursor.execute('''
            SELECT * FROM members
            WHERE userid = ? AND password = ?
        ''', (username, password))
    
        # Fetch one row from the query results
        user = cursor.fetchone() 

        # Close the database connection
        conn.close()

        # Check if a user was found
        if user is not None:
            user_id = user[0]  # Get the user_id from the query result
            chatroom_id = user[4]

            # If login is successful, open the chatroom GUI and destroy the login GUI
            self.master.destroy()
            chatroom_window = tk.Tk()
            ChatroomGUI(chatroom_window, chatroom_id, user_id)
            return user_id  # Return the user_id to the calling function

        else:
            # Show error message for invalid username or password
            messagebox.showerror("Login", "Invalid username or password")
            return None  # Return None to indicate login failure

    def clear_inputs(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


class ChatroomGUI:
    def __init__(self, master, chatroom_id, user_id):
        self.master = master
        self.master.title("Chatroom")

        # Create the main application window
        self.master.geometry('720x540')

        self.master.config(bg="lightgreen")

        # Function to exit the application
        def exit_application():
            expire = messagebox.askyesno("Exit", "Are you sure you want to exit?")
            if expire:
                self.master.quit()

        import datetime

        def store_message(chatroom_id, user_id, message):
            # Get the current date and time
            current_datetime = datetime.datetime.now()
            # Format the date and time as a string
            date_time_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
            # Open the file in append mode
            with open(f"_internal/internal/Chats/chat_messages_{chatroom_id}.txt", 'a') as file:
                # Write the user ID, date and time, and message to the file
                file.write(f"{user_id}, {date_time_str}, {message}\n")
        
        def display_text(user_id):
            existing_text = self.label.cget("text")
            new_text = self.entry.get()
            updated_text = existing_text + "\n" + new_text
            
            # Update the label text
            self.label.config(text=updated_text, justify='right', anchor='se', padx=10, pady=20)
            
            # Clear the entry widget
            self.entry.delete(0, tk.END)
            
            # Call the store_message function to store the message in the file
            store_message(chatroom_id, user_id, new_text)

        def load_chat_history(chatroom_id):
            # Initialize an empty list to store chat messages
            messages = []

            # Try opening the file associated with the chatroom_id
            try:
                with open(f"_internal/internal/Chats/chat_messages_{chatroom_id}.txt", 'r') as file:
                    # Read all lines in the file and add them to the list of messages
                    lines = file.readlines()
                    for line in lines:
                        messages.append("\n")
                        messages.append(line.strip())
                    messages.append("\n__________________Previous Chats__________________\n")
                    
            except FileNotFoundError:
                # If the file does not exist, return an empty list
                pass

            # Join all messages with a newline character and return the result
            return "\n".join(messages)

        # Load chat history for the given chatroom_id
        chat_history = load_chat_history(chatroom_id)
        self.label = tk.Label(self.master, text=chat_history, bg='white', font=("Arial", 10, "bold"), wraplength=350)
        self.label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nsew')
        self.label.config(height=15, width=50, justify='right', anchor='se')

        # Create an Entry widget to accept User Input
        self.entry = tk.Entry(self.master, width=50)
        self.entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='ew', rowspan=2)
        self.entry.focus_set()

        # Bind the Enter key event to the display_text function
        self.master.bind('<Return>', lambda event: display_text(user_id))

        # Create a Button to exit the application
        exit_button = tk.Button(self.master, text="Exit", command=exit_application, activeforeground="green", activebackground="orange", pady=8)
        exit_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Create a Button to clear chat messages
        clear_button = tk.Button(self.master, text="Clear Chat", command= lambda :self.clear_messages(chatroom_id), activeforeground="green", activebackground="orange", pady=8)
        clear_button.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

        # Create a Button to send the message
        send_button = tk.Button(self.master, text="Send", width=20, command=display_text, activeforeground="yellow", activebackground="orange", pady=8)
        send_button.grid(row=1, column=3, padx=10, pady=10, sticky='ew')

        # Configure the grid layout for responsiveness
        self.master.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand and shrink
        self.master.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand and shrink
        self.master.grid_columnconfigure(1, weight=2)  # Allow column 1 to expand more than column 0
        self.master.grid_columnconfigure(2, weight=1)  # Allow column 2 to expand and shrink
        self.master.grid_columnconfigure(3, weight=1)  # Allow column 3 to expand and shrink

    def clear_messages(self, chatroom_id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all messages?")
        if confirm:
            # Clear the chat messages from the label
            self.label.config(text="")
            # Clear the chat messages from the file
            # with open(f"_internal/internal/Chats/chat_messages_{chatroom_id}.txt", 'w') as file:
            #     file.truncate()

# Create the main application window and start the login GUI
root = tk.Tk()
logo = PhotoImage(file="_internal/internal/logo.png")
root.iconphoto(True, logo)
LoginGUI(root)
root.mainloop()
