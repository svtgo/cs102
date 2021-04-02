import string
from bottle import route, run, template, request, redirect
from sqlalchemy.orm import session
import typing as tp

from hw06.database import News, get_session, engine, change_label, next_news
from hw06.bayes import NaiveBayesClassifier


@tp.no_type_check
@route("/")
@route("/news")
def news_list():
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@tp.no_type_check
@route("/add_label/")
def add_label():
    s = get_session(engine)
    http_request = request.query_string
    label, id = http_request.split("&")
    label, id = label.split("=")[1], int(id.split("=")[1])
    change_label(s, [label, id])
    redirect("/news")


@tp.no_type_check
@route("/update")
def update_news():
    s = get_session(engine)
    next_news(s)
    redirect("/news")


colors = {"good": "#00d2fe", "never": "#180f3b", "maybe": "#969696"}


@tp.no_type_check
@route("/classify")
def classify_news():
    s = get_session(engine)
    model = NaiveBayesClassifier()
    train_set = s.query(News).filter(News.label != None).all()
    model.fit([clean(news.title).lower() for news in train_set], [news.label for news in train_set])
    test = s.query(News).filter(News.label == None).all()
    cell = list(map(lambda x: model.predict(x.title), test))
    return template(
        "recommended_template",
        rows=list(map(lambda x: (x[1], colors[cell[x[0]]]), enumerate(test))),
    )


def clean(s: str) -> str:
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    run(host="localhost", port=8080)
