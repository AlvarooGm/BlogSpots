from flask import Blueprint,request,flash,redirect,url_for,render_template,g

from .auth import loginrequired
from .models import Post
from blogr import db


bp = Blueprint('post',__name__,url_prefix='/post')



@bp.route('/posts', methods=('GET','POST'))
@loginrequired
def posts():
    
    posts = Post.query.all()
    
    return render_template('admin/posts.html',posts=posts)



@bp.route('/create',methods=('GET','POST'))
@loginrequired
def create():
    if request.method == 'POST':
        author = g.user.id
        url = request.form.get('url')
        url.replace(' ','-')
        title = request.form.get('title')
        info = request.form.get('text')
        content =request.form.get('ckeditor')
      
        post = Post(author,url,title,info,content)
        
        error = None
        
        pUrl = Post.query.filter_by(url=url).first()
        
        if pUrl == None:
            db.session.add(post)
            db.session.commit()
            flash(f'El blog {post.title} se creo correctamente')
            return redirect (url_for('post.posts'))
        else:
            error='El URL {url} ya esta registrado'
            
        flash(error)
    return render_template('admin/create.html')


@bp.route('/update/<int:id>' , methods=('GET','POST'))
@loginrequired
def update(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.info = request.form.get('desc')
        post.contet = request.form.get('ckeditor')
        
        db.session.commit()
        flash(f'El blog {post.title} se ha actualizado correctamente')
        return redirect(url_for('post.posts'))
    
    
    return render_template('admin/update.html' , post = post)


@bp.route('/delete/<int:id>')
@loginrequired
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post.posts'))

