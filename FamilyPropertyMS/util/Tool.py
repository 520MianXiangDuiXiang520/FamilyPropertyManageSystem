import datetime

import pytz


def timeout_judgment(field, attr: str, time_line: str):
    """
    判断从数据表中某个时间类型的字段有没有超时，超时返回True
    :param field: extends Model: Model对象
    :param attr: str: 时间类型的字段名
    :param time_line: str: 超时时间，比如表示3小时超时，应设置为（3/h）
    :return: bool
    """
    num, period = time_line.split('/')
    db_time = getattr(field, attr)
    delta = (datetime.datetime.now(tz=pytz.timezone('UTC')).replace(tzinfo=pytz.timezone('UTC'))
             - db_time.replace(tzinfo=pytz.timezone('UTC')))
    return delta.seconds > {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period] * int(num)
