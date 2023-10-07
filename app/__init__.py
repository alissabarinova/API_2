from flask import Flask

app = Flask(__name__)

USERS = [] # list for objects type User
POSTS = [] # list for objects type Post

from app import views
from app import models