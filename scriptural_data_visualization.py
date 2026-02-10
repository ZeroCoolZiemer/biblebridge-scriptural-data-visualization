import os
import requests
import re
from collections import Counter
import matplotlib.pyplot as plt

API_BASE = "https://holybible.dev/api"
API_KEY = os.getenv("BIBLEBRIDGE_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing BIBLEBRIDGE_API_KEY. Set it as an environment variable.")

BOOK_ID = 20
CHAPTERS = 31
VERSION = "KJV"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

STOPWORDS = {
    "the", "and", "of", "to", "in", "is", "that", "for", "with", "as",
    "on", "be", "are", "by", "this", "which", "or", "it", "from",
    "at", "there", "when", "but", "not",
    "a", "an", "i", "my", "me", "mine",
    "him", "his", "her", "hers", "they", "them", "their",
    "he", "she", "we", "us", "our",
    "ye", "thou", "thee", "thy", "thine",
    "hath", "had", "have", "having",
    "shall", "will", "may", "might",
    "unto", "thereof", "wherefore",
    "all", "own", "so", "than", "son", "s"
}

def normalize(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return [w for w in words if w not in STOPWORDS]

word_counts = Counter()

for chapter in range(1, CHAPTERS + 1):
    print(f"Fetching Proverbs {chapter}/{CHAPTERS}")

    response = requests.get(
        API_BASE,
        headers=HEADERS,
        params={
            "bookID": BOOK_ID,
            "chapter": chapter,
            "version": VERSION
        },
        timeout=5
    )

    response.raise_for_status()
    payload = response.json()

    for verse in payload["data"]:
        word_counts.update(normalize(verse["text"]))

words, counts = zip(*word_counts.most_common(10))

plt.bar(words, counts)
plt.title("Top 10 Key Themes in Proverbs (KJV)")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
