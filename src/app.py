from flask import Flask, render_template,request,session,make_response
from src.models.user import User
from src.models.blog import Blog
from src.common.database import Database

app=Flask(__name__)
app.secret_key="Shubham"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth/register',methods=['POST'])
def user_register():
    email=request.form['email']
    password=request.form['password']
    User.register(email,password)
    return render_template('profile.html',email=email)

@app.route('/auth/login',methods=['POST'])
def user_login():
    email=request.form['email']
    password=request.form['password']
    if User.login_valid(email,password):
        User.login(email)
    else:
        session['email']=None
    return render_template('profile.html',email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def get_blog(user_id=None):
    if user_id is not None:
        user=User.get_by_id(user_id)
    else:
        user=User.get_by_email(session['email'])
    print(session['email'])
    blogs=user.get_blogs()
    return render_template('user_blogs.html',email=user.email,blogs=blogs)


@app.route('/posts/<string:blog_id>')
def get_posts(blog_id):
    blog=Blog.from_mongo(blog_id)
    posts=blog.get_posts()
    return render_template("posts.html",blog_title=blog.title,posts=posts,blog_id=blog_id)


@app.route('/blogs/new',methods=['POST','GET'])
def new_blogs():
    if request.method=="GET":
        return render_template("new_blog.html")
    else:
        user=User.get_by_email(session['email'])
        blog=Blog(author=user.email,
                  title=request.form['title'],
                  author_id=user._id,
                  description=request.form['description'])
        blog.save_to_mongo()
        return make_response(get_blog(user._id))


@app.route('/posts/new/<string:blog_id>',methods=['POST','GET'])
def new_posts(blog_id):
    if request.method=="GET":
        return render_template("new_posts.html",blog_id=blog_id)
    else:
        blog=Blog.from_mongo(blog_id)

        blog.new_post(title=request.form['title'],
                      content=request.form['content'])
        print(request.form['title'])
        return make_response(get_posts(blog_id))

if __name__=='__main__':
    app.run(debug=True)