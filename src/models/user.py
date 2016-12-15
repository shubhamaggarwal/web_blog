from src.common.database import Database
import uuid
from flask import session
from src.models.blog import Blog
import datetime

class User(object):

    def __init__(self,email,password,_id=None):
        self.email=email
        self.password=password
        self._id=uuid.uuid4().hex if _id is None else _id

    @classmethod # this is a class method because when we are using this thing we don't yet have the user object
                    # and it would be great to have one
    def get_by_email(cls,email):
        data=Database.find_one(collection='users',data={'email':email})
        if data is not None:
            return cls(**data)
        return None # default in python

    @classmethod
    def get_by_id(cls,_id):
        data = Database.find_one(collection='users', data={'_id':_id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        data=User.get_by_email(email)
        if data is not None:
            return data.password==password
        return False

    @staticmethod
    def login(email):
        # login_valid has already been called
        session['email']=email

    @staticmethod
    def logout():
        session['email']=None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self,title,description):
        blog=Blog(author=self.email,
                   title=title,
                   description=description,
                   author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id,title,content,date=datetime.datetime.utcnow()):
        blog=Blog.from_mongo(blog_id)
        blog=Blog.new_post(date,title=title,content=content)

    @classmethod
    def register(cls,email,password):
        user=cls.get_by_email(email)
        if user is None:
            user=cls(email=email,password=password)
            user.save_to_mongo()
            session['email']=email
            return True
        else:
            return False

    def json(self):
        return {
            'email':self.email,
            '_id': self._id,
            'password':self.password
        }

    def save_to_mongo(self):
        Database.insert(collection='users',data=self.json())