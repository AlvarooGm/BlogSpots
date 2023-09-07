from blogr import db

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(125),nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)
    photo = db.Column(db.String(200))
    #LA FOTO LA GUARDAMOS EN UNA CARPETA DE NUESTRO PROYECTO Y SUBIMOS LA RUTA
    
    def  __init__(self,username,email,password,photo=None):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo
        
      
        
from datetime import datetime        
class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    url = db.Column(db.String(125),nullable=False,unique=True)
    title = db.Column(db.String(125),nullable=False)
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    createDate = db.Column (db.DateTime,nullable=False,default = datetime.utcnow)
    
    def __init__(self,author,url,title,info,content) -> None:
        self.author = author
        self.url = url
        self.title = title
        self.info = info
        self.content = content
        
        
    
    
   
            