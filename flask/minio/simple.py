"""
Bucket operations
make_bucket     创建bucket
list_buckets    枚举所有的bucket
bucket_exists   bucket是否存在
remove_bucket   删除bucket
list_objects    (bucket_name, prefix, recursive) 枚举bucket下所有的object
list_objects_v2         枚举bucket下所有的object
list_incomplete_uploads (bucket_name, prefix, recursive)枚举bucket部分上传的object
get_bucket_policy   (bucket_name, prefix) 获取bucket的策略
set_bucket_policy   (bucket_name, prefix, policy) 设置bucket的策略.READ_ONLY,WRITE_ONLY,READ_WRITE,NONE

Object operations
get_object          下载object
put_object          上传object
copy_object
fput_object         (bucket_name, object_name, file_path, content_type)上传文件
fget_object         (bucket_name, object_name, file_path)下载到文件
get_partial_object
stat_object         获取object状态
remove_object       删除object
remove_objects      删除多个object
remove_incomplete_upload

Presigned operations
presigned_get_object
presigned_put_object
presigned_post_policy
set_bucket_notification
remove_all_bucket_notification
listen_bucket_notification

Bucket policy/notification operations
get_bucket_policy
set_bucket_policy
get_bucket_notification
"""

from minio import Minio
from minio.error import *


def test1():
    client = Minio("localhost:9000",
                   access_key="minio",
                   secret_key="abcde12345", secure=False)

    # 所有的buckets
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name)

    bucket_name = "files"

    # 检查和创建bucket
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # files下所有的文件
    files = client.list_objects(bucket_name, recursive=True)
    for f in files:
        print(f.object_name)

    object_name = "mydir/test.py"   # 可以有目录，也可以没有
    try:
        # 获取object的状态
        r = client.stat_object(bucket_name, object_name)
        print(object_name, r.size)
    except NoSuchKey as e:
        print("not exists", object_name)

    # 写入文件到object
    client.fput_object(bucket_name, object_name, "test1.py")

    content = client.get_object(bucket_name, object_name)
    print(object_name, len(content.data))


if __name__ == "__main__":
    test1()