# PDF Merger

A Python script to merge multiple PDF files into a single PDF. This project is designed to handle large numbers of PDFs, log the process, and gracefully handle errors such as corrupted files or permission issues.

---

## Features
- **Merge PDFs**: Combines all PDF files in a specified directory into a single PDF.
- **Error Handling**: Handles corrupted PDFs and permission errors gracefully.
- **Logging**: Logs the merging process, errors, and time taken to complete the task.
- **Progress Indicator**: Displays the number of files processed in real-time.
- **Cleanup**: Deletes all original PDFs after merging, leaving only the final merged PDF.

---

## Requirements
- Python 3.x
- PyPDF4 (`pip install PyPDF4`)

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Noman1461/qxresearch.git