<!--
 * @Author: flwfdd
 * @Date: 2022-03-10 17:24:45
 * @LastEditTime: 2022-03-10 19:14:05
 * @Description: 
 * _(:з」∠)_
-->
# 序

后端框架使用了基于`Python`的`Flask`，数据库使用`MariaDB`，缓存使用`Redis`。

入口程序为`app.py`，配置在`config.py`中。

# 用户系统

本来想用`Flask-Login`，但由于`Cookie`复杂的跨域规则，且需要前后端分离及域名备案问题，最终还是自行定义了一个`Fake-Cookie`头并完成相关验证流程。后端不会接触到用户的密码，也不存储任何用户敏感信息，认证部分完全借助学校的统一身份认证系统完成，后续使用`Fake-Cookie`完成校验。


## 学校登录流程

首先访问登录页面，获取头中的`Set-Cookie`、页面中的`pwdEncryptSalt`和对应的`execution`，然后在前端将明文密码和`pwdEncryptSalt`传入`EncryptPassword.js`计算出加密后的密码，再将`Cookie`、加密后的密码和`execution`通过`POST`发送到登陆页面，然后会经历一大堆乱七八糟的`302`重定向，坑的是`requests`库默认重定向是不携带`Cookie`的，所以需要手动处理。之后访问每一个`webvpn`的子模块或多或少都需要前序验证，其实就是访问一个页面然后经历一大堆重定向，具体干了啥俺也晓不得(＠_＠;)。

另外，`webvpn`的过期机制至今仍未探明，现在只能是用到相关服务的时候都重新走流程登录一遍。

## webvpn网址备份

[登录](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue)

[学生信息页面前序验证](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=4585275700341858&appName=jbxxapp)

[学生信息页面](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/*default/index.do)

[基本信息API](https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/modules/infoStudent/getStuBatchInfo.do)