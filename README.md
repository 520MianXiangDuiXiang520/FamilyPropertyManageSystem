# FamilyPropertyManageSystem

## 接口文档

所有需要认证的接口必须通过GET方式传递表示唯一身份认证的`token`字段，该字段由首次注册或登录时返回，`token`在服务器保存并校验，用户15分钟无动作
`token`会被自动删除

### 注册

URL ：http://127.0.0.1:8000/api/v1/user_manage/register/  
method: POST  
认证：无需认证  
请求数据格式：  

```json
{
	"username": "demo",
	"password": "demo",
	"pwdagain": "demo"
}
```

成功响应  

```json
{
	"code": 200,
	"msg": "ok"
}
```

失败响应  

```json
{
	"code": 400,
	"msg": "用户名重复"
}
```
```json
{
	"code": 400,
	"msg": "两次密码不一致"
}
```

### 登录

URL：http://127.0.0.1:8000/api/v1/user_manage/login/  
method：POST  
认证：无需认证  
请求数据  

```json
{
	"username": "name",
	"password": "222"
}
```

成功响应数据  

```json
{
	"code": 200,
	"msg": "ok",
	"token": "82b63e3c-23e6-4a24-ab19-1d5c8c5f0d96"
}
```

失败响应数据  

```json
{
	"code": 400,
	"msg": "Bad Request"
}
```

### 登出

URL：http://127.0.0.1:8000/api/v1/user_manage/logout/  
method：DELETE  
认证：需要认证  
请求数据  

```json
{
	"token": "d5d8354d-646d-4d83-a4d4-4f3d8628eb2b"
}
```

成功响应

```json
{
	"code": 200,
	"msg": "ok"
}
```

失败响应

```json
{
	"code": 400,
	"msg": "登出失败"
}
```

### 用户信息查看与修改

URL：http://127.0.0.1:8000/api/v1/user_manage/user_info/  
认证：需要认证  

#### 用户信息查看

method：GET  
请求格式：null  
成功响应：

```json
{
	"id": 1,
	"username": "junbao",
	"password": "222",
	"telephone": "15364968962",
	"email": "15364968962@163.com",
	"sex": 1,
	"family1": null,
	"family2": null
}
```

失败响应：如果服务器异常可能返回500  

```json
{
	"code": 500,
	"msg": "Internal Server Error"
}
```

#### 用户信息修改

method: PUT  
请求格式：要修改的的数据项作为键，新值作为值传递

```json
{
	"username": "junbao",
	"telephone": "15364968962",
	"email": "15364968962@163.com"
}
```

响应： 成功得到200响应，否则可能抛出500服务器内部异常  

### 用户间通信

URL： http://127.0.0.1:8000/api/v1/message/  
认证： 需要认证

#### 查看个人“邮件”

method: GET  
成功响应：

```json
[
	{
		"id": 1,
		"send_id": "admin",
		"receive_id": "junbao",
		"title": "系统测试",
		"text": "系统测试消息",
		"send_time": "2019-11-16T16:17:52Z",
		"state": 2
	},
    {
        "id": 2,
        "send_id": "admin",
        "receive_id": "junbao",
        "title": "系统测试",
        "text": "系统测试消息",
        "send_time": "2019-11-16T16:17:52Z",
        "state": 2
       }
]
```

失败响应：

#### 删除个人“邮件”

method: DELETE  
请求格式：

```json
{
	"id": "1"
}
```

失败响应： 失败会返回403或400  

#### 修改“邮件”状态

“邮件“有三种状态  
method: PUT

```python
STATE = [(0, '未读'), (1, '星标'), (2, '已读')]
```

请求格式：

```json
{
	"id": "1",
	"state": "2"
}
```

