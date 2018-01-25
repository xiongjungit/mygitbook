本文介绍了阿里云账号管理方面的最佳安全实践，主要从密钥（AccessKey，简称 AK）管理和访问控制（RAM）两方面提供相关实践建议。

#AccessKey 泄露处置指南

AccessKey 是阿里云颁发给用户的一种身份凭证，用于在 API 调用进行身份验证。AccessKey 相当于获取用户云资源的钥匙，一旦泄露，将带来云资源泄露以及被恶意利用等风险。建议您定期自查内部 AccessKey 是否存在泄漏。

如您发现包含 AccessKey 的敏感信息已在公网泄露，请尽快删除已泄露的代码或信息，并登录到阿里云控制台上禁用或删除 AccessKey。操作步骤如下：

1. 登录到 [阿里云控制台](https://home.console.aliyun.com/?spm=5176.7756346.2.3.vNGUp7)，并在屏幕右上角 用户菜单 下单击 accesskeys。

2. 在 AccessKey 管理 页面，单击被泄露 AccessKey 操作 列表下的 禁用 或 删除。

#云账号安全实践

- 尽量不要使用 Github 类代码托管服务。特殊情况下，一定要使用的话，建议您自建私有仓库，或搭建企业内部代码托管系统，以防敏感信息泄露，确保代码安全。

- 采用云上安全产品进行预警、检测，如阿里云提供的免费版云盾 [态势感知](https://www.aliyun.com/product/sas?spm=5176.7756346.2.4.vNGUp7)。态势感知能够检测到您系统账号的安全漏洞，您可登录到云盾控制台免费开通该服务，并开启自动检测功能。

- 启用阿里云权限管理机制，包括 [访问控制](https://help.aliyun.com/document_detail/28636.html?spm=5176.7756346.2.5.vNGUp7)（Resource AccessManagement，简称 RAM）和 安全凭证管理（SecurityToken Service，简称 STS。根据需求使用不同权限的子账号来访问云资源（如 OSS），或为用户提供访问的临时授权。

- 遵循 [RAM 最佳实践](https://help.aliyun.com/document_detail/28642.html?spm=5176.7756346.2.7.vNGUp7)，从登录验证、账号授权、权限分配等方面配置 RAM，有效地使用 RAM 进行用户身份管理和资源访问控制。主要的访问控制策略包括：

	- 为主账号和 RAM 用户启用 MFA
	- 为用户登录配置强密码策略
	- 定期轮转用户登录密码和访问密钥
	- 遵循最小授权原则
	- 使用策略限制条件
	- 及时撤销用户不再需要的权限
	- 不要为主账号创建访问密钥
	- 使用群组给 RAM 用户分配权限
	- 将用户管理、权限管理与资源管理分离
	- 将控制台用户与 API 用户分离
	

- 遵循 OSS 安全实践，包括：

	- 不使用主账号访问 OSS
	- 读写分离
	- Bucket 权限隔离
	- 使用 STS 的临时凭证来访问 OSS


具体请参考 阿里云 OSS Android SDK 开发文档。

在企业内建立安全制度，开展必要的安全意识培训等工作，提升全员安全意识。

#更多信息
- [安全上云实践](https://yq.aliyun.com/articles/55947?spm=5176.7756346.2.9.vNGUp7)
- [阿里云访问控制 RAM](https://help.aliyun.com/document_detail/28627.html?spm=5176.7756346.2.10.vNGUp7)
- [阿里云 OSS 权限管理](https://help.aliyun.com/document_detail/31929.html?spm=5176.7756346.2.11.vNGUp7)
- [阿里云 OSS Android SDK](https://help.aliyun.com/document_detail/32044.html?spm=5176.7756346.2.12.vNGUp7)