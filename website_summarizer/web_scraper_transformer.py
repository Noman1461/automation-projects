import requests
from bs4 import BeautifulSoup
import re

# URL of the article
url = 'Enter the URL of the article here'

# Fetch and parse the website content
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')

    if paragraphs:
        text = " ".join([p.text for p in paragraphs])
    else:
        print("No Paragraphs Found!")
        exit()

    print(text[:500])  # Print first 500 characters for debugging
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# Preprocessing the Text
def clean_text(text):
    # Step 1: Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # Step 2: Replace multiple whitespaces (including tabs and newlines) with a single space
    text = re.sub(r"\s+", " ", text)
    # Step 3: Strip leading and trailing spaces
    text = text.strip()
    return text

cleaned_text = clean_text(text)

if len(cleaned_text) > 500:
    cleaned_text = cleaned_text[:500]  # Trim to first 500 characters

# Hugging Face Inference API for summarization
def summarize_text_with_huggingface(text, max_length=100):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": 50,
            "do_sample":False #ensure that the output is deterministics
        },
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error for bad responses
        summary = response.json()[0]["summary_text"]
        return summary
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None

# Print the summary
summary = summarize_text_with_huggingface(cleaned_text, max_length=100)
if summary:
    print(f"Summary:\n{summary}")
else:
    print("Failed to generate summary.")