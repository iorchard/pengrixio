import boto
import boto.s3.connection

access_key = '7F5FX1JZJLAG2B9IFL8X'
secret_key = 'P5Inyn0UZUSZ5tKjB7ciLU10CIyWDyoLMouOQVUx'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = '192.168.24.10',
        port = 31597,
        is_secure = False,
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

for bucket in conn.get_all_buckets():
    print("{name}\t{created}".format(
        name = bucket.name,
        created = bucket.creation_date,
        ))
    for key in bucket.list():
        print("{name}\t{size}\t{modified}".format(
            name = key.name,
            size = key.size,
            modified = key.last_modified,
            ))

