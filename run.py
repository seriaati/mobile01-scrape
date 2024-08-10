from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import Playwright, sync_playwright

from src.database import load_posts, save_posts
from src.scraper import get_last_page, get_posts
from src.utils import line_notify


def main(playwright: Playwright) -> None:
    logger.info("Start scraping")
    load_dotenv()

    last_page = get_last_page(playwright)
    logger.info(f"Last page: {last_page}")

    posts = get_posts(playwright, last_page)
    logger.info(f"Found {len(posts)} posts")

    current_posts = load_posts()
    logger.info(f"Found {len(current_posts)} posts in database")

    saved_posts = save_posts(posts, current_posts)
    logger.info(f"Saved {len(saved_posts)} posts")

    for post in saved_posts:
        line_notify(f"\n新貼文\n發布於: {post.posted_at}\n\n{post.content or '無內容'}")

    logger.info("Scraping finished")


if __name__ == "__main__":
    with sync_playwright() as playwright:
        main(playwright)
