import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret='ine5225'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, Udacity!')


##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('email =', name).get()
        return u

    @classmethod
    def register(cls, pw, email):
        pw_hash = make_pw_hash(email, pw)
        return User(parent = users_key(),
                    name = email,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, email, pw):
        u = cls.by_name(email)
        if u and valid_pw(email, pw, u.pw_hash):
            return u


##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class PagInicial(BlogHandler): #handler da pagina inicial
    def get(self):
        if self.user:
            self.redirect('/blog/front', self.user.name)
        else:
            self.render("principal.html")

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        
        if not email:
            msg = 'Invalid e-mail'
            self.render('principal.html', error = msg)
        else:
            u = User.login(email, password)
            if u:
                self.login(u)
                self.redirect('/blog/front', email)
            else:
                msg = 'Invalid login'
                self.render('principal.html', error = msg)
                
class Profile (BlogHandler):
    def get(self):
        if self.user:
            
            perfil = db.GqlQuery("select * from Perfil where owner='%s'" %self.user.name)
            for n in perfil:
                n=n.nome_usuario
            for img in perfil:
                img=img.imagem
           
            self.render('welcome.html', username = n, foto=img)
            
            
        else:
            self.redirect('/')
            
class Alterar_Perfil(BlogHandler):
    def get(self):
        self.render("mod_perfil.html")

    def post(self):
        have_error = False
        
        nome_usuario = self.request.get('nome')
        imagem = self.request.get('imagem')
        

        
            
        #make sure the user doesn't already exist
        u = Perfil.by_name(nome_usuario)
        if u:
            msg = 'That user already exists.'
            self.render('mod_perfil.html', error_nome = msg)
        else:
            u = Perfil.register(self.user.email, nome_usuario, imagem)
            u.put()
            
            self.redirect('/blog/front')

        


    def post(self):
        have_error = False
        #self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')


        params = dict(username = self.email,
                      email = self.email)

 
        
    
    
class NovoBlog (BlogHandler):
    def get(self, profile):
        if self.user:
            self.render("novo_blog.html")
        else:
            self.redirect('/')
            
    def post(self, profile):
        if not self.user:
            self.redirect('/')
        
        nome = self.request.get('nome')
        autor = self.request.get('autor')
        
        if not nome:
            msg = 'Coloque um nome para o blog'
            self.render('novo_blog.html', error = msg)
            
        profile=self.request.get("profile")
        q = db.GqlQuery("select * from Perfil where nome_usuario='%s'" %profile)
        results=q.fetch(100)
        if not q:
            self.redirect("/")
        else:
            for p in results:
                owner=p.nome_usuario

        
        if not autor:
            b = blog(parent = blog_key(), endereco="nenhum", nome = nome, autor=self.user.email, owner=owner)
            b.put()
            blog.criar_blog(b)
        else:
            b = blog(parent = blog_key(), endereco="nenhum", nome = nome, autor=autor, owner=owner)
            b.put()
            blog.criar_blog(b)
                
            
        self.redirect('/Perfil?profile='+profile)
        
 
def post_key(name = 'default'):
    return db.Key.from_path('post', name)
 
        
class NovaPostagem(BlogHandler):
    def get(self, b):
        if self.user:
            b=self.request.get("b")
            q = db.GqlQuery("select * from blog where endereco='%s'" %b)
            results=q.fetch(100)
            
            if not q:
                self.redirect("/")
            else:
                for p in results:
                    nome=p.autor
                
            self.render("newpost.html", nome_usuario=nome)
        else:
            self.redirect("/")

    def post(self, b):
        if not self.user:
            
            self.redirect('/')
        b=self.request.get("b")
        subject = self.request.get('subject')
        content = self.request.get('content')
       

        if subject and content:
            p = postagem(parent = post_key(), link="vazio", titulo = subject, conteudo = content, n_views=0, n_likes=0, n_shares=0, link_coments="vazio", endereco=b)
            p.put()
            postagem.criar_post(p)
            self.redirect("/view?b="+b)
            
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, conteudo=content, error=error)
        

class BlogFront(BlogHandler):
    def get(self):
        if self.user:

            u = self.user.email
            
            perfis =  db.GqlQuery("select * from Perfil where owner='%s'" %u)
 
            
            self.render('front.html', perfis = perfis)
        else:
            self.redirect('/')








USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    def get(self):
        self.render("registro.html")

    def post(self):
        have_error = False
       
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

  
        params = dict(username = self.email,
                      email = self.email)



        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('registro.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError



class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.email)
        if u:
            msg = 'That user already exists.'
            self.render('registro.html', error_email = msg)
        else:
            u = User.register(self.password, self.email)
            u.put()
 
            
            self.login(u)
            self.redirect('/novo_perfil')
            
            
            
            
            



class NovoPerfil(BlogHandler):
    
    def get(self):
        if self.user:
            self.render('new_profile.html')
        else:
            self.render('/')

    def post(self):
        have_error = False
        nome_usuario = self.request.get('nome')
        imagem = self.request.get('imagem')
        
        params = dict(username = nome_usuario,
                      imagem = imagem)


        if not valid_username(nome_usuario):
            params['error_username'] = "Este nao foi um usuario valido."
            have_error = True

        if have_error:
            self.render('new_profile.html', **params)
        else:
            q = db.GqlQuery("select * from Perfil where nome_usuario='%s'" %nome_usuario)
            results=q.fetch(100)
            comp=''
            for p in results:
                comp=p.nome_usuario
                
            
            if comp==nome_usuario:
                msg = 'That user already exists.'
                self.render('new_profile.html', error_username = msg)
            else:
                if imagem:
                    p = Perfil.criar_perfil(self.user.email, nome_usuario, imagem)
                    p.put()
                else:
                    p = Perfil.criar_perfil(self.user.email, nome_usuario, imagem="vazia")
                    p.put()
                self.redirect('/blog/front')




        
class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if not email:
            msg = 'Invalid e-mail'
            self.render('principal.html', error = msg)
        else:
            u = User.login(email, password)
            if u:
                self.login(u)
                self.redirect('/blog/front', email)
            else:
                msg = 'Invalid login'
                self.render('principal.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')


            
            

class PagBlog(BlogHandler):
    def get(self,b):
        if self.user:
            b=self.request.get("b")
        else:
            self.redirect('/')
            
                
        posts =  db.GqlQuery("select * from postagem where endereco='%s'" %b)

     
        self.render('rosto.html', posts = posts, endereco=b)

    
class PagPerfil(BlogHandler):
    def get(self, profile):
        if self.user:
            profile=self.request.get("profile")
            
            blogs=[]
            b = db.GqlQuery("select * from blog where autor='%s'" %profile)

            
            
            self.render("profile.html", nome_perfil=profile, blogs=b )
        else:
            self.redirect("/")
#
class PL(BlogHandler):
    def get(self, l):
        if self.user:
            link=self.request.get("l")
            posts = db.GqlQuery("select * from postagem where link='%s'" %link)
            self.render("permalink.html", posts=posts)
        else:
            self.redirect("/")
#            
            
            

app = webapp2.WSGIApplication([('/', PagInicial),
                               ('/perma?([a-zA-Z0-9_-])', PL),
                               ('/blog/front',BlogFront),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/Perfil?([a-zA-Z0-9_-])',PagPerfil),
                               ('/modificar', Alterar_Perfil),
                               ('/new_blog?([a-zA-Z0-9_-])', NovoBlog),
                               ('/post?([a-zA-Z0-9_-])', NovaPostagem),
                               ('/novo_perfil', NovoPerfil),
                               ('/view?([a-zA-Z0-9_-])', PagBlog),
                               ],
                              debug=True)




    
class Perfil(db.Model):
    nome_usuario=db.StringProperty(required = True)
    ultimo_acesso=db.DateTimeProperty(auto_now = True)
    imagem=db.StringProperty(required = True)
    owner=db.StringProperty(required = True)
    
    @classmethod
    def criar_perfil(cls, owner, nome, imagem):
        return Perfil(nome_usuario = nome,
                    imagem = imagem,
                    owner=owner)
     

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('nome_usuario =', name).get()
        return u
    
    @classmethod    
    def alterar_imagem(cls, imagem, owner):
        updated = []
        
        per =  db.GqlQuery("select * from Perfil where owner='%s'" %owner)
        for p in per.fetch(100):
            p.imagem=imagem
            updated.append(p)
        return db.put(updated)

    def render(self):
        self._render_text = self.nome_usuario.replace('\n', '<br>')
        return render_str("miniperfil.html", nome_usuario = self.nome_usuario, imagem=self.imagem)
        


        
        
    
    
class blog(db.Model):
    endereco=db.StringProperty(required = True)
    nome=db.StringProperty(required = True)
    autor=db.StringProperty(required = True)
    owner=db.StringProperty(required = True)
    
    @classmethod
    def criar_blog (cls,b):
        endereco=str(b.owner)+str(b.key().id())        
        updated = []
        #q = db.GqlQuery("SELECT * FROM blog WHERE __key__='%s'" %b.key())  # nao funciona pois a entidade __key__ nao eh considerada string
        
        for entity in blog.all().filter("__key__", b.key()).fetch(100):
            entity.endereco = endereco
            updated.append(entity)
        return db.put(updated)
        
    def render(self):
        self._render_text = self.nome.replace('\n', '<br>')
        return render_str("miniblog.html", nome = self.nome, autor=self.autor, endereco=self.endereco)
        
    
class postagem(db.Model):
    link=db.StringProperty(required = True)
    titulo=db.StringProperty(required = True)
    conteudo=db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    n_views = db.IntegerProperty(required = True)
    n_likes = db.IntegerProperty(required = True)
    n_shares = db.IntegerProperty(required = True)
    link_coments=db.StringProperty(required = True)
    endereco=db.StringProperty(required = True)
    
    @classmethod
    def criar_post (cls,p):
        link=str(p.endereco)+str(p.key().id())        
        updated = []
        #q = db.GqlQuery("SELECT * FROM blog WHERE __key__='%s'" %b.key())  # nao funciona pois a entidade __key__ nao eh considerada string
        
        for entity in postagem.all().filter("__key__", p.key()).fetch(100):
            entity.link = link
            updated.append(entity)
        return db.put(updated)
    
    
    @classmethod    
    def like(cls, link):
        updated = []
        
        pos =  db.GqlQuery("select * from postagem where link='%s'" %link)
        for p in pos.fetch(100):
            p.n_likes=p.n_likes + 1
            updated.append(p)
        return db.put(updated)
    
    @classmethod    
    def view(cls, link):
        updated = []
        
        pos =  db.GqlQuery("select * from postagem where link='%s'" %link)
        for p in pos.fetch(100):
            p.n_views=p.n_views + 1
            updated.append(p)
        return db.put(updated)
        
        
    @classmethod    
    def share(cls, link):
        updated = []
        
        pos =  db.GqlQuery("select * from postagem where link='%s'" %link)
        for p in pos.fetch(100):
            p.n_shares=p.n_shares + 1
            updated.append(p)
        return db.put(updated)
    

    def render(self):
        self._render_text = self.conteudo.replace('\n', '<br>')
        return render_str("post.html", p = self)