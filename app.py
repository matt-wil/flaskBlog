from flask import Flask, render_template, request, redirect, url_for
from model.storage import read_data, save_data
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
        new_id = len(blog_posts) + 1

        # create new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
        }

        # append new post then save to JSON
        blog_posts.append(new_post)
        save_data(blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
