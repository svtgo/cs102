from re import sub
import requests
import typing as tp
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
    """ Extract news from a given web page """

    news_list = []
    title_list = []
    links_list = []
    author_list = []
    points_list = []

    title = parser.select(".storylink")
    points = parser.select(".score")
    subtext = parser.select(".subtext")

    for i in title:
        title_list.append(i.text)
        link = i.get("href", None)
        if link.startswith("item"):
            links_list.append("https://news.ycombinator.com/" + link)
        else:
            links_list.append(link)

    for i in range(len(subtext)):
        author = subtext[i].select(".hnuser")
        if author == []:
            author = "Anonymous"
        else:
            author = author[0].text
        author_list.append(author)
        points = subtext[i].select(".score")
        if points == []:
            points = 0
        else:
            points = int(points[0].text.split()[0])
        points_list.append(points)

    for i in range(len(title)):
        news_list.append(
            {
                "title": title_list[i],
                "url": links_list[i],
                "author": author_list[i],
                "points": points_list[i],
            }
        )

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """ Extract next page URL """
    link = parser.select(".morelink")[0]["href"]
    return str(link)


def get_news(url: str, n_pages: int = 1) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    n = get_news(url="https://news.ycombinator.com/newest/", n_pages=4)
    print(len(n))
    print(n[1])
    print(n[11])
    print(n[111])