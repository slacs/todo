#__TODOS__
install required packages with
```
pip install -r requirements.txt
```

#__TODOS Day Two:__
##__Part One: Deployment__
SLACers love Heroku. Easy deployment, no management, easy addons.

##Tools:
* git
```sudo apt-get install git```
* Heroku
```wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh```
* Virtualenv
```sudo easy_install pip```
```sudo pip install virtualenv```

##Part One:
#What is Git?
Git is a source control system. It allows you to keep track of all changes you make to code over time, allowing you to roll back, merge multiple edits of code and work collaboratively with others without sending eachother code via email (which sucks).
When you store code in Git, you create a repository which tracks your code, and any changes you make.
Let's start by creating one.
In your todos folder:
```git init```

To add a file to source control, simply:
```git add <filename>```

Or, even better, let's add all of the files in this folder:
```git add .```

Let's check the status of Git to ensure that the operation was succesful:
```git status```
--Yep,  we added a bunch of new files.

In Git, code is stored by commiting changes. You can think about this like printing off a copy of a paper you are writing, and filing it near your desk with a revision number.
Let's go ahead and commit our changes, leaving a fun message to make sure we know what we did during these changes:
```git commit -am "first commit"```

Now, let's change one of these files, and see how easy it is to roll back in case we make a mistake; let's add "Scary ghosts~" to the bottom of the `app.py` file
```echo 'Scary Ghost' >> app.py```
Note that we just used two new commands: `echo` to 'print' a string ("Scary Ghost") and the `>>` operator to append to a file. Let's go ahead and confirm our change with another useful command: `cat app.py`. Can you see "Scary ghosts"?
Now, if we run this, it will fail, as Scary Ghosts is not yet valid python. But don't worry, we can roll back this simple mistake very easily.
The simplest way to do this is to simple stash these recent changes, and revert to the last commit:
```git stash```
Verify your code is the same as earlier, either manually or by using diff (showing the differences):
```git diff HEAD```

Cool. Git rocks. Checkout Github for a place to host repositories (more on that later).

#Deploying to Heroku
Okay, enough of the boring source control, let's go ahead and get this code on the web.
Heroku is this awesome place where you can easily deploy your Python code to run on the web, for millions. 
And I promise it is easy! We only need to make two changes:
##1:Tell Heroku how to run our application
Create a file named 'Procfile' (capitalisation matters~). And tell Heroku the command to launch your application `web: python app.py`
##2: Tell Heroku what packages you need!
An awesome tool named virtualenv makes managing packages in python a breeze! 
Let's create a virtual environment to store python packages in:
```virtualenv VENV```
and use this python environment: ```source VENV/bin/activate```

Now you will see a cute `(VENV)` in front of your terminal prompt, reminding you that you are using a different python than the one installed on your system.

Now, we will use pip to install the packages we need:
`pip install flask`
You saw the list of packages it installed, but let's tell Heroku that you need Flask to run your application, by freezing your environment:
``` pip freeze >requirements.txt```
let's add requiremets.txt and Procfile to git:
```git add requiremts.txt Procfile```

We need to make one more change to really be ready for the web:
Open up app.py and replace the code below:

```if __name__ == '__main__':
  app.run()```
with:
```
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

And commit:
```git commit -am "I can't wait to run on the web"```

Awesome, let's deploy it.

Everyone go to Heroku.com and create an account
next, run:
```heroku keys:add```
Now let's create a new application on Heroku:
```heroku create```
Let's push it live!
```git push heroku master```

Go online and you are running!

