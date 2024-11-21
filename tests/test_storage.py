import os.path

import pytest
from flaskBlog.model.storage import read_data, save_data

TEST_JSON_FILE = 'test_blog_posts.json'


@pytest.fixture
def setup_and_down():
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)
    yield
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)


def test_create_file_if_missing():
    read_data(TEST_JSON_FILE)
    assert os.path.exists(TEST_JSON_FILE)


def test_read_data():
    blog_posts = read_data()
    assert blog_posts == []


def test_save_data():
    blog_posts = read_data(TEST_JSON_FILE)
    post = {'id': 1, 'author': 'John Doe', 'title': 'Test Post', 'content': 'This is a test post.'}
    blog_posts.append(post)
    save_data(blog_posts, TEST_JSON_FILE)

    loaded_posts = read_data(TEST_JSON_FILE)
    assert loaded_posts == [post]
