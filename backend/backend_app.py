from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import utils
app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/api/docs"
API_URL="/static/masterblog.json"


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sorting_key = request.args.get('sort')
    sort_direction = request.args.get('direction')

    if sort_direction or sort_direction == "":
        if sort_direction.lower() not in ['asc', 'desc']:
            return jsonify({
                "message": "Bad Request: Invalid sort direction. Use 'asc' or 'desc'."
            })

    if sorting_key or sorting_key == "":
        if sorting_key.lower() not in ['title', 'content', 'author', 'date']:
            return jsonify({
                "message": "Bad Request: Invalid sort key. Use 'title' or 'content'."
            }), 400

        reverse_sort = True if sort_direction == 'desc' else False
        return jsonify(
            sorted(utils.fetch_blog_posts(),
                   key=lambda post: post[sorting_key.lower()],
                   reverse=reverse_sort)
        ), 200

    return jsonify(utils.fetch_blog_posts()), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if ('title' not in data and 'content' not in data
        and 'author' not in data and 'date' not in data):
        return jsonify({
            "message": "Invalid request body: 'title', 'content', 'author' and 'date' are missing"
        }), 400
    elif 'title' not in data:
        return jsonify({
            "message": "Invalid request body: 'title' is missing"
        }), 400
    elif 'content' not in data:
        return jsonify({
            "message": "Invalid request body: 'content' is missing"
        }), 400
    elif 'author' not in data:
        return jsonify({
            "message": "Invalid request body: 'author' is missing"
        }), 400
    elif 'date' not in data:
        return jsonify({
            "message": "Invalid request body: 'date' is missing"
        }), 400

    posts = utils.fetch_blog_posts()
    try:
        new_post = {
            "id": posts[-1].get('id', 0) + 1,
            "title": data['title'],
            "content": data['content'],
            "author": data['author'],
            "date": data['date']
        }
    except ValueError:
        return jsonify({
            "message": "Invalid date format: Provide date by following format: YYYY-MM-DD"
        }), 400

    posts.append(new_post)
    utils.save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    posts = utils.fetch_blog_posts()
    post = list(filter(lambda post: post['id'] == post_id, posts))

    if not post:
        return jsonify({
            "message": f"Post with ID {post_id} doesn't exists."
        }), 404

    posts.remove(post[0])
    utils.save_posts(posts)

    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    }), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    posts = utils.fetch_blog_posts()
    post = list(filter(lambda post: post['id'] == post_id, posts))

    if not post:
        return jsonify({
            "message": f"Post with ID {post_id} doesn't exists."
        }), 404

    data = request.get_json()
    if 'title' in data:
        post[0].update({"title": data['title']})

    if 'content' in data:
        post[0].update({"content": data['content']})

    if 'author' in data:
        post[0].update({"author": data['author']})

    if 'date' in data:
        post[0].update({"date": datetime.strptime(data['date'], '%Y-%m-%d')})

    utils.save_posts(posts)
    return jsonify(post[0]), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    results = []
    blog_posts = utils.fetch_blog_posts()

    title = request.args.get('title')
    if title:
        posts = list(filter(
            lambda post: title.lower() in post['title'].lower(), blog_posts
        ))
        for result in posts:
            results.append(result)

    content = request.args.get('content')
    if content:
        posts = list(filter(
            lambda post: content.lower() in post['content'].lower(), blog_posts
        ))
        for result in posts:
            results.append(result)

    author = request.args.get('author')
    if author:
        posts = list(filter(
            lambda post: author.lower() in post['author'].lower(), blog_posts
        ))
        for result in posts:
            results.append(result)

    date = request.args.get('date')
    if date:
        posts = list(filter(
            lambda post: date.lower() == post['date'].lower(), blog_posts
        ))
        for result in posts:
            results.append(result)

    return jsonify(results), 200


if __name__ == '__main__':
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Masterblog API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.run(host="0.0.0.0", port=5002, debug=True)
