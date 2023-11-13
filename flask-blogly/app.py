"""Blogly application."""

from flask import Flask, render_template, session, request, jsonify, flash, redirect, url_for
from flask_wtf import FlaskForm
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "CALL-JENNY-867-5309"

# enable debugToolbar
debug = DebugToolbarExtension(app) #i'm getting a weird error when trying to import debugtoolbar! 

with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()
   seed_user = User(first_name="Dave", last_name="Morgan", image_url='data:image/jpeg;base64,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')
   db.session.add(seed_user)
   db.session.commit()
   seed_post = Post(title="how to avoid police", content="don't do anything illegal and don't go outside", user_id = 1)
   db.session.add(seed_post)
   db.session.commit()
   seed_tag = Tag(name="new")
   db.session.add(seed_tag)
   db.session.commit()
   seed_post_tag = PostTag(post_id=1, tag_id=1)
   db.session.add(seed_post_tag)
   db.session.commit()

@app.route("/")
def show_users():
    all_users = User.query.all()
    return render_template("users.html", all_users = all_users)

@app.route("/new_user")
def create_new_user():
   return render_template("new_user.html")


@app.route("/add_user", methods=["POST"])
def add_user_():
   first_name = request.form['first_name']
   last_name = request.form['last_name']
   image_url = request.form['image_url']
   
   new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
   db.session.add(new_user)
   db.session.commit()

   return redirect ("/")

@app.route("/user_details/<int:id>")
def show_user_details(id):
   user = User.query.filter(User.id == id).first()
   posts = Post.query.filter(Post.user_id == id).all()

   return render_template("user_details.html", user=user, posts=posts)


@app.route("/edit_user/<int:id>")
def edit_user(id):
   user = User.query.filter(User.id == id).first()
   return render_template("edit_user.html", user=user)

@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
   user = User.query.get(id)
   if(user):
      user.first_name = request.form['first_name']
      user.last_name = request.form['last_name']
      user.image_url = request.form['image_url']
      db.session.commit()
      return redirect (f'/user_details/{id}')
   
@app.route("/delete_user/<int:id>")
def delete_user(id):
   user = User.query.get(id)
   if(user):
      db.session.delete(user)
      db.session.commit()
      return redirect('/')
   
@app.route("/users/<int:id>/posts/new")
def add_post(id):
   user = User.query.get(id)
   if(user):
      return render_template("add_post.html", user=user)

@app.route("/new_post/<int:user_id>", methods=['POST'])
def save_new_post(user_id):
   new_post = Post(title=request.form['title'], content=request.form['content'], user_id = user_id)
   db.session.add(new_post)
   db.session.commit()
   return redirect(f"/user_details/{user_id}")
   
@app.route("/post_details/<int:id>")
def show_post_details(id):
   post = Post.query.get(id)
   user = User.query.get(post.user_id)
   if(post):
      tags = post.tags
   if(post and user and tags):
      return render_template("post_details_tags.html", post = post, user=user, tags=tags)
   elif(post and user):
      return render_template("post_details.html", post=post, user=user)
   
   
@app.route("/edit_post/<int:id>")
def edit_post(id):
   post = Post.query.get(id)
   user = User.query.get(post.user_id)
   selected_tags = post.tags
   all_tags = Tag.query.all()

   if(post and user and selected_tags and all_tags):
      return render_template("edit_post.html", post=post, user=user, all_tags=all_tags)
   elif (post and user):
      return render_template("edit_post.html", post=post, user=user)

@app.route("/update_post/<int:id>", methods = ['POST'])
def update_post(id):
   post = Post.query.get(id)
   if (post):
      post.title = request.form['title']
      post.content = request.form['content']
      checked_tag_str_ids = request.form.getlist('tags[]')
      #we need to delete any PostTag records for this post or we will get integrity error
      PostTag.query.filter(PostTag.post_id == id).delete()
      db.session.commit()

      for tag_id_str in checked_tag_str_ids:
         tag_id = int(tag_id_str)  #I would normally put a try block around this but I'm lazy
         new_tag = PostTag(post_id = post.id, tag_id=tag_id)
         db.session.add(new_tag)
      
      db.session.commit()
      return redirect (f'/user_details/{post.user_id}')

@app.route("/tags/new", methods=['GET'])
def show_new_tag_form():
   return render_template("new_tag_form.html")

@app.route("/tags/new", methods=['POST'])
def add_new_tag():
   new_tag = Tag(name=request.form['tag'])
   db.session.add(new_tag)
   db.session.commit()
   return redirect ('/tags')

@app.route("/tags/<int:id>/edit", methods=["GET"])
def edit_existing_tag(id):
   tag = Tag.query.get(id)
   if(tag):
      return render_template('edit_tag.html', tag=tag)

@app.route("/tags/<int:id>/edit", methods=["POST"])
def update_existing_tag(id):
   tag = Tag.query.get(id)
   if (tag):
      tag.name = request.form['tag-name']
      db.session.add(tag)
      db.session.commit()
      
      return redirect("/tags")

@app.route("/tags")
def show_tag_list_page():
   tags = Tag.query.all()
   return render_template("tag_list_page.html", tags=tags)

@app.route("/tags/<int:id>")
def show_tag_details(id):
   tag = Tag.query.get(id)
   return render_template("tag_details.html", tag=tag)

@app.route("/tag/<int:id>/delete", methods=["POST"])
def delete_tag(id):
   #first delete from join table
   PostTag.query.filter(PostTag.tag_id == id).delete()
   db.session.commit() #commit so we don't get foreign key constraint violation

   #now we can delete the tag itself
   tag = Tag.query.get(id)
   if(tag):
      db.session.delete(tag)
      db.session.commit()
   return redirect("/")





@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8080, debug=True)
