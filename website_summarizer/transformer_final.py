import requests
from bs4 import BeautifulSoup
import re
import textwrap

# URL of the article
url = 'https://www.dawn.com/news/1894667/pakistan-uae-sign-5-five-accords-of-cooperation-on-abu-dhabi-crown-princes-first-official-visit'

# Fetch and parse the website content
try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')

    if paragraphs:
        text = " ".join([p.text for p in paragraphs])
    else:
        print("No Paragraphs Found!")
        exit()

    print("Article Fetched Successfully.")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
    exit()

# Preprocessing the Text
def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

cleaned_text = clean_text(text)

# Hugging Face Inference API for summarization
def summarize_text_with_huggingface(text, max_length=150):
    API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"  # Faster Model
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": 50,
            "do_sample": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["summary_text"]
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None

# **Step 1: Split Article into Chunks of ~500 words**
chunk_size = 1000  # Each chunk should be around 1000 characters
chunks = textwrap.wrap(cleaned_text, chunk_size)

# **Step 2: Summarize Each Chunk Separately**
summaries = []
for chunk in chunks:
    summary = summarize_text_with_huggingface(chunk, max_length=150)
    if summary:
        summaries.append(summary)

# **Step 3: Summarize All Summaries into a Final Summary**
final_summary = " ".join(summaries)
if len(final_summary) > 1000:  # If still too long, summarize the summary
    final_summary = summarize_text_with_huggingface(final_summary, max_length=200)

# Print the final summary
print("\nFinal Summary:")
print(final_summary)
