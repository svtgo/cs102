import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    athing_list = parser.table.findAll("tr", attrs={"class": "athing"})
    titles_list = []
    url_list = []
    for athing in athing_list:
        if athing.findAll("a", attrs={"class": "storylink"}):
            title = athing.findAll("a", attrs={"class": "storylink"})[0].text
            titles_list.append(title)
            url = athing.findAll("a", attrs={"class": "storylink"})[0]["href"]
            if "item?id" in url:
                url = "https://news.ycombinator.com/" + url
            url_list.append(url)
        else:
            titles_list.append("not indicated")
            url_list.append("not indicated")

    subtext_list = parser.table.findAll("td", attrs={"class": "subtext"})
    points_list = []
    authors_list = []
    comments_list = []
    for subtext in subtext_list:
        if subtext.findAll("span", attrs={"class": "score"}):
            points = subtext.findAll("span", attrs={"class": "score"})[0].text
            for i in range(len(points)):
                if points[i] not in "0123456789":
                    points = points.replace(points[i], " ")
            points_list.append(int(points))
        else:
            points_list.append(None)

        if subtext.findAll("a", attrs={"class": "hnuser"}):
            author = subtext.findAll("a", attrs={"class": "hnuser"})[0].text
            authors_list.append(author)
        else:
            authors_list.append("not indicated")

        a_list = subtext.findAll("a")
        n = 0
        for a in a_list:
            if "comment" in a.text:
                num = ""
                for sym in a.text:
                    if sym in "0123456789":
                        num += sym
                try:
                    comments_list.append(int(num))
                except:
                    comments_list.append(None)
                n += 1
            elif "discuss" in a.text and n == 0:
                comments_list.append(0)
                n += 1
        if n == 0:
            comments_list.append(None)

    for i in range(30):
        d = dict(
            author=authors_list[i],
            comments=comments_list[i],
            points=points_list[i],
            title=titles_list[i],
            url=url_list[i],
        )
        news_list.append(d)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    more = parser.table.findAll("a", attrs={"class": "morelink"})[0]
    link = more["href"]
    return link


def get_news(url, n_pages=1):
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
        time.sleep(10)
    return news
