from pathlib import Path
from PIL import Image
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb, pillow_heif

# function used to resize images
def img_resize(
        img: Image.Image,
        width:int | None = None,
        height:int | None = None,
        keep_aspect: bool = True
        ) -> Image.Image: 
    
    if not width and not height:
            return img
        
    orig_width, orig_height = img.size

    if keep_aspect:
        if width is not None and height is not None:          
            ratio = min(width / orig_width, height / orig_height)
            width = int(orig_width * ratio)
            height = int(orig_height * ratio)
        if width is None and height is not None:
            ratio = height / orig_height
            width = int(orig_width * ratio)
        if height is None and width is not None:
            ratio = width / orig_width
            height = int(orig_height * (width / orig_width))    

    return img.resize((width, height))

file_path = Path("local-test/img_files/png.png")
img = Image.open("local-test/img_files/png.png")

target_format = "tiff"

resized_image = img_resize(img, 200, 600, True)
out_path = file_path.with_stem(file_path.stem + "_Converted").with_suffix(f".{target_format}")

resized_image.save(out_path)