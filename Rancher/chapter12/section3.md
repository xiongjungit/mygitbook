##Kubernetes - Cloud Providers
在Kubernetes中, 有一个cloud providers的概念, cloud provider是Kubernetes的一个模块，提供接口用于管理负载均衡、节点(也就是主机)以及网络路由。

目前, Rancher在 设置Kubernetes 时支持以下两种类型的cloud provider。 你可以选择使用哪种cloud provider。

###RANCHER
- 节点: 支持任何可以被加入Rancher的主机。
- 负载均衡: 启动Rancher的负载均衡, 使用HAproxy和rancher/lb-service-haproxy镜像作为负载均衡服务。 默认情况下, 负载均衡将请求以轮询方式发送给pods。

默认情况下, Kubernetes的cloud proivder被设置为rancher。

###AWS
- 节点: 仅支持以自定义主机方式添加AWS主机。
- 负载均衡: 启动一个AWS Elastic Load Balancer (ELB)作为负载均衡服务。 同时，你仍然可以通过使用ingress对象来创建Rancher负载均衡。
- 持久化卷(PV): 能够使用AWS Elastic Block Stores (EBS)用于persistent volumes.

####添加主机
在设置Kubernetes以aws cloud provider运行后，任何加入环境的主机都必须是一个AWS EC2实例并且至少具有以下IAM策略：

```
{
  "Effect": "Allow",
  "Action": "ec2:Describe*",
  "Resource": "*"
}
```
为了在Kubernetes中使用Elastic Load Balancers (ELBs)和EBS, 主机需要拥有一个具备合适权限的IAM角色。

#####IAM角色策略示例:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "ec2:AttachVolume",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "ec2:DetachVolume",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:*"],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": ["elasticloadbalancing:*"],
      "Resource": ["*"]
    }
  ]
}
```

####ELASTIC LOAD BALANCER (ELB)作为一个KUBERNETES服务
在设置Kubernetes中选择aws作为cloud provider并确保主机拥有配置ELB的相应IAM策略后，你可以开始创建负载均衡。

LB.YML文件示例
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-lb
  labels:
    app: nginx
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - name: http
    port: 80
    protocol: TCP
```

通过使用kubectl客户端, 让我们在Kubernetes中启动我们的负载均衡服务。 记住, 你可以通过为本地主机配置kubectl在本机使用kubectl客户端或者通过UI界面中的Kubernetes -> kubectl 命令行界面使用kubectl客户端。

```
$ kubectl create -f lb.yml
service "nginx-lb" created
$ kubectl describe services nginx-lb
Name:			nginx-lb
Namespace:		default
Labels:			app=nginx
Selector:		name=nginx
Type:			LoadBalancer
IP:			10.43.137.5
LoadBalancer Ingress:	a4c7d4290f48011e690470275ac52fef-1158549671.us-west-2.elb.amazonaws.com
Port:			http	80/TCP
NodePort:		http	32166/TCP
Endpoints:		<none>
Session Affinity:	None
Events:
  FirstSeen	LastSeen	Count	From			SubObjectPath	Type		Reason			Message
  ---------	--------	-----	----			-------------	--------	------			-------
  17s		17s		1	{service-controller }			Normal		CreatingLoadBalancer	Creating load balancer
  14s		14s		1	{service-controller }			Normal		CreatedLoadBalancer	Created load balancer
```

####使用EBS卷
在设置Kubernetes使用aws作为cloud provider并确保主机拥有配置EBS的相应IAM策略后，你可以开始使用EBS卷.