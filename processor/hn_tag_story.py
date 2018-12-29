#!/usr/bin/env python

from __future__ import unicode_literals


# a lambda for handling a AWS Gateway route, which sends some kind of metadata
# from a custom chrome extension, enqueues it, and passes it along to dynamodb.
# the long term goal is to provide a center for me to tag HN posts as I like,
# bookmark them for the future, and be able to sort and search them down to the
# comment level. as well as do some ML for sentiment and predicted like/dislike values

def handler(event, context):
    print("NOT IMPLEMENTED")

if __name__ == "__main__":
    handler(None, None)
