import re
import sys

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from wordfreq import zipf_frequency


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


if __name__ == '__main__':
    filename = sys.argv[1]
    book = epub.read_epub(filename)
    items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    # example_item = next(items)
    # text = text_from_item(example_item)
    # print(text)
    all_words = set()
    for item in items:
        text = text_from_item(item)
        # print(text)
        words_pattern = '[a-z]+'
        words = set([x.lower() for x in re.findall(words_pattern, text, flags=re.IGNORECASE) if x[0].islower()])
        all_words.update(words)

    for word in all_words:
        freq = zipf_frequency(word, 'en')
        if freq < 2.5:
            # print(word, freq)
            print(word)
