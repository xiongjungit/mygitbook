##3 - 节点需求
Whether you’re configuring Rancher to run in a single-node or high-availability setup, each node running Rancher Server must meet the following requirements.

###Operating Systems
Rancher is supported on the following operating systems and their subsequent releases.

- Ubuntu 16.04 (64-bit)
- Red Hat Enterprise Linux 7.5 (64-bit)
- RancherOS 1.4 (64-bit)
- Windows Server version 1803 (64-bit)

If you are using RancherOS, make sure you switch the Docker engine to a supported version using:

```
sudo ros engine switch docker-17.03.2-ce
```

###Hardware

Hardware requirements scale based on the size of your Rancher deployment. Provision each individual node according to the requirements.

|Deployment Size	|Clusters	|Nodes	|vCPUs	|RAM
|-|-|-|-|-|
|Small	|Up to 5	|Up to 50	|4	|16GB
|Medium	|Up to 100	|Up to 500	|8	|32GB
|Large	|Over 100	|Over 500	|Contact Rancher|Contact Rancher

###Software

A supported version of Docker is required.

Supported Versions:

- 1.12.6
- 1.13.1
- 17.03.2
- 17.06 (for Windows)

If you are using RancherOS, make sure you switch the Docker engine to a supported version using:

```
sudo ros engine switch docker-17.03.2-ce
```
Docker Documentation: Installation Instructions

###Networking

####Node IP address
Each node used (either for the Single Node Install, High Availability (HA) Install or nodes that are used in clusters) should have a static IP configured. In case of DHCP, the nodes should have a DHCP reservation to make sure the node gets the same IP allocated.

####Port requirements
When deploying Rancher in an HA cluster, certain ports on your nodes must be open to allow communication with Rancher. The ports that must be open change according to the type of machines hosting your cluster nodes. For example, if your are deploying Rancher on nodes hosted by an IaaS, port 22 must be open for SSH. The following diagram depicts the ports that are opened for each cluster type.

Cluster Type Port Requirements

![](../image/chapter2/1-1.svg)

Rancher nodes:
Nodes running the rancher/rancher container

####Rancher nodes - Inbound rules

<table>    <tbody><tr>        <th>Protocol</th>        <th>Port</th>        <th align="left">Source</th>        <th align="left">Description</th>    </tr>    <tr>  

      <td>TCP</td>        <td>80</td>        <td><ul><li>Load balancer/proxy that does external SSL termination</li></ul></td>        <td>Rancher UI/API when 

external SSL termination is used</td>    </tr>    <tr>        <td>TCP</td>        <td>443</td>        <td><ul><li>etcd nodes</li><li>controlplane 

nodes</li><li>worker nodes</li><li>Hosted/Imported Kubernetes</li><li>any that needs to be able to use UI/API</li></ul></td>        <td>Rancher agent, Rancher 

UI/API, kubectl</td>    </tr></tbody></table>

####Rancher nodes - Outbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Destination</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>22</td>            <td><ul><li>Any node IP from a node created using Node Driver</li></ul></td>            <td>SSH provisioning of nodes using Node Driver</td>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>35.160.43.145/32</li><li>35.167.242.46/32</li><li>52.33.59.17/32</li></ul></td>            <td>git.rancher.io (catalogs)</td>        </tr>        <tr>            <td>TCP</td>            <td>2376</td>            <td><ul><li>Any node IP from a node created using Node Driver</li></ul></td>            <td>Docker daemon TLS port used by Docker Machine</td>        </tr>        <tr>            <td>TCP</td>            <td>6443</td>            <td><ul><li>Hosted/Imported Kubernetes API</li></ul></td>            <td>Kubernetes apiserver</td>        </tr>    </tbody></table>

etcd nodes:
Nodes with the role etcd

####etcd nodes - Inbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Source</th>            <th align="left">Description</th>        </tr>            <tr>                <td>TCP</td>                <td>2376</td>                <td><ul><li>Rancher nodes</li></ul></td>                <td>Docker daemon TLS port used by Docker Machine<br>(only needed when using Node Driver/Templates)</td>            </tr>        <tr>            <td>TCP</td>            <td>2379</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li></ul></td>            <td>etcd client requests</td>        </tr>        <tr>            <td>TCP</td>            <td>2380</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li></ul></td>            <td>etcd peer communication</td>        </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>etcd node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP</td>            <td>10250</td>            <td><ul><li>controlplane nodes</li></ul></td>            <td>kubelet</td>        </tr>    </tbody></table>

####etcd nodes - Outbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Destination</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>Rancher nodes</li></ul></td>            <td>Rancher agent</td>        </tr>        <tr>            <td>TCP</td>            <td>2379</td>            <td><ul><li>etcd nodes</li></ul></td>            <td>etcd client requests</td>        </tr>        <tr>            <td>TCP</td>            <td>2380</td>            <td><ul><li>etcd nodes</li></ul></td>            <td>etcd peer communication</td>        </tr>        <tr>            <td>TCP</td>            <td>6443</td>            <td><ul><li>controlplane nodes</li></ul></td>            <td>Kubernetes apiserver</td>        </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>etcd node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>    </tbody></table>

controlplane nodes:
Nodes with the role controlplane

####controlplane nodes - Inbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Source</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>80</td>            <td><ul><li>Any that consumes Ingress services</li></ul></td>            <td>Ingress controller (HTTP)</td>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>Any that consumes Ingress services</li></ul></td>            <td>Ingress controller (HTTPS)</td>        </tr>            <tr>                <td>TCP</td>                <td>2376</td>                <td><ul><li>Rancher nodes</li></ul></td>                <td>Docker daemon TLS port used by Docker Machine<br>(only needed when using Node Driver/Templates)</td>            </tr>        <tr>            <td>TCP</td>            <td>6443</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Kubernetes apiserver</td>        </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>controlplane node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP</td>            <td>10250</td>            <td><ul><li>controlplane nodes</li></ul></td>            <td>kubelet</td>        </tr>        <tr>            <td>TCP</td>            <td>10254</td>            <td><ul><li>controlplane node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Ingress controller livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP/UDP</td>            <td>30000-32767</td>            <td><ul><li>Any source that consumes NodePort services</li></ul></td>            <td>NodePort port range</td>        </tr>    </tbody></table>

####controlplane nodes - Outbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Destination</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>Rancher nodes</li></ul></td>            <td>Rancher agent</td>        </tr>        <tr>            <td>TCP</td>            <td>2379</td>            <td><ul><li>etcd nodes</li></ul></td>            <td>etcd client requests</td>        </tr>        <tr>            <td>TCP</td>            <td>2380</td>            <td><ul><li>etcd nodes</li></ul></td>            <td>etcd peer communication</td>        </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>controlplane node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP</td>            <td>10250</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>kubelet</td>        </tr>        <tr>            <td>TCP</td>            <td>10254</td>            <td><ul><li>controlplane node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Ingress controller livenessProbe/readinessProbe</td>        </tr>    </tbody></table>

worker nodes:
Nodes with the role worker

####worker nodes - Inbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Source</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>80</td>            <td><ul><li>Any that consumes Ingress services</li></ul></td>            <td>Ingress controller (HTTP)</td>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>Any that consumes Ingress services</li></ul></td>            <td>Ingress controller (HTTPS)</td>        </tr>            <tr>                <td>TCP</td>                <td>2376</td>                <td><ul><li>Rancher nodes</li></ul></td>                <td>Docker daemon TLS port used by Docker Machine<br>(only needed when using Node Driver/Templates)</td>            </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>worker node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP</td>            <td>10250</td>            <td><ul><li>controlplane nodes</li></ul></td>            <td>kubelet</td>        </tr>        <tr>            <td>TCP</td>            <td>10254</td>            <td><ul><li>worker node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Ingress controller livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP/UDP</td>            <td>30000-32767</td>            <td><ul><li>Any source that consumes NodePort services</li></ul></td>            <td>NodePort port range</td>        </tr>    </tbody></table>

####worker nodes - Outbound rules

<table>        <tbody><tr>            <th>Protocol</th>            <th>Port</th>            <th align="left">Destination</th>            <th align="left">Description</th>        </tr>        <tr>            <td>TCP</td>            <td>443</td>            <td><ul><li>Rancher nodes</li></ul></td>            <td>Rancher agent</td>        </tr>        <tr>            <td>TCP</td>            <td>6443</td>            <td><ul><li>controlplane nodes</li></ul></td>            <td>Kubernetes apiserver</td>        </tr>        <tr>        <td>UDP</td>            <td>8472</td>            <td><ul><li>etcd nodes</li><li>controlplane nodes</li><li>worker nodes</li></ul></td>            <td>Canal/Flannel VXLAN overlay networking</td>        </tr>        <tr>        <td>TCP</td>            <td>9099</td>            <td><ul><li>worker node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Canal/Flannel livenessProbe/readinessProbe</td>        </tr>        <tr>            <td>TCP</td>            <td>10254</td>            <td><ul><li>worker node itself (local traffic, not across nodes)</li></ul>See <a href="#local-node-traffic">Local node traffic</a></td>            <td>Ingress controller livenessProbe/readinessProbe</td>        </tr>    </tbody></table>

####Information on local node traffic
Kubernetes healthchecks (livenessProbe and readinessProbe) are executed on the host itself. On most nodes, this is allowed by default. When you have applied strict host firewall (i.e. iptables) policies on the node, or when you are using nodes that have multiple interfaces (multihomed), this traffic gets blocked. In this case, you have to explicitly allow this traffic in your host firewall, or in case of public/private cloud hosted machines (i.e. AWS or OpenStack), in your security group configuration. Keep in mind that when using a security group as Source or Destination in your security group, that this only applies to the private interface of the nodes/instances.

```
<h3 id="amazonec2-securitygroup-nodedriver">Amazon EC2 security group when using Node Driver</h3>
<p>If you are <a href="/docs/rancher/v2.x/en/cluster-provisioning/rke-clusters/node-pools/ec2/">Creating an Amazon EC2 Cluster</a>, you can choose to let Rancher create a Security Group called <code>rancher-nodes</code>. The following rules are automatically added to this Security Group.
</p>
```

Security group: rancher-nodes

####Inbound rules

<table>        <tbody><tr>            <th>Type</th>            <th>Protocol</th>            <th align="left">Port Range</th>            <th align="left">Source</th>        </tr>            <tr>                <td>SSH</td>                <td>TCP</td>                <td>22</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>HTTP</td>                <td>TCP</td>                <td>80</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>443</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>2376</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>2379-2380</td>                <td>sg-xxx (rancher-nodes)</td>            </tr>            <tr>                <td>Custom UDP Rule</td>                <td>UDP</td>                <td>4789</td>                <td>sg-xxx (rancher-nodes)</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>6443</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>Custom UDP Rule</td>                <td>UDP</td>                <td>8472</td>                <td>sg-xxx (rancher-nodes)</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>10250-10252</td>                <td>sg-xxx (rancher-nodes)</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>10256</td>                <td>sg-xxx (rancher-nodes)</td>            </tr>            <tr>                <td>Custom TCP Rule</td>                <td>TCP</td>                <td>30000-32767</td>                <td>0.0.0.0/0</td>            </tr>            <tr>                <td>Custom UDP Rule</td>                <td>UDP</td>                <td>30000-32767</td>                <td>0.0.0.0/0</td>            </tr>    </tbody></table>

####Outbound rules

<table>        <tbody><tr>            <th>Type</th>            <th>Protocol</th>            <th align="left">Port Range</th>            <th align="left">Destination</th>        </tr>        <tr>        <td>All traffic</td>            <td>All</td>            <td>All</td>            <td>0.0.0.0/0</td>        </tr>    </tbody></table>