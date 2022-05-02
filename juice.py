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


def get_formations():
    f = open("reversed-deformations.txt", "r")
    _origins = set()
    _formation_map = dict()
    _dict_words = set()
    for line in f.readlines():
        arr = line.split(" ")
        if len(arr) == 2:
            (formation, _origin) = arr
            _origins.add(_origin)
            _formation_map[formation] = _origin
            _dict_words.add(formation)
            _dict_words.add(_origin)

    return _origins, _formation_map, _dict_words


if __name__ == '__main__':
    filename = sys.argv[1]
    book = epub.read_epub(filename)
    items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    # example_item = next(items)
    # text = text_from_item(example_item)
    # print(text)
    all_words = set()
    _, formation_map, dict_words = get_formations()
    print("len ", len(formation_map), len(dict_words))
    print("contains", 'standoffs' in dict_words)
    # sys.exit(0)

    for item in items:
        text = text_from_item(item)
        # print(text)
        words_pattern = '[a-z]+'
        words = set([x.lower() for x in re.findall(words_pattern, text, flags=re.IGNORECASE) if x[0].islower()])
        all_words.update(words)

    freqMax = 3.5
    freqMin = 1
    not_in_dict = set()
    origins = set()
    formations = set()

    for word in all_words:
        if word not in dict_words:
            print(word, " not in dict")
            not_in_dict.add(word)
        else:
            if word in formation_map.keys():
                print("word ", word, " in keys")
                origin = formation_map[word]
                freq = zipf_frequency(origin, 'en')
                if freqMax > freq > freqMin:
                    origins.add(origin)
            else:
                print("else ", word)
                freq = zipf_frequency(word, 'en')
                if freqMax > freq > freqMin:
                    formations.add(word)

    print("not in dict size:", len(not_in_dict))
    with open('not_in_dict.txt', 'w') as not_in_dict_file:
        not_in_dict_file.writelines(sorted(not_in_dict))

    print("origins size:", len(origins))
    with open('origins.txt', 'w') as origins_file:
        origins_file.writelines(sorted(origins))

    print("formations size:", len(formations))
    with open('formations.txt', 'w') as formations_file:
        formations_file.writelines(sorted(formations))
