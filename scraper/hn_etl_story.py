#!/usr/bin/env python

from __future__ import unicode_literals
from hackernews import HackerNews

import os
import json
from collections import deque

BUCKET_NAME = os.getenv('BUCKET_NAME', 'article-cache')

class Story():
    def in_aws(self):
        return __name__ != '__main__'

    def __init__(self, story_id):
        self.hn = HackerNews()
        self.id = story_id
        if self.in_aws():
            import boto3
            self.s3 = boto3.resource('s3')

    def run(self):
        print('running...')
        obj = self.get_obj_if_exists()
        if obj == None:
            print(f"unable to access aws obj: {self.id}")
            return False

        data = self.fetch_data()
        jsonified_data = json.dumps(data, separators=[',',':'])
        self.save_data(jsonified_data, obj)
        print('done')

        return True

    def get_obj_if_exists(self):
        if not self.in_aws():
            print ('not running s3 stuff, not in aws')
            return None

        from botocore.exceptions import ClientError

        obj = self.s3.Object(BUCKET_NAME, f"hackernews/article-{self.id}.json")
        try:
            obj.load()
        except ClientError:
            return obj
        except:
            return None

        return obj

    def fetch_data(self):
        if not self.in_aws():
            print('skipping fetching data, not in aws')
            return {'story':None, 'comments': None}

        story = self.hn.get_item(self.id)
        kids = []
        queue = deque([story.kids])
        while len(queue) > 0:
            batch = queue.popleft()
            if batch == None:
                break

            result = self.hn.get_items_by_ids(batch)
            kids += result
            [queue.append(x.kids) for x in result if x.kids != None]

        return {'story':story.raw, 'comments':list(map(lambda x: x.raw, kids))}

    def save_data(self, data, obj):
        if not self.in_aws():
            with open(f"article-{self.id}.json") as f:
                f.writelines(data)
        else:
            from io import StringIO
            handle = StringIO(data)
            done = obj.put(Body=handle.read())
            #print(f"done ({done}): {self.id}")
            if not done:
                # TODO send error message to cloudwatch
                pass

def handler(event, context):
    story_id = int(event['Records'][0]['body'])
    story_obj = Story(story_id)
    story_obj.run()


if __name__ == '__main__':
    handler({
      "Records": [
        {
          "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
          "receiptHandle": "MessageReceiptHandle",
          "body": "18762860",
          "attributes": {
            "ApproximateReceiveCount": "1",
            "SentTimestamp": "1523232000000",
            "SenderId": "123456789012",
            "ApproximateFirstReceiveTimestamp": "1523232000001"
          },
          "messageAttributes": {},
          "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
          "eventSource": "aws:sqs",
          "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
          "awsRegion": "us-west-2"
        }
      ]
    }, None)


