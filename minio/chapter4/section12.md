# MinIO Haskell SDK API参考

## 初始化MinIO Client对象。

### MinIO-用于公共Play服务器

```haskell
minioPlayCI :: ConnectInfo
minioPlayCI
```

### AWS S3

```haskell
awsCI :: ConnectInfo
awsCI { connectAccesskey = "your-access-key"
      , connectSecretkey = "your-secret-key"
      }
```

| 操作存储桶                                                   | 操作对象                                                     | Presigned 操作                                               |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [`listBuckets`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#listBuckets) | [`getObject`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#getObject) | [`presignedGetObjectUrl`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#presignedGetObjectUrl) |
| [`makeBucket`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#makeBucket) | [`putObject`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#putObject) | [`presignedPutObjectUrl`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#presignedPutObjectUrl) |
| [`removeBucket`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#removeBucket) | [`fGetObject`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#fGetObject) | [`presignedPostPolicy`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#presignedPostPolicy) |
| [`listObjects`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#listObjects) | [`fPutObject`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#fPutObject) |                                                              |
| [`listObjectsV1`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#listObjectsV1) | [`Object`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#Object) |                                                              |
| [`listIncompleteUploads`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#listIncompleteUploads) | [`removeObject`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#removeObject) |                                                              |
| [`bucketExists`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#bucketExists) | [`selectObjectContent`](http://docs.minio.org.cn/docs/master/haskell-client-api-reference#selectObjectContent) |                                                              |

## 1.连接和运行存储服务上的操作

Haskell MinIO SDK提供了高级功能来执行 MinIO服务器或任何类似于AWS S3的API兼容存储上的操作 服务。

### `ConnectInfo`类型

“ ConnectInfo”记录类型包含一个连接的信息。 特定的服务器。 建议构造`ConnectInfo` 使用由提供的几个智能构造函数之一的值 库，在以下小节中介绍。

该库通过以下方式自动发现存储区 默认。 这对于可能在其中存储桶的AWS尤其有用 不同地区。 执行上传，下载或其他操作时 操作时，图书馆向服务请求一个位置 存储桶并将其缓存以供后续请求。

#### awsCI :: ConnectInfo

`awsCI`是一个提供AWS连接信息的值 S3。 可以通过覆盖两个字段来提供凭据 所以：

```haskell
awsConn = awsCI {
    connectAccessKey = "my-AWS-access-key"
  , connectSecretKey = "my-AWS-secret-key"
  }
```

#### awsWithRegionCI :: Region -> Bool -> ConnectInfo

这个构造函数允许指定初始区域和一个布尔值 启用/禁用自动区域发现行为。

表达式“ awsWithRegion region autoDiscover”中的参数为：

| 参数           | 类型                        | 描述                                                         |
| :------------- | :-------------------------- | :----------------------------------------------------------- |
| `region`       | *Region* (alias for `Text`) | 默认情况下，所有请求连接到的区域。                           |
| `autoDiscover` | *Bool*                      | 如果为True，将启用区域发现。 如果为False，则禁用发现，并且所有请求仅进入给定区域。 |

#### minioPlayCI :: ConnectInfo

该构造函数向以下对象提供连接和身份验证信息 在以下位置连接到公共MinIO Play服务器 `https://play.min.io/`.

#### minioCI :: Text -> Int -> Bool -> ConnectInfo

用于连接到MinIO服务器。

`minioCI host port isSecure`表达式中的参数为：

| 参数       | 类型   | 描述                                |
| :--------- | :----- | :---------------------------------- |
| `host`     | *Text* | MinIO或其他S3-API兼容服务器的主机名 |
| `port`     | *Int*  | 要连接的端口号                      |
| `isSecure` | *Bool* | 服务器是否使用HTTPS？               |

#### ConnectInfo字段和默认实例

下表显示了ConnectInfo记录类型中的字段：

| 字段                        | 类型                        | 描述                                          |
| :-------------------------- | :-------------------------- | :-------------------------------------------- |
| `connectHost`               | *Text*                      | 服务器的主机名。 默认为`localhost'。          |
| `connectPort`               | *Int*                       | 服务器侦听的端口号。 默认为9000               |
| `connectAccessKey`          | *Text*                      | 用于身份验证的访问密钥。 默认为`minio`。      |
| `connectSecretkey`          | *Text*                      | 用于身份验证的密钥。 默认为`minio123`。       |
| `connectIsSecure`           | *Bool*                      | 指定服务器是否使用TLS。 默认为False           |
| `connectRegion`             | *Region* (alias for `Text`) | 指定要使用的区域。 默认为'us-east-1'          |
| `connectAutoDiscoverRegion` | *Bool*                      | 指定库是否应自动发现存储桶的区域。 默认为True |

类型为ConnectInfo的def值具有上述所有默认值 价值观。

### The Minio Monad

此monad提供执行请求所需的环境 针对MinIO或其他S3 API兼容服务器。 它使用 提供给它的`ConnectInfo`值的连接信息。 它 执行连接池，存储桶位置缓存，错误处理 和资源清理行动。

runMinio函数执行Minio中提供的动作 monad并返回一个“ IO（MinioErr a）”值：

```haskell
{-# Language OverloadedStrings #-}

import Network.Minio

main :: IO ()
main = do
  result <- runMinio def $ do
    buckets <- listBuckets
    return $ length buckets

  case result of
    Left e -> putStrLn $ "Failed operation with error: " ++ show e
    Right n -> putStrLn $ show n ++ " bucket(s) found."
```

上面执行一次“ listBuckets”操作并返回 服务器中的存储桶。 如果有任何错误，将被退回 作为类型“ MinioErr”的值作为“左”值。

## 2. 操作存储桶



### listBuckets :: Minio [BucketInfo]

列出存储桶。

**返回值**

| 返回值类型           | 描述       |
| :------------------- | :--------- |
| *Minio [BucketInfo]* | 列出存储桶 |

**BucketInfo记录类型**

| 字段             | 类型                       | 描述         |
| :--------------- | :------------------------- | :----------- |
| `biName`         | *Bucket* (alias of `Text`) | 桶名         |
| `biCreationDate` | *UTCTime*                  | 桶的创建时间 |



### makeBucket :: Bucket -> Maybe Region -> Minio ()

创建一个新的存储桶。 如果未指定区域，则该区域 使用由`ConnectInfo`指定的。

**参数**

在“makeBucket bucketName region”表达式中，参数为：

| 参数         | 类型                        | 描述                                                         |
| ------------ | --------------------------- | ------------------------------------------------------------ |
| `bucketName` | *Bucket* (alias for `Text`) | 桶名                                                         |
| `region`     | *Maybe Region*              | 创建存储桶的区域。 如果未指定，则默认为`ConnectInfo`中的区域。 |

**示例**

```haskell
{-# Language OverloadedStrings #-}

main :: IO ()
main = do
    res <- runMinio minioPlayCI $ do
        makeBucket bucketName (Just "us-east-1")
    case res of
        Left err -> putStrLn $ "Failed to make bucket: " ++ (show res)
        Right _ -> putStrLn $ "makeBucket successful."
```



### removeBucket :: Bucket -> Minio ()

删除存储桶。 存储桶必须为空，否则将引发错误。

**参数**

在表达式`removeBucket bucketName`中，参数为：

| 参数         | 类型                        | 描述       |
| ------------ | --------------------------- | ---------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶桶名 |

**示例**

```haskell
{-# Language OverloadedStrings #-}

main :: IO ()
main = do
    res <- runMinio minioPlayCI $ do
        removeBucket "mybucket"

    case res of
        Left err -> putStrLn $ "Failed to remove bucket: " ++ (show res)
        Right _ -> putStrLn $ "removeBucket successful."
```



### listObjects :: Bucket -> Maybe Text -> Bool -> C.ConduitM () ObjectInfo Minio ()

列出给定存储桶中的对象，实现了AWS S3 API的版本2。

**参数**

在表达式“ listObjects bucketName prefix recursive”中， 参数是：

| 参数         | 类型                        | 描述                                                         |
| :----------- | :-------------------------- | :----------------------------------------------------------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名                                                     |
| `prefix`     | *Maybe Text*                | 对象前缀                                                     |
| `recursive`  | *Bool*                      | true代表递归查找，false代表类似文件夹查找，以'/'分隔，不查子文件夹。 |

**返回值**

| 返回值类型                          | 描述                                         |
| :---------------------------------- | :------------------------------------------- |
| *C.ConduitM () ObjectInfo Minio ()* | 对应于每个对象的`ObjectInfo`值的管道生产者。 |

**ObjectInfo记录类型**

| 字段         | 类型                        | 描述                       |
| :----------- | :-------------------------- | :------------------------- |
| `oiObject`   | *Object* (alias for `Text`) | 对象名称                   |
| `oiModTime`  | *UTCTime*                   | 对象的上次修改时间         |
| `oiETag`     | *ETag* (alias for `Text`)   | 对象的ETag                 |
| `oiSize`     | *Int64*                     | 对象的大小（以字节为单位） |
| `oiMetadata` | *HashMap Text Text*         | 键值用户元数据对的映射     |

**示例**

```haskell
{-# LANGUAGE OverloadedStrings #-}
import           Network.Minio

import           Conduit
import           Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
    bucket = "test"

  -- Performs a recursive listing of all objects under bucket "test"
  -- on play.min.io.
  res <- runMinio minioPlayCI $
    runConduit $ listObjects bucket Nothing True .| mapM_C (\v -> (liftIO $ print v))
  print res
```



### listObjectsV1 :: Bucket -> Maybe Text -> Bool -> C.ConduitM () ObjectInfo Minio ()

列出给定存储桶中的对象，实现AWS S3 API的版本1。 这个API 提供了与旧版S3兼容的对象存储端点。

**参数**

在表达式“ listObjectsV1 bucketName prefix recursive”中， 参数是：

| 参数         | 类型                        | 描述                                                         |
| :----------- | :-------------------------- | :----------------------------------------------------------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶桶名                                                   |
| `prefix`     | *Maybe Text*                | 对象前缀                                                     |
| `recursive`  | *Bool*                      | true代表递归查找，false代表类似文件夹查找，以'/'分隔，不查子文件夹。 |

**返回值**

| 返回值类型                          | 描述                                         |
| :---------------------------------- | :------------------------------------------- |
| *C.ConduitM () ObjectInfo Minio ()* | 对应于每个对象的`ObjectInfo`值的管道生产者。 |

**ObjectInfo记录类型**

| 字段        | 类型                        | 描述                       |
| :---------- | :-------------------------- | :------------------------- |
| `oiObject`  | *Object* (alias for `Text`) | 对象名称                   |
| `oiModTime` | *UTCTime*                   | 对象的上次修改时间         |
| `oiETag`    | *ETag* (alias for `Text`)   | 对象的ETag                 |
| `oiSize`    | *Int64*                     | 对象的大小（以字节为单位） |

**示例**

```haskell
{-# LANGUAGE OverloadedStrings #-}
import           Network.Minio

import           Conduit
import           Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
    bucket = "test"

  -- Performs a recursive listing of all objects under bucket "test"
  -- on play.min.io.
  res <- runMinio minioPlayCI $
    runConduit $ listObjectsV1 bucket Nothing True .| mapM_C (\v -> (liftIO $ print v))
  print res
```



### listIncompleteUploads :: Bucket -> Maybe Prefix -> Bool -> C.Producer Minio UploadInfo

列出未完全上传的对象。

**参数**

在表达式“ listIncompleteUploads bucketName前缀递归”中 参数为：

| 参数         | 类型                        | 描述                                                         |
| :----------- | :-------------------------- | :----------------------------------------------------------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶桶名                                                   |
| `prefix`     | *Maybe Text*                | 对象前缀                                                     |
| `recursive`  | *Bool*                      | true代表递归查找，false代表类似文件夹查找，以'/'分隔，不查子文件夹。 |

**返回值**

| 返回值类型                          | 描述                                                 |
| :---------------------------------- | :--------------------------------------------------- |
| *C.ConduitM () UploadInfo Minio ()* | 对应于每个不完整分段上传的`UploadInfo`值的管道生产者 |

**UploadInfo记录类型**

| 字段         | 类型     | 描述                     |
| :----------- | :------- | :----------------------- |
| `uiKey`      | *Object* | 上传对象不完整的名称     |
| `uiUploadId` | *String* | 未完全上传的对象的上传ID |
| `uiSize`     | *Int64*  | 上传对象不完整的大小     |

**示例**

```haskell
{-# LANGUAGE OverloadedStrings #-}
import           Network.Minio

import           Conduit
import           Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
    bucket = "test"

  -- Performs a recursive listing of incomplete uploads under bucket "test"
  -- on a local MinIO server.
  res <- runMinio minioPlayCI $
    runConduit $ listIncompleteUploads bucket Nothing True .| mapM_C (\v -> (liftIO $ print v))
  print res
```

## 3. 对象操作



### getObject :: Bucket -> Object -> GetObjectOptions -> Minio (C.ConduitM () ByteString Minio ())

从S3服务获取对象，还可以选择提供对象范围。

**参数**

在表达式“ getObject bucketName objectName opts”中，参数 是：

| 参数         | 类型                        | 描述                                           |
| :----------- | :-------------------------- | :--------------------------------------------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶桶名                                     |
| `objectName` | *Object* (alias for `Text`) | 对象名称                                       |
| `opts`       | *GetObjectOptions*          | GET请求的选项指定其他选项，例如If-Match，Range |

**GetObjectOptions记录类型**

| 字段                   | 类型                            | 描述                                                         |
| :--------------------- | :------------------------------ | :----------------------------------------------------------- |
| `gooRange`             | `Maybe ByteRanges`              | 表示对象的字节范围。 例如ByteRangeFromTo 0 9表示对象的前十个字节 |
| `gooIfMatch`           | `Maybe ETag` (alias for `Text`) | （可选）对象的ETag应该匹配                                   |
| `gooIfNoneMatch`       | `Maybe ETag` (alias for `Text`) | （可选）对象的ETag不匹配                                     |
| `gooIfUnmodifiedSince` | `Maybe UTCTime`                 | （可选）自对象未被修改以来的时间                             |
| `gooIfModifiedSince`   | `Maybe UTCTime`                 | （可选）自修改对象以来的时间                                 |

**返回值**

| 可以增量读取返回值以处理以下内容 物体。     | 返回值类型         | 描述 |
| :------------------------------------------ | :----------------- | ---- |
| *Minio (C.ConduitM () ByteString Minio ())* | 字节串值的管道源。 |      |

**示例**

```haskell
{-# LANGUAGE OverloadedStrings #-}
import           Network.Minio

import qualified Data.Conduit        as C
import qualified Data.Conduit.Binary as CB

import           Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
      bucket = "my-bucket"
      object = "my-object"
  res <- runMinio minioPlayCI $ do
    src <- getObject bucket object def
    C.connect src $ CB.sinkFileCautious "/tmp/my-object"

  case res of
    Left e  -> putStrLn $ "getObject failed." ++ (show e)
    Right _ -> putStrLn "getObject succeeded."
```



### putObject :: Bucket -> Object -> C.ConduitM () ByteString Minio () -> Maybe Int64 -> PutObjectOptions -> Minio ()

从给定输入将对象上载到服务中的存储桶 具有可选长度的字节流。 您也可以选择指定 对象的其他元数据。

**参数**

在表达式putObject bucketName objectName inputSrc中，参数 是：

| 参数         | 类型                                | 描述                           |
| :----------- | :---------------------------------- | :----------------------------- |
| `bucketName` | *Bucket* (alias for `Text`)         | 存储桶桶名                     |
| `objectName` | *Object* (alias for `Text`)         | 对象名称                       |
| `inputSrc`   | *C.ConduitM () ByteString Minio ()* | 管道生产者的ByteString值       |
| `size`       | *Int64*                             | 提供流大小（可选）             |
| `opts`       | *PutObjectOptions*                  | 为对象提供其他元数据的可选参数 |

**示例**

```haskell
{-# LANGUAGE OverloadedStrings #-}
import           Network.Minio

import qualified Data.Conduit.Combinators as CC

import           Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
      bucket = "test"
      object = "obj"
      localFile = "/etc/lsb-release"
      kb15 = 15 * 1024

  -- Eg 1. Upload a stream of repeating "a" using putObject with default options.
  res <- runMinio minioPlayCI $
    putObject bucket object (CC.repeat "a") (Just kb15) def
  case res of
    Left e   -> putStrLn $ "putObject failed." ++ show e
    Right () -> putStrLn "putObject succeeded."
```



### fGetObject :: Bucket -> Object -> FilePath -> GetObjectOptions -> Minio ()

将对象从服务中的存储桶下载到给定文件

**参数**

在表达式“ fGetObject bucketName objectName inputFile”中，参数 是：

| 参数         | 类型                        | 描述                                           |
| :----------- | :-------------------------- | :--------------------------------------------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶桶名                                     |
| `objectName` | *Object* (alias for `Text`) | 对象名称                                       |
| `inputFile`  | *FilePath*                  | 要上传文件的路径                               |
| `opts`       | *GetObjectOptions*          | GET请求的选项指定其他选项，例如If-Match，Range |

**GetObjectOptions记录类型**

| 字段                   | 类型                            | 描述                                                         |
| :--------------------- | :------------------------------ | :----------------------------------------------------------- |
| `gooRange`             | `Maybe ByteRanges`              | 表示对象的字节范围。 例如ByteRangeFromTo 0 9表示对象的前十个字节 |
| `gooIfMatch`           | `Maybe ETag` (alias for `Text`) | (可选）对象的ETag应该匹配                                    |
| `gooIfNoneMatch`       | `Maybe ETag` (alias for `Text`) | （可选）对象的ETag不匹配                                     |
| `gooIfUnmodifiedSince` | `Maybe UTCTime`                 | （可选）自对象未被修改以来的时间                             |
| `gooIfModifiedSince`   | `Maybe UTCTime`                 | （可选）自修改对象以来的时间                                 |

```haskell

{-# Language OverloadedStrings #-}
import Network.Minio

import Data.Conduit (($$+-))
import Data.Conduit.Binary (sinkLbs)
import Prelude

-- | The following example uses MinIO play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

main :: IO ()
main = do
  let
      bucket = "my-bucket"
      object = "my-object"
      localFile = "/etc/lsb-release"

  res <- runMinio minioPlayCI $ do
    src <- fGetObject bucket object localFile def
    (src $$+- sinkLbs)

  case res of
    Left e -> putStrLn $ "fGetObject failed." ++ (show e)
    Right _ -> putStrLn "fGetObject succeeded."
```



### fPutObject :: Bucket -> Object -> FilePath -> Minio ()

从给定文件将对象上传到服务中的存储桶

**参数**

在表达式“ fPutObject bucketName objectName inputFile”中，参数 是：

| 参数         | 类型                        | 描述         |
| :----------- | :-------------------------- | :----------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名称   |
| `objectName` | *Object* (alias for `Text`) | 对象名称     |
| `inputFile`  | *FilePath*                  | 上传文件路径 |

**示例**

```haskell
{-# Language OverloadedStrings #-}
import Network.Minio
import qualified Data.Conduit.Combinators as CC

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"
    localFile = "/etc/lsb-release"

  res <- runMinio minioPlayCI $ do
           fPutObject bucket object localFile

  case res of
    Left e -> putStrLn $ "Failed to fPutObject " ++ show bucket ++ "/" ++ show object
    Right _ -> putStrLn "fPutObject was successful"
```



### Object :: DestinationInfo -> SourceInfo -> Minio ()

将对象的内容从服务复制到另一个

**参数**

在表达式Object dstInfo srcInfo中，参数 是：

| 参数      | 类型              | 描述                 |
| :-------- | :---------------- | :------------------- |
| `dstInfo` | *DestinationInfo* | 代表目标对象属性的值 |
| `srcInfo` | *SourceInfo*      | 代表源对象属性的值   |

**SourceInfo记录类型**

| 字段                   | 类型                   | 描述                                                         |
| :--------------------- | :--------------------- | :----------------------------------------------------------- |
| `srcBucket`            | `Bucket`               | 存储桶名称                                                   |
| `srcObject`            | `Object`               | 对象名称                                                     |
| `srcRange`             | `Maybe (Int64, Int64)` | （可选）表示源对象的字节范围。 （0，9）代表源对象的前十个字节 |
| `srcIfMatch`           | `Maybe Text`           | （可选）ETag源对象应匹配                                     |
| `srcIfNoneMatch`       | `Maybe Text`           | （可选）ETag源对象不匹配                                     |
| `srcIfUnmodifiedSince` | `Maybe UTCTime`        | （可选）自修改源对象以来的时间                               |
| `srcIfModifiedSince`   | `Maybe UTCTime`        | （可选）自修改源对象以来的时间                               |
|                        |                        |                                                              |

**Destination记录类型**

| 字段        | 类型     | 描述                             |
| :---------- | :------- | :------------------------------- |
| `dstBucket` | `Bucket` | 服务器端Object中的目标存储桶名称 |
| `dstObject` | `Object` | 服务器端Object中目标对象的名称   |

**示例**

```haskell
{-# Language OverloadedStrings #-}
import Network.Minio

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"
    object = "obj-"

  res <- runMinio minioPlayCI $ do
           Object def { dstBucket = bucket, dstObject = object } def { srcBucket = bucket, srcObject = object }

  case res of
    Left e -> putStrLn $ "Failed to Object " ++ show bucket ++ show "/" ++ show object
    Right _ -> putStrLn "Object was successful"
```



### removeObject :: Bucket -> Object -> Minio ()

从服务中删除对象

**参数**

在表达式`removeObject bucketName objectName`中，参数 是：

| 参数         | 类型                        | 描述       |
| :----------- | :-------------------------- | :--------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名称 |
| `objectName` | *Object* (alias for `Text`) | 对象名称   |

**示例**

```haskell
{-# Language OverloadedStrings #-}
import Network.Minio

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"

  res <- runMinio minioPlayCI $ do
           removeObject bucket object

  case res of
    Left e -> putStrLn $ "Failed to remove " ++ show bucket ++ "/" ++ show object
    Right _ -> putStrLn "Removed object successfully"
```



### removeIncompleteUpload :: Bucket -> Object -> Minio ()

从服务中删除正在进行的对象分段上传

**参数**

在表达式`removeIncompleteUpload bucketName objectName`中，参数 是：

| 参数         | 类型                        | 描述       |
| :----------- | :-------------------------- | :--------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名称 |
| `objectName` | *Object* (alias for `Text`) | 对象名称   |

**示例**

```haskell
{-# Language OverloadedStrings #-}
import Network.Minio

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"

  res <- runMinio minioPlayCI $
           removeIncompleteUpload bucket object

  case res of
    Left _ -> putStrLn $ "Failed to remove " ++ show bucket ++ "/" ++ show object
    Right _ -> putStrLn "Removed incomplete upload successfully"
```



### selectObjectContent :: Bucket -> Object -> SelectRequest -> Minio (ConduitT () EventMessage Minio ())

从服务中删除正在进行的对象分段上传

**参数**

在“ selectObjectContent bucketName objectName selReq”表达式中 参数为：

| 参数         | 类型                        | 描述         |
| :----------- | :-------------------------- | :----------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名称   |
| `objectName` | *Object* (alias for `Text`) | 对象名称     |
| `selReq`     | *SelectRequest*             | 选择请求参数 |

**SelectRequest 记录**

该记录是使用selectRequest创建的。 有关更多信息，请参考Haddock。

**返回值**

返回值可用于读取响应中的各个`EventMessage`。 有关更多信息，请参考Haddock。

| 返回值                                        | 描述                        |
| :-------------------------------------------- | :-------------------------- |
| *Minio (C.conduitT () EventMessage Minio ())* | “ EventMessage”值的管道源。 |

**示例**

```haskell
{-# Language OverloadedStrings #-}
import Network.Minio

import qualified Conduit              as C

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"

  res <- runMinio minioPlayCI $ do
    let sr = selectRequest "Select * from s3object"
             defaultCsvInput defaultCsvOutput
    res <- selectObjectContent bucket object sr
    C.runConduit $ res C..| getPayloadBytes C..| C.stdoutC

  case res of
    Left _ -> putStrLn "Failed!"
    Right _ -> putStrLn "Success!"
```



### bucketExists :: Bucket -> Minio Bool

检查存储桶是否存在。

**参数**

在“ bucketExists bucketName”表达式中，参数为：

| 参数         | 类型                        | 描述       |
| :----------- | :-------------------------- | :--------- |
| `bucketName` | *Bucket* (alias for `Text`) | 存储桶名称 |

## 4. Presigned 操作



### presignedGetObjectUrl :: Bucket -> Object -> UrlExpiry -> Query -> RequestHeaders -> Minio ByteString

生成带有身份验证签名的URL，以获取（下载） 宾语。 在此处传递的所有其他查询参数和标头将是 已签名，并且在使用生成的URL时是必需的。 询问 参数可用于更改由 服务器。 标头可用于设置Etag匹配条件等。

有关可能的请求参数和标头的列表，请参阅 GET对象REST API AWS S3文档。

**参数**

在表达式“ presignedGetObjectUrl bucketName objectName expiry queryParams headers”中 参数为：

| 参数          | 类型                                                         | 描述                       |
| :------------ | :----------------------------------------------------------- | :------------------------- |
| `bucketName`  | *Bucket* (alias for `Text`)                                  | 存储桶名称                 |
| `objectName`  | *Object* (alias for `Text`)                                  | 对象名称                   |
| `expiry`      | *UrlExpiry* (alias for `Int`)                                | 网址到期时间（以秒为单位） |
| `queryParams` | *Query* (from package `http-types:Network.HTTP.Types`)       | 查询参数添加到URL          |
| `headers`     | *RequestHeaders* (from package `http-types:Network.HTTP.Types` | 网址应使用的请求标头       |

**返回值**

返回生成的URL-将包括身份验证 信息。

| 返回值类型   | 描述               |
| :----------- | :----------------- |
| *ByteString* | 生成 presigned URL |

**示例**

```haskell
{-# Language OverloadedStrings #-}

import Network.Minio
import qualified Data.ByteString.Char8 as B

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"

  res <- runMinio minioPlayCI $ do
           -- Set a 7 day expiry for the URL
           presignedGetObjectUrl bucket object (7*24*3600) [] []

  -- Print the URL on success.
  putStrLn $ either
    (("Failed to generate URL: " ++) . show)
    B.unpack
    res
```



### presignedPutObjectUrl :: Bucket -> Object -> UrlExpiry -> RequestHeaders -> Minio ByteString

生成带有身份验证签名的网址以PUT（上传） 宾语。 任何多余的标头（如果通过）都将被签名，因此它们是 使用URL上载数据时必需。 这可以用于 例如，在对象上设置用户元数据。

有关可能通过的标头的列表，请参考PUT对象 REST API AWS S3文档。

**参数**

在表达式“ presignedPutObjectUrl bucketName objectName expiry headers”中 参数为：

| 参数         | 类型                                                         | 描述                       |
| :----------- | :----------------------------------------------------------- | :------------------------- |
| `bucketName` | *Bucket* (alias for `Text`)                                  | 存储桶名称                 |
| `objectName` | *Object* (alias for `Text`)                                  | 对象名称                   |
| `expiry`     | *UrlExpiry* (alias for `Int`)                                | 网址到期时间（以秒为单位） |
| `headers`    | *RequestHeaders* (from package `http-types:Network.HTTP.Types` | 网址应使用的请求标头       |

**返回值**

返回生成的URL-将包括身份验证 信息。

| 返回值类型   | 描述               |
| :----------- | :----------------- |
| *ByteString* | 生成 presigned URL |

**示例**

```haskell
{-# Language OverloadedStrings #-}

import Network.Minio
import qualified Data.ByteString.Char8 as B

main :: IO ()
main = do
  let
    bucket = "mybucket"
    object = "myobject"

  res <- runMinio minioPlayCI $ do
           -- Set a 7 day expiry for the URL
           presignedPutObjectUrl bucket object (7*24*3600) [] []

  -- Print the URL on success.
  putStrLn $ either
    (("Failed to generate URL: " ++) . show)
    B.unpack
    res
```



### presignedPostPolicy :: PostPolicy -> Minio (ByteString, HashMap Text ByteString)

生成预签名的URL和POST策略以通过POST上传文件 请求。 用于浏览器上传并生成表单数据 应当在请求中提交。

PostPolicy参数是使用newPostPolicy函数创建的：

#### newPostPolicy :: UTCTime -> [PostPolicyCondition] -> Either PostPolicyError PostPolicy

在“ newPostPolicy expirationTime条件”表达式中，参数为：

| 参数             | 类型                                              | 描述                     |
| :--------------- | :------------------------------------------------ | :----------------------- |
| `expirationTime` | *UTCTime* (from package `time:Data.Time.UTCTime`) | 保单的到期时间           |
| `conditions`     | *[PostPolicyConditions]*                          | 要添加到策略中的条件列表 |

使用各种辅助功能创建策略条件- 有关详细信息，请参阅Haddock。

由于条件是通过`newPostPolicy`验证的，因此它返回一个 任一个值。

**返回值**

presignedPostPolicy返回一个2元组-生成的URL和一个映射 包含应随请求一起提交的表单数据。

**示例**

```haskell
{-# Language OverloadedStrings #-}

import Network.Minio

import qualified Data.ByteString       as B
import qualified Data.ByteString.Char8 as Char8
import qualified Data.HashMap.Strict   as H
import qualified Data.Text.Encoding    as Enc
import qualified Data.Time             as Time

main :: IO ()
main = do
  now <- Time.getCurrentTime
  let
    bucket = "mybucket"
    object = "myobject"

    -- set an expiration time of 10 days
    expireTime = Time.addUTCTime (3600 * 24 * 10) now

    -- create a policy with expiration time and conditions - since the
    -- conditions are validated, newPostPolicy returns an Either value
    policyE = newPostPolicy expireTime
              [ -- set the object name condition
                ppCondKey "photos/my-object"
                -- set the bucket name condition
              , ppCondBucket "my-bucket"
                -- set the size range of object as 1B to 10MiB
              , ppCondContentLengthRange 1 (10*1024*1024)
                -- set content type as jpg image
              , ppCondContentType "image/jpeg"
                -- on success set the server response code to 200
              , ppCondSuccessActionStatus 200
              ]

  case policyE of
    Left err -> putStrLn $ show err
    Right policy -> do
      res <- runMinio minioPlayCI $ do
        (url, formData) <- presignedPostPolicy policy

        -- a curl command is output to demonstrate using the generated
        -- URL and form-data
        let
          formFn (k, v) = B.concat ["-F ", Enc.encodeUtf8 k, "=",
                                    "'", v, "'"]
          formOptions = B.intercalate " " $ map formFn $ H.toList formData

        return $ B.intercalate " " $
          ["curl", formOptions, "-F file=@/tmp/photo.jpg", url]

      case res of
        Left e -> putStrLn $ "post-policy error: " ++ (show e)
        Right cmd -> do
          putStrLn $ "Put a photo at /tmp/photo.jpg and run command:\n"

          -- print the generated curl command
          Char8.putStrLn cmd
```