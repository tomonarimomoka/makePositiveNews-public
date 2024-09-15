from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ARTICLE_BODY_TAG = "article_body"
ANCHOR_PROPS_KEY = "data-cl-params"
ANCHOR_PROPS_VALUE = "_cl_vmodule:page;_cl_link:next;"


class ArticleParser(object):
    def __init__(self, root_url: str):
        self.root_url: str = root_url
        self.url = urlparse(root_url)
        self.title = ""

    def get_article_body(self) -> dict:
        try:
            url: str = self.root_url
            contents: list[str] = []
            while True:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                article_body = soup.find("div", class_=ARTICLE_BODY_TAG).get_text(
                    strip=True
                )
                contents.append(article_body)

                if not self.title:
                    self.title = soup.find("article").find("h1").get_text(strip=True)
    
                next_anchor = soup.find(
                    "a", attrs={ANCHOR_PROPS_KEY: ANCHOR_PROPS_VALUE}
                )
                if next_anchor:
                    # 得られるのがhost以降のリンクなので、host以前を結合してかえす
                    url = self.url._replace(path=next_anchor.get("href")).geturl()
                else:
                    break
            return {"title": self.title, "body": "\n".join(contents)}
        except:
            return {}
