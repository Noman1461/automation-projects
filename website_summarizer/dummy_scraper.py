import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.dawn.com/news/1894667/pakistan-uae-sign-5-five-accords-of-cooperation-on-abu-dhabi-crown-princes-first-official-visit'

try:
    response = requests.get(url)
    response.raise_for_status() #raise error for bad responces
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')

    if paragraphs:
        text = " ".join([p.text for p in paragraphs])
    else:
        print("No Paragraphs Found!")
        exit()

    print(text[:500])
except requests.exceptions.RequestException as e:
    print(f"Request Errors: {e}")
except AttributeError as e:
    print(f"Parsing Errors: {e}")
except Exception as e:
    print(f"An error occured:{e}")


#Preprocessing the Text
def remove_text(text):
# Step 1: Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
# Step 2: Replace multiple whitespaces (including tabs and newlines) with a single space
    text = re.sub(r"\s+", " ", text)
# Step 3: Strip leading and trailing spaces
    text = text.strip()
    return text

cleaned_text = remove_text(text)

print(cleaned_text)