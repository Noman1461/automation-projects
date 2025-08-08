text = "  This is an    example   text.\nIt has    extra spaces.\n\nAnd line breaks!  "

import re

def remove_text(text):
# Step 1: Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

# Step 2: Replace multiple whitespaces (including tabs and newlines) with a single space
    text = re.sub(r"\s+", " ", text)

# Step 3: Strip leading and trailing spaces
    text = text.strip()

    return text


