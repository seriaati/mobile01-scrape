# type: ignore[reportOptionalMemberAccess]
from typing import TYPE_CHECKING, Final

from .schema import Post

if TYPE_CHECKING:
    from playwright.sync_api import Playwright

AUTHOR: Final[str] = "連人帶車100KG還騎超快"
URL: Final[str] = "https://www.mobile01.com/topicdetail.php?f=291&t=5077716&p={page}"


def get_last_page(playwright: "Playwright") -> str:
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(URL.format(page=1))
    # Search for li with class "l-pagination__page"
    page.wait_for_selector("li.l-pagination__page", timeout=10000)
    lis = page.query_selector_all("li.l-pagination__page")
    li = lis[-1]
    last_page = li.inner_text()

    browser.close()

    return last_page


def get_posts(playwright: "Playwright", last_page: str) -> list[Post]:
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    # Go to last page
    page.goto(URL.format(page=last_page))

    # Find second div with class "l-articlePage"
    page.wait_for_selector("div.l-articlePage", timeout=10000)
    articles = page.query_selector_all("div.l-articlePage")

    posts: list[Post] = []
    for article in articles[1:]:
        # Find div inside it with class "l-articlePage__author"
        author_name = (
            article.query_selector("div.l-articlePage__author")
            .query_selector("div.c-authorInfo__id")
            .inner_text()
        )
        if author_name != AUTHOR:
            continue

        # Find div with class "l-articlePage__publish"
        div_publish = article.query_selector("div.l-articlePage__publish")
        content = div_publish.query_selector("article")
        fonts = content.query_selector_all("font")
        content = ""
        for font in fonts:
            content += f"{font.inner_text()}\n"
        # Remove empty lines
        content = "\n".join(line for line in content.splitlines() if line.strip())

        div_navigation = div_publish.query_selector("div.l-navigation__item")
        spans = div_navigation.query_selector_all("span")
        posted_at = spans[0].inner_text()
        post_id = spans[1].inner_text()

        posts.append(Post(id=post_id, content=content, posted_at=posted_at))

    browser.close()

    return posts
