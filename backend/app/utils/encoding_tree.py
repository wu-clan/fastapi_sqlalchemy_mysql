#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def to_tree(data, root, root_field, node_field):
    """
    解析list数据为树结构
    :param data: 被解析的数据
    :param root: 根节点值
    :param root_field: 根节点字段
    :param node_field: 节点字段
    :return: list
    """
    l = []
    for i in data:
        if i.get(root_field) == root:
            l.append(i)

    # i的内存ID 是一样的 所以不需要对list进行修改
    for i in data:
        node = i.get(node_field)
        children = []
        for j in data:
            parent = j.get(root_field)
            if node == parent:
                children.append(j)

        if children:
            i['children'] = children

    return l


def to_disorder_tree(data: list):
    """
       利用对象内存共享生成无序树
       :param data:
       :return:
       """
    res = {}
    for v in data:
        res.setdefault(v["id"], v)
    for v in data:
        res.setdefault(v["parent_id"], {}).setdefault("children", []).append(v)
    return res[0]["children"]


if __name__ == '__main__':
    test_data = [
        {'id': 1, 'title': 'GGG', 'parent_id': 0},
        {'id': 2, 'title': 'AAA', 'parent_id': 0},
        {'id': 4, 'title': 'CCC', 'parent_id': 1},
        {'id': 5, 'title': 'DDD', 'parent_id': 2},
        {'id': 6, 'title': 'EEE', 'parent_id': 3},
        {'id': 7, 'title': 'FFF', 'parent_id': 4},
        {'id': 3, 'title': 'BBB', 'parent_id': 1},
    ]
    print(json.dumps(to_tree(test_data, 0, 'parent_id', 'id'), indent=4))

    data = [
        {'id': 10, 'parent_id': 8, 'name': "ACAB"},
        {'id': 9, 'parent_id': 8, 'name': "ACAA"},
        {'id': 8, 'parent_id': 7, 'name': "ACA"},
        {'id': 7, 'parent_id': 1, 'name': "AC"},
        {'id': 6, 'parent_id': 3, 'name': "ABC"},
        {'id': 5, 'parent_id': 3, 'name': "ABB"},
        {'id': 4, 'parent_id': 3, 'name': "ABA"},
        {'id': 3, 'parent_id': 1, 'name': "AB"},
        {'id': 2, 'parent_id': 0, 'name': "AA"},
        {'id': 1, 'parent_id': 0, 'name': "A"},
    ]

    print(json.dumps(to_disorder_tree(data), indent=4))
