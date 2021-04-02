from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


@tp.no_type_check
def get_session(engine: Engine) -> Session:
    local_session.configure(bind=engine)
    return local_session()


def table_news(session: Session, news: tp.List[tp.Dict[str, tp.Union[int, str]]]) -> None:
    for i in range(len(news)):
        means = News(
            title=news[i]["title"],
            author=news[i]["author"],
            url=news[i]["url"],
            points=news[i]["points"],
        )
        session.add(means)
    session.commit()


@tp.no_type_check
def change_label(session: Session, data: tp.List[tp.Union[str, int]]) -> None:
    item = session.query(News).get(data[1])
    item.label = data[0]
    session.commit()


def next_news(session: Session) -> None:
    news = get_news(url="https://news.ycombinator.com/newest")
    news_news = []
    for something in news:
        main, name = something["title"], something["author"]
        if not list(session.query(News).filter(News.title == main, News.author == name)):
            news_news.append(something)
    table_news(session, news_news)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    table_news(get_session(engine), get_news(url="https://news.ycombinator.com/newest", n_pages=4))
