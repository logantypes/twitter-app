# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 11:10:51 2020

@author: logan
"""

from Assignment_5 import db
# but we can also import the respective classes for each table
from Assignment_5 import User, Post
from flask_bcrypt import Bcrypt
import pandas as pd
bcrypt = Bcrypt()
db.create_all()
User.query.all()
user1 = User(name="Obiwan",
             surname="Kenobi",
             username="Obiwan",
             email="kenobi.obiwan@unisg.ch",
             password=bcrypt.generate_password_hash(password="password"))

user2 = User(name="Yoda",
             surname="Master",
             username="Yoda",
             email="yoda.master@unisg.ch",
             password= bcrypt.generate_password_hash(password="123456"))

db.session.add(user1)
db.session.add(user2)

db.session.commit()

post1 = Post(name="Super Quote",
                    description="""Do. Or do not. There is no try.""",
                    length=len("""Do. Or do not. There is no try."""),
                    user_id=2)
post2 = Post(name="Mega Quote",
                    description="""In my experience there is no such thing as luck.""",
                    length=len("""In my experience there is no such thing as luck."""),
                    user_id=1)
post3 = Post(name="Mega Quote 2",
                    description="""Your eyes can deceive you. Don’t trust them.""",
                    length=len("""Your eyes can deceive you. Don’t trust them."""),
                    user_id=1)
db.session.add_all([post1, post2, post3])
db.session.commit()
all_products = Post.query.all()
Post.query.all()