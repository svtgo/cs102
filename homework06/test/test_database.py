from sqlalchemy.engine import create_engine
from hw06 import database
import pytest


test_news = [
    {"title": "Sveta great fprogrammer", "url": "mail.ru", "points": 200, "author": "Sveta"},
    {
        "title": "Sveta did lab",
        "url": "google.com",
        "points": 13,
        "author": "Git",
    },
]


def db_set_up(engine):
    database.Base.metadata.create_all(bind=engine)


def db_tear_down(session):
    session.query(database.News).delete()
    session.commit()
    session.close()


@pytest.fixture
def engine():
    return create_engine("sqlite://")


@pytest.fixture
def session(engine):
    session = database.get_session(engine)
    db_set_up(engine)
    yield session
    db_tear_down(session)


def test_news_can_be_saved(session):
    database.table_news(session=session, news=test_news)

    saved_item = session.query(database.News).get(1)
    assert saved_item.title == test_news[0]["title"]
    assert saved_item.author == test_news[0]["author"]

    saved_item = session.query(database.News).get(2)
    assert saved_item.title == test_news[1]["title"]
    assert saved_item.author == test_news[1]["author"]


def test_can_news_be_labeled(session):
    database.table_news(session=session, news=test_news)

    saved_item = session.query(database.News).get(1)
    assert saved_item.label is None

    label = "good"
    database.change_label(session=session, data=[label, 1])
    saved_item = session.query(database.News).get(1)
    assert saved_item.label == label
