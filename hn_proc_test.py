# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import unicode_literals

from bs4 import BeautifulSoup

from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import os
import json
import pdb

class Story():
    def __init__(self, story_id):
        self.id = story_id

    def load(self):
        with open(f"./data/hackernews/article-{self.id}.json") as f:
            self.data = json.loads(f.read())
        return self.data

    def comments(self):
        return self.data['comments']

    def story(self):
        return self.data['story']

class HNDataObj():
    def __init__(self, obj):
        self.unhandled_tags = [None]
        self.handled_tags = ['p', 'span']

        self.obj = obj
        self.data = json.loads(self.obj)
        self.id = int(self.data['id'])
        self.text = self.data['text']

        self.parsed = BeautifulSoup(self.text, 'html.parser')
        self.parsed_text = self.parsed.text

    def __str__(self):
        json.dumps(self.data)

    def load(self):
        #pdb.set_trace()
        self.sentences = self.reduceBody(self.parsed.descendants)
        return self.sentences

    # running currently with an importance of preserving order of sents
    def reduceBody(self, data, body=[]):
        for node in data:
            if node.name == None and node.parent.name != 'a':
                body.append(node)

            elif node.name == 'a':
                body.append((node.attrs['href'], node.text))

            # elif node.name not in self.handled_tags and node.name not in self.unhandled_tags:
            #     print(f"Unhandled tag found: {node.name}")
            #     self.unhandled_tags.append(node.name)

        return body

    def runSentiment(self):
        #tokens_raw = [sent_tokenize(sent) for sent in self.text]
        tokens = [word_tokenize(str(sent)) for sent in self.sentences]
        stop_words = stopwords.words('english')

        import string
        table = str.maketrans('','',string.punctuation)
        stripped = [w.translate(table).lower() for sent in tokens for w in sent if w.isalpha()]

        from nltk.stem.porter import PorterStemmer
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in stripped]


        pdb.set_trace()


class Comment():
    def __init__(self, obj):
        self.obj = obj

    def load(self):
        self.data = json.loads(self.obj)
        self.id = int(data['id'])
        self.text = data['text']
        self.parsed = BeautifulSoup(self.text, 'html.parser')
        self.parsed_text = self.parsed.text
        self.links = self.parsed.find_all('a')

    def run(self):
        return True


def handler(event, context):
    pass

if __name__ == '__main__':
    # s = Story('18742855').load()
    # ret = s['comments'][0]
    # ret = HNDataObj(ret)
    # ret.load()
    pass

    #comments = list(map(lambda x: json.loads(x), ret['comments']))
    #downcoded = [(c['id'], BeautifulSoup(c['text'], features="html5lib").text) for c in comments]



