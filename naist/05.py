import numpy as np


def predict_all(model, input_test):
    predict_count = 0
    count = 0
    for line in input_test:
        count += 1
        phi, y1 = create_features(line)
        y2 = predict_one(w, phi)
        if y1 == y2:
            predict_count += 1
    print(predict_count / count)


def predict_one(w, phi):
    score = 0
    for name, value in phi.items():
        if name in w.keys():
            score += value * w[name]
    if score >= 0:
        return 1
    else:
        return -1


def create_features(input_text):
    phi = {}
    line = input_text.rstrip('\n')
    text = line.split('\t')
    words = text[1].split(' ')
    y = text[0]
    for word in words:
        if word in phi.keys():
            phi[word] += 1
        else:
            phi[word] = 1
    return phi, int(y)


def create_w(w, train_data):
    for line in train_data:
        phi, y = create_features(line)
        val = calculate_val(w, phi, y)
        if val <= 0:
            w = update_weights(w, phi, y)
        # yr = predict_one(w, phi)
        # if yr != y:
        #    w = update_weights2(w, phi, y)
    return w


def calculate_val(w, phi, y):
    val = 0
    for name, value in phi.items():
        val += w[name]*value*y
    return val


def update_weights(w, phi, y):
    for name, value in phi.items():
        w[name] += value * y
    return w


def update_weights2(w, phi, y):
    for name, value in w.items():
        if abs(value) < 0.01:
            w[name] = 0
        else:
            w[name] -= (1/(1+np.exp(value)))*0.01
    for name, value in phi.items():
        w[name] += value * y
    return w


def init_w(train_data):
    w = {}
    for line in train_data:
        line = line.rstrip('\n')
        text = line.split('\t')
        words = text[1].split(' ')
        for word in words:
            if word not in w.keys():
                w[word] = 0
    return w


input_file = open('titles-en-train.labeled')
train_data = input_file.readlines()
w = init_w(train_data)
w = create_w(w, train_data)

test_file = open('titles-en-test.word')
test_data = test_file.readlines()
predict_all(w, test_data)
