# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/28 23:17
from wtforms.validators import StopValidation


class Optional(object):
    """
    Allows empty input and stops the validation chain from continuing.

    If input is empty, also removes prior errors (such as processing errors)
    from the field.

    :param strip_whitespace:
        If True (the default) also stop the validation chain on input which
        consists of only whitespace.
    """
    field_flags = ('optional', )

    def __init__(self, strip_whitespace=True):
        if strip_whitespace:
            self.string_check = lambda s: s.strip()
        else:
            self.string_check = lambda s: s

    def __call__(self, form, field):
        if not field.data:
            field.errors[:] = []
            raise StopValidation()
