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
    return jsonify(POSTS)


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
