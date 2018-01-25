Kubernetes提供了许多可以极大地提高应用程序安全性的选项。配置它们要求你熟悉 Kubernetes 以及其部署的安全要求。

以下是部署安全的Kubernetes应用的建议：

#确保镜像没有安全漏洞

运行有漏洞的容器使你的环境会遭受损害的风险。许多攻击可以简单地通过将软件升级为没有漏洞的版本来避免。

在部署前，应该确保所有的操作系统软件、Kubernetes软件为官方最新版本，防止部署后因为漏洞而造成入侵事件。

在运维过程中，要不断实现Continuous Security Vulnerability Scanning （持续安全漏洞扫描）——容器可能包括含有已知漏洞（CVE）的过时包。新的漏洞每天都会发布，所以这不是一个“一次性”的工作，对镜像持续进行安全评估是至关重要的。

定期对环境进行安全更新，一旦发现运行中容器的漏洞，你应该及时更新镜像并重新部署容器。尽量避免直接更新（例如， ‘apt-update’ ）到正在运行的容器，因为这样打破了镜像与容器的对应关系。

使用Kubernetes滚动升级功能升级容器非常简单，该功能允许通过升级镜像到最新版本来逐步更新正在运行的容器。

#确保在你的环境中只使用授权镜像

如果无法保证只运行符合组织策略的镜像，那么组织会面临运行脆弱甚至恶意容器的危险。从未知的来源下载和运行镜像是危险的，它相当于在生产服务器上运行未知服务商的软件，所以千万别这样做！

使用私有镜像存储你的合法镜像，这样能大量减少可能进入到你的环境的镜像数量。将成安全评估（如漏洞扫描）加入持续集成（CI）中，使其成为构建流程的一部分。

持续集成应确保只使用审查通过的代码来构建镜像。当镜像构建成功后，要对它进行安全漏洞扫描，然后只有当没有发现问题时，镜像才能被推送私有镜像仓库。在安全评估中失败的镜像不应该被推送到镜像仓库中。

Kubernetes镜像授权插件的工作已经完成（预计随kubernetes 1.4发布）。该插件允许阻止未授权镜像的分发。具体请查看[详情](https://github.com/kubernetes/kubernetes/pull/27129?spm=5176.7760782.2.3.H8q4AE)。

#限制对Kubernetes节点的直接访问

应该限制SSH登陆或SSH Key免登Kubernetes节点，减少对主机资源未授权的访问。应该要求用户使用“ kubectl exec ”命令，此命令能够在不访问主机的情况下直接访问容器环境。

你可以使用kubernetes授权插件来进一步控制用户对资源的访问。它允许设置对指定命名空间、容器和操作的细粒度访问控制规则。

#修改默认端口

Kubernets API Server进程提供Kuvernetes API。通常情况下，有一个进程运行在单一kubernetes-master节点上。

默认情况，Kubernetes API Server提供HTTP的两个端口：

##1.本地主机端口

- HTTP服务默认端口8080，修改标识–insecure-port
- 默认IP是本地主机，修改标识—insecure-bind-address
- 在HTTP中没有认证和授权检查
- 主机访问受保护

##2.Secure Port

- 默认端口6443，修改标识—secure-port
- 默认IP是首个非本地主机的网络接口，修改标识—bind-address HTTPS服务。
- 设置证书和秘钥的标识，–tls-cert-file，–tls-private-key-file
- 认证方式，令牌文件或者客户端证书
- 使用基于策略的授权方式

##3.移除：只读端口

基于安全考虑，会移除只读端口，使用Service Account代替。

#API管理端口访问控制

在某些配置文件中有一个代理（nginx）作为API Server进程运行在同一台机器上。该代理是HTTPS服务，认证端口是443，访问API Server是本地主机8080端口。在这些配置文件里，Secure Port通常设置为6443。

使用[ECS安全组防火墙规则](https://help.aliyun.com/document_detail/25475.html?spm=5176.7760782.2.4.H8q4AE)，限制外部HTTPS通过443端口访问。

上面的都是默认配置，每个云提供商可能会有所不同，您可以根据不同的业务场景灵活配置和调整。

#创建资源间的管理界限

限制用户权限的范围可以减少错误或恶意活动的影响。Kubernetes 命名空间允许将资源划分为逻辑命名组。在一个命名空间中创建的资源对其他命名空间是隐藏的。

默认情况下，用户在Kubernetes 集群中创建的每个资源运行在名称为“default”的默认空间内。你也可以创建额外的命名空间并附加资源和用户给它们。你可以使用Kubernetes 授权插件来创建策略，以便将不同用户的访问请求隔离到不同的命名空间中。

例如：以下策略将允许 ‘alice’ 从命名空间 ‘fronto’ 读取pods。

```
{
  "apiVersion": "abac.authorization.kubernetes.io/v1beta1", 
  "kind": "Policy", 
  "spec": {
    "user": "alice",
    "namespace": "fronto",
    "resource": "pods",
    "readonly": true
  }
}
```

#定义资源配额

运行没有资源限制的容器会将你的系统置于DoS或被其他租户干扰的风险中。为了防止和最小化这些风险，你应该定义资源配额。

默认情况下，Kubernetes 集群中的所有资源没有对CPU 和内存的使用限制。你可以创建资源配额策略，并附加到Kubernetes命名空间中来限制Pod对CPU和内存的使用。

下面的例子将限制命名空间中Pod 的数量为4个，CPU使用在1和2之间，内存使用在1GB 和 2GB 之间。

compute-resources.yaml：

```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    pods: "4"
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
```

分配资源配额到命名空间：

```
kubectl create -f ./compute-resources.yaml --namespace=myspace
```

#划分网络安全域

在相同的Kubernetes集群上运行不同的应用程序会导致恶意程序攻击其他应用程序的风险。所以网络分割对确保容器只与那些被允许的容器进行通信很重要。

Kubernetes 部署的挑战之一是创建Pod,服务和容器之间的网络分段。原因在于容器网络标识符（IP地址）动态的“天性”，以及容器可以在同一节点或节点间进行通信的事实。

谷歌云平台的用户受益于自动防火墙规则，能够防止跨集群通信。类似的实现可以使用网络防火墙或SDN解决方案部署。这方面的工作由Kubernetes 网络特别兴趣小组（Special Interest Group）完成，这将大大提高 pod到pod 的通信策略。

新的网络策略API应该解决 Pod之间创建防火墙规则的需求，限制容器化可以进行的网络访问。

下面展示了只允许前端（frontend）Pod访问后端（backend）Pod的网络策略：

```
POST /apis/net.alpha.kubernetes.io/v1alpha1/namespaces/tenant-a/networkpolicys
{
  "kind": "NetworkPolicy",
  "metadata": {
    "name": "pol1"
  },
  "spec": {
    "allowIncoming": {
      "from": [{
        "pods": { "segment": "frontend" } 
      }],
      "toPorts": [{
        "port": 80,
        "protocol": "TCP" 
      }]
    },
    "podSelector": { 
      "segment": "backend" 
    }
  }
}
```

点击[这里](http://blog.kubernetes.io/2016/04/Kubernetes-Network-Policy-APIs.html?spm=5176.7760782.2.5.H8q4AE)阅读更多网络策略的内容。

#将安全环境应用到你的Pods和容器中

当设计你的容器和pods时，确保为你的pods，容器和存储卷配置安全环境。安全环境是定义在yaml文件中的一项属性。它控制分配给 pod/容器/存储卷的安全参数。一些重要的参数是：

|安全环境设置项|描述|
|-|-|
|SecurityContext->runAsNonRoot|容器应该以非root用户运行|
|SecurityContext->Capabilities|控制分配给容器的Linux行为|
|SecurityContext->readOnlyRootFilesystem|控制容器对root文件系统是否只读|
|PodSecurityContext->runAsNonRoot|防止root用户作为pod的一部分运行容器|

以下是一个具有安全环境参数的pod 定义示例：

```
apiVersion: v1
kind: Pod
metadata:
  name: hello-world
spec:
  containers:
  # specification of the pod’s containers
  # ...
  securityContext:
    readOnlyRootFilesystem: true
    runAsNonRoot: true
```

[点击查看更多策略信息。](https://kubernetes.io/docs/api-reference/v1.8/?spm=5176.7760782.2.6.H8q4AE#_v1_podsecuritycontext)

#API Server认证与授权

API Server权限控制分为三种：Authentication（身份认证）、Authorization(授权)、AdmissionControl(准入控制)。

##1.身份认证:

当客户端向Kubernetes非只读端口发起API请求时，Kubernetes通过三种方式来认证用户的合法性。kubernetes中，验证用户是否有权限操作api的方式有三种：证书认证，token认证，基本信息认证。

###证书认证:

设置apiserver的启动参数：--client_ca_file=SOMEFILE

这个被引用的文件中包含的验证client的证书，如果被验证通过，那么这个验证记录中的主体对象将会作为请求的username。

###Token认证:

设置apiserver的启动参数：--token_auth_file=SOMEFILE

token file的格式包含三列：token，username，userid。当使用token作为验证方式时，在对apiserver的http请求中，增加 一个Header字段：Authorization ，将它的值设置为：Bearer SOMETOKEN。

###基本信息认证:

设置apiserver的启动参数：--basic_auth_file=SOMEFILE

如果更改了文件中的密码，只有重新启动apiserver使 其重新生效。其文件的基本格式包含三列：passwork，username，userid。当使用此作为认证方式时，在对apiserver的http 请求中，增加一个Header字段：Authorization，将它的值设置为： Basic BASE64ENCODEDUSER:PASSWORD。

##2.授权:

在Kubernetes中，认证和授权是分开的，而且授权发生在认证完成之后，认证过程是检验发起API请求的用户是不是他所声称的那个人。而授权过程则 判断此用户是否有执行该API请求的权限，因此授权是以认证的结果作为基础的。Kubernetes授权模块应用于所有对APIServer的HTTP访 问请求（只读端口除外），访问只读端口不需要认证和授权过程。APIServer启动时默认将authorization_mode设置为 AlwaysAllow模式，即永远允许。

Kubernetes授权模块检查每个HTTP请求并提取请求上下文中的所需属性（例如：user，resource kind，namespace）与访问控制规则进行比较。任何一个API请求在被处理前都需要通过一个或多个访问控制规则的验证。

目前Kubernetes支持并实现了以下的授权模式（authorization_mode），这些授权模式可以通过在apiserver启动时传入参数进行选择。

```
--authorization_mode=AlwaysDeny
--authorization_mode=AlwaysAllow
--authorization_mode=ABAC
```

AlwaysDeny 模式屏蔽所有的请求（一般用于测试）。AlwaysAllow模式允许所有请求，默认apiserver启动时采用的便是AlwaysAllow模式）。 ABAC（Attribute-Based Access Control，即基于属性的访问控制）模式则允许用户自定义授权访问控制规则。

###ABAC模式：

一个API请求中有4个属性被用于用户授权过程：

UserName：String类型，用于标识发起请求的用户。如果不进行认证、授权操作，则该字符串为空。

ReadOnly：bool类型，标识该请求是否仅进行只读操作（GET就是只读操作）。

Kind：String类型，用于标识要访问的Kubernetes资源对象的类型。当访问例如/api/v1beta1/pods等API endpoint时，Kind属性才非空，但访问其他endpoint时，例如/version，/healthz等，Kind属性为空。

Namespace：String类型，用于标识要访问的Kubernetes资源对象所在的namespace。

对ABAC模式，在apiserver启动时除了需要传入—authorization_mode=ABAC选项外，还需要指定 —authorization_policy_file=SOME_FILENAME。authorization_policy_file文件的每一 行都是一个JSON对象，该JSON对象是一个没有嵌套的map数据结构，代表一个访问控制规则对象。一个访问控制规则对象是一个有以下字段的map：

```
user：--token_auth_file指定的user字符串。
readonly：true或false，如果是true则表明该规则只应用于GET请求。
kind：Kubernetes内置资源对象类型，例如pods、events等。
namespace：也可以缩写成ns。
```

一个简单的访问控制规则文件如下所示，每一行定义一条规则。

```
{"user":"admin"}
{"user":"alice", "ns": "projectCaribou"}
{"user":"kubelet", "readonly": true, "kind": "pods"}
{"user":"kubelet", "kind": "events"}
{"user":"bob", "kind": "pods", "readonly": true, "ns": "projectCaribou"}
```

注：缺省的字段与该字段类型的零值（空字符串，0，false等）等价。

规则逐行说明如下。

- 第一行表明，admin可以做任何事情，不受namespace，资源类型，请求类型的限制。
- 第二行表明，alice能够在namespace “projectCaribou”中做任何事情，不受资源类型，请求类型的限制。
- 第三行表明，kubelet有权限读任何一个pod的信息。
- 第四行表明，kubelet有权限读写任何一个event。
- 第五行表明，Bob有权限读取在namespace “projectCaribou”中所有pod的信息。

一个授权过程就是一个比较API请求中各属性与访问控制规则文件中对应的各字段是否匹配的一个过程。当apiserver接收到一个API请求时，该请求 的各属性就已经确定了，如果有一个属性未被设置，则apiserver将其设为该类型的空值（空字符串，0，false等）。匹配规则很简单，如下所示。

如果API请求中的某个属性为空值，则规定该属性与访问控制规则文件中对应的字段匹配。

如果访问控制规则的某个字段为空值，则规定该字段与API请求的对应属性匹配。

如果API请求中的属性值非空且访问控制规则的某个字段值也非空，则将这两个值进行比较，如果相同则匹配，反之则不匹配。

API请求的属性元组（tuple）会与访问控制规则文件中的所有规则逐条匹配，只要有一条匹配则表示匹配成功，如若不然，则授权失败。

更多关于[Kubernetes API](http://docs.kubernetes.org.cn/27.html?spm=5176.7760782.2.7.H8q4AE) 访问控制介绍请点击查看。

#记录所有的日志

Kubernetes提供基于集群的日志，允许将容器活动日志记录到一个日志中心。当集群被创建时，每个容器的标准输出和标准错误都可以通过运行在每个节点上的Fluentd 服务记录到Stackdriver或Elasticsearch中，然后使用Kibana进行查看。

#总结

Kubernetes对创建安全部署提供多种选择，没有适合所有情况的万能解决方案，所以熟悉这些安全选项、了解它们如何提高应用程序安全性是很重要的。

我们推荐这篇文章中提到的安全实践，将Kubernetes的灵活配置能力加入到持续集成中，自动将安全性无缝融合到整个流程中。

参考信息：

Kubernetes官方最佳实践:http://blog.kubernetes.io/2016/08/security-best-practices-kubernetes-deployment.html
Kubernetes API文档:http://docs.kubernetes.org.cn/31.html