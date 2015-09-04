import os

from boto.s3.connection import S3Connection

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


class S3Client(object):

    _cls_cache = {}

    @classmethod
    def _get_bucket(cls, amazon_bucket_name):
        try:
            return cls._cls_cache[amazon_bucket_name]
        except KeyError:
            connection = S3Connection(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY)
            cls._cls_cache[amazon_bucket_name] = connection.lookup(amazon_bucket_name)
            return cls._cls_cache[amazon_bucket_name]
