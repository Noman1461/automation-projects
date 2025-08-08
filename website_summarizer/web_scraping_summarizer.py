from bs4 import BeautifulSoup
import requests
import argparse
import yaml
import openai
import os
import time

# Check if file exists before opening
file_path = "pass.yml"
if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
else:
    print(f"File {file_path} not found!")
    content = None  # Set content to None if the file is not found

# Proceed only if the content is not empty
if content:
    my_credential = yaml.safe_load(content)
    print("Parsed credentials:", my_credential)
else:
    print("File is empty or could not be read.")
    my_credential = {}  # Set an empty dictionary to avoid errors

# Simulate API key assignment (only if credentials exist)
if 'api' in my_credential:
    api_key = my_credential["api"]
    print("API key set.")
else:
    print("No API key found in the credentials.")

# Mock argparse arguments for testing
parser = argparse.ArgumentParser(description="Website Summarizer")

# Add arguments
parser.add_argument('--web', type=str, help='website link (default : https://github.com/xiaowuc2/ChatGPT-Python-Applications)', default="https://github.com/xiaowuc2/ChatGPT-Python-Applications")
parser.add_argument('limit', type=int, help='summarized text limit (default : 100)', default=100)

# Bypass the command-line arguments
args = parser.parse_args(args=['--web', 'https://www.dawn.com/news/1894667/pakistan-uae-sign-5-five-accords-of-cooperation-on-abu-dhabi-crown-princes-first-official-visit', '150'])

# Print the parsed arguments for testing
print(f"Web: {args.web}")
print(f"Limit: {args.limit}")

responce = requests.get(args.web)

soup = BeautifulSoup(responce.content, 'html.parser')

text = ''

for p in soup.find_all('p'):
    text += p.text

mine = int(len(text)/4.2)

allowed = 16132

h = len(text) - allowed

#if the text is greater thean the allowed limit than we have to trim the text.
ntext = text[:len(text)-h]

client = openai.OpenAI(api_key=api_key)

def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=150,
            temperature=0.5,
        )
        return response["choices"][0]["message"]["content"]
    except openai.RateLimitError:
        print("Rate limit exceeded. Waiting before retrying...")
        #time.sleep(10)  # Wait before retrying
        return summarize_text(text)  # Retry the request
    
# Generate and print the summary
summary = summarize_text(ntext)
print(f"Summary:\n{summary}")
