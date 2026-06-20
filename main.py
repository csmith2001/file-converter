from pathlib import Path
from PIL import Image
from tkinter import filedialog
import tkinter as tk, pillow_heif

pillow_heif.register_heif_opener()

root = tk.Tk()
root.withdraw()

img_types = "*.jpg *.jpeg *.png *.heic *.webp"
file_types = [("Image Files:", img_types)]

files = filedialog.askopenfilenames(filetypes=file_types)

suffixes = list({f"*{Path(file).suffix.lower()}" for file in files})

print(suffixes)