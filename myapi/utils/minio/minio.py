from minio import Minio
from myapi.config import MINIO_SETTINGS


# from minio.error import S3Error


class FlaskMinio:
    def __init__(self, config=None):
        config = {} if config is None else config

        self.config = {
            key: config.get(key) or value for key, value in MINIO_SETTINGS.items()
        }

    def make_client(self):
        client = Minio(**self.config)
        return client

    def make_bucket(self, bucket_name):
        client = self.make_client()
        bucket_exists = client.bucket_exists(bucket_name)
        if not bucket_exists:
            client.make_bucket(bucket_name)
        return client


print(FlaskMinio().make_client())
# client.fput_object(
#     "westhide", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
# )
