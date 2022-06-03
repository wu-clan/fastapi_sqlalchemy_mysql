#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def list_to_tree(data_list, parent_id=0) -> list:
    """
    递归获取树形结构数据

    :param data_list: 数据列表
    :param parent_id: 父级id
    :return:
    """
    tree = []
    for data in data_list:
        if data['parent_id'] == parent_id:
            tree.append(data)
            data['children'] = list_to_tree(data_list, data['id'])
    return tree


def ram_list_to_tree(data_list: list) -> list:
    """
    利用对象内存共享生成树

    :param data_list: 数据列表
    :return:
    """
    res = {}
    for v in data_list:
        res.setdefault(v["id"], v)
    for v in data_list:
        res.setdefault(v["parent_id"], {}).setdefault("children", []).append(v)
    return res[0]["children"]


if __name__ == '__main__':
    test_data = [
        {'id': 1, 'title': 'GGG', 'parent_id': 0},
        {'id': 2, 'title': 'AAA', 'parent_id': 0},
        {'id': 3, 'title': 'BBB', 'parent_id': 1},
        {'id': 4, 'title': 'CCC', 'parent_id': 1},
        {'id': 5, 'title': 'DDD', 'parent_id': 2},
        {'id': 6, 'title': 'EEE', 'parent_id': 3},
        {'id': 7, 'title': 'FFF', 'parent_id': 4},
        {'id': 3, 'title': 'BBB', 'parent_id': 1},
    ]

    print(json.dumps(list_to_tree(test_data), indent=4))

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

    print(json.dumps(ram_list_to_tree(data), indent=4))
