from src.common.database import Database
import uuid
import datetime
class Post(object):

    def __init__(self,title,content,author,blog_id,date=datetime.datetime.utcnow(),_id=None):
        self.content = content
        self.title = title
        self.author = author
        self._id=uuid.uuid4().hex if _id is None else _id
        self.blog_id=blog_id
        self.date=date


    def save_to_mongo(self):
        Database.insert(collection='posts',data=self.json())

    def json(self):
        return {
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'blog_id':self.blog_id,
            '_id':self._id,
            'date':self.date
        }

    @classmethod
    def from_mongo(cls,id):
        data = Database.find_one(collection='posts', data = {'_id': id})
        return cls(**data)
        # this does the same thing as below
        # return cls(title=data['title'],
        #           author=data['author'],
        #           content=data['content'],
        #           blog_id=data['blog_id'],
        #           date=data['date'],
        #           _id=data['_id'])

    @classmethod
    def from_blog(cls,blog_id):
        data_cursor = Database.find_all(collection='posts',data={'blog_id':blog_id})
        data=[cls(**data_parts) for data_parts in data_cursor]
        return data