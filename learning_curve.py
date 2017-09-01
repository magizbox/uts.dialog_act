import numpy
import pandas as pd
from numpy import mean
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import make_scorer, accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from underthesea.feature_engineering.text import Text
from underthesea.word_sent.tokenize import tokenize
from pylab import rcParams

df = pd.read_excel("data/data.xlsx")
X = list(df["text"])


def convert_text(x):
    try:
        return Text(x)
    except:
        pass
    return ""


X = [convert_text(x) for x in X]
# transformer = TfidfVectorizer()
transformer = TfidfVectorizer(min_df=0.4, tokenizer=tokenize)
# transformer = TfidfVectorizer(tokenizer=tokenize)
X = transformer.fit_transform(X)

Y = list(df["SPEED_BANDWIDTH"])
# Y = list(df["PRICE"])

import matplotlib.pyplot as plt


class ExperimentLab:
    def __init__(self):
        self.experiments = []

    def add(self, experiment):
        self.experiments.append(experiment)

    def run(self):
        ir = numpy.arange(0.4, 1, 0.05)
        N = [int(i * len(Y)) for i in ir]
        clfs = [SVC(), NuSVC(), LinearSVC(), GaussianNB()]
        models = ["SVC", "NuSVC", "LinearSVC", "GaussianNB"]
        colors = ['red', 'green', 'yellow', 'blue']
        legends = []

        fig, ax = plt.subplots(figsize=(10, 6))
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        for i, clf in enumerate(clfs):
            f1_scores = []
            accuracy_scores = []
            for n in N:
                e = DataExperiment(n, clf)
                f1, accuracy = e.run()
                f1_scores.append(f1)
                accuracy_scores.append(accuracy)
            plt.gca().set_color_cycle([colors[i], colors[i]])
            plt.plot(N, f1_scores, ls='solid')
            plt.plot(N, accuracy_scores, ls='dotted')
            legends.append("{} f1".format(models[i]))
            legends.append("{} accuracy".format(models[i]))
        ax.legend(legends, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel("Train size")
        plt.ylabel("Score")
        plt.savefig("learning_curve.png")
        plt.show()

    def visualize(self):
        pass


class DataExperiment:
    def __init__(self, n, clf):
        self.n = n
        self.clf = clf

    def run(self):
        X_ = X[:self.n]
        Y_ = Y[:self.n]
        accuracy_scores = []
        f1_scores = []
        try:
            f1 = []
            accuracy = []

            def score_func(y_true, y_pred, **kwargs):
                accuracy_scores.append(accuracy_score(y_true, y_pred, **kwargs))
                f1_scores.append(f1_score(y_true, y_pred, **kwargs))
                return 0

            scorer = make_scorer(score_func)
            cross_val_score(self.clf, X_.toarray(), Y_, cv=3, scoring=scorer)
            print(f1_scores)
            print("F1: {:.4f}".format(mean(f1_scores)))
            f1.append(mean(f1_scores))
            print(accuracy_scores)
            print("Accuracy: {:.4f}".format(mean(accuracy_scores)))
            accuracy.append(mean(accuracy_scores))
            f1 = mean(f1_scores)
            accuracy = mean(accuracy_scores)
        except:
            f1 = 0
            accuracy = 0
        return f1, accuracy


lab = ExperimentLab()
lab.run()