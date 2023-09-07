from flask import Blueprint,render_template,request,flash,redirect,url_for,session,g

from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from blogr import db


bp = Blueprint('auth',__name__,url_prefix='/auth')

#ME TENGO QUE ACORDAR QUE EN LOS FORMS DE CADA VISTA USAR EL METHODS POST
#METODO PARA REGISTRAR
@bp.route('/register', methods=('GET','POST'))
def register():
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        passwd = request.form.get('passwd')
    
        usua = User(username,email,generate_password_hash(passwd))
        error = None
        user_email = User.query.filter_by(email=email).first()
    
        if user_email == None:
            db.session.add(usua)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f"El email {email} ya esta en uso" 
        
        flash(error)
        
    return render_template('auth/register.html')


#METODO PARA EL LOGIN
@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
       
        email = request.form.get('email')
        passwd = request.form.get('passwd')
    
       
        error = None
        user_email = User.query.filter_by(email=email).first()
    
        if user_email == None or not check_password_hash(user_email.password,passwd):
            error = 'El correo o la contraseña son incorrectos '
            
        
        if error is None:
            session.clear()
            session['user_id']=user_email.id
            return redirect(url_for('post.posts'))
        
        flash(error)  
        
    return render_template('auth/login.html')


#METODO PARA TENER LAS SESION INICIADA  
@bp.before_app_request
def load_logged_in_user():
    user_id =session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user=User.query.get_or_404(user_id) 
        
#METODO DE CERRAR SESION        
@bp.route('/logout')
def logout() :
    session.clear()
    return redirect(url_for('home.index'))       



#ESTO PARA QUE NO PUEDA ACCEDER A CIERTAS PARTES SIN LOGGEAR PRIMERO
import functools

def loginrequired(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view   




#EDITAR PERFIL
from werkzeug.utils import secure_filename
@bp.route('/profile/<int:id>', methods=('GET','POST'))
@loginrequired
def profile(id):
    user = User.query.get_or_404(id)
    
    
    if request.method == 'POST':
        
        user.username = request.form.get('username')
        password = request.form.get('password')
        
        
        error = None
        
        if len(password) != 0:
            
            user.password = generate_password_hash(password)
            
        elif  len(password) > 0   and len(password) < 6 :
            error = 'La longitud tiene que ser mas grande'
            
            
        if request.files['foto']:
            photo = request.files['foto'] 
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')   
            user.photo = f'media/{secure_filename(photo.filename)}'
            
            
            
        if error is  not None:
            flash(error)
        else:  
              
            db.session.commit()
            return redirect(url_for('auth.profile', id=user.id))
        
        flash(error)
        
        
    return render_template('auth/profile.html',user=user)


    