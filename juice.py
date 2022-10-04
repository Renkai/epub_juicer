import re
import sys

from wordfreq import zipf_frequency

import get_words
from juice_mdx import etymology


def get_formations():
    f = open("reversed-deformations.txt", "r")
    dict_titles = set()
    with open('dict_titles.txt', 'r') as dict_titles_file:
        for title in dict_titles_file:
            dict_titles.add(title.strip())

    _origins = set()
    _formation_map = dict()
    _dict_words = set()
    for dict_line in f.readlines():
        arr = [x.strip() for x in dict_line.split(" ")]
        if len(arr) == 2:
            if 'secrets' in arr:
                print("in in in !")
                print(arr)
            (formation, _origin) = arr
            _origins.add(_origin)
            _formation_map[formation] = _origin
            _dict_words.add(formation)
            _dict_words.add(_origin)

    return _origins, _formation_map, _dict_words.union(dict_titles)


def find_etymology(word_list):
    def find_ety_for_word(the_word, recursive=2):
        recursive -= 1
        if the_word in etymology:
            e_text = etymology[the_word]
            if 'Old English' in e_text or 'German' in e_text:
                return 'anglo'
            elif 'French' in e_text:
                return 'french'
            elif 'Latin' in e_text:
                return 'latin'
            else:
                if recursive < 0:
                    return 'else'
                else:
                    got = re.search(r'entry://(\w+)', e_text)
                    # got = re.search(r'entry://', e_text)
                    print("got", got)
                    if got:
                        return find_ety_for_word(got.group(1), recursive)
                    else:
                        return 'else'
        else:
            return 'notfound'

    anglo = open('ety_anglo.txt', 'w')
    french = open('ety_french.txt', 'w')
    latin = open('ety_latin.txt', 'w')
    ety_else = open('ety_else.txt', 'w')
    ety_notfound = open('ety_notfound.txt', 'w')
    files = {
        'anglo': anglo,
        'french': french,
        'latin': latin,
        'else': ety_else,
        'notfound': ety_notfound
    }

    for word_for_e in word_list:
        ety = find_ety_for_word(word_for_e)
        # print("ety" + ety)
        files[ety].write(word_for_e + '\n')

    anglo.close()
    french.close()
    latin.close()
    ety_else.close()
    ety_notfound.close()


filename = sys.argv[1]
all_words = get_words.get_words(filename)

_, formation_map, dict_words = get_formations()
print("len ", len(formation_map), len(dict_words))
print("contains", 'secret' in dict_words)

freqMax = 3.5
freqMin = 1
not_in_dict = set()
origins = dict()
formations = dict()

for word in all_words:
    if word not in dict_words:
        # print(word, " not in dict")
        not_in_dict.add(word)
    else:
        if word in formation_map.keys():
            # print("word ", word, " in keys")
            origin = formation_map[word]
            freq = zipf_frequency(origin, 'en')
            if freqMax > freq > freqMin:
                origins[origin] = all_words[word]
        else:
            # print("else ", word)
            freq = zipf_frequency(word, 'en')
            if freqMax > freq > freqMin:
                formations[word] = all_words[word]

print("not in dict size:", len(not_in_dict))
with open('not_in_dict.txt', 'w') as not_in_dict_file:
    for line in sorted(not_in_dict):
        not_in_dict_file.write(line + "\n")

print("origins size:", len(origins))
with open('origins.txt', 'w') as origins_file:
    for line in sorted(origins.keys()):
        origins_file.write(line + "\n")

print("formations size:", len(formations.keys()))
with open('formations.txt', 'w') as formations_file:
    for line in sorted(formations):
        formations_file.write(line + "\n")

from collections import Counter

with open('origins-count.txt', 'w') as origins_file:
    cc = Counter(origins)
    for k, v in cc.most_common():
        origins_file.write(f"{k} {v}" + "\n")

with open('formations-count.txt', 'w') as formations_file:
    cc = Counter(formations)
    for k, v in cc.most_common():
        formations_file.write(f"{k} {v}" + "\n")

find_etymology(list(origins.keys()) + list(formations.keys()))

if __name__ == '__main__':
    pass
