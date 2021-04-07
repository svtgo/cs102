from bayes import NaiveBayesClassifier
from database import News, local_session

X, y = [], []

model = NaiveBayesClassifier(alpha=0.05)
s = local_session()
rows = s.query(News).filter(News.label != None).all()
for row in rows:
    X.append(f"{row.title} {row.author} {row.url}")
    y.append(row.label)

limit = len(rows) // 100 * 70
X_train, y_train, X_test, y_test = X[:limit], y[:limit], X[limit:], y[limit:]

model.fit(X, y)

print(model.score(X_test, y_test))
