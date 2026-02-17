# Convert/Combine images and pdfs into a pdf or images

---
<img width="2559" height="1377" alt="image" src="https://github.com/user-attachments/assets/e90680f1-c899-4036-becf-422b163f14df" />

## Description

version 2 of something i made 5 years ago: PDF-and-Image-Converter. No ui back then, entire code in a single file and exe does not work

Now
- Can upload files by selecting in file explorer or drag and drop
- Reorder existing files / pages in pdfs
- Compact files to show grouped pages for easy reordering
- Download pages individually
- Download all as pdf or images
- Image download can toggle download quality
- Disable preview if working with very large file

---

## Not a thing

- No progress bar for download
- No editing of pages

---

## Run

Download and run the exe in executable/dist. Will have certificate warning


---

## Running from source code
Seting up virtual environment
```bash
python -m venv venv

# Install dependencies
pip install -r requirements.txt

# Running the program
python main.py
```

## Creating .exe file

Converting to executable (In the virtual environment)
```bash
pip install PySide6 pyinstaller

# For a single exe (Takes very long to load)
python -m PyInstaller __main__.py --name "Pdf and Image Converter" --onefile --windowed --icon=static/app.ico

# Slightly larger with multiple files/folder but takes a few seconds to load
python -m PyInstaller __main__.py --name "Pdf and Image Converter" --windowed --icon=static/app.ico
```

- Generated folders: dist, build (Contains the .exe file) 
- Generated file: .spec
