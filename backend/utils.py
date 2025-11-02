import json
from typing import Any, Optional


def fetch_blog_posts() -> Optional[Any]:
    try:
        with open("data/posts.json", "r") as file_obj:
            return json.load(file_obj)
    except FileNotFoundError:
        print("Error: File database posts.json not found")


def save_posts(posts: list[dict]) -> None:
    try:
        with open("data/posts.json", "w") as file_obj:
            file_obj.write(json.dumps(posts))
    except FileNotFoundError:
        print("Error: File database posts.json not found")
    else:
        print("Posts saved to file storage")


def fetch_post_by_id(post_id: int) -> Optional[dict]:
    posts = fetch_blog_posts()
    post_by_id = list(filter(lambda post: post['id'] == post_id, posts))

    if post_by_id:
        return post_by_id[0]

    return None
