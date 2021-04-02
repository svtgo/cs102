import collections
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=0.01):
        self.a = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.classes = list(set(y))
        self.classes.sort()
        self.classes_prob = dict.fromkeys(self.classes)
        c_y = collections.Counter()
        for word in y:
            c_y[word] += 1
        for word in c_y:
            self.classes_prob[word] = c_y[word] / len(y)

        words = []
        for _ in X:
            words.extend(_.split())
        words = list(set(words))
        words.sort()

        self.defdict = collections.defaultdict(list)
        for _ in words:
            for i in range(len(self.classes)):
                self.defdict[_].append(0)

        for cl in self.classes:
            for msg in X:
                for key in self.defdict:
                    if key in msg.split() and y[X.index(msg)] == cl:
                        self.defdict[key][self.classes.index(cl)] += 1

        class_word_am = dict.fromkeys(self.classes, 0)
        for key in self.defdict:
            for cl in class_word_am:
                class_word_am[cl] += self.defdict[key][self.classes.index(cl)]

        for _ in words:
            for i in range(len(self.classes)):
                self.defdict[_].append(
                    (self.defdict[_][i] + self.a)
                    / (class_word_am[self.classes[i]] + len(self.defdict) * self.a)
                )

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        titles = []
        for msg in X:
            probs_cl = dict.fromkeys(self.classes)
            for cl in self.classes:
                prob = math.log(self.classes_prob[cl])
                for word in msg.split():
                    if word in self.defdict:
                        prob += math.log(
                            self.defdict[word][self.classes.index(cl) + len(self.classes)]
                        )
                probs_cl[cl] = prob
            max_prob = max(probs_cl.values())
            for key, mean in probs_cl.items():
                if mean == max_prob:
                    titles.append(key)
                    break
        return titles

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(X_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        score = count / len(y_test)
        return score
