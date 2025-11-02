from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


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
        if sorting_key.lower() not in ['title', 'content']:
            return jsonify({
                "message": "Bad Request: Invalid sort key. Use 'title' or 'content'."
            }), 400

        reverse_sort = True if sort_direction == 'desc' else False
        return jsonify(
            sorted(POSTS,
                   key=lambda post: post[sorting_key.lower()],
                   reverse=reverse_sort)
        ), 200

    return jsonify(POSTS), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    req_body = request.get_json()

    if not req_body['title'] and not req_body['content']:
        return jsonify({
            "message": "Invalid request body: 'title' and 'content' are missing"
        }), 400
    elif not req_body['title']:
        return jsonify({
            "message": "Invalid request body: 'title' is missing"
        }), 400
    elif not req_body['content']:
        return jsonify({
            "message": "Invalid request body: 'content' is missing"
        }), 400

    new_post = {
        "id": POSTS[-1]['id'] + 1,
        "title": req_body['title'],
        "content": req_body['content']
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    post = list(filter(lambda post: post['id'] == post_id, POSTS))

    if not post:
        return jsonify({
            "message": f"Post with ID {post_id} doesn't exists."
        }), 404

    POSTS.remove(post[0])
    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    }), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    post = list(filter(lambda post: post['id'] == post_id, POSTS))

    if not post:
        return jsonify({
            "message": f"Post with ID {post_id} doesn't exists."
        }), 404

    req_body = request.get_json()
    if 'title' in req_body:
        post[0].update({"title": req_body['title']})

    if 'content' in req_body:
        post[0].update({"content": req_body['content']})

    return jsonify(post[0]), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    results = []

    title = request.args.get('title')
    if title:
        posts = list(filter(
            lambda post: title.lower() in post['title'].lower(), POSTS
        ))
        for result in posts:
            results.append(result)

    content = request.args.get('content')
    if content:
        posts = list(filter(
            lambda post: content.lower() in post['content'].lower(), POSTS
        ))
        for result in posts:
            results.append(result)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
