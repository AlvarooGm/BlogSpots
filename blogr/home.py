from flask import Blueprint,render_template,request

from .models import User,Post

bp = Blueprint('home',__name__)


def getUsuario(id):
    user = User.query.get_or_404(id)
    return user


def buscar_post(query):
    posts =  Post.query.filter(Post.title.ilike(f'%{query}%'))
    return posts

@bp.route('/',methods=('GET','POST'))
def index():
    posts = Post.query.all()
    if request.method == 'POST':
        query = request.form.get('search')
        posts=buscar_post(query)
        return render_template('index.html',posts = posts , getUsuario = getUsuario)
    return render_template('index.html',posts = posts , getUsuario = getUsuario)

@bp.route('/blog/<url>')
def blog(url):
    
    post= Post.query.filter_by(url=url).first()
    
    
    return render_template('blog.html',post=post,getUsuario = getUsuario)