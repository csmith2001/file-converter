###########################
## IMPORTS ##
###########################

from pathlib import Path
from PIL import Image
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb, pillow_heif

###########################
## GLOBALS ##
###########################

IMG_FORMATS = ["jpg", "jpeg", "png", "heic", "webp", "tiff", "bmp"]
TXT_FORMATS = ["csv", "txt", "md"]
THEMES = ["flatly", "darkly", "cosmo", "solar", "morph", "vapor", "superhero", "cyborg", "journal", "litera", "lumen", "minty", "pulse", "sandstone", "united", "yeti", "simplex", "cerculean"]

###########################
## FUNCTIONS ##
###########################

# function used to restart app
def restart_app(main_frame, file_widgets, files_row, rows, buttons, window):
        new_files = filedialog.askopenfilenames()

        if not new_files:
            return

        # Clear old UI
        for widget in file_widgets:
            widget.destroy()
        file_widgets.clear()
        rows.clear()

        # Clear old buttons
        for b in buttons:
            b.destroy()
        buttons.clear()

        # Rebuild file rows
        for i, file in enumerate(new_files, start=files_row):
            file_path = Path(file)

            label = tb.Label(
                main_frame,
                text=file_path.name
            )
            label.grid(row=i, column=0)

            valid_formats = get_gui_formats(file_path)
            var = tb.StringVar(value=valid_formats[0])

            combo = tb.Combobox(
                main_frame,
                textvariable=var,
                values=valid_formats
            )
            combo.grid(row=i, column=1, padx=10, pady=5)

            file_widgets.extend([label, combo])
            rows.append((file_path, var))

        # Recreate buttons
        buttons_row = files_row + len(rows)

        convert_all = tb.Button(
            main_frame,
            text="Convert All",
            command=lambda: convert_files(window, rows)
        )
        convert_all.grid(row=buttons_row, column=0, padx=10, pady=20)

        restart = tb.Button(
            main_frame,
            text="Choose more files",
            command=lambda: restart_app(main_frame, file_widgets, files_row, rows, buttons, window)
        )
        restart.grid(row=buttons_row, column=1, padx=10, pady=20)

        exit_btn = tb.Button(
            main_frame,
            text="Exit",
            command=window.destroy
        )
        exit_btn.grid(row=buttons_row, column=2, padx=10, pady=20)

        buttons.extend([convert_all, restart, exit_btn])

# function to change theme styles
def change_theme(window, selected_theme, *args):
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
def convert_files(window, rows):
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

def main():
    # HEIC support
    pillow_heif.register_heif_opener()

    # File Types
    img_types = [f"*.{format}" for format in IMG_FORMATS]
    file_types = [("Image Files:", img_types)]

    # Prompt for file selection
    files = filedialog.askopenfilenames(filetypes=file_types)

    if not files:
        return

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
    main_frame = tb.Frame(window,padding=15)
    main_frame.grid(row=title_row,column=0,sticky="nsew")

    # Add labels for window elements
    tb.Label(
        main_frame,
        text=title,
        font=("Segoe UI",20,"bold")
    ).grid(row=title_row,column=0,columnspan=4,pady=(0,15))

    tb.Label(
        main_frame,
        text=r"Select a theme:"
    ).grid(row=title_row,column=5,padx=10,pady=10)

    # GUI button for theme selection
    selected_theme = tb.StringVar(value="darkly")
    selected_theme.trace_add("write",lambda *args: change_theme(window,selected_theme, *args))

    tb.Combobox(
        main_frame,
        textvariable=selected_theme,
        values=THEMES,
        state="readonly",
        width=10
    ).grid(row=title_row,column=6,padx=10,pady=10)

    tb.Separator(
        main_frame,
        orient='horizontal'
    ).grid(row=title_row+2,column=0,columnspan=7,sticky="ew",pady=5)

    tb.Label(
        main_frame,
        text="File"
    ).grid(row=headers_row,column=0,padx=10,pady=10)

    tb.Label(
        main_frame,
        text="Convert to"
    ).grid(row=headers_row,column=1,padx=10,pady=10)

    # Create rows
    rows = []
    file_widgets = []
    buttons = []

    for i, file in enumerate(files,start=files_row):
        file_path = Path(file)

        label = tb.Label(main_frame,text=file_path.name)
        label.grid(row=i,column=0)

        valid_formats = get_gui_formats(file_path)
        gui_format = tb.StringVar(value=valid_formats[0] if valid_formats else "")

        combo = tb.Combobox(
            main_frame,
            textvariable=gui_format,
            values=valid_formats,
            state="readonly",
            width=10
        )
        combo.grid(row=i,column=1,padx=10,pady=5)

        rows.append((file_path, gui_format))
        file_widgets.extend([label, combo])
    
    buttons_row = files_row + len(rows)

    convert_btn = tb.Button(
        main_frame,
        text="Convert All",
        command=lambda: convert_files(window, rows)
    )
    convert_btn.grid(row=buttons_row, column=0, padx=10, pady=20)

    restart_btn = tb.Button(
        main_frame,
        text="Choose more files",
        command=lambda: restart_app(main_frame, file_widgets, files_row, rows, buttons, window)
    )
    restart_btn.grid(row=buttons_row, column=1, padx=10, pady=20)

    exit_btn = tb.Button(
        main_frame,
        text="Exit",
        command=window.destroy
    )
    exit_btn.grid(row=buttons_row, column=2, padx=10, pady=20)

    buttons.extend([convert_btn, restart_btn, exit_btn])

    window.mainloop()

if __name__ == "__main__":
    main()

###########################
## NOTES ##
###########################
"""
1. TODO 6/20/26 - Work on other file formats
2. TODO 6/20/26 - Work on adding more complex support to images. I.e. support for animated file types
"""