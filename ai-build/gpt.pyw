# Imports
from openai import OpenAI
import os
from datetime import datetime
import json
import pyttsx3
import tkinter as tk

# Varbiables
file = open("api_key.txt", "r")
apikey = f"{file.read()}"
file.close()

root = tk.Tk()

# Read-only text display
display = tk.Text(root, height=10, width=50, wrap='word')
display.insert('1.0', "Chatlog:\n\n")  # Initial content
display.config(state='disabled')  # Make it read-only
display.pack(padx=10, pady=10)

# Input field
input_field = tk.Entry(root, width=40)
input_field.bind('<Return>', lambda event: main())
input_field.pack(padx=10, pady=(0, 5))

root.title("ChatGPT in python tkinter")

client = OpenAI(api_key=apikey)

if os.path.exists("./instructions.txt"):
    file = open("instructions.txt", "r")
    instructions = f"{file.read()}"
    file.close()

tts = pyttsx3.init()

# Functions
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def save_chat_history(chat_history):
    with open("chat.json", "w") as f:
        json.dump(chat_history, f, indent=3)

def load_chat_history():
     if os.path.exists("chat.json"):
        with open("chat.json", "r") as f:
            return json.load(f)
     return []

def main():
    chat_history = load_chat_history()
    user_input = input_field.get()

    chat_history.append({"time": f"{datetime.now()}", "role": "you", "content": user_input})
    response = chat_with_gpt(user_input)
    if user_input.strip():  # Avoid blank lines
        display.config(state='normal')  # Temporarily make it editable
        display.insert(tk.END, response + '\n\n')  # Add input to display
        display.config(state='disabled')  # Make it read-only again
        input_field.delete(0, tk.END)  # Clear the input field

    chat_history.append({"time": f"{datetime.now()}", "role": "chatgpt", "content": response})
    save_chat_history(chat_history)
    tts.say(f"{response}")
    tts.runAndWait()

# Submit button
submit_button = tk.Button(root, text="Send", command=main)
submit_button.pack(padx=10, pady=(0, 10))

root.mainloop()

file.close()