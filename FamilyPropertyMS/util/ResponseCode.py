CODE = {
    200: {'code': 200, 'msg': "ok"},
    201: {'code': 201, 'msg': "no data"},
    400: {'code': 400, 'msg': "Bad Request"},  # 请求错误
    401: {'code': 401, 'msg': "Unauthorized"},  # 没有用户凭证
    403: {'code': 403, 'msg': 'Forbidden'},  # 拒绝授权
    418: {'code': 418, 'msg': 'happy new year'},
    429: {'code': 429, 'msg': "Too many request"},
    460: {'code': 460, 'msg': 'Reach the upper limit'},  # 自定义，达到上限
    500: {'code': 500, 'msg': "Internal Server Error"}  # 服务器异常
}