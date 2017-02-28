import re
import numpy as np


def word_vector(text):
    count = 0
    dic = {}
    label = np.zeros(len(text))
    for line in text:
        line = line.split('\t')
        line = line[1]
        words = line.split(' ')
        for word in words:
            word = word.lower()
            if word not in dic.keys() and re.match(r'^[a-zA-Z]+$', word):
                dic[word] = count
                count += 1
    return dic


def create_vec(text, ids):
    word_vec = np.zeros([len(text), len(ids)])
    label = np.zeros(len(text))
    for i, line in enumerate(text):
        line = line.split('\t')
        label[i] = int(line[0])
        line = line[1]
        words = line.split(' ')
        for word in words:
            if re.match(r'^[a-zA-Z]+$', word):
                word = word.lower()
                try:
                    word_vec[i][ids[word]] += 1
                except:
                    pass
    return word_vec, label


def predict_one(weigths, x):
    score = np.dot(weigths, x)
    return 1 if score >= 0 else -1


def update_weights(weights, x, y):
    """
    c = 0.0001
    weights[abs(weights) <= c] = 0
    weights[weights > 0] -= c
    weights[weights < 0] += c
    """
    weights += x * y * 0.01
    return weights


def create_weights(weights, w_vec, label):
    eta = 0.1
    beta = 1.0
    epoch = 20
    for i in range(epoch):
        print(i)
        for x, y in zip(w_vec, label):
            # ロジスティック回帰
            # predict = np.dot(x, np.exp(np.dot(weights, x)) /
            #                 (1 + np.exp(np.dot(weights, x))**2))*y
            # weights += eta * predict
            # サポートベクターマシン
            val = np.dot(weights, x) * y
            if val <= 0.6:
                weights = update_weights(weights, x, y)
            # パーセプトロン
            # y1 = predict_one(weights, x)
            # if int(y) != int(y1):
            #    weights = update_weights(weights, x, y)
        eta *= 0.9
    return weights


def predcit_test(model, test_data, test_label):
    count = 0
    pred = 0
    for x, y in zip(test_data, test_label):
        count += 1
        y1 = predict_one(model, x)
        if int(y) == int(y1):
            pred += 1
    return pred / count

train_file = open('titles-en-train.labeled')
train_corpus = train_file.readlines()
test_file = open('titles-en-test.word')
test_corpus = test_file.readlines()

ids = word_vector(train_corpus)
train_data, train_label = create_vec(train_corpus, ids)
test_data, test_label = create_vec(test_corpus, ids)
weights = np.random.randn(len(train_data[0]))
model = create_weights(weights, train_data, train_label)
metrics = predcit_test(model, test_data, test_label)
print('精度:', end="")
print(metrics)
