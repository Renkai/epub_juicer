import re

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def text_from_item(item):
    soup = BeautifulSoup(item.content, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

        # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def get_epub_words(filename: str):
    book = epub.read_epub(filename)
    items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    all_words = dict()

    for item in items:
        text = text_from_item(item)
        # print(text)
        words_pattern = '[a-z]+'
        words = [x.lower() for x in re.findall(words_pattern, text, flags=re.IGNORECASE) if x[0].islower()]
        # all_words.update(words)
        for word in words:
            all_words[word] = (all_words.get(word) if word in all_words else 0) + 1
    return all_words
