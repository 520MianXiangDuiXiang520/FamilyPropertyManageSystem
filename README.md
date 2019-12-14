# FamilyPropertyManageSystem

家庭财产管理系统  

要求功能：

|  |  |
|---|--|
||（1）用户登录模块|  
||（2）收支管理|
||（3）银行储蓄管理|
||（4）借还钱管理|
||（5） 生成资产报告|

依赖

```txt
Django==2.2.2
djangorestframework==3.9.4
PyMySQL==0.9.3
pytz==2019.1
sqlparse==0.3.0
django-cors-headers==3.2.0
```


## 接口文档

所有需要认证的接口必须通过GET方式传递表示唯一身份认证的`token`字段，该字段由首次注册或登录时返回，`token`在服务器保存并校验，用户15分钟无动作
`token`会被自动删除 认证失败将会返回

```json
{
	"detail": "认证失败(no token)"
}
```

响应状态码：

[标准浏览器状态码](#https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)  

```py
CODE = {
    200: {'code': 200, 'msg': "ok"},
    400: {'code': 400, 'msg': "Bad Request"},  # 请求错误
    401: {'code': 401, 'msg': "Unauthorized"},  # 没有用户凭证
    403: {'code': 403, 'msg': 'Forbidden'},  # 拒绝授权
    418: {'code': 418, 'msg': 'happy new year'},
    429: {'code': 429, 'msg': "Too many request"},
    460: {'code': 460, 'msg': 'Reach the upper limit'},  # 自定义，达到上限
    500: {'code': 500, 'msg': "Internal Server Error"}  # 服务器异常
}
```

### 注册

|URL|http://127.0.0.1:8000/api/v1/user_manage/register/  |
|-|-|
|method| POST|  
|认证|无需认证|

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
	"id": 3,
	"username": "家长",
	"telephone": "",
	"email": "jiazhang@163.com",
	"sex": "jiazhang@163.com",
	"family1": {
		"id": 2,
		"family_name": "newfamily",
		"family_member": {
			"parent1": "家长",
			"members3": "用户3",
			"members4": "用户2"
		}
	}
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
	"id": 3,
	"username": "家长",
	"telephone": "",
	"email": "jiazhang@163.com",
	"sex": "jiazhang@163.com",
	"family1": {
		"id": 2,
		"family_name": "newfamily",
		"family_member": {
			"parent1": "家长",
			"members3": "用户3",
			"members4": "用户2"
		}
	}
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

### 家庭管理

每个用户只能对应一个家庭，可以没有家庭，一个家庭最多8位成员（包括两位家长）

#### 创建家庭

|URL|127.0.0.1:8000/api/v1/family/familyManage/|
|---|--|
|method|POST|
|认证|需要认证|
|权限|无|

请求格式：

```json
{
	"family_name": "newfamily"
}
```

成功响应：`200,ok`  

失败响应：

如果用户已经有对应的家庭了

```json
{
	"code": 460,
	"msg": "Reach the upper limit"
}
```

请求数据错误可能返回400，服务器内部错误可能返回500


#### 查看家庭信息

|URL|127.0.0.1:8000/api/v1/family/familyManage/|
|---|---|
|method|GET|
|认证|需要认证|
|权限|无|


成功返回示例：

如果用户并没有加入家庭

```json
{
	"code": 200,
	"msg": "ok",
	"family": "null"
}
```

如果用户加入了家庭

```json
{
	"code": 200,
	"msg": "ok",
	"token": "949a6236-c8a3-4fdd-8ea8-2ac24b77776d",
	"id": 2,
	"family_name": "newfamily",
	"family_member": {
		"parent1": "家长",
		"members3": "用户3",
		"members4": "用户2"
	}
}
```

错误返回：

如果用户已经加入过家庭，将会返回**460**  
如果申请表中不存在该用户申请的记录，返回**418**

#### 用户申请加入家庭

>在用户管理（userManage）app 下

|URL|http://127.0.0.1:8000/api/v1/user_manage/about_family/|
|---|--|
|method|POST|
|认证|需要认证|
|权限|无|

请求格式：

```json
{
	"family_id": "1"
}
```

响应

成功响应**200**
如果已经加入了家庭，响应**460**  
请求数据错误响应**400**


#### 家长审核用户加入家庭的请求

|URL|http://127.0.0.1:8000/api/v1/family/familyMember/|
|---|--|
|method|PUT|
|认证|需要认证|
|权限|家长权限|

请求格式

```json
{
	"parent_id": "2",
	"user_id": "5",
	"is_agree": "0"
}
```

`is_agree` 0代表同意， 1代表不同意

#### 用户退出家庭

TODO：

#### 家长位置转让

### 账单管理

#### 收入管理

1. 查看收入账单

|url|http://127.0.0.1:8000/api/v1/bill/Income/|
|---|---|
|method|GET|
|认证|需要认证|
|权限|无|

响应示例

```json
[
	{
		"id": 1,
		"remarks": "yyy",
		"money": 111,
		"time": "2019-12-13 21:42:22",
		"username": "***",
		"bill_type": "收入"
	},
	{
		"id": 2,
		"remarks": "dfgf",
		"money": 333,
		"time": "2019-12-19 21:42:35",
		"username": "***",
		"bill_type": "收入"
	},
]
```

2. 新增收入

|url|http://127.0.0.1:8000/api/v1/bill/Income/|
|---|---|
|method|POST|
|认证|需要认证|
|权限|无|

请求数据格式

```json
{
	"money": "510",
	"remarks": "学习2",
	"time": "2019-10-1 12:12:12"
}
```

响应示例：

同查询

