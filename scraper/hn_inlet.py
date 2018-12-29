#!/usr/bin/env python

from __future__ import unicode_literals

import os
import json
from random import randint

import aiohttp
import asyncio


QUEUE_NAME = os.getenv('QUEUE_NAME', 'scraper-hn-story-queue')
QUEUE_URL = os.getenv('QUEUE_URL', 'https://sqs.us-west-2.amazonaws.com/547755016564/scraper-hn-story-queue')
STORIES_URL = os.getenv('STORIES_URL', 'https://hacker-news.firebaseio.com/v0/topstories.json')

class Queue():
    def in_aws(self):
        return __name__ != '__main__'

    def __init__(self):
        if self.in_aws():
            import boto3
            self.sqs_client = boto3.client('sqs')
            self.enqueue = self.sqs_enqueue
        else:
            self.enqueue = self.test_enqueue

    def sqs_enqueue(self, s_id):
        print('sqs enqueued id', s_id)
        self.sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=str(s_id),
            DelaySeconds=randint(0,3)
        )

    def test_enqueue(self, s_id):
        print('enqueued id', s_id)
        sc_st = __import__('scraper-hn-story-etl')
        sc_st.handler({'story_id': s_id}, None)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        queue = Queue()
        story_ids = await fetch(session, STORIES_URL)
        if story_ids:
            story_ids = json.loads(story_ids)
            results = [queue.enqueue(s_id) for s_id in story_ids]
        else:
            print('failed to enqueue story ids', story_ids)


# script logical flow: (cronned)
# - get rss feed list
# - for each item in the feed
#   - get some normalized hash of an item (url w/o params, etc)
#   - if the hash of that item exists in s3,
#       - scan and update comments, unless the publish date is > 3 days
#   - else download item, and comments
# -

def handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == '__main__':
    handler(None, None)
