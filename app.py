from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click






app=Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_BINDS']={'users':'sqlite:///' +os.path.join(app.root_path,'data.db')}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACk_MODIFICATIONS']= False

db = SQLAlchemy(app)   #初始化扩展，传入程序实例app



@app.cli.command()
def forge():
    db.create_all()

    name = 'fenghaha'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done')

@app.context_processor    #模板上下文处理函数
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.cli.command()# 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop',is_flag=True,help ='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all ()
    click.echo('Initialized database')

@app.route('/')
def index():
    # user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    return render_template('404.html'), 404

@app.route("/home")
def hello1():
    return"主页面"

@app.route('/user/<name>')
def user_page(name):
    return name

@app.route('/ha') 
def text():
    print(url_for('hello'))
    return url_for('hello')

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))








# if __name__ == "__main__":
#     app.run()
    