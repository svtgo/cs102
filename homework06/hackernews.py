from bottle import route, run, template, request, redirect
from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id_value = request.query.id
    s = session()
    news = s.query(News).filter(News.id == id_value).one()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=4)
    s = session()
    for news in news_list:
        if (
            s.query(News).filter(News.title == news["title"], News.author == news["author"]).first()
            == None
        ):
            newest = News(
                title=news["title"],
                author=news["author"],
                url=news["url"],
                comments=news["comments"],
                points=news["points"],
            )
            s.add(newest)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()
    train_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    classifier.fit(x_train, y_train)

    test_news = s.query(News).filter(News.label == None).all()
    x = [row.title for row in test_news]
    x = [clean(news).lower() for news in x]
    labels = classifier.predict(x)

    good = [test_news[i] for i in range(len(test_news)) if labels[i] == "good"]
    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == "maybe"]
    never = [test_news[i] for i in range(len(test_news)) if labels[i] == "never"]
    rows = [good] + [maybe] + [never]
    return template("recommend_news_template", rows=rows, label=["good :)", "maybe :/", "never :("])


if __name__ == "__main__":
    run(host="localhost", port=8080)
