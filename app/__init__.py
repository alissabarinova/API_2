from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects type User
POSTS = []  # list for objects type Post
EMAILS = []  # list for user's email

from app import views
from app import models
