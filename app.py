from flask import Flask, render_template
from flask import url_for





app=Flask(__name__)


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


@app.route('/')
def index():
    return render_template('index.html',name=name, movies=movies)

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








# if __name__ == "__main__":
#     app.run()
    