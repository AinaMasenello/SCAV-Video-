import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def cut_video(input_file, output_file, start_time=14, duration=9):
    # Cut video using ffmpeg
    subprocess.run([
        'ffmpeg',
        '-ss', str(start_time),  # Start time
        '-i', input_file,  # Input file
        '-t', str(duration),  # Duration to cut
        '-c', 'copy',
        output_file  # Output file
    ])

def extract_macroblocks_motion_vectors(input_file, output_file):
    # Extract macroblocks and motion vectors using ffmpeg
    subprocess.run([
        'ffmpeg',
        '-hide_banner',
        '-flags2', '+export_mvs',
        '-i', input_file,
        '-vf', 'codecview=mv=pf+bf+bb',
        '-an',
        output_file
    ])

def generate_video_with_histogram(input_file, output_file):
    # Generate a video with YUV histogram using FFmpeg
    subprocess.run([
        'ffmpeg',
        '-hide_banner',
        '-i', input_file,
        '-vf', 'split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay',
        output_file
    ])

def select_file():
    return filedialog.askopenfilename()

def perform_cut():
    input_file = select_file()
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".mp4")
        if output_file:
            cut_video(input_file, output_file)
            reset_selections()

def perform_extract_macroblocks():
    input_file = select_file()
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".mp4")
        if output_file:
            extract_macroblocks_motion_vectors(input_file, output_file)
            reset_selections()

def perform_generate_histogram():
    input_file = select_file()
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".mp4")
        if output_file:
            generate_video_with_histogram(input_file, output_file)
            reset_selections()

def reset_selections():
    # Reset file selections
    button_cut.config(state=tk.NORMAL)
    button_extract_macroblocks.config(state=tk.NORMAL)
    button_generate_histogram.config(state=tk.NORMAL)

# GUI setup
root = tk.Tk()
root.title("Video Processing GUI")

# Set the size of the window
root.geometry("400x300")  # Width x Height

background_image = Image.open("background.webp")
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_photo  # Keep a reference to the image

bg_color_label = background_image.getpixel((400, 59))  # Sample color from a specific pixel

# Label for the welcome message
label = tk.Label(root, text="WELCOME!\nChoose any of the following options:", font=("Arial", 20), bg='#%02x%02x%02x' % bg_color_label)
label.pack(pady=20)

# Sample a color from the background image (you might adjust the coordinates to suit)
bg_color = background_image.getpixel((267, 209))  # Sample color from a specific pixel

# Create a frame to hold the buttons and center it in the window
frame = tk.Frame(root, bg='#%02x%02x%02x' % bg_color)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

button_cut = tk.Button(frame, text="Cut Video", command=perform_cut)
button_cut.pack(pady=5)

button_extract_macroblocks = tk.Button(frame, text="Extract Macroblocks and Motion Vectors", command=perform_extract_macroblocks)
button_extract_macroblocks.pack(pady=5)

button_generate_histogram = tk.Button(frame, text="Generate Video with Histogram", command=perform_generate_histogram)
button_generate_histogram.pack(pady=5)

root.mainloop()