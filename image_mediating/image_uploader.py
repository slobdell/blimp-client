AWS_S3_PARTIAL_URL = "https://%s.s3.amazonaws.com/%s"

from .s3_client import S3Client


class ImageUploader(S3Client):

    def __init__(self, aws_bucket_name):
        self.aws_bucket_name = aws_bucket_name

    def _full_path(self, key):
        return AWS_S3_PARTIAL_URL % (self.aws_bucket_name, key.name)

    def upload(self, output_path, raw_image_data):
        bucket = self._get_bucket(self.aws_bucket_name)
        key = bucket.new_key(output_path)
        key.set_contents_from_string(raw_image_data)
        key.make_public()
        return self._full_path(key)
