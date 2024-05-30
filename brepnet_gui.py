import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import os
import subprocess

# Function to process and visualize the input STEP file
def process_step_file(filepath):
    # Placeholder commands - Replace with actual BRepNet commands
    dataset_dir = os.path.dirname(filepath)
    step_file = os.path.basename(filepath)
    
    # Preprocess the file
    subprocess.run(['python', '-m', 'pipeline.quickstart', '--dataset_dir', dataset_dir, '--num_workers', '5'])

    # Run the evaluation
    latest_checkpoint = 'logs/latest_model/checkpoints/epoch=x-step=x.ckpt'  # Update with the correct path
    subprocess.run(['python', '-m', 'eval.test', '--dataset_file', f'{dataset_dir}/processed/dataset.json',
                    '--dataset_dir', f'{dataset_dir}/processed/', '--model', latest_checkpoint])

    # Update image placeholder with results
    update_image(f'{dataset_dir}/processed/results/segmentation_output.png')  # Update with the actual output image path

# Function to load the file
def load_file():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select STEP file",
                                          filetypes=(("STEP files", "*.step *.stp"), ("all files", "*.*")))
    if filepath:
        process_step_file(filepath)

# Function to update image in the GUI
def update_image(image_path):
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

# Setting up the GUI
root = tk.Tk()
root.title("BRepNet GUI")
canvas = tk.Canvas(root, height=600, width=600, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

open_file = tk.Button(root, text="Open STEP File", padx=10, pady=5, fg="white", bg="#263D42", command=load_file)
open_file.pack()

# Placeholder for output image
placeholder_img = Image.open("assets/placeholder.png")
placeholder_img = placeholder_img.resize((250, 250), Image.ANTIALIAS)
placeholder_img = ImageTk.PhotoImage(placeholder_img)

panel = tk.Label(frame, image=placeholder_img)
panel.pack(padx=10, pady=10)

root.mainloop()
