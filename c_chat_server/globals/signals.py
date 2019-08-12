# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/21 17:19
from flask.signals import _signals

after_create = _signals.signal('after_create')
before_create = _signals.signal('before_create')

@before_create.connect
def af(sender,*args,**kwargs):
    """
    :param sender: before_create
    :param args: ()
    :param kwargs: {'model': <Role (transient 1740278212536)>}
    :return:
    """
    ...