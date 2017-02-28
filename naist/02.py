# -*- coding:utf-8 -*-


def ngram(train, n):
    train_dic = {}
    context_counts = {}
    count = 0
    for line in train:
        line = line.rstrip('\n')
        words = line.split(' ')
        words.insert(0, '<s>')
        words.append('</s>')
        for i in range(len(words)):
            bi = []
            count += 1
            if i < len(words)-n:
                bi = words[i:i+n]
            else:
                bi = words[i]
            context = " ".join(bi[0:n-1])
            if context in context_counts.keys():
                context_counts[context] += 1
            else:
                context_counts[context] = 1
            bi = " ".join(bi)
            if bi in train_dic.keys():
                train_dic[bi] += 1
            else:
                train_dic[bi] = 1
    for k, v in context_counts.items():
        print(k, v/context_counts[k])
    for k, v in train_dic.items():
        word = k.split(' ')
        word = " ".join(word[:n-1])
        train_dic[k] = v
        train_dic[k] = v/context_counts[word]
    return train_dic

file = open('wiki-en-train.word.txt')
# file2 = open('02_train.txt', 'a')
train = file.readlines()
train_dic = ngram(train, 2)
# for k, v in train_dic.items():
#    print(k+'\t'+str(v), file=file2)
