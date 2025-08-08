import logging.config
from PyPDF4 import PdfFileMerger
from PyPDF4.utils import PdfReadError
import os
import logging
import time

logging.basicConfig(
    filename='pdf_merger.log',
    level = logging.INFO,
    format= '%(asctime)s - %(levelname)s - %(message)s'
)
total_files = len([file for file in os.listdir() if file.endswith('.pdf') and file != 'Final_pdf.pdf'])
processed_files = 0

#start time
start = time.time()
#create an object of PdfFile
merger = PdfFileMerger()
logging.info("Pdf merging start...")

#step 1: check if the the extrension of file is .pdf add it.
for items in os.listdir(f'C:/Users/Noman/Desktop/Python Projects/10 lines of code'):
    if items.endswith('.pdf') and items != 'Final_pdf.pdf':
        try:
            merger.append(items)
            logging.info(f"File {items} have been merged")
        except PdfReadError:
            logging.info(f'Error: {items} is corrupted and cannot be retreived.')
        except PermissionError:
            logging.info(f"permission NOT available for {items}")
        except Exception as e:
            logging.info(f"Unexpected error occured with {items}:{e}")

        processed_files += 1
        print(f"{processed_files} have been processed out of {total_files}")
merger.write('Final_pdf.pdf')
merger.close()

end = time.time()
time_taken = end - start
logging.info(f'The total time taken merging files is {time_taken}')
logging.info(f"Pdf merging ends...")

#delete all other pdf and only saves 'Final_pdf.pdf'
for items in os.listdir():
    if items != 'Final_pdf.pdf' and items.endswith('.pdf'):
        os.remove(items)


