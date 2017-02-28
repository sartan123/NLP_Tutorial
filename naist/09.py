import random


class TopicModel:

    def __init__(self, documents, K):
        self.K = K
        self.documents = documents
        self.all_words = []
        self.documents_topic = []
        self.document_lenghts = [len(d.split(' ')) for d in self.documents]
        self.documents_topic_counts = {i: {} for i in range(len(self.documents))}
        self.topic_counts = [0] * self.K
        self.topic_word_counts = {k: {} for k in range(self.K)}
        self.__create_documents_topic__()

    def __create_documents_topic__(self):
        for docid, line in enumerate(self.documents):
            topics = []
            words = line.split(' ')
            for word in words:
                topic = random.randint(0, self.K - 1)
                topics.append(topic)
                if word not in self.all_words:
                    self.all_words.append(word)
                self.__addcounts__(topic, word, docid, 1)
            self.documents_topic.append(topics)

    def __addcounts__(self, topic, word, docid, amount):
        self.topic_counts[topic] += amount
        self.document_lenghts[docid] += amount
        if word in self.topic_word_counts[topic]:
            self.topic_word_counts[topic][word] += amount
        else:
            self.topic_word_counts[topic][word] = 1
        if topic in self.documents_topic_counts[docid]:
            self.documents_topic_counts[docid][topic] += amount
        else:
            self.documents_topic_counts[docid][topic] = 1

    def __sampleone(self, probs):
        z = sum(probs.values())
        remaining = z * random.random()
        for k, v in probs.items():
            remaining -= v
            if remaining <= 0:
                return k

    def fit(self):
        p_x_y = 0
        p_y_Y = 0
        probs = {k: 0 for k in range(self.K)}
        for _ in range(100):
            for i in range(len(self.documents)):
                text = self.documents[i]
                words = text.split(' ')
                for j in range(len(words)):
                    word = words[j]
                    topic = self.documents_topic[i][j]
                    self.__addcounts__(topic, word, i, -1)
                    for k in range(self.K):
                        try:
                            p_x_y = (self.documents_topic_counts[i][k] + 0.1) / (self.document_lenghts[i] + 0.1 * self.K)
                            p_y_Y = (self.topic_word_counts[k][word] + 0.1) / (self.topic_counts[k] + len(self.all_words) * 0.1)
                        except:
                            pass
                        probs[k] = p_x_y * p_y_Y
                    new_y = self.__sampleone(probs)
                    self.documents_topic[i][j] = new_y
                    self.__addcounts__(new_y, word, i, 1)

    def _DEBUG(self):
        for k, v in zip(self.documents, self.documents_topic):
            print(k, v)


NUM_TOPICS = 4

documents = [
    "Hadoop Big-Data HBase Java Spark Storm Cassandra",
    "NoSQL MongoDB Cassandra HBase Postgres",
    "Python scikit-learn scipy numpy statsmodels pandas",
    "R Python statistics regression probability",
    "machine-learning regression decision-trees libsvm",
    "Python R Java C++ Haskell programming-languages",
    "statistics probability mathematics theory",
    "machine-learning scikit-learn Mahout neural-networks",
    "neural-networks deep-learning Big-Data artificial-intelligence",
    "Hadoop Java MapReduce Big-Data",
    "statistics R statsmodels",
    "C++ deep-learning artificial-intelligence probability",
    "pandas R Python",
    "databases HBase Postgres MySQL MongoDB",
    "libsvm regression support-vector-machines"
]

token = TopicModel(documents, NUM_TOPICS)
# print(token.topic_word_counts)
print(token.documents_topic)
# print(token.documents_topic_counts)
"""
token._DEBUG()
token.fit()
print('*********************************')
token._DEBUG()
"""