import tkinter as tk
from tkinter import scrolledtext
import requests
from PIL import Image, ImageTk, ImageSequence
from io import BytesIO

# Function to fetch a GIF from Giphy API
def fetch_gif(query):
    api_key = 'RRB1f9qpFlH7gyPTHRuLzBmFY0mpZQ58'  
    url = f'https://api.giphy.com/v1/gifs/search?q={query}&api_key={api_key}&limit=1'
    response = requests.get(url)
    data = response.json()
    if data['data']:
        return data['data'][0]['images']['original']['url']
    return None

# Function to handle user input and display GIF
def send_message():
    user_input = entry.get()
    chat_log.insert(tk.END, f"You: {user_input}\n")
    entry.delete(0, tk.END)

    gif_url = fetch_gif(user_input)
    if gif_url:
        chat_log.insert(tk.END, "Bot: \n")
        display_gif(gif_url)
    else:
        chat_log.insert(tk.END, "Bot: Sorry, I couldn't find a GIF for that.\n")

# Function to display GIF in the chat window
def display_gif(gif_url):
    global gif_label, gif_frames, gif_duration, frame_index, update_id

    response = requests.get(gif_url)
    gif_data = response.content
    gif_image = Image.open(BytesIO(gif_data))

    # Create a sequence of frames
    gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]
    gif_duration = gif_image.info.get('duration', 100)  # Default to 100ms if no duration info
    frame_index = 0

    # Create a label to display the GIF if it doesn't exist
    if gif_label is None:
        gif_label = tk.Label(chat_log)
        gif_label.pack()
    
    # If there's an ongoing update, cancel it
    if update_id is not None:
        root.after_cancel(update_id)

    # Start the animation
    update_gif()

def update_gif():
    global frame_index, gif_label, gif_frames, gif_duration, update_id

    frame = gif_frames[frame_index]
    gif_label.config(image=frame)
    gif_label.image = frame
    frame_index = (frame_index + 1) % len(gif_frames)
    update_id = root.after(gif_duration, update_gif)

# Create the main window
root = tk.Tk()
root.title("GIF Chatbot")

# Create a chat log area
chat_log = scrolledtext.ScrolledText(root, width=50, height=20)
chat_log.pack(padx=10, pady=10)

# Create an entry widget for user input
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

# Initialize the GIF label and frames
gif_label = None
gif_frames = []
gif_duration = 0
frame_index = 0
update_id = None

# Start the Tkinter event loop
root.mainloop()
