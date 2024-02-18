from flask import Flask, render_template
from flask import url_for,request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin,login_required,logout_user,current_user,login_user
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
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):   # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user




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


#用户登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            
            flash('登录成功')
            return redirect(url_for('index'))

        flash('账户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')


#登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('bye')
    return redirect(url_for('index'))

#设置用户名
@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) >20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Settings updated')
        return redirect(url_for('index'))
    return render_template('settings.html')



#生成管理员账户
@app.cli.command()
@click.option('--username',prompt=True, help='username used to login')
@click.option('--password',prompt=True,confirmation_prompt=True,help='password used to login')
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('updating user......')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user......')
        user = User(username=username,name='admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('done')



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

#创建电影条目  
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form.get('title')    # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input')
            return redirect (url_for('index'))  #重定向回主页
        #保存表单数据到数据库
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return(url_for('index'))
        # user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
    


#编辑电影条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('输入错误')      
            return redirect(url_for('edit',movie_id= movie_id))   #重定向回对应编辑页面
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('index'))
    return render_template ('edit.html', movie = movie)

#删除电影条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  #登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('index'))

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



class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self,password):   # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)

    def validate_password(self,password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash,password)    #返回布尔值
        

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


    






# if __name__ == "__main__":
#     app.run()
    