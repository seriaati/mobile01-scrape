import json
import pathlib

from .schema import Post

DB_PATH = pathlib.Path("posts.json")


def load_posts() -> list[Post]:
    if not DB_PATH.exists():
        return []
    with DB_PATH.open(encoding="utf-8") as f:
        return [Post(**post) for post in json.load(f)]


def get_post(posts: list[Post], post_id: str) -> Post | None:
    for post in posts:
        if post.id == post_id:
            return post
    return None


def save_posts(posts_to_save: list[Post], current_posts: list[Post]) -> list[Post]:
    posts_to_save = [post for post in posts_to_save if get_post(current_posts, post.id) is None]
    current_posts.extend(posts_to_save)
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump([post.model_dump() for post in current_posts], f, ensure_ascii=False, indent=2)

    return posts_to_save
