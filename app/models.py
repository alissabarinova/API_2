import re
import json


class User:
    def __init__(self, user_id, first_name, last_name, email, total_reactions, posts):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    def to_dict(self):
        user_posts = json.dumps(
            [
                {
                    "id": p.post_id,
                    "author_id": p.author_id,
                    "text": p.text,
                    "reactions": p.reactions,
                }
                for p in self.posts
            ]
        )

        return dict(
            {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "total_reactions": self.total_reactions,
                "posts": user_posts,
            }
        )


class Post:
    def __init__(self, post_id, author_id, text, reactions=[]):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions

    def __lt__(self, other):
        return len(self.reactions) < len(other.reactions)

    def to_dict(self):
        return dict(
            {
                "id": self.post_id,
                "author_id": self.author_id,
                "text": self.text,
                "reactions": self.reactions,
            }
        )
