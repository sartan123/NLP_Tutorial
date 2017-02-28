# -*- coding:utf-8 -*-
import math


def cost_entro(test, train):
    word_count = 0
    beta = 0.95
    beta2 = 0.05
    unknown_word = 0
    V = 10000000
    H = 0
    for line in lines:
        line = line.rstrip('\n')
        words = line.split(' ')
        words[0] = '<s>' + words[0]
        words[-1] = words[-1] + '</s>'
        word_count += len(words)
        for word in words:
            P = beta2 / V
            if word in train.keys():
                P += beta * train[word]
            else:
                unknown_word += 1
            H += -(math.log2(P))
    print(H/word_count)
    print((word_count-unknown_word)/word_count)


def create_dic_text(train):
    dic = {}
    for lines in train:
        lines = lines.rstrip('\n')
        lines = lines.split('\t')
        dic[lines[0]] = float(lines[1])
    return dic


train = open('train_pro.txt')
lines = train.readlines()
train_dic = create_dic_text(lines)

test = open('wiki-en-train.word.txt')
lines = test.readlines()
cost_entro(lines, train_dic)
