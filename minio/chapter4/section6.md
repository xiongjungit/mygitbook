# Python Client API文档

## 初使化MinIO Client对象。

## MinIO

```py
from minio import Minio
from minio.error import ResponseError

minioClient = Minio('play.min.io',
                  access_key='Q3AM3UQ867SPQQA43P2F',
                  secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                  secure=True)
```

## AWS S3

```py
from minio import Minio
from minio.error import ResponseError

s3Client = Minio('s3.amazonaws.com',
                 access_key='YOUR-ACCESSKEYID',
                 secret_key='YOUR-SECRETACCESSKEY',
                 secure=True)
```

| 操作存储桶                                                   | 操作对象                                                     | Presigned操作                                                | 存储桶策略/通知                                              |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [`make_bucket`](http://docs.minio.org.cn/docs/master/python-client-api-reference#make_bucket) | [`get_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#get_object) | [`presigned_get_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#presigned_get_object) | [`get_bucket_policy`](http://docs.minio.org.cn/docs/master/python-client-api-reference#get_bucket_policy) |
| [`list_buckets`](http://docs.minio.org.cn/docs/master/python-client-api-reference#list_buckets) | [`put_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#put_object) | [`presigned_put_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#presigned_put_object) | [`set_bucket_policy`](http://docs.minio.org.cn/docs/master/python-client-api-reference#set_bucket_policy) |
| [`bucket_exists`](http://docs.minio.org.cn/docs/master/python-client-api-reference#bucket_exists) | [`_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#_object) | [`presigned_post_policy`](http://docs.minio.org.cn/docs/master/python-client-api-reference#presigned_post_policy) | [`get_bucket_notification`](http://docs.minio.org.cn/docs/master/python-client-api-reference#get_bucket_notification) |
| [`remove_bucket`](http://docs.minio.org.cn/docs/master/python-client-api-reference#remove_bucket) | [`stat_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#stat_object) |                                                              | [`set_bucket_notification`](http://docs.minio.org.cn/docs/master/python-client-api-reference#set_bucket_notification) |
| [`list_objects`](http://docs.minio.org.cn/docs/master/python-client-api-reference#list_objects) | [`remove_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#remove_object) |                                                              | [`remove_all_bucket_notification`](http://docs.minio.org.cn/docs/master/python-client-api-reference#remove_all_bucket_notification) |
| [`list_objects_v2`](http://docs.minio.org.cn/docs/master/python-client-api-reference#list_objects_v2) | [`remove_objects`](http://docs.minio.org.cn/docs/master/python-client-api-reference#remove_objects) |                                                              | [`listen_bucket_notification`](http://docs.minio.org.cn/docs/master/python-client-api-reference#listen_bucket_notification) |
| [`list_incomplete_uploads`](http://docs.minio.org.cn/docs/master/python-client-api-reference#list_incomplete_uploads) | [`remove_incomplete_upload`](http://docs.minio.org.cn/docs/master/python-client-api-reference#remove_incomplete_upload) |                                                              |                                                              |
|                                                              | [`fput_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#fput_object) |                                                              |                                                              |
|                                                              | [`fget_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#fget_object) |                                                              |                                                              |
|                                                              | [`get_partial_object`](http://docs.minio.org.cn/docs/master/python-client-api-reference#get_partial_object) |                                                              |                                                              |

## 1. 构造函数



### Minio(endpoint, access_key=None, secret_key=None, secure=True, region=None, http_client=None)

|                                                              |
| ------------------------------------------------------------ |
| `Minio(endpoint, access_key=None, secret_key=None, secure=True, region=None, http_client=None)` |
| 初使化一个新的client对象。                                   |

参数

| 参数          | 类型                              | 描述                                                         |
| :------------ | :-------------------------------- | :----------------------------------------------------------- |
| `endpoint`    | *string*                          | S3兼容对象存储服务endpoint。                                 |
| `access_key`  | *string*                          | 对象存储的Access key。（如果是匿名访问则可以为空）。         |
| `secret_key`  | *string*                          | 对象存储的Secret key。（如果是匿名访问则可以为空）。         |
| `secure`      | *bool*                            | 设为`True`代表启用HTTPS。 (默认是`True`)。                   |
| `region`      | *string*                          | 设置该值以覆盖自动发现存储桶region。 （可选，默认值是`None`）。 |
| `http_client` | *urllib3.poolmanager.PoolManager* | 设置该值以使用自定义的http client，而不是默认的http client。（可选，默认值是`None`）。 |

**示例**

### MinIO

```py
from minio import Minio
from minio.error import ResponseError

minioClient = Minio('play.min.io',
                    access_key='Q3AM3UQ867SPQQA43P2F',
                    secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')
from minio import Minio
from minio.error import ResponseError
import urllib3

httpClient = urllib3.ProxyManager(
                'https://proxy_host.sampledomain.com:8119/'
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                cert_reqs='CERT_REQUIRED',
                retries=urllib3.Retry(
                    total=5,
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504]
                )
            )
minioClient = Minio('your_hostname.sampledomain.com:9000',
                    access_key='ACCESS_KEY',
                    secret_key='SECRET_KEY',
                    secure=True,
                    http_client=httpClient)
```

### AWS S3

```py
from minio import Minio
from minio.error import ResponseError

s3Client = Minio('s3.amazonaws.com',
                 access_key='ACCESS_KEY',
                 secret_key='SECRET_KEY')
```

## 2. 操作存储桶



### make_bucket(bucket_name, location='us-east-1')

创建一个存储桶。

参数

| 参数          | 类型     | 描述                                                         |
| ------------- | -------- | ------------------------------------------------------------ |
| `bucket_name` | *string* | 存储桶名称。                                                 |
| `location`    | *string* | 存储桶被创建的region(地区)，默认是us-east-1(美国东一区)，下面列举的是其它合法的值： |
|               |          | us-east-1                                                    |
|               |          | us-west-1                                                    |
|               |          | us-west-2                                                    |
|               |          | eu-west-1                                                    |
|               |          | eu-central-1                                                 |
|               |          | ap-southeast-1                                               |
|               |          | ap-northeast-1                                               |
|               |          | ap-southeast-2                                               |
|               |          | sa-east-1                                                    |
|               |          | cn-north-1                                                   |

**示例**

```py
try:
    minioClient.make_bucket("mybucket", location="us-east-1")
except ResponseError as err:
    print(err)
```



### list_buckets()

列出所有的存储桶。

参数

| 返回值                 | 类型       | 描述               |
| :--------------------- | :--------- | :----------------- |
| `bucketList`           | *function* | 所有存储桶的list。 |
| `bucket.name`          | *string*   | 存储桶名称。       |
| `bucket.creation_date` | *time*     | 存储桶的创建时间。 |

**示例**

```py
buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)
```



### bucket_exists(bucket_name)

检查存储桶是否存在。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |

**示例**

```py
try:
    print(minioClient.bucket_exists("mybucket"))
except ResponseError as err:
    print(err)
```



### remove_bucket(bucket_name)

删除存储桶。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |

**示例**

```py
try:
    minioClient.remove_bucket("mybucket")
except ResponseError as err:
    print(err)
```



### list_objects(bucket_name, prefix=None, recursive=False)

列出存储桶中所有对象。

参数

| 参数                                                         | 类型     | 描述                                         |
| :----------------------------------------------------------- | :------- | :------------------------------------------- |
| `bucket_name`                                                | *string* | 存储桶名称。                                 |
| `prefix`                                                     | *string* | 用于过滤的对象名称前缀。可选项，默认为None。 |
| `recursive`   | *bool* |`True`代表递归查找，`False`代表类似文件夹查找，以'/'分隔，不查子文件夹。（可选，默认值是`False`）。 |          |                                              |

**返回值**

| 参数     | 类型     | 描述                                           |
| :------- | :------- | :--------------------------------------------- |
| `object` | *Object* | 该存储桶中所有对象的Iterator，对象的格式如下： |

| 参数                                                         | 类型                | 描述                   |
| :----------------------------------------------------------- | :------------------ | :--------------------- |
| `object.bucket_name`                                         | *string*            | 对象所在存储桶的名称。 |
| `object.object_name`                                         | *string*            | 对象的名称。           |
| `object.is_dir`       |  *bool*  | `True`代表列举的对象是文件夹（对象前缀）， `False`与之相反。 |                     |                        |
| `object.size`                                                | *int*               | 对象的大小。           |
| `object.etag`                                                | *string*            | 对象的etag值。         |
| `object.last_modified`                                       | *datetime.datetime* | 最后修改时间。         |
| `object.content_type`                                        | *string*            | 对象的content-type。   |
| `object.metadata`                                            | *dict*              | 对象的其它元数据。     |

**示例**

```py
# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects('mybucket', prefix='my-prefixname',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)
```



### list_objects_v2(bucket_name, prefix=None, recursive=False)

使用V2版本API列出一个存储桶中的对象。

参数

| 参数                                                         | 类型     | 描述                                         |
| :----------------------------------------------------------- | :------- | :------------------------------------------- |
| `bucket_name`                                                | *string* | 存储桶名称。                                 |
| `prefix`                                                     | *string* | 用于过滤的对象名称前缀。可选项，默认为None。 |
| `recursive`   | *bool* |`True`代表递归查找，`False`代表类似文件夹查找，以'/'分隔，不查子文件夹。（可选，默认值是`False`）。 |          |                                              |

**返回值**

| 参数     | 类型     | 描述                                           |
| :------- | :------- | :--------------------------------------------- |
| `object` | *Object* | 该存储桶中所有对象的Iterator，对象的格式如下： |

| 参数                                                         | 类型                | 描述                   |
| :----------------------------------------------------------- | :------------------ | :--------------------- |
| `object.bucket_name`                                         | *string*            | 对象所在存储桶的名称。 |
| `object.object_name`                                         | *string*            | 对象的名称。           |
| `object.is_dir`       |  *bool*  | `True`代表列举的对象是文件夹（对象前缀）， `False`与之相反。 |                     |                        |
| `object.size`                                                | *int*               | 对象的大小。           |
| `object.etag`                                                | *string*            | 对象的etag值。         |
| `object.last_modified`                                       | *datetime.datetime* | 最后修改时间。         |
| `object.content_type`                                        | *string*            | 对象的content-type。   |
| `object.metadata`                                            | *dict*              | 对象的其它元数据。     |

**示例**

```py
# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects_v2('mybucket', prefix='my-prefixname',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)
```



### list_incomplete_uploads(bucket_name, prefix, recursive=False)

列出存储桶中未完整上传的对象。

参数

| 参数                                                         | 类型     | 描述                     |
| :----------------------------------------------------------- | :------- | :----------------------- |
| `bucket_name`                                                | *string* | 存储桶名称。             |
| `prefix`                                                     | *string* | 用于过滤的对象名称前缀。 |
| `recursive` |*bool* |`True`代表递归查找，`False`代表类似文件夹查找，以'/'分隔，不查子文件夹。（可选，默认值是`False`）。 |          |                          |

**返回值**

| 参数            | 类型     | 描述                                |
| :-------------- | :------- | :---------------------------------- |
| `multipart_obj` | *Object* | multipart对象的Iterator，格式如下： |

| 参数                        | 类型     | 描述                       |
| :-------------------------- | :------- | :------------------------- |
| `multipart_obj.object_name` | *string* | 未完整上传的对象的名称。   |
| `multipart_obj.upload_id`   | *string* | 未完整上传的对象的上传ID。 |
| `multipart_obj.size`        | *int*    | 未完整上传的对象的大小。   |

**示例**

```py
# List all object paths in bucket that begin with my-prefixname.
uploads = minioClient.list_incomplete_uploads('mybucket',
                                         prefix='my-prefixname',
                                         recursive=True)
for obj in uploads:
    print(obj.bucket_name, obj.object_name, obj.upload_id, obj.size)
```



### get_bucket_policy(bucket_name, prefix)

获取存储桶的当前策略。

参数

| 参数          | 类型     | 描述             |
| :------------ | :------- | :--------------- |
| `bucket_name` | *string* | 存储桶名称。     |
| `prefix`      | *string* | 对象的名称前缀。 |

**返回值**

| 参数     | 类型                  | 描述                                                         |
| :------- | :-------------------- | :----------------------------------------------------------- |
| `Policy` | *minio.policy.Policy* | Policy枚举：Policy.READ_ONLY，Policy.WRITE_ONLY，Policy.READ_WRITE或 Policy.NONE。 |

**示例**

```py
# Get current policy of all object paths in bucket that begin with my-prefixname.
policy = minioClient.get_bucket_policy('mybucket',
                                       'my-prefixname')
print(policy)
```



### set_bucket_policy(bucket_name, prefix, policy)

给指定的存储桶设置存储桶策略。如果`prefix`不为空，则该存储桶策略仅对匹配这个指定前缀的对象生效。

参数

| 参数          | 类型                  | 描述                                                         |
| :------------ | :-------------------- | :----------------------------------------------------------- |
| `bucket_name` | *string*              | 存储桶名称。                                                 |
| `prefix`      | *string*              | 对象的名称前缀。                                             |
| `Policy`      | *minio.policy.Policy* | Policy枚举：Policy.READ_ONLY，Policy.WRITE_ONLY，Policy.READ_WRITE或 Policy.NONE。 |

**示例**

```py
# Set policy Policy.READ_ONLY to all object paths in bucket that begin with my-prefixname.
minioClient.set_bucket_policy('mybucket',
                              'my-prefixname',
                              Policy.READ_ONLY)
```



### get_bucket_notification(bucket_name)

获取存储桶上的通知配置。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |

**返回值**

| 参数           | 类型   | 描述                                                         |
| :------------- | :----- | :----------------------------------------------------------- |
| `notification` | *dict* | 如果没有通知配置，则返回一个空的dictionary，否则就和set_bucket_notification的参数结构一样。 |

**示例**

```py
# Get the notifications configuration for a bucket.
notification = minioClient.get_bucket_notification('mybucket')
# If no notification is present on the bucket:
# notification == {}
```



### set_bucket_notification(bucket_name, notification)

给存储桶设置通知配置。

参数

| 参数           | 类型     | 描述                               |
| :------------- | :------- | :--------------------------------- |
| `bucket_name`  | *string* | 存储桶名称。                       |
| `notification` | *dict*   | 非空dictionary，内部结构格式如下： |

`notification`参数格式如下：

- (dict) --
  - **TopicConfigurations** (list) -- 服务配置项目的可选列表，指定了AWS SNS Topics做为通知的目标。
  - **QueueConfigurations** (list) -- 服务配置项目的可选列表，指定了AWS SQS Queues做为通知的目标。
  - **CloudFunctionconfigurations** (list) -- 服务配置项目的可选列表，指定了AWS Lambda Cloud functions做为通知的目标。

以上项目中至少有一项需要在`notification`参数中指定。

上面提到的“服务配置项目”具有以下结构：

- (dict) --

  - **Id** (string) -- 配置项的可选ID，如果不指定，服务器自动生成。

  - **Arn** (string) -- 指定特定的Topic/Queue/Cloud Function identifier。

  - **Events** (list) -- 一个含有事件类型字符串的非空列表，事件类型取值如下： *'s3:ReducedRedundancyLostObject'*, *'s3:ObjectCreated:\*'*, *'s3:ObjectCreated:Put'*, *'s3:ObjectCreated:Post'*, *'s3:ObjectCreated:'*, *'s3:ObjectCreated:CompleteMultipartUpload'*, *'s3:ObjectRemoved:\*'*, *'s3:ObjectRemoved:Delete'*, *'s3:ObjectRemoved:DeleteMarkerCreated'*

  - **Filter** (dict) -- 一个可选的dictionary容器，里面含有基于键名称过滤的规则的对象。

  - Key

     (dict) -- dictionary容器，里面含有基于键名称前缀和后缀过滤的规则的对象。

    - **FilterRules** (list) -- 指定过滤规则标准的容器列表。
    - (dict) -- 键值对的dictionary容器，指定单个的过滤规则。
      - **Name** (string) -- 对象的键名称，值为“前缀”或“后缀”。
      - **Value** (string) -- 指定规则适用的值。

没有返回值。如果目标服务报错，会抛出`ResponseError`。如果有验证错误，会抛出`InvalidArgumentError`或者`TypeError`。输入参数的configuration不能为空 - 为了删除存储桶上的通知配置，参考`remove_all_bucket_notification()` API。

**示例**

```py
notification = {
    'QueueConfigurations': [
        {
            'Id': '1',
            'Arn': 'arn1',
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'prefix',
                            'Value': 'abc'
                        }
                    ]
                }
            }
        }
    ],
    'TopicConfigurations': [
        {
            'Arn': 'arn2',
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': '.jpg'
                        }
                    ]
                }
            }
        }
    ],
    'CloudFunctionConfigurations': [
        {
            'Arn': 'arn3',
            'Events': ['s3:ObjectRemoved:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': '.jpg'
                        }
                    ]
                }
            }
        }
    ]
}

try:
    minioClient.set_bucket_notification('mybucket', notification)
except ResponseError as err:
    # handle error response from service.
    print(err)
except (ArgumentError, TypeError) as err:
    # should happen only during development. Fix the notification argument
    print(err)
```



### remove_all_bucket_notification(bucket_name)

删除存储桶上配置的所有通知。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |

没有返回值，如果操作失败会抛出 `ResponseError` 异常。

**示例**

```py
# Remove all the notifications config for a bucket.
minioClient.remove_all_bucket_notification('mybucket')
```



### listen_bucket_notification(bucket_name, prefix, suffix, events)

监听存储桶上的通知，可以额外提供前缀、后缀和时间类型来进行过滤。使用该API前不需要先设置存储桶通知。这是一个MinIO的扩展API，MinIO Server会基于过来的请求使用唯一标识符自动注册或者注销。

当通知发生时，产生事件，调用者需要遍历读取这些事件。

参数

| 参数          | 类型     | 描述                       |
| :------------ | :------- | :------------------------- |
| `bucket_name` | *string* | 监听事件通知的存储桶名称。 |
| `prefix`      | *string* | 过滤通知的对象名称前缀。   |
| `suffix`      | *string* | 过滤通知的对象名称后缀。   |
| `events`      | *list*   | 启用特定事件类型的通知。   |

完整示例请看 [这里](https://raw.githubusercontent.com/minio/minio-py/master/examples/listen_notification.py)。

```py
# Put a file with default content-type.
events = minioClient.listen_bucket_notification('my-bucket', 'my-prefix/',
                                                '.my-suffix',
                                                ['s3:ObjectCreated:*',
                                                 's3:ObjectRemoved:*',
                                                 's3:ObjectAccessed:*'])
for event in events:
    print event
```

## 3. 操作对象



### get_object(bucket_name, object_name, request_headers=None)

下载一个对象。

参数

| 参数              | 类型     | 描述                                    |
| :---------------- | :------- | :-------------------------------------- |
| `bucket_name`     | *string* | 存储桶名称。                            |
| `object_name`     | *string* | 对象名称。                              |
| `request_headers` | *dict*   | 额外的请求头信息 （可选，默认为None）。 |

**返回值**

| 参数     | 类型                            | 描述                    |
| :------- | :------------------------------ | :---------------------- |
| `object` | *urllib3.response.HTTPResponse* | http streaming reader。 |

**示例**

```py
# Get a full object.
try:
    data = minioClient.get_object('mybucket', 'myobject')
    with open('my-testfile', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)
```



### get_partial_object(bucket_name, object_name, offset=0, length=0, request_headers=None)

下载一个对象的指定区间的字节数组。

参数

| 参数                                                         | 类型     | 描述                                    |
| :----------------------------------------------------------- | :------- | :-------------------------------------- |
| `bucket_name`                                                | *string* | 存储桶名称。                            |
| `object_name`                                                | *string* | 对象名称。                              |
| `offset`   |*int* |`offset` 是起始字节的位置                 |          |                                         |
| `length`   |*int* |`length`是要读取的长度 (可选，如果无值则代表读到文件结尾)。 |          |                                         |
| `request_headers`                                            | *dict*   | 额外的请求头信息 （可选，默认为None）。 |

**返回值**

| 参数     | 类型                            | 描述                    |
| :------- | :------------------------------ | :---------------------- |
| `object` | *urllib3.response.HTTPResponse* | http streaming reader。 |

**示例**

```py
# Offset the download by 2 bytes and retrieve a total of 4 bytes.
try:
    data = minioClient.get_partial_object('mybucket', 'myobject', 2, 4)
    with open('my-testfile', 'wb') as file_data:
        for d in data:
            file_data.write(d)
except ResponseError as err:
    print(err)
```



### fget_object(bucket_name, object_name, file_path, request_headers=None)

下载并将文件保存到本地。

参数

| 参数              | 类型     | 描述                                    |
| :---------------- | :------- | :-------------------------------------- |
| `bucket_name`     | *string* | 存储桶名称。                            |
| `object_name`     | *string* | 对象名称。                              |
| `file_path`       | *dict*   | 对象数据要写入的本地文件路径。          |
| `request_headers` | *dict*   | 额外的请求头信息 （可选，默认为None）。 |

**返回值**

| 参数  | 类型     | 描述                       |
| :---- | :------- | :------------------------- |
| `obj` | *Object* | 对象的统计信息，格式如下： |

| 参数                | 类型        | 描述                 |
| :------------------ | :---------- | :------------------- |
| `obj.size`          | *int*       | 对象的大小。         |
| `obj.etag`          | *string*    | 对象的etag值。       |
| `obj.content_type`  | *string*    | 对象的Content-Type。 |
| `obj.last_modified` | *time.time* | 最后修改时间。       |
| `obj.metadata`      | *dict*      | 对象的其它元数据。   |

**示例**

```py
# Get a full object and prints the original object stat information.
try:
    print(minioClient.fget_object('mybucket', 'myobject', '/tmp/myobject'))
except ResponseError as err:
    print(err)
```



### _object(bucket_name, object_name, object_source, _conditions=None, metadata=None)

拷贝对象存储服务上的源对象到一个新对象。

注意：本API支持的最大文件大小是5GB。

参数

| 参数            | 类型         | 描述                                             |
| :-------------- | :----------- | :----------------------------------------------- |
| `bucket_name`   | *string*     | 新对象的存储桶名称。                             |
| `object_name`   | *string*     | 新对象的名称。                                   |
| `object_source` | *string*     | 要拷贝的源对象的存储桶名称+对象名称。            |
| `_conditions`   | *Conditions* | 拷贝操作需要满足的一些条件（可选，默认为None）。 |

**示例**

以下所有条件都是允许的，并且可以组合使用。

```py
import time
from datetime import datetime
from minio import Conditions

_conditions = Conditions()
# Set modified condition,  object modified since 2014 April.
t = (2014, 4, 0, 0, 0, 0, 0, 0, 0)
mod_since = datetime.utcfromtimestamp(time.mktime(t))
_conditions.set_modified_since(mod_since)

# Set unmodified condition,  object unmodified since 2014 April.
_conditions.set_unmodified_since(mod_since)

# Set matching ETag condition,  object which matches the following ETag.
_conditions.set_match_etag("31624deb84149d2f8ef9c385918b653a")

# Set matching ETag except condition,  object which does not match the following ETag.
_conditions.set_match_etag_except("31624deb84149d2f8ef9c385918b653a")

# Set metadata
metadata = {"test-key": "test-data"}

try:
    _result = minioClient._object("mybucket", "myobject",
                                          "/my-sourcebucketname/my-sourceobjectname",
                                          _conditions,metadata=metadata)
    print(_result)
except ResponseError as err:
    print(err)
```



### put_object(bucket_name, object_name, data, length, content_type='application/octet-stream', metadata=None)

添加一个新的对象到对象存储服务。

注意：本API支持的最大文件大小是5TB。

参数

| 参数           | 类型           | 描述                                                         |
| :------------- | :------------- | :----------------------------------------------------------- |
| `bucket_name`  | *string*       | 存储桶名称。                                                 |
| `object_name`  | *string*       | 对象名称。                                                   |
| `data`         | *io.RawIOBase* | 任何实现了io.RawIOBase的python对象。                         |
| `length`       | *int*          | 对象的总长度。                                               |
| `content_type` | *string*       | 对象的Content type。（可选，默认是“application/octet-stream”）。 |
| `metadata`     | *dict*         | 其它元数据。（可选，默认是None）。                           |

**返回值**

| 参数   | 类型     | 描述           |
| :----- | :------- | :------------- |
| `etag` | *string* | 对象的etag值。 |

**示例**

单个对象的最大大小限制在5TB。put_object在对象大于5MiB时，自动使用multiple parts方式上传。这样，当上传失败时，客户端只需要上传未成功的部分即可（类似断点上传）。上传的对象使用MD5SUM签名进行完整性验证。

```py
import os
# Put a file with default content-type, upon success prints the etag identifier computed by server.
try:
    with open('my-testfile', 'rb') as file_data:
        file_stat = os.stat('my-testfile')
        print(minioClient.put_object('mybucket', 'myobject',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

# Put a file with 'application/csv'.
try:
    with open('my-testfile.csv', 'rb') as file_data:
        file_stat = os.stat('my-testfile.csv')
        minioClient.put_object('mybucket', 'myobject.csv', file_data,
                    file_stat.st_size, content_type='application/csv')
except ResponseError as err:
    print(err)
```



### fput_object(bucket_name, object_name, file_path, content_type='application/octet-stream', metadata=None)

通过文件上传到对象中。

参数

| 参数           | 类型     | 描述                                                         |
| :------------- | :------- | :----------------------------------------------------------- |
| `bucket_name`  | *string* | 存储桶名称。                                                 |
| `object_name`  | *string* | 对象名称。                                                   |
| `file_path`    | *string* | 本地文件的路径，会将该文件的内容上传到对象存储服务上。       |
| `content_type` | *string* | 对象的Content type（可选，默认是“application/octet-stream”）。 |
| `metadata`     | *dict*   | 其它元数据（可选，默认是None）。                             |

**返回值**

| 参数   | 类型     | 描述           |
| :----- | :------- | :------------- |
| `etag` | *string* | 对象的etag值。 |

**示例**

单个对象的最大大小限制在5TB。fput_object在对象大于5MiB时，自动使用multiple parts方式上传。这样，当上传失败时，客户端只需要上传未成功的部分即可（类似断点上传）。上传的对象使用MD5SUM签名进行完整性验证。

```py
# Put an object 'myobject' with contents from '/tmp/otherobject', upon success prints the etag identifier computed by server.
try:
    print(minioClient.fput_object('mybucket', 'myobject', '/tmp/otherobject'))
except ResponseError as err:
    print(err)

# Put on object 'myobject.csv' with contents from
# '/tmp/otherobject.csv' as 'application/csv'.
try:
    print(minioClient.fput_object('mybucket', 'myobject.csv',
                             '/tmp/otherobject.csv',
                             content_type='application/csv'))
except ResponseError as err:
    print(err)
```



### stat_object(bucket_name, object_name)

获取对象的元数据。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |
| `object_name` | *string* | 名称名称。   |

**返回值**

| 参数  | 类型     | 描述                       |
| :---- | :------- | :------------------------- |
| `obj` | *Object* | 对象的统计信息，格式如下： |

| 参数                | 类型        | 描述                    |
| :------------------ | :---------- | :---------------------- |
| `obj.size`          | *int*       | 对象的大小。            |
| `obj.etag`          | *string*    | 对象的etag值。          |
| `obj.content_type`  | *string*    | 对象的Content-Type。    |
| `obj.last_modified` | *time.time* | UTC格式的最后修改时间。 |
| `obj.metadata`      | *dict*      | 对象的其它元数据信息。  |

**示例**

```py
# Fetch stats on your object.
try:
    print(minioClient.stat_object('mybucket', 'myobject'))
except ResponseError as err:
    print(err)
```



### remove_object(bucket_name, object_name)

删除一个对象。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |
| `object_name` | *string* | 对象名称。   |

**示例**

```py
# Remove an object.
try:
    minioClient.remove_object('mybucket', 'myobject')
except ResponseError as err:
    print(err)
```



### remove_objects(bucket_name, objects_iter)

删除存储桶中的多个对象。

参数

| 参数           | 类型                           | 描述                     |
| :------------- | :----------------------------- | :----------------------- |
| `bucket_name`  | *string*                       | 存储桶名称。             |
| `objects_iter` | *list* , *tuple* or *iterator* | 多个对象名称的列表数据。 |

**返回值**

| 参数                    | 类型                                       | 描述                                  |
| :---------------------- | :----------------------------------------- | :------------------------------------ |
| `delete_error_iterator` | *iterator* of *MultiDeleteError* instances | 删除失败的错误信息iterator,格式如下： |

*注意*

1. 由于上面的方法是延迟计算（lazy evaluation），默认是不计算的，所以上面返回的iterator必须被evaluated（比如：使用循环）。
2. 该iterator只有在执行删除操作出现错误时才不为空，每一项都包含删除报错的对象的错误信息。

该iterator产生的每一个删除错误信息都有如下结构：

| 参数                             | 类型     | 描述                 |
| :------------------------------- | :------- | :------------------- |
| `MultiDeleteError.object_name`   | *string* | 删除报错的对象名称。 |
| `MultiDeleteError.error_code`    | *string* | 错误码。             |
| `MultiDeleteError.error_message` | *string* | 错误信息。           |

**示例**

```py
# Remove multiple objects in a single library call.
try:
    objects_to_delete = ['myobject-1', 'myobject-2', 'myobject-3']
    # force evaluation of the remove_objects() call by iterating over
    # the returned value.
    for del_err in minioClient.remove_objects('mybucket', objects_to_delete):
        print("Deletion Error: {}".format(del_err))
except ResponseError as err:
    print(err)
```



### remove_incomplete_upload(bucket_name, object_name)

删除一个未完整上传的对象。

参数

| 参数          | 类型     | 描述         |
| :------------ | :------- | :----------- |
| `bucket_name` | *string* | 存储桶名称。 |
| `object_name` | *string* | 对象名称。   |

**示例**

```py
# Remove an partially uploaded object.
try:
    minioClient.remove_incomplete_upload('mybucket', 'myobject')
except ResponseError as err:
    print(err)
```

## 4. Presigned操作



### presigned_get_object(bucket_name, object_name, expiry=timedelta(days=7))

生成一个用于HTTP GET操作的presigned URL。浏览器/移动客户端可以在即使存储桶为私有的情况下也可以通过这个URL进行下载。这个presigned URL可以有一个过期时间，默认是7天。

参数

| 参数                                                         | 类型                | 描述                            |
| :----------------------------------------------------------- | :------------------ | :------------------------------ |
| `bucket_name`                                                | *string*            | 存储桶名称。                    |
| `object_name`                                                | *string*            | 对象名称。                      |
| `expiry`                                                     | *datetime.datetime* | 过期时间，单位是秒，默认是7天。 |
| `response_headers`   | *dictionary*    |额外的响应头 （比如：`response-content-type`、`response-content-disposition`）。 |                     |                                 |

**示例**

```py
from datetime import timedelta

# presigned get object URL for object name, expires in 2 days.
try:
    print(minioClient.presigned_get_object('mybucket', 'myobject', expires=timedelta(days=2)))
# Response error is still possible since internally presigned does get bucket location.
except ResponseError as err:
    print(err)
```



### presigned_put_object(bucket_name, object_name, expires=timedelta(days=7))

生成一个用于HTTP PUT操作的presigned URL。浏览器/移动客户端可以在即使存储桶为私有的情况下也可以通过这个URL进行上传。这个presigned URL可以有一个过期时间，默认是7天。

注意：你可以通过只指定对象名称上传到S3。

参数

| 参数          | 类型                | 描述                            |
| :------------ | :------------------ | :------------------------------ |
| `bucket_name` | *string*            | 存储桶名称。                    |
| `object_name` | *string*            | 对象名称。                      |
| `expiry`      | *datetime.datetime* | 过期时间，单位是秒，默认是7天。 |

**示例**

```py
from datetime import timedelta

# presigned Put object URL for an object name, expires in 3 days.
try:
    print(minioClient.presigned_put_object('mybucket',
                                      'myobject',
                                      expires=timedelta(days=3)))
# Response error is still possible since internally presigned does get
# bucket location.
except ResponseError as err:
    print(err)
```



### presigned_post_policy(PostPolicy)

允许给POST操作的presigned URL设置策略条件。这些策略包括比如，接收对象上传的存储桶名称，名称前缀，过期策略。

创建policy：

```py
from datetime import datetime, timedelta

from minio import PostPolicy
post_policy = PostPolicy()

# Apply upload policy restrictions:

# set bucket name location for uploads.
post_policy.set_bucket_name('mybucket')
# set key prefix for all incoming uploads.
post_policy.set_key_startswith('myobject')
# set content length for incoming uploads.
post_policy.set_content_length_range(10, 1024)
# set content-type to allow only text
post_policy.set_content_type('text/plain')

# set expiry 10 days into future.
expires_date = datetime.utcnow()+timedelta(days=10)
post_policy.set_expires(expires_date)
```

获得POST表单的键值对形式的对象：

```py
try:
    signed_form_data = minioClient.presigned_post_policy(post_policy)
except ResponseError as err:
    print(err)
```

使用`curl`POST你的数据：

```py
curl_str = 'curl -X POST {0}'.format(signed_form_data[0])
curl_cmd = [curl_str]
for field in signed_form_data[1]:
    curl_cmd.append('-F {0}={1}'.format(field, signed_form_data[1][field]))

# print curl command to upload files.
curl_cmd.append('-F file=@<FILE>')
print(' '.join(curl_cmd))
```

## 5. 了解更多

- [MinIO Golang Client SDK快速入门](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)
- [MinIO Java Client SDK快速入门](http://docs.minio.org.cn/docs/master/java-client-quickstart-guide)
- [MinIO JavaScript Client SDK快速入门](http://docs.minio.org.cn/docs/master/javascript-client-quickstart-guide)