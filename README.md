<!--
 * @Author: flwfdd
 * @Date: 2022-07-27 16:44:47
 * @LastEditTime: 2023-09-17 16:42:58
 * @Description: 
 * _(:з」∠)_
-->

![p92oJjH.png](https://s1.ax1x.com/2023/05/16/p92oJjH.png)

<div align="center">

<h1 style="color:#FF9A57;text-decoration:underline;text-decoration-color:#00ABD6;">BIT101</h1>

[网站( bit101.cn )](https://bit101.cn) ｜ [API文档](https://bit101-api.apifox.cn)

[Go服务端](https://github.com/BIT101-dev/BIT101-GO) ｜ [Android客户端](https://github.com/BIT101-dev/BIT101-Android)

[了解BIT101](https://bit101-project.feishu.cn/wiki/W8TxwAs7rizGVEkONjAcvgvsnxe) ｜ [加入BIT101](https://bit101-project.feishu.cn/wiki/OY1Xw6y27iNZqgkSDCkc5Cfdnjc)

</div>

---

`BIT101`企划旨在打造一个富于互联网精神的、开放共享的社区，打破校内信息壁垒，使同学们学习生活得更加优雅。现在包括由`Vue3`+`Naïve UI`构建的网站前端（本仓库）、基于`Gin`框架的[Go后端](https://github.com/flwfdd/BIT101-GO)和基于`Jetpack Compose`构建的[Android客户端](https://github.com/BIT101-dev/BIT101-Android)。

如果有`Bug`提交、功能建议或其他任何问题，欢迎提交`issues`、加入交流QQ群[726965926](https://jq.qq.com/?_wv=1027&k=OTttwrzb)或邮件[admin@bit101.cn](mailto:admin@bit101.cn)提出。

也希望你能把`BIT101`告诉更多的同学_(:з」∠)_

🥳`BIT101`期待你的贡献！！

> 注意，本仓库目前仅包含网页前端，后端、客户端代码请移步另外的仓库。`doc`目录下的文档和`backend`目录下的`Python`后端已经废弃。

## 启动！
首先下载或克隆仓库：
```bash
git clone https://github.com/BIT101-dev/BIT101.git
```

然后配置好`pnpm`环境后即可启动：
```bash
cd BIT101 #进入目录
pnpm install #安装依赖
pnpm dev #开发模式
pnpm build #编译
```

## 发行日志

* `2022-08-01`：`version:0.0.1`首次部署，撒花！完成了预想中的功能：用户系统（使用学校统一身份认证和邮箱辅助注册）、文章（校园维基）、课程评教和资料共享、成绩查询。

* `2022-08-14`：`version:0.0.2`1.完善成绩查询，由于挂科重修等规则复杂，添加支持手动选择计入GPA的课程。2.添加可信成绩单查询。3.添加教学大纲查询。

* `2023-05-16`：`version:0.1.0`1.迁移到`GO`后端。2.添加消息系统。3.添加地图。

