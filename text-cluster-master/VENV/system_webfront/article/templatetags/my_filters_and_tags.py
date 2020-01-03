from django import template

register = template.Library()


@register.filter(name='toArray')
def toArray(value):
    """将输出强制转换为字符串 arg """
    array = value.split(',')
    return array


@register.filter(name='halfArray')
def halfArray(value):
    """将一个数组分为两部分"""
    next_array = []
    index = int(len(value) / 2)
    for j in range(index, len(value)):
        next_array.append(value[j])
    return next_array


@register.filter(name='frontArray')
def frontArray(value):
    """将一个数组分为两部分"""
    next_array = []
    index = int(len(value) / 2)
    for j in range(0, index):
        next_array.append(value[j])
    return next_array