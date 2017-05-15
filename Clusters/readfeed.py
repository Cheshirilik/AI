import feedparser
import re
from bs4 import BeautifulSoup

# выделяем слова из html
def get_words(html):
    # txt = re.compile(r'<[^>]+>').sub('', html)                  # причесываем html
    #txt = re.sub(r'<[^>]+>', '', html)  # причесываем html

    #words = re.compile(r"[^A-Z^a-z]+").split(txt)               # выделяем слова

    #soup = BeautifulSoup(html)
    #words = ''.join(soup.findAll(text=True))
    words = BeautifulSoup(html).text

    return [word.lower() for word in words if word != '']       # возвращаем в нижнем регистре


# получаем таблицу слов
def get_words_count(url):
    feed = feedparser.parse(url)
    table = {}

    for i in feed.entries:
        if "summary" in i:
            summary = i
        else:
            summary = i.description

        print("i['title'] = ", i['title'])
        print("i['link'] = ", i['link'])
        print("i['description'] = ", i['description'])
        # words = get_words(i.title + ' ' + summary)
        words = get_words(i.title) + get_words(summary)
        for word in words:
            table.setdefault(word, 0)
            table[word] += 1

    return feed.feed.title, table


# MAIN


feedparser._HTMLSanitizer.acceptable_elements.update(['iframe'])

apcount = {}
wordcounts = {}
strings = [s for s in open("feedlist.txt", 'r')]
for i in strings:
    title, wc = get_words_count(i)
    wordcounts[title] = wc

    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

wordlist = []
for w, bc in apcount.times():
    frac = float(bc)/len(strings)
    if 0.1 < frac < 0.5:
        wordlist.append(w)


out = open("blogdata1.txt", "w")
out.write("Blog")
for word in wordlist:
    out.write("\t%s" % word)

out.write("\n")

for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write("\t%d" % wc[word])
        else:
            out.write("\t0")
        out.write("\n")





















