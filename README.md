# PDF to Markdown Batch Converter

A simple and efficient batch conversion tool that converts PDF files to Markdown format while extracting embedded images. Particularly suitable for importing large volumes of PDF documents into Markdown note-taking software like Obsidian.

## Features

- 📄 **Batch Conversion**: Process multiple PDF files at once
- 🖼️ **Image Extraction**: Automatically extract and save all images from PDFs
- 📝 **Obsidian Optimized**: Uses Obsidian image link format with perfect support for Chinese filenames
- 🚀 **High Performance**: Fast conversion based on PyMuPDF
- 📊 **Progress Display**: Real-time conversion progress indicator
- 🔧 **Flexible Configuration**: Supports command-line arguments and configuration files

## Installation

### Requirements

- Python 3.7+

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pymupdf pillow
```

## Usage

### Method 1: Command-Line Arguments

```bash
python pdf_to_markdown.py -i "PDF_folder_path" -o "output_folder_path"
```

Example:

```bash
python pdf_to_markdown.py -i "C:/Documents/PDFs" -o "C:/Documents/Markdown"
```

### Method 2: Modify Default Paths in Script

Open `pdf_to_markdown.py` and modify the following two lines in the `main()` function:

```python
pdf_directory = r"your_PDF_folder_path"
output_directory = r"your_output_folder_path"
```

Then run directly:

```bash
python pdf_to_markdown.py
```

## Output Structure

```
output_directory/
├── file1.md
├── file2.md
├── ...
└── images/
    ├── file1_page1_img1.png
    ├── file1_page2_img1.jpeg
    └── ...
```

## Example

Before conversion:
```
input_folder/
├── report1.pdf
├── report2.pdf
└── report3.pdf
```

Run conversion:
```bash
python pdf_to_markdown.py -i "input_folder" -o "output_folder"
```

After conversion:
```
output_folder/
├── report1.md
├── report2.md
├── report3.md
└── images/
    ├── report1_page1_img1.png
    ├── report2_page1_img1.jpeg
    └── ...
```

## Configuration Options

### Image Link Format

Default uses Obsidian format: `![[images/image_name.png]]`

If you need to use standard Markdown format, modify the image reference section in the code:

```python
# Obsidian format (default)
markdown_content.append(f"![[images/{image_filename}]]\n\n")

# Standard Markdown format
markdown_content.append(f"![Image](images/{image_filename})\n\n")
```

### Add Page Number Markers

If you need to preserve page number information in Markdown, uncomment the relevant section in the code:

```python
# In the convert_pdf_to_markdown method
if total_pages > 1:
    markdown_content.append(f"## Page {page_num + 1}\n\n")
```

## Technical Details

- **PDF Processing**: PyMuPDF (fitz)
- **Image Processing**: Pillow
- **Supported Formats**:
  - Input: PDF
  - Output: Markdown (.md)
  - Images: PNG, JPEG, and other formats supported by PyMuPDF

## FAQ

### Q: Images not displaying in Obsidian?

A: Make sure you're using Obsidian's wiki-style link format `![[images/image_name]]`, not standard Markdown format. This tool uses Obsidian format by default.

### Q: Garbled Chinese filenames?

A: This tool automatically handles Chinese filenames using UTF-8 encoding. If you encounter issues, please check your system encoding settings.

### Q: Slow conversion speed?

A: PyMuPDF is one of the fastest PDF processing libraries available. Large files or PDFs with many images will take some time to process. You can monitor the real-time progress display.

### Q: Some PDFs fail to convert?

A: The PDF file may be corrupted or encrypted. Check the error message and ensure the PDF file can be opened normally.

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License

## Acknowledgments

- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - Powerful PDF processing library
- [Pillow](https://github.com/python-pillow/Pillow) - Python imaging library

---

If this tool helps you, please give it a Star ⭐️
