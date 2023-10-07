from app import app, USERS, models, POSTS
from flask import request, Response
import json
from http import HTTPStatus


@app.route('/')
def index():
    return "<h1>Hello wrold</h1>"


@app.post('/users/create')
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, last_name, email)

    USERS.append(user)
    response = Response(json.dumps({
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "total_reactions": str(user.total_reactions),
        "posts": user.posts,
    }),
        HTTPStatus.OK,
        mimetype='application/json')
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(json.dumps({
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "total_reactions": str(user.total_reactions),
        "posts": user.posts,
    }), HTTPStatus.OK, mimetype='application/json')
    return response


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data['author_id']
    text = data['text']

    post = models.Post(post_id, author_id, text)
    POSTS.append(post)
    user = USERS[int(author_id)]
    user.posts.append(post)

    response = Response(json.dumps({
        "id": str(post.post_id),
        "author_id": str(post.author_id),
        "text": post.text,
        "reactions": post.reactions
    }),
        HTTPStatus.OK,
        mimetype='application/json')
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(json.dumps({
        "id": str(post.post_id),
        "author_id": str(post.author_id),
        "text": post.text,
        "reactions": post.reactions
    }),
        HTTPStatus.OK,
        mimetype='application/json')
    return response


@app.post("/posts/<int:post_id>/reaction")
def create_reaction(post_id):
    data = request.get_json()
    user_id = int(data['user_id'])
    reaction = data['reaction']
    if post_id < 0 or post_id >= len(POSTS) or user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    post.reactions.append(reaction)
    user = USERS[user_id]
    user.total_reactions += 1
    return Response(status=HTTPStatus.OK)
