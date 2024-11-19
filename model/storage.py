import json
import os.path
from os.path import join


file_path = join("data", "blogs.json")


def read_data(filename=file_path):
    """
    Check if the JSON storage file exists. if not the file is then created.
    If the file exists the data is read and returned.

    :param filename:
        (str) key word param. the file path.

    :return:
        [list] of {dictionaries}
    """
    if not os.path.exists(filename):
        with open(filename, 'w') as file_obj:
            json.dump([], file_obj, indent=4)
        return []

    try:
        with open(filename, "r") as file_obj:
            return json.load(file_obj)

    except Exception as e:
        return f"Error: {e}"


def save_data(post, filename=file_path):
    """Save the JSON data """
    with open(filename, "w") as file_obj:
        json.dump(post, file_obj, indent=4)
    return "Data Successfully Saved"


def get_post_by_id(post_id, blog_posts):
    """Retrieves a certain post by the post id from the list of blog_posts"""
    for post in blog_posts:
        if post.get('id') == post_id:
            return post
    return None


