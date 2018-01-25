#WannaCry 勒索病毒
WannaCry（又名 Wanna Decryptor），是一种“蠕虫式”勒索病毒软件。WannaCry 勒索病毒在全球范围内爆发，至少150个国家、30万名用户收到影响，已造成损失达80亿美元。

WannaCry 利用 Windows 操作系统445端口存在的漏洞进行传播，并具有自我复制、主动传播的特性。被该勒索病毒入侵后，用户主机系统内的照片、图片、文档、音频、视频等几乎所有类型的文件都将被加密，加密文件的后缀名被统一修改为“．WNCRY”，并在桌面弹出勒索对话框，要求受害者支付比特币。

#WannaCry 解密修复工具
阿里云安全团队经过分析研究，找到 WannaCry 加密勒索病毒的解密方式，发布针对 WannaCry 勒索病毒的一键解密和修复工具。
经反复测试验证，该工具可以恢复已被 WannaCry 勒索病毒加密的文件。

##前提条件
感染 WannaCry 勒索病毒后，未重启操作系统。

##适用范围
该工具适用于 Windows 云服务器和本地服务器，支持的操作系统版本包括：Windows Server 2003、Windows Server 2008。

##修复步骤

1. 单击 WannaCry修复工具，将修复工具下载到被感染的 Windows 服务器或 PC 机上。
2. 双击 Wanna-CryDecryt-Tool.exe 文件，运行修复工具。
![WannaCry修复工具](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/57115/cn_zh/1500626786185/4b90fa9f8c8637ca6c423b08eb992d7264841566.png)
3. 单击恢复文件，执行文件恢复功能。
执行时间较长，请耐心等待。
![WannaCry修复工具恢复文件](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/57115/cn_zh/1500626972016/2fa78c92371f6c4067c26186fc7e5f4bcf365680.png)
4. 单击清除病毒。
执行时间较长，请耐心等待。
![WannaCry修复工具清除病毒](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/57115/cn_zh/1500627176088/52bb4c42af69028d24608dd787cd0e40173363e7.png)

注意事项
- 大多数情况下，被加密的文件可以被成功恢复。但可能因内存数据被二次写入，覆盖原有加密状态时的数据，导致数据恢复不成功。解密和修复文件失败，不会对操作系统造成任何影响。

- 阿里云安全团队强烈建议，在感染 WannaCry 勒索病毒后，不要关闭或重启操作系统，也不要手工查杀病毒，建议优先使用该修复工具尝试恢复数据。

- 该修复工具针对 WannaCry 勒索病毒加密方式研发，Windows 系统均可使用。