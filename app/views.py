from app import app, USERS, models, POSTS, EMAILS
from flask import request, Response, jsonify
import json
from http import HTTPStatus


@app.route('/')
def index():
    return "<h1>Hello wrold</h1>"


@app.post('/users/create')
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
# todo: случай, когда пользователь уже зарегистрирован
    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    if email in EMAILS:
        return Response(status=HTTPStatus.CONFLICT)
    EMAILS.append(email)
    new_user = models.User(user_id, first_name, last_name, email, 0, [])

    USERS.append(new_user)
    new_user_posts = json.dumps([{
        "id": p.post_id,
        "author_id": p.author_id,
        "text": p.text,
        "reactions": p.reactions
    } for p in new_user.posts])

    response = Response(json.dumps({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "total_reactions": new_user.total_reactions,
        "posts": new_user_posts
    }),
        HTTPStatus.OK,
        mimetype='application/json')
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_user = USERS[user_id]
    temp_user_posts = json.dumps([{
            "id": p.post_id,
            "author_id": p.author_id,
            "text": p.text,
            "reactions": p.reactions
        } for p in temp_user.posts])

    response = Response(json.dumps({
        "id": temp_user.id,
        "first_name": temp_user.first_name,
        "last_name": temp_user.last_name,
        "email": temp_user.email,
        "total_reactions": temp_user.total_reactions,
        "posts": temp_user_posts,
    }), HTTPStatus.OK, mimetype='application/json')
    return response


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = int(data['author_id'])
    text = data['text']

    new_post = models.Post(post_id, author_id, text, [])
    POSTS.append(new_post)
    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_user = USERS[author_id]
    temp_user.posts.append(new_post)

    response_data = {
        "id": new_post.post_id,
        "author_id": new_post.author_id,
        "text": new_post.text,
        "reactions": new_post.reactions
    }

    response = Response(json.dumps(response_data), HTTPStatus.OK, mimetype='application/json')
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_post = POSTS[post_id]
    response_data = {
        "id": temp_post.post_id,
        "author_id": temp_post.author_id,
        "text": temp_post.text,
        "reactions": temp_post.reactions
    }

    response = Response(json.dumps(response_data), HTTPStatus.OK, mimetype='application/json')
    return response


@app.post("/posts/<int:post_id>/reaction")
def create_reaction(post_id):
    data = request.get_json()
    user_id = int(data["user_id"])
    new_reaction = data["reaction"]
    if post_id < 0 or post_id >= len(POSTS) or user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    current_post = POSTS[post_id]
    current_post.reactions.append(new_reaction)
    temp_user = USERS[user_id]
    temp_user.total_reactions += 1
    return Response(status=HTTPStatus.OK)

@app.get("/users/<int:user_id>/posts")
def get_users_posts(user_id):
    data = request.get_json()
    type_sort = data["sort"]
    user = USERS[user_id]

    if type_sort == 'asc':
        sorted_posts = [post.to_dict() for post in sorted(user.posts)]
        return Response(
            json.dumps({"posts": sorted_posts}),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )
    elif type_sort == 'desc':
        sorted_posts = [post.to_dict() for post in sorted(user.posts, reverse=True)]
        return Response(
            json.dumps({"posts": sorted_posts}),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

@app.get("/users/leaderboard")
def get_graph():
    data = request.get_json()
    stat_type = data["type"]
    if stat_type != "graph":
        return Response(status=HTTPStatus.BAD_REQUEST)
