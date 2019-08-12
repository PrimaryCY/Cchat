# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 23:33
import os
import uuid
import time
import itertools
import datetime
from collections import Iterable, Mapping

from xpinyin import Pinyin

pin=Pinyin()

def getFlatten(arr:Iterable)->Iterable:
    """
    获取扁平数组的第一个数组
    :param arr:
    :return:
    """
    arr=list(itertools.chain(*arr))
    return arr[0] if len(arr) else None


def random_filename(filename:str)->str:
    """
    随机文件名
    :param filename: 原始文件名称
    :return: uuid之后的新文件名称
    """
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def get_day_zero_time() ->tuple:
    """
    获取到今日凌晨的秒数
    :return: 当前时间到今日凌晨所剩的秒数
    """
    now=datetime.datetime.now()
    date_zero = datetime.datetime.now().replace(year=now.year, month=now.month,
                                            day=now.day, hour=23, minute=59, second=59)
    date_zero_time = time.mktime(date_zero.timetuple())
    return now.strftime('%Y-%m-%d'),round(date_zero_time-time.time())


def sort_pinyin(queryset:Iterable)->dict:
    """
    根据用户名称的首字母进行分类
    :param queryset:
    :return: 返回字典{'a':[],'b':[]}
    """
    dic={}
    for i in queryset:
        user_dict=i[0].to_dict()
        userCheck=i[1].to_dict()
        pinyin = pin.get_pinyin(userCheck['remark'])[0]  # 以备注作为分组
        dic.setdefault(pinyin,[])
        user_dict['is_friend'] = True
        user_dict['pinyin']=pinyin
        user_dict['user']=userCheck
        dic[pinyin].append(user_dict)
    return dict(sorted(dic.items(),key=lambda x:x[0]))



if __name__ == '__main__':
    now=datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
