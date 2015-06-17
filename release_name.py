# encoding=utf-8
import json
import httplib
import sys
import time


url = u'/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=10&format=json'
host = u'fr.wikipedia.org'


def parse_random_list(conn, host, url, word):
    conn.request('GET', url, headers={'User-Agent': u'Random Word Correlation Release Namer 0.1'})
    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)
    for page in data['query']['random']:
        test_word = page['title'].lower()
        if test_word.startswith(word[0].lower()):
            return page['title']
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print u"Usage: release_name.py <word>"
        sys.exit()
    word = sys.argv[1]
    conn = httplib.HTTPSConnection(host)
    c = 0
    while True:
        c += 1
        print "Try {}".format(c)
        page = parse_random_list(conn, host, url, word)
        if page:
            print u"Found page: {}".format(page)
            print u"Possible release names:"
            print u"\t- {}-{}".format(page.split()[0].lower(), word.lower())
            print u"\t- {}-{}".format(word.lower(), page.split()[0].lower())
            break

        # We don't want to spam wikipedia too much
        if c % 10 == 0:
            time.sleep(10)
        else:
            time.sleep(2)
