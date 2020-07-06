# -*- coding:utf-8 -*-
from simhash import Simhash
import re


def filter_html(html):
    """
    :param html: html
    :return: 返回去掉html的纯净文本
    """
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', html).strip()
    return dd


# 求两篇文章相似度
def simhash_similarity(text1, text2):
    """
    :param tex1: 文本1
    :param text2: 文本2
    :return: 返回两篇文章的相似度
    """
    aa_simhash = Simhash(text1)
    bb_simhash = Simhash(text2)
    print(1,bin(aa_simhash.value))
    print(2, bin(aa_simhash.value))
    max_hashbit = max(len(bin(aa_simhash.value)), (len(bin(bb_simhash.value))))

    print(max_hashbit)

    # 汉明距离
    distince = aa_simhash.distance(bb_simhash)
    print(distince)

    similar = 1 - distince / max_hashbit

    return similar


if __name__ == '__main__':
    text1 = "simhash算法的主要思想是降维，将高维的特征向量映射成一个低维的特征向量，通过两个向量的Hamming Distance来确定文章是否重复或者高度近似。"

    text2 = "simhash算法的主要思想是降维，将高维的特征向量映射成一个低维的特征向量，通过两个向量的Hamming Distance来确定文章是否重复或者高度近似。"

    similar = simhash_similarity(text1, text2)
    print(similar)