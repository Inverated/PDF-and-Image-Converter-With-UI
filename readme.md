# Convert/Combine images and pdfs into a pdf or images

---

## Description

version 2 of something i made 5 years ago: PDF-and-Image-Converter. No ui, entire code in a single file and exe does not work

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

## Installation

```bash
# Set up virtual environment
python -m venv venv

# Install dependencies
pip install -r requirements.txt

# Running the program
python main.py

# Convert to executable
pyinstaller main.py --name "Pdf and Image Converter" --onefile --windowed --icon=static/app.ico
Generated folders: dist, build
Generated file: .spec
