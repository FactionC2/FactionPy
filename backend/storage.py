from pathlib import Path
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from config import MINIO_ACCESSKEY, MINIO_SECRETKEY

minioClient = Minio('minio',
                    access_key=MINIO_ACCESSKEY,
                    secret_key=MINIO_SECRETKEY,
                    secure=True)


def make_bucket(bucket_name):
    try:
        minioClient.make_bucket(bucket_name, location="faction")
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise


def upload_blob(bucket_name, file_path):
    filename = Path(file_path).name
    minioClient.fput_object(bucket_name, filename, file_path)


def download_blob(bucket_name, file_path):
    filename = Path(file_path).name
    return minioClient.fget_object(bucket_name, filename, file_path)


def get_bucket_contents(bucket_name, prefix=None):
    return minioClient.list_objects_v2(bucket_name, prefix, recursive=True)

