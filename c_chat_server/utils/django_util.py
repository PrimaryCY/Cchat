# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/8 10:14
from importlib import import_module
from collections import Iterable




def import_string(dotted_path:str) -> object:
    """
    给出字符串路径,加载该模块
    :param dotted_path: 字符串路径
    :return: 模块
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path}:不是一个module路径" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(f'Module {module_path} 没有找到 {class_name} 属性/类' ) \
            from err




