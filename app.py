from flask import Flask, render_template, request, redirect, url_for, jsonify
from model.storage import read_data, save_data, get_post_by_id
from datetime import datetime
from random import randint
app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
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
    blog_posts = read_data()
    # remove post
    blog_posts = [post for post in blog_posts if post.get('id') != post_id]
    save_data(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
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
    blog_posts = read_data()
    post = get_post_by_id(post_id, blog_posts)

    if post:
        post['like'] += 1
        save_data(blog_posts)
        return jsonify({'success': True, 'likes': post['like']})

    return jsonify({'success': False, 'message': 'Post not found'}), 404


@app.route('/dislike/<post_id>', methods=['POST'])
def dislike(post_id):
    blog_posts = read_data()
    post = get_post_by_id(post_id, blog_posts)

    if post:
        post['dislike'] += 1
        save_data(blog_posts)
        return jsonify({'success': True, 'dislikes': post['dislike']})

    return jsonify({'success': False, 'message': 'Post not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
