#-*- coding: utf-8 -*-
import pprint
import datetime
import json

def p(obj):
    """ 打印对象

    Args:
        obj: 任何类型的对象

    Returns:
        字符串
    """
    return pprint.pformat(obj)

def returnJson(success, message='', data={}):
    """HTTP标准返回格式

    Args:
        success: bool类型, 操作是否成功
        message: str类型, 错误信息
        data: dict类型, 返回数据

    Returns: 
        JSON格式的字符串, 用于HTTP接口
    """
    return json.dumps({
      'success' : success,
      'message' : message,
      'data' : data,
    })
