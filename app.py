from flask import Flask, render_template, request, redirect, url_for, jsonify
from model.storage import read_data, save_data, get_post_by_id
from datetime import datetime
from random import randint
app = Flask(__name__)


@app.route('/')
def index():
    """
    Index route to display all blog posts (main/home page)
    Fetches all blog posts from the storage and renders them on the index page
    :return: Rendered index.html with list of blog posts
    """
    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add new blog post route.
    Handles both GET and POST requests:
    - GET: Displays the form for adding a new blog post
    - POST: Receives the form data, generates a new ID and add the post to the storage.json file
    :return: Redirect to index.html page on success or render the add.html page
    """
    if request.method == 'POST':
        # get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # read json
        blog_posts = read_data()

        # generate ID
        now = datetime.now()
        second_stamp = int(now.timestamp() * 10)
        random_num = randint(1, 10000)
        new_id = str(second_stamp) + str(random_num)

        # create new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
            'like': 0,
            'dislike': 0
        }

        # append new post then save to JSON
        blog_posts.append(new_post)
        save_data(blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete a blog post via its ID number
    :param post_id: ID of the blog post to delete
    :return: Redirect to the index page after deletion
    """
    blog_posts = read_data()
    # remove post
    blog_posts = [post for post in blog_posts if post.get('id') != post_id]
    save_data(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post by its ID
    Handles both GET and POST requests
    - GET: Displays the current post in a form for editing
    - POST: Updates the post and saves in storage
    :param post_id: ID number of the blog post to update
    :return: Redirect to index.html upon success or renders the update.html
    """
    blog_posts = read_data()
    post = get_post_by_id(post_id, blog_posts)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        save_data(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


@app.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    """
    Increases the 'like' count for the post via the ID give and returns the updated count
    :param post_id: ID of the blog post
    :return: JSON response with success status and like count
    """
    blog_posts = read_data()
    post = get_post_by_id(post_id, blog_posts)

    if post:
        post['like'] += 1
        save_data(blog_posts)
        return jsonify({'success': True, 'likes': post['like']})

    return jsonify({'success': False, 'message': 'Post not found'}), 404


@app.route('/dislike/<post_id>', methods=['POST'])
def dislike(post_id):
    """
    Increases the 'dislike' count for the post via the ID give and returns the updated count
    :param post_id: ID of the blog post
    :return: JSON response with success status and dislike count
    """
    blog_posts = read_data()
    post = get_post_by_id(post_id, blog_posts)

    if post:
        post['dislike'] += 1
        save_data(blog_posts)
        return jsonify({'success': True, 'dislikes': post['dislike']})

    return jsonify({'success': False, 'message': 'Post not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
