<!--
 * @Author: flwfdd
 * @Date: 2022-05-29 14:05:31
 * @LastEditTime: 2022-07-14 21:28:45
 * @Description: 
 * _(:з」∠)_
-->
# 序

前端使用`Vue3`+`NaiveUI`+`TypeScript`+`Vite`构建，贯彻落实前后端分离和单页面应用的思想。

后端使用基于`Python`的`Flask`网络框架，辅以`MariaDB`数据库和`Redis`缓存。

此文档主要为了记录相关接口和备忘，方便之后可能的移植和开发。

# 后端API

后端的`API`参考了`RESTful API`设计风格。

后端整体设计是想要满足`Serverless`的，理论上全部移植到函数计算+云数据库应该也是可行的。现阶段还是使用物理机进行部署。

## API整体说明

所有`API`均返回`JSON`格式的数据，同时返回相应的状态码，状态码含义参考`MDN`的[HTTP 响应状态码](https://developer.mozilla.org/zh-CN/docs/web/http/status)。

对于`POST`接口，若无特殊说明，皆需要发送`application/json`，不能直接用`url`（因为前端用`axios`就默认如此）。

对于大部分接口，都会返回一个`msg`参数说明操作的结果（如“登陆成功”、“参数错误”等），前端可以使用状态码判断操作结果，也可以直接对用户展示`msg`内容。简明起见，之后的接口说明中对状态码和`msg`参数都不作特别说明。

**一些状态码说明**：
* `200`：操作成功
* `400`：请求参数错误
* `401`：用户鉴权未通过
* `500`：操作错误

## 用户系统

本来想用`Flask-Login`配合原生`Cookie`实现，但由于`Cookie`复杂的跨域规则，且考虑到前后端分离及域名备案等问题，最终还是自行定义了一个`fake-cookie`头并完成相关验证流程。后端不会接触到用户的明文密码，也不存储任何用户敏感信息，认证部分借助学校邮箱或是学校的统一身份认证系统完成。

在需要身份认证的接口上，都需要在请求标头中携带`fake-cookie`。


### 发送邮件验证码
**接口地址**：`GET /user/mail_verify/`

**参数说明**：
* `sid`：学号

**返回说明**：无


### 统一身份认证验证初始化
**接口地址**：`GET /user/webvpn_verify_init/`

**参数说明**：
* `sid`：可选，学号，用于做是否需要验证码的检查

**返回说明**：
各参数具体含义见[学校统一身份认证登录流程](#学校统一身份认证登录流程)。
```json
{
    "salt":"",
    "execution":"",
    "cookie":"",
    "captcha":false //如果需要验证码则为base64编码的验证码图片
}
```


### 统一身份认证验证
**接口地址**：`POST /user/webvpn_verify/`

**参数说明**：
考虑到`execution`较大，限制只能通过`POST`发送`application/json`，不能直接用`url`
```json
{
    "username":"", //学号
    "password":"", //EncryptPassword.js加密后的统一身份认证密码
    "execution":"", //同初始化中收到的
    "cookie":"", //同初始化中收到的
    "captcha":"" //可选，验证码识别结果
}
```

**返回说明**：
`verify_code`为注册验证码，`cookie`可用于进行`webvpn`相关操作。
```json
{
    "verify_code":"",
    "cookie":""
}
```


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
    "fake_cookie":""
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
    "fake_cookie":""
}
```

### 获取用户信息
**接口地址**：`GET /user/info/`

**参数说明**：
可以不携带`fake-cookie`
* `id`：可选，用户id，传入`0`或不传则返回当前`fake-cookie`用户的信息。

**返回说明**：
```json
{
    "id": 1, //用户编号
    "sid": "", //学号
    "avatar": "", //头像URL
    "motto": "I offer you the BITterness of a man who has looked long and long at the lonely moon.", //格言简介
    "nickname": "BIT101-77ff33f3", //昵称
    "register_time": "Mon, 30 May 2022 02:34:36 GMT" //注册时间
}
```

### 修改用户信息
**接口地址**：`POST /user/info/`

**参数说明**：
需要携带`fake-cookie`
* `nickname`：昵称
* `motto`：格言/简介
* `avatar`：头像`url`（需要先用[图床接口](#上传图片)上传后获取）

**返回说明**：
无


## 文件和图床

关于图床，后端会计算图片的`MD5`，将其视为图片的`id`。尽管现在已经有了较为成熟的碰撞算法，但考虑到`MD5`在自然状态下碰撞概率很低，图片也并不是什么敏感的重要数据，就暂时没有做防碰撞。

### 上传图片
**接口地址**：`POST /upload/image/`

**参数说明**：
有两种不同的调用方式。
1. 发送一个`multipart/form-data;`表单，文件在`file`字段下。
2. 发送`application/json`，有一个`url`参数为图片链接，服务器会下载该图片并保存。

**返回说明**：
```json
{
    "url":"" //图片的url
}
```

## 文章模块

### 获取文章
可以不携带`fake-cookie`
**接口地址**：`GET /paper/`

**参数说明**：
* `id`：文章`id`

**返回说明**：
```json
{
    "id":1,
    "title":"俺是标题！",
    "intro":"简介",
    "data":"{}", //字符串化的editor.js数据
    "create_time":"Sun, 10 Jul 2022 21:58:41 GMT",
    "update_time":"Sun, 10 Jul 2022 22:15:08 GMT",
    "user":1, //发表者 匿名为-1
    "like_num":1,
    "comment_num":1,
    "like":true, // 当前用户的点赞状态
}
```


### 发表文章
**接口地址**：`POST /paper/`

**参数说明**：
需要携带`fake_cookie`
* `id`：文章`id`，为`0`则为新建文章。
* `title`：标题
* `intro`：简介
* `data`：文章内容，使用`editor.js`
* `last_time`：文章开始编辑之前的`UNIX`时间戳，用于防撞车
* `now_time`：文章最后编辑的`UNIX`时间戳
* `anonymous`：是否匿名，为`1`匿名

**返回说明**：
```json
{
    "id":"" //文章id
}
```


## 交互反馈模块

包括点赞、评论等。由于各种东西的点赞、评论都是类似的，所以就可复用，统一使用，而操作的对象使用`obj`进行标识，以下是`obj`的不同种类，`obj`由类型标识符+对应`id`组成，如`1`号文章的`obj`为`paper1`。

* `paper`


### 点赞
**接口地址**：`POST /reaction/like/`

**参数说明**：
需要携带`fake_cookie`
* `obj`：操作对象的标识字符串

**返回说明**：
```json
{
    "like":true, //操作后的点赞状态
    "like_num":1, //操作后的点赞数
}
```

## webvpn相关

### 成绩查询
**接口地址**：`GET /score/`

后端通过`webvpn`调用相关接口获取成绩，可以在前端计算均分绩点等。详细成绩需要批量请求可能速度较慢，尽量不要调用。

**参数说明**：
* `cookie`：`webvpn`的`cookie`，获取见[统一身份认证验证](#统一身份认证验证)
* `detail`：可选，不为空则查询详细信息

**返回说明**：
```json
{
    "data":[] //二维表格，第一行为表头，之后每行为一条成绩信息
}
```

# webvpn

`webvpn`是从外网访问学校内网的转发系统，通过分析调用`webvpn`即可实现对学校接口的操作。有一位学长做过一个非常好用的[转换工具](https://webvpn.vercel.app/)。

## webvpn网址备份

[登录](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue)

[登录是否需要验证码](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/checkNeedCaptcha.htl?username=2333)

[获取登录验证码](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/getCaptcha.htl)

[学生信息页面前序验证](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=4585275700341858&appName=jbxxapp)

[学生信息页面](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/*default/index.do)

[基本信息API](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/modules/infoStudent/getStuBatchInfo.do)

## 学校统一身份认证登录流程

首先访问登录页面，获取头中的`Set-Cookie`、页面中的`pwdEncryptSalt`和对应的`execution`，几次密码错误后需要获取验证码，保证`Cookie`为同一个即可。然后在前端将明文密码和`pwdEncryptSalt`传入`EncryptPassword.js`计算出加密后的密码，再将`Cookie`、加密后的密码、`execution`、验证码（如果需要的话）通过`POST`发送到登陆页面，然后会经历一大堆乱七八糟的`302`重定向，坑的是`requests`库默认重定向是不携带`Cookie`的，所以需要手动处理。之后访问每一个`webvpn`的子模块或多或少都需要前序验证，其实就是访问一个页面然后经历一大堆重定向，具体干了啥俺也晓不得(＠_＠;)。

另外，`webvpn`的过期机制至今仍未探明，现在只能是用到相关服务的时候都重新走流程登录一遍。


# 前端

由于前端比较杂乱无章，但是可以直接看到效果，所以文档基本掠过。

## 主题色

色相为`24`，主色为<span style="color:#FF8533;">#FF8533</span>，配色为<span style="color:#FF9A57;">#FF9A57</span>以及<span style="color:#CC5200;">#CC5200</span>。