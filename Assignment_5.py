import pandas as pd
import datetime

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# new import line
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required

from forms import RegistrationForm, LoginForm, PostForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "enter-a-hard-to-guess-string"

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


login_manager.login_view = "login"


###############################################################################
# Database configuration
###############################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
  
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=True)
  
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="vendor", lazy=True)

    def __repr__(self):
        """
        This is the string that is printed out if we call the print function
            on an instance of this object
        """
        return f"User(id: '{self.id}', name: '{self.name}', surname: '{self.surname}', email: '{self.email}',description: '{self.description}' " +\
               f" username: '{self.username}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(140), nullable=False)
    
   
    length=db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    

    def __repr__(self):
        """
        This is the string that is printed out if we call the print function
            on an instance of this object
        """
        return f"Post(id: '{self.id}', name: '{self.name}' ,length: '{self.length}' "  +\
               f" description:'{self.description}' "+\
               f": ' date_created{self.date_created}', vendor: '{self.user_id}')"


###############################################################################
# Routes
###############################################################################


@app.route("/")
def index():
    posts = get_posts()
    return render_template("index.html", posts_df=posts)


@app.route("/register", methods=["GET", "POST"])
def register():

   
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        registration_worked = register_user(form)
        if registration_worked:
            flash("Registration successful")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        if is_login_successful(form):
            flash("Login successful")
            return redirect(url_for("feed"))
        if is_username_successful(form):
            flash("Wrong Passwod")
            
        else:
            flash("Login unsuccessful, please check your credentials and try again")
            return redirect(url_for("register"))

    return render_template("login.html", form=form)





@app.route("/homepage/feed", methods=["GET", "POST"])
@login_required
def feed():
    posts = get_posts()
    users = get_user()
    return render_template("feed.html", posts_df=posts, users_df=users)
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()

    if form.validate_on_submit():
        if is_post_successful(form):
            add_post(form)
            flash("Post uploaded successfully")
            return redirect(url_for("feed"))
            
        else:
            flash("Your post is longer than 140 character , please make it shorter")
        
    return render_template("post.html", form=form)
@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    
    username=str(username)
    user = User.query.filter_by(username=username).first()
    if username_already_taken(username)==True:
        surname=user.surname
        name=user.name
        return render_template('profile.html', name=name, surname=surname, username= username)
    else:
        flash("This username is not recognized")
        return redirect(url_for("feed"))

@app.route("/logout")
def logout():
 
    logout_user()
    return redirect(url_for("login"))


###############################################################################
# Helper functions
###############################################################################
def username_already_taken(username):
        if User.query.filter_by(username=username).count() > 0:
            return True
        else:
            return False
def register_user(form_data):

    def username_already_taken(username):
        if User.query.filter_by(username=username).count() > 0:
            return True
        else:
            return False

    if username_already_taken(form_data.username.data):
        flash("That username is already taken!")
        return False

 
    hashed_password = bcrypt.generate_password_hash(form_data.password.data)

    user = User(name=form_data.name.data,
                surname=form_data.surname.data,
                email=form_data.email.data,
                username=form_data.username.data,
                password=hashed_password)

    db.session.add(user)

    db.session.commit()

    return True


def is_login_successful(form_data):

    username = form_data.username.data
    password = form_data.password.data

    user = User.query.filter_by(username=username).first()

    if user is not None:
        if bcrypt.check_password_hash(user.password, password):

            
            login_user(user)

            return True

    return False

def is_username_successful(form_data):

    username = form_data.username.data
    

    user = User.query.filter_by(username=username).first()

    if user is not None:

        return True

    return False

def is_post_successful(form_data):

    
    description=form_data.description.data
                     

    if len(description) <=140:       

       return True

    return False


def add_post(form_data):

    post = Post(name=form_data.item_name.data,
                       description=form_data.description.data,
                       length= len(form_data.description.data),
                       user_id=current_user.id)

    db.session.add(post)

    db.session.commit()


def get_posts():
    df = pd.read_sql(Post.query.statement, db.session.bind)

    return df
def get_user():
    df = pd.read_sql(User.query.statement,db.session.bind)
    return df


if __name__ == "__main__":
    app.run(debug=True)
