import linked_list
import hash_table
import binary_search_tree
import random

from sqlite3 import Connection as SQLite3Connection
from datetime import date, datetime
from flask import Flask, request, jsonify
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# configure sqlite3 to enforce foreign key constraints


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):

    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()


# models
class User(db.Model):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):

    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(240), nullable=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# routes
@app.route("/user", methods=["POST"])
def create_user():

    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"})


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():

    users = User.query.all()

    if not users:
        return jsonify({"message": "no user data found"})

    all_users_ll = linked_list.LinkedList()
    for user in users:
        all_users_ll.insert_at_head(
            {"id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
             }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():

    users = User.query.all()

    if not users:
        return jsonify({"message": "no user data found"})

    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )
    return jsonify(all_users_ll.to_list())


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id: int):

    users = User.query.all()
    all_user_ll = linked_list.LinkedList()
    for user in users:
        all_user_ll.insert_at_head(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = all_user_ll.get_by_id(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404
    
    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "user not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "user deleted"}), 204


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):

    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "unauthorized"}), 400

    ht = hash_table.HashTable(10)

    ht.add_key_value("title",data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)
    
    new_blog = BlogPost(
        title = ht.get_value("title"),
        body = ht.get_value("body"),
        date = ht.get_value("date"),
        user_id = ht.get_value("user_id")
    )
    db.session.add(new_blog)
    db.session.commit()

    return jsonify({"message": "new blog post created"}), 201


@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):

    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert(
            {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "date": post.date
            }
        )    
    post = bst.search(blog_post_id)
    print(post)

    if not post:
        return jsonify({"message": "post not found"}), 404

    return jsonify(post), 200


@app.route("/blog_post/<user_id>", methods=["GET"])
def get_all_blog_post(user_id):
    pass


@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
