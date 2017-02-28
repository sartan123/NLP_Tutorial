# -*- coding:utf-8 -*-
import math


def before_step(train, train_dic):
    count = 1
    for line in train:
        best_edge = []
        best_score = []
        best_edge.append('NULL')
        best_score.append(0)
        for end in range(1, len(line)):
            best_score.append(10**10)
            for begin in range(end):
                word = line[begin:end]
                # print(word)
                if (word in train_dic.keys()) or len(word) == 1:
                    prob = train_dic[word]
                    my_score = best_score[begin] + -math.log2(prob)
                    if my_score < best_score[end]:
                        best_score[end] = my_score
                        best_edge.append([begin, end])
        words = []
        next_edge = best_edge[len(best_edge)-1]
        while next_edge != 'NULL':
            word = line[next_edge[0]:next_edge[1]]
            words.append(word)
            next_edge = best_edge[next_edge[0]]
        text = ' '.join(words[::-1])
        print(text)
        print(text, file=file)


def load_model(model):
    dic = {}
    for line in model:
        line = line.rstrip('\n')
        word = line.split('\t')
        try:
            dic[word[0]] = float(word[1])
        except:
            pass
    return dic


def n_gram(train, n):
    dic = {}
    count = 0
    for line in train:
        line = line.rstrip('\n')
        for i in range(len(line)):
            word = line[i:i+n]
            count += 1
            if word in dic.keys():
                dic[word] += 1
            else:
                dic[word] = 1
    for k, v in dic.items():
        dic[k] = v / count
        print(k + '\t' + str(v / count), file=outfile)
    return dic


if __name__ == '__main__':
    infile = open('wiki-ja-test.txt')
    infile = infile.readlines()
    """
    outfile = open('03_train.txt', 'w')
    for i in range(1, 4):
        n_gram(infile, i)
    """
    file = open('03_output.txt', 'w')
    outfile = open('03_train.txt')
    model = outfile.readlines()
    model_dic = load_model(model)
    before_step(infile, model_dic)
