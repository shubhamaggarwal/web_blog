import uuid
from src.models.post import Post
import datetime
from src.common.database import Database

class Blog():
    def __init__(self,author,title,description,author_id,_id=None):
        self.author=author
        self.title=title
        self.description=description
        self.author_id=author_id
        self._id=uuid.uuid4().hex if _id is None else _id

    def new_post(self,title,content,date=datetime.datetime.utcnow()):
        post=Post(title=title,
                  date=date,
                  author=self.author,
                  blog_id=self._id,
                  content=content)
        post.save_to_mongo()

    def save_to_mongo(self):
        Database.insert(collection='blogs',data=self.json())

    def get_posts(self):
        return Post.from_blog(self._id)

    def json(self):
        return {
            'author':self.author,
            'title':self.title,
            'description':self.description,
            '_id':self._id,
            'author_id':self.author_id
        }

    @classmethod
    def from_mongo(cls,id):
        blog_data = Database.find_one(collection='blogs',data={'_id':id})
        return cls(**blog_data)
        # return cls(author= blog_data['author'],
        #           title=blog_data['title'],
        #           description=blog_data['description'],
        #           _id=blog_data['_id'])

    @classmethod
    def find_by_author_id(cls,author_id):
        blogs=Database.find_all(collection='blogs',data={'author_id':author_id})
        return [cls(**blog) for blog in blogs]
