###########################
## IMPORTS ##
###########################

from pathlib import Path
from PIL import Image
from tkinter import ttk, filedialog
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb, pillow_heif

###########################
## GLOBALS ##
###########################

IMG_FORMATS = ["jpg", "jpeg", "png", "heic", "webp", "tiff", "bmp"]
TXT_FORMATS = ["csv", "txt", "md"]
THEMES = ["flatly", "darkly"]

###########################
## FUNCTIONS ##
###########################

# function to change theme styles
def change_theme(*args):
    window.style.theme_use(selected_theme.get())

# function to get file formats
def get_gui_formats(file_path: Path) -> list[str]:
    extension = file_path.suffix.lower().replace(".","")

    if extension in IMG_FORMATS:
        return list(IMG_FORMATS)
    return []

# function to image file types
def convert_img(file_path: Path, target_format: str) -> None:
    img = Image.open(file_path)

    # JPGs / JPEGs cannot decipher empty backgrounds (alpha channel), so we must convert RGBA to RGB
    if target_format in ["jpg", "jpeg"]:
        img = img.convert("RGB")

    # Convert file extension and save to path
    out_path = file_path.with_stem(file_path.stem + "_Converted").with_suffix(f".{target_format}")
    img.save(out_path)

# function to convert files
def convert_files():
    # Iterate through selected files assigning source/target formats for images
    for file_path, file_format in rows:
        target_format = file_format.get().lower()
        source_format = file_path.suffix.lower().replace(".", "")

        try:
            if file_path.suffix.lower() == f".{target_format}":
                continue

            if not target_format:
                continue

            if source_format not in IMG_FORMATS or target_format not in IMG_FORMATS:
                raise ValueError(f"File Type not supported: {source_format}")
            
            convert_img(file_path, target_format)     

        except Exception as e:
            Messagebox.show_error(f"Something went wrong: {e}", parent=window)

###########################
## MAIN PROGRAM ##
###########################

# HEIC support
pillow_heif.register_heif_opener()

# File Types
img_types = [f"*.{format}" for format in IMG_FORMATS]
file_types = [("Image Files:", img_types)]

# Prompt for file selection
files = filedialog.askopenfilenames(filetypes=file_types)

# Convert selected file suffixes set to list
suffixes = list({f"*{Path(file).suffix.lower()}" for file in files})

# Window constants
title = "Really Cool File Converter"
title_row = 0
headers_row = title_row + 3
files_row = headers_row + 2

# Initialize window and set default theme/title
window = tb.Window(themename="darkly")
window.title(title)

# Bring window to front focus
window.lift()
window.focus_force()

# Update after all widgets are created
window.update_idletasks()

# Get required size based on widgets
width = max(window.winfo_reqwidth(), 900)
height = max(window.winfo_reqheight(), 600)

# Set minimum window size
window.minsize(width, height)

# Center the window
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)

window.geometry(f"{width}x{height}+{x}+{y}")

# Create main frame for window
main_frame = ttk.Frame(window, padding=15)
main_frame.grid(row=title_row, column=0, sticky="nsew")

# Add labels for window elements
ttk.Label(main_frame,text=title,font=("Segoe UI", 20, "bold")).grid(row=title_row, column=0, columnspan=4, pady=(0, 15))
ttk.Label(main_frame, text=r"Select a theme:").grid(row=title_row, column=5, padx=10, pady=10)

# GUI button for theme selection
selected_theme = tb.StringVar(value="darkly")
selected_theme.trace_add("write", change_theme)

ttk.Combobox(main_frame,textvariable=selected_theme,values=THEMES,state="readonly",width=10).grid(row=title_row, column=6, padx=10, pady=10)
ttk.Separator(main_frame,orient='horizontal').grid(row=title_row + 2, column=0, columnspan=2, sticky="ew", pady=5)

ttk.Label(main_frame,text="File").grid(row=headers_row,column=0,padx=10,pady=10)
ttk.Label(main_frame,text="Convert to").grid(row=headers_row,column=1,padx=10,pady=10)

# Create rows
rows = []

for i, file in enumerate(files,start=files_row):
    file_path = Path(file)

    ttk.Label(main_frame,text=file_path.name).grid(row=i,column=0)

    valid_formats = get_gui_formats(file_path)
    gui_format = tb.StringVar(value=valid_formats[0] if valid_formats else "")

    combo = ttk.Combobox(main_frame, textvariable=gui_format, values=valid_formats, state="readonly",width=10)
    combo.grid(row=i,column=1,padx=10,pady=5)

    rows.append((file_path, gui_format))

ttk.Button(main_frame,text="Convert All",command=convert_files).grid(row=files_row + len(files), column=0, columnspan=2, pady=20)

window.mainloop()

###########################
## NOTES ##
###########################
"""
1. TODO 6/20/26 Work on other file formats
2. TODO 6/20/26 Work on adding more complex support to images. I.e. support for animated file types.
"""