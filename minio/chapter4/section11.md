# 用于Haskell的MinIO Client SDK

MinIO Haskell客户端SDK提供了简单的API，可以访问[MinIO]（https://min.io）和与Amazon S3兼容的对象存储服务器。

## 最低需求

-Haskell [堆栈](https://docs.haskellstack.org/en/stable/README/)

## 安装

### 添加到您的项目

只需像往常一样，将minio-hs添加到项目的.cabal依赖项部分，或者如果使用hpack，则将其添加到package.yaml文件即可。

### 直接尝试 ghci

从主文件夹或任何非haskell项目目录中，只需运行：

```sh
stack install minio-hs
```

然后启动解释器会话，并使用以下命令浏览可用的API：

```sh
$ stack ghci
> :browse Network.Minio
```

## 示例

该 [示例](https://github.com/minio/minio-hs/tree/master/examples) 文件夹中包含许多例子，你可以尝试和使用学习和与发展中国家自己的项目的帮助。

### 快速入门示例-文件上传器

该示例程序连接到MinIO对象存储服务器，在服务器上创建存储桶，然后将文件上传到存储桶。

在此示例中，我们将使用运行在https://play.min.io的MinIO服务器。随意使用此服务进行测试和开发。访问凭证存在于库中，并向公众开放。

### FileUploader.hs

```haskell
#!/usr/bin/env stack
-- stack --resolver lts-14.11 runghc --package minio-hs --package optparse-applicative --package filepath

--
-- MinIO Haskell SDK, (C) 2017-2019 MinIO, Inc.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a  of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

{-# LANGUAGE OverloadedStrings   #-}
{-# LANGUAGE ScopedTypeVariables #-}
import           Network.Minio

import           Data.Monoid           ((<>))
import           Data.Text             (pack)
import           Options.Applicative
import           System.FilePath.Posix
import           UnliftIO              (throwIO, try)

import           Prelude

-- | The following example uses minio's play server at
-- https://play.min.io.  The endpoint and associated
-- credentials are provided via the libary constant,
--
-- > minioPlayCI :: ConnectInfo
--

-- optparse-applicative package based command-line parsing.
fileNameArgs :: Parser FilePath
fileNameArgs = strArgument
               (metavar "FILENAME"
                <> help "Name of file to upload to AWS S3 or a MinIO server")

cmdParser = info
            (helper <*> fileNameArgs)
            (fullDesc
             <> progDesc "FileUploader"
             <> header
             "FileUploader - a simple file-uploader program using minio-hs")

main :: IO ()
main = do
  let bucket = "my-bucket"

  -- Parse command line argument
  filepath <- execParser cmdParser
  let object = pack $ takeBaseName filepath

  res <- runMinio minioPlayCI $ do
    -- Make a bucket; catch bucket already exists exception if thrown.
    bErr <- try $ makeBucket bucket Nothing

    -- If the bucket already exists, we would get a specific
    -- `ServiceErr` exception thrown.
    case bErr of
      Left BucketAlreadyOwnedByYou -> return ()
      Left e                       -> throwIO e
      Right _                      -> return ()

    -- Upload filepath to bucket; object name is derived from filepath.
    fPutObject bucket object filepath defaultPutObjectOptions

  case res of
    Left e   -> putStrLn $ "file upload failed due to " ++ show e
    Right () -> putStrLn "file upload succeeded."
```

### 运行FileUploader

```sh
./FileUploader.hs "path/to/my/file"
```

## 有助于

[贡献者指南](https://github.com/minio/minio-hs/blob/master/CONTRIBUTING.md)

### 发展历程

建立:

```sh
git clone https://github.com/minio/minio-hs.git

cd minio-hs/

stack install
```

测试可以通过以下方式运行：

```sh

stack test
```

https://play.min.io  默认情况下，测试的一部分使用远程MinIO Play服务器。对于库开发，使用此远程服务器可能很慢。要在本地运行的MinIO live服务器上运行测试 http://localhost:9000 ， 只需将环境设置MINIO_LOCAL为任何值（然后取消设置以切换回Play）即可。

要运行实时服务器测试，请设置构建标志，如下所示：

```sh

stack test --flag minio-hs:live-test

# OR against a local MinIO server with:

MINIO_LOCAL=1 stack test --flag minio-hs:live-test
```

对于每个更改，配置的CI系统始终运行两个测试套件。

可以使用以下方法在本地构建文档：

```sh

stack haddock
```

