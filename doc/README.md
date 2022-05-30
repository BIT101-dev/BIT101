<!--
 * @Author: flwfdd
 * @Date: 2022-05-29 14:05:31
 * @LastEditTime: 2022-05-30 15:16:31
 * @Description: 
 * _(:з」∠)_
-->
# BITself

前端使用`Vue3`+`NaiveUI`(+`TypeScript`+`Vite`)构建，应用了前后端分离和单页面应用的思想。

后端使用基于`Python`的`Flask`网络框架，辅以`MariaDB`数据库和`Redis`缓存。

此文档主要为了记录相关`API`，方便之后可能的移植和开发。

# 后端API

后端的`API`接口参考了`RESTful API`设计风格。

后端整体设计是想要满足`Serverless`的，理论上全部移植到函数计算+云数据库应该也是可行的。现阶段还是使用物理机进行部署。

## API整体说明

所有`API`均返回`JSON`格式的数据，同时返回相应的状态码，状态码含义参考`MDN`的[HTTP 响应状态码](https://developer.mozilla.org/zh-CN/docs/web/http/status)。

对于大部分接口，都会返回一个`msg`参数说明操作的结果（如“登陆成功”、“参数错误”等），客户端可以使用状态码判断操作结果，也可以直接对用户展示`msg`内容。简明起见，之后的接口说明中对状态码和`msg`参数都不作特别说明。

**一些状态码说明**：
* `200`：操作成功
* `400`：请求参数错误
* `401`：用户鉴权未通过
* `500`：操作错误

## 用户系统

本来想用`Flask-Login`配合原生`Cookie`实现，但由于`Cookie`复杂的跨域规则，且考虑到前后端分离及域名备案等问题，最终还是自行定义了一个`fake-cookie`头并完成相关验证流程。后端不会接触到用户的明文密码，也不存储任何用户敏感信息，认证部分借助学校邮箱或是学校的统一身份认证系统完成。

总之，在需要身份认证的接口上，都需要在请求标头中携带`fake-cookie`。


### 发送邮件验证码
**接口地址**：`GET /user/mail_verify/`

**参数说明**：
* `sid`：学号

**返回说明**：无


### 注册/重置密码
注册时，要先通过邮箱或统一身份认证获取验证码，然后携带验证码即可完成注册。重置密码也同理，后端检测到已经存在学号会用新密码替换旧密码。

**接口地址**：`GET /user/register/`

**参数说明**：
* `sid`：学号
* `password`：`MD5`加密（32位小写）后的密码
* `verify_code`：验证码

**返回说明**：
```json
{
    "fake_cookie":"db80dfda-c2d7-480f-ae90-c201ee2ede1b"
}
```


### 登录
**接口地址**：`GET /user/login/`

**参数说明**：
* `sid`：学号
* `password`：`MD5`加密（32位小写）后的密码

**返回说明**：
```json
{
    "fake_cookie":"db80dfda-c2d7-480f-ae90-c201ee2ede1b"
}
```

# webvpn

`webvpn`是从外网访问学校内网的转发系统，通过分析调用`webvpn`即可实现对学校接口的操作。有一个学长做过一个非常好用的[转换工具](https://webvpn.vercel.app/)。

## webvpn网址备份

[登录](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue)

[学生信息页面前序验证](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=4585275700341858&appName=jbxxapp)

[学生信息页面](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/*default/index.do)

[基本信息API](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/modules/infoStudent/getStuBatchInfo.do)

## 学校统一身份认证登录流程

首先访问登录页面，获取头中的`Set-Cookie`、页面中的`pwdEncryptSalt`和对应的`execution`，然后在前端将明文密码和`pwdEncryptSalt`传入`EncryptPassword.js`计算出加密后的密码，再将`Cookie`、加密后的密码和`execution`通过`POST`发送到登陆页面，然后会经历一大堆乱七八糟的`302`重定向，坑的是`requests`库默认重定向是不携带`Cookie`的，所以需要手动处理。之后访问每一个`webvpn`的子模块或多或少都需要前序验证，其实就是访问一个页面然后经历一大堆重定向，具体干了啥俺也晓不得(＠_＠;)。

另外，`webvpn`的过期机制至今仍未探明，现在只能是用到相关服务的时候都重新走流程登录一遍。


# 前端

由于前端比较杂乱无章，但是可以直接看到效果，所以文档基本掠过。

## 主题色

色相为`24`，主色为<span style="color:#FF8533;">#FF8533</span>，配色为<span style="color:#FF9A57;">#FF9A57</span>以及<span style="color:#CC5200;">#CC5200</span>。