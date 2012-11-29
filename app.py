########################################################################
# Imports
########################################################################

import flask
import shutil
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template, flash, Response
# import sql alchemy
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing
from datetime import datetime
import os

########################################################################
# Configuration
########################################################################

DEBUG = True
# create app
app = Flask(__name__)
# set up sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # this creates a db in /tmp
db = SQLAlchemy(app)

app.config.from_object(__name__)
app.secret_key = '123bsdfwedfs'

task_dic = {} # name: task_list

########################################################################
# db models
########################################################################

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True)

  def __init__(self, name):
    self.name = name

  # print out <User name> when this object is coverted to a string
  def __repr__(self):
    return '<User %r>' % self.name

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  
  # we want every task to be associated with a user. we can do this
  # through foreign keys. This ties the user.id with a task.id. Later
  # on we can just find all tasks with a particular user.id to find a 
  # user's tasks.
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  # this allows us to get a user from a task (task.user) and to get
  # all tasks from a user (user.tasks)
  user = db.relationship('User', 
    backref=db.backref('tasks', lazy='dynamic'))

  title = db.Column(db.String(80))
  description = db.Column(db.Text)
  created = db.Column(db.DateTime)

  def __init__(self, title, description, user, created=None):
    self.title = title
    self.description = description
    self.user = user
    if not created:
      # grab time in UTC to avoid localization issues later
      self.created = datetime.utcnow() 

  def __repr__(self):
    return '<Task %r>' % self.title

########################################################################
# Routes
########################################################################

@app.route('/todo/<name>', methods=['GET', 'POST'])
def todo(name):
  # find the user 
  user = User.query.filter_by(name=name).first()

  # check if its a post
  if request.method == 'POST':
    # create a new task related to that user
    db.session.add(Task(request.form.get('task'), 
      request.form.get('description'), user))
    db.session.commit() # save it

  task_list = user.tasks
  return render_template('todo.html', user = user, task_list = task_list)

@app.route('/', methods=['GET', 'POST'])
def main():
  if request.method == "POST":
    # check if we already have this user
    person = request.form.get('person')

    # grab the first user with this name
    user = User.query.filter_by(name=person).first()
    # create the user if we dont have one
    if not user:
      user = User(person)
      db.session.add(user)
      db.session.commit() # save it

    return redirect(url_for('todo', name=user.name))

  users = User.query.all()
  return render_template('main.html', users=users)

########################################################################
# Entry
########################################################################

if __name__ == '__main__':
  db.create_all() # create the database the first time it's run
  app.run()
