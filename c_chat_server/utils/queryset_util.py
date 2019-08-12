# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/20 10:18
from collections import Iterable

from sqlalchemy import text
from flask_sqlalchemy.model import Model

from c_chat_server.extensions import db


def sort_queryset(model:Model,sort_list:Iterable,sort_field:str = 'id') -> list:
    """
    自定义排序
    :param model:模型类
    :param sort_list: 预先要组成的顺序列表
    :param sort_field: 默认排序依据字段
    :return: 已经排好序的List
    """
    assert isinstance(sort_field,Iterable),(
        f'传入的sort_list,{sort_list},不是一个可迭代对象'
    )
    assert hasattr(model,sort_field),(
        f'`{model}`模型类没有`{sort_field}`属性!'
    )

    sku_ids = ','.join([str(i) for i in sort_list])
    field_sql = f"FIELD(`{sort_field}`,{sku_ids}) as field_sql"

    model_attr=getattr(model,sort_field)
    query=db.session.query(model, field_sql).filter(model_attr.in_(sort_list)).order_by(
        text('field_sql')).all()
    return [i[0] for i in query]


def model_to_dict(result:Model) -> dict:
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), str(res.__dict__.values()))) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')