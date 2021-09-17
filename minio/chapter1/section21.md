# 选择API快速入门指南

传统的对象检索始终是整个实体，即5 GiB对象的GetObject将始终返回5 GiB数据。S3 Select API允许我们使用简单的SQL表达式来检索数据的子集。通过使用Select API仅检索应用程序所需的数据，可以实现大幅的性能改进。

您可以使用Select API查询具有以下功能的对象：

- CSV，JSON和Parquet-对象必须为CSV，JSON或Parquet格式。
- UTF-8是Select API支持的唯一编码类型。
- GZIP或BZIP2-可以使用GZIP或BZIP2压缩CSV和JSON文件。Select API支持使用GZIP，Snappy，LZ4对Parquet进行列压缩。Parquet对象不支持整个对象压缩。
- 服务器端加密-Select API支持查询受服务器端加密保护的对象。

当未键入值时（例如，读取CSV数据时），将根据上下文执行类型推断和值的自动转换。如果存在，则CAST功能将覆盖自动转换。

## 1. 先决条件

- 从[这里](http://docs.min.io/docs/minio-quickstart-guide)安装MinIO Server 。
- 熟悉AWS S3 API。
- 熟悉Python和安装依赖项。

## 2.安装 boto3

`aws-sdk-python`从[此处](https://aws.amazon.com/sdk-for-python/)安装适用于Python的AWS开发工具包官方文档

## 3. 例子

例如，让我们以gzip压缩的CSV文件为例。如果没有S3  Select，我们将需要下载，解压缩和处理整个CSV以获得所需的数据。使用Select  API，可以使用简单的SQL表达式仅从您感兴趣的CSV中返回数据，而不是检索整个对象。以下Python示例显示了如何`Location`从包含CSV格式数据的对象中检索第一列。

请更换`endpoint_url`，`aws_access_key_id`，`aws_secret_access_key`，`Bucket`和`Key`在这个本地设置`select.py`文件。

```py
#!/usr/bin/env/env python3
import boto3

s3 = boto3.client('s3',
                  endpoint_url='http://localhost:9000',
                  aws_access_key_id='minio',
                  aws_secret_access_key='minio123',
                  region_name='us-east-1')

r = s3.select_object_content(
    Bucket='mycsvbucket',
    Key='sampledata/TotalPopulation.csv.gz',
    ExpressionType='SQL',
    Expression="select * from s3object s where s.Location like '%United States%'",
    InputSerialization={
        'CSV': {
            "FileHeaderInfo": "USE",
        },
        'CompressionType': 'GZIP',
    },
    OutputSerialization={'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
```

## 4. 运行程序

使用以下命令将样本数据集上传到MinIO。

```sh
$ curl "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv" > TotalPopulation.csv
$ mc mb myminio/mycsvbucket
$ gzip TotalPopulation.csv
$ mc cp TotalPopulation.csv.gz myminio/mycsvbucket/sampledata/
```

现在，让我们继续运行我们的选择示例，以查询`Location`匹配的内容`United States`。

```sh
$ python3 select.py
840,United States of America,2,Medium,1950,1950.5,79233.218,79571.179,158804.395

840,United States of America,2,Medium,1951,1951.5,80178.933,80726.116,160905.035

840,United States of America,2,Medium,1952,1952.5,81305.206,82019.632,163324.851

840,United States of America,2,Medium,1953,1953.5,82565.875,83422.307,165988.190
....
....
....

Stats details bytesScanned:
6758866
Stats details bytesProcessed:
25786743
```

F有关更详细的SELECT SQL参考，请参见[此处](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html)

## 5. 进一步探索

- [`mc` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)
- [`mc sql` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/minio-client-complete-guide.html#sql)
- [`minio-go` SDK 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)
- [`aws-cli` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/aws-cli-with-minio)
- [`s3cmd` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/s3cmd-with-minio)
- [MinIO文档网站](http://docs.minio.org.cn)

## 6. 实施状况

- 支持完整的AWS S3 [SELECT SQL](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html)语法。
- 支持所有[运算符](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-operators.html) 。
- 支持所有聚合，条件，类型转换和字符串函数。
- `FROM S3Object[*].path`尚未评估JSON路径表达式。
- 尚不支持大号（有符号的64位范围之外）。
- 日期的[功能](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-date.html) `DATE_ADD`，`DATE_DIFF`，`EXTRACT`并`UTCNOW`使用类型转换沿`CAST`的`TIMESTAMP`数据类型，目前支持。
- 尚未遵守AWS S3的[保留关键字](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-keyword-list.html)列表。
- The Date [functions](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-date.html) `DATE_ADD`, `DATE_DIFF`, `EXTRACT` and `UTCNOW` along with type conversion using `CAST` to the `TIMESTAMP` data type are currently supported.
- CSV输入字段（甚至带引号）也不能包含换行符，即使`RecordDelimiter`是其他内容也是如此。