##Kubernetes中的持久化存储
Rancher能够通过Kubernetes原生资源对象创建拥有持久化存储的服务。在Kubernetes中, 持久化存储通过API资源对象管理, 其中包括PersistentVolume和PersistentVolumeClaim。Kubernetes中的存储组件支持多种后端存储(例如：NFS、EBS等), 存储具有独立于pod的生命周期。根据你希望使用的持久化卷的类型，你可能需要设置Kubernetes环境.

以下是如何在Rancher的Kubernetes环境中使用NFS和EBS的示例。

###PERSISTENT VOLUMES - NFS
在Kubernetes中使用NFS卷时，文件系统(也就是NFS)将被挂载在pod中。NFS允许多个pod同时进行写操作，这些pod使用相同的persistent volume claim。通过使用NFS卷，相同的数据可以在多个pod之间共享。

####NFS设置
你需要有一台正常运行的NFS服务器并设置了共享目录。在下面的示例中，我们假定/nfs被设置为共享目录。

####创建PERSISTENT VOLUMES (PV)和PERSISTENT VOLUME CLAIMS (PVC)
在Kubernetes模板中，kind需要被设置为PersistentVolume并使用nfs资源。 服务器将使用`<IP_OF_NFS_SERVER>`中设置的地址以及path所指定的路径作为共享目录(在我们的示例yaml文件中也就是/nfs目录)。

示例pv-nfs.yml文件

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs
spec:
  capacity:
    storage: 1Mi
  accessModes:
    - ReadWriteMany
  nfs:
    server: <IP_OF_NFS_SERVER>
    # Exported path of your NFS server
    path: "/nfs"
```

通过kubectl客户端, 我们可以使用下面的命令在Kubernetes中创建persistent volume。记住, 你可以通过为本地主机配置kubectl在本机使用kubectl客户端或者通过UI界面中的Kubernetes -> kubectl 命令行界面使用kubectl客户端。

```
$ kubectl create -f pv-nfs.yml
```

创建persistent volume之后, 你可以创建persistent volume claim，用于请求创建的persistent volume资源。

示例pvc-nfs.yml文件

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Mi
```

通过kubectl客户端, 我们可以使用以下命令在Kubernetes中创建persistent volume claim。记住，你可以通过为本地主机配置kubectl在本机使用kubectl客户端或者通过UI界面中的Kubernetes -> kubectl 命令行界面使用kubectl客户端。

```
$ kubectl create -f pvc-nfs.yml
```

在创建了persistent volume和persistent volume claim之后, 你可以通过以下命令确认persistent volume已绑定。

```
$ kubectl get pv,pvc

NAME      CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM         REASON    AGE
pv/nfs    1Mi        RWX           Retain          Bound     default/nfs             8s

NAME      STATUS    VOLUME    CAPACITY   ACCESSMODES   AGE
pvc/nfs   Bound     nfs       1Mi        RWX           5s
```

####创建一个POD使用PERSISTENT VOLUME CLAIM
现在persistent volume claim已经被创建, 我们可以创建使用这个persistent volume claim的pods。这些pods将会访问相同的数据。

示例rc-nfs.yml文件

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: rc-nfs-test
spec:
  replicas: 2
  selector:
    app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
          - name: nginx
            containerPort: 80
        volumeMounts:
            - name: nfs
              mountPath: "/usr/share/nginx/html"
      volumes:
      - name: nfs
        persistentVolumeClaim:
          claimName: nfs
```

通过kubectl客户端, 我们可以使用以下命令在Kubernetes中创建replication controller和两个pods。记住，你可以通过为本地主机配置kubectl在本机使用kubectl客户端或者通过UI界面中的Kubernetes -> kubectl 命令行界面使用kubectl客户端。

```
$ kubectl create -f rc-nfs-test.yml
service "nginx-service" created
replicationcontroller "nginx" created

$ kubectl get pods
NAME           READY     STATUS    RESTARTS   AGE
rc-nfs-test-42785   1/1       Running   0          10s
rc-nfs-test-rt3ld   1/1       Running   0          10s
```

我们可以测试两个pods都可以访问同一个persistent volume以及NFS服务端产生的修改。示例如下，我们可以在NFS服务器端的/nfs目录下创建一个文件。

```
$ echo "NFS Works!" > /nfs/index.html
```

在NFS服务器端创建文件后，我们可以在两个pods中查看这个文件。

```
$ kubectl exec rc-nfs-test-42785 cat /usr/share/nginx/html/index.html
NFS Works!
$ kubectl exec rc-nfs-test-rt3ld cat /usr/share/nginx/html/index.html
NFS Works!
```

###PERSISTENT VOLUMES - EBS


要在Kubernetes中使用EBS作为persistent volume，你需要对Kubernetes进行一些设置。

1. 参考AWS cloud provider选项文档中的步骤设置Kubernetes环境.
2. 所有主机必须是AWS EC2实例并且拥有正确的IAM策略。

在Kubernetes中使用EBS数据卷的操作可以分为两种: 静态初始化, 和通过storage classes动态初始化。

####静态初始化
在Kubernetes环境中使用persistent volume之前，需要预先在Rancher主机所在的AWS区域和可用区中创建EBS卷。为了使用persistent volume, 你需要先创建persistent volume资源对象。

示例pv-ebs.yml文件

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: ebs
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  awsElasticBlockStore:
    fsType: ext4
    # The EBS volume ID
    volumeID: <VOLUME_ID_IN_EBS>
```

通过kubectl客户端, 我们可以使用以下命令在Kubernetes中创建persistent volume。 文件中的<VOLUME_ID_IN_EBS>需要被替换为相应的EBS volume id。 记住，你可以通过为本地主机配置kubectl在本机使用kubectl客户端或者通过UI界面中的Kubernetes -> kubectl 命令行界面使用kubectl客户端。

```
$ kubectl create -f pv-ebs.yml
```

创建persistent volume之后, 你可以创建persistent volume claim，用于请求创建的persistent volume资源。

```
Example pvc-ebs.yml

kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvs-ebs
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  selector:
    matchLabels:
      release: "stable"
```

在创建了persistent volume和persistent volume claim之后, 你可以通过以下命令确认persistent volume已绑定。

$ kubectl get pv,pvc
创建一个POD使用PERSISTENT VOLUME CLAIM
创建persistent volume claim之后, 你只需要创建一个pod来使用它。

示例pod-ebs.yml文件

```
apiVersion: v1
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: ebs
  volumes:
    - name: ebs
      persistentVolumeClaim:
        claimName: pvc-ebs
```

在pod使用了相应的卷之后，AWS中卷的状态应当从可用变为使用中。

```
$ kubectl get pods,pv,pvc
NAME       READY     STATUS    RESTARTS   AGE
po/mypod   1/1       Running   0          3m

NAME      CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             REASON    AGE
pv/ebs    1Gi        RWO           Recycle         Bound     default/myclaim             3m

NAME          STATUS    VOLUME    CAPACITY   ACCESSMODES   AGE
pvc/pvc-ebs  Bound     pv1       1Gi        RWO           3m
```

####动态创建
在Kubernetes中使用EBS的另外一种方法是动态创建, 这种方式使用StorageClass自动创建并挂载数据卷到pods中。在我们的示例中, storage class将指定AWS作为storage provider并使用gp2类型以及us-west-2a可用区。

示例storage-class.yml文件

```
kind: StorageClass
apiVersion: storage.k8s.io/v1beta1
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  zone: us-west-2a
```

###创建POD使用STORAGE CLASSES
你可以在任何pod中使用storage class从而使Kubernetes自动创建新的卷并挂载到pod中。

```
{
  "kind": "PersistentVolumeClaim",
  "apiVersion": "v1",
  "metadata": {
    "name": "claim2",
    "annotations": {
      "volume.beta.kubernetes.io/storage-class": "standard"
    }
  },
  "spec": {
    "accessModes": [
      "ReadWriteOnce"
    ],
    "resources": {
      "requests": {
        "storage": "1Gi"
      }
    }
  }
}
```

通过在pod中使用这种请求方式，你将看到一个新的pv被创建并自动和pvc绑定:

```
$ kubectl get pv,pvc,pods
NAME                                          CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             REASON    AGE
pv/pvc-36fcf5dd-f476-11e6-b547-0275ac92095a   1Gi        RWO           Delete          Bound     default/claim2              1m

NAME          STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
pvc/claim2    Bound     pvc-36fcf5dd-f476-11e6-b547-0275ac92095a   1Gi        RWO           1m

NAME       READY     STATUS    RESTARTS   AGE
po/nginx   1/1       Running   0          29s
```