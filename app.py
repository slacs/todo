########################################################################
# Imports
########################################################################

import flask
import shutil
from flask import Flask, request, session, g, redirect, url_for, \
   abort, render_template, flash, Response
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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

  def __repr__(self):
    return '<User %r>' % self.name

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
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
    db.session.add(Task(request.form.get('task'), 
      request.form.get('description'), user))
    db.session.commit()

  task_list = user.tasks
  return render_template('todo.html', user = user, task_list = task_list)

@app.route('/', methods=['GET', 'POST'])
def main():
  if request.method == "POST":
    # check if we already have this user
    person = request.form.get('person')
    user = User.query.filter_by(name=person).first()
    # create the user if we dont have one
    if not user:
      user = User(person)
      db.session.add(user)
      db.session.commit() # save it
    # keep track that this is the person we want

    return redirect(url_for('todo', name=user.name))

  users = User.query.all()
  return render_template('main.html', users=users)

########################################################################
# Entry
########################################################################

if __name__ == '__main__':
  db.create_all()
  app.run()
