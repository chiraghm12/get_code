from datetime import datetime
from io import BytesIO
import math
from flask import Flask,render_template,request,session,redirect,send_file
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key' 
app.config['UPLOAD_FOLDER'] = params['codefile-uploadpath']

if(params['local_server']):
    # app.config['MYSQL_HOST'] = params["MYSQL_HOST"]
    # app.config['MYSQL_USER'] = params['MYSQL_USER']
    # app.config['MYSQL_PASSWORD'] = params['MYSQL_PASSWORD']
    # app.config['MYSQL_DB'] = params['MYSQL_DB']
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = params['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)
# db = MySQL(app)

class Contacts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)

class Posts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(120), nullable=True)
    slug = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(80), nullable=False)
    codefilename = db.Column(db.String(200), nullable=False)
    codefiledata = db.Column(db.LargeBinary)


@app.route('/searchbylanguage', methods = ['GET','POST'])
def search_by_language():
    if request.method == 'POST':
        language = request.form.get('search')
        posts = Posts.query.filter_by(language=language).all()
        last = math.ceil(len(posts)/int(params['no_of_posts']))
        page = request.args.get('page')
        if(not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page-1)*int(params['no_of_posts']) : ((page-1)*int(params['no_of_posts']) + int(params['no_of_posts']))]
        if page==1:
            prev = "#"
            next = "/?page="+ str(page+1)
        elif page==last:
            prev = "/?page="+ str(page-1)
            next = "#"
        else:
            prev = "/?page="+ str(page-1)
            next = "/?page="+ str(page+1)
    
        return render_template("searchtext.html", params=params, posts=posts, prev=prev, next=next, language=language)
    else:
        return redirect('/')

@app.route('/searchdate', methods = ['GET','POST'])
def searchdate():
    if request.method == 'POST':
        date = request.form.get('date')
        posts = Posts.query.filter_by(date=date).all()
        last = math.ceil(len(posts)/int(params['no_of_posts']))
        
        page = request.args.get('page')
        if(not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page-1)*int(params['no_of_posts']) : ((page-1)*int(params['no_of_posts']) + int(params['no_of_posts']))]
        if page==1:
            prev = "#"
            next = "/?page="+ str(page+1)
        elif page==last:
            prev = "/?page="+ str(page-1)
            next = "#"
        else:
            prev = "/?page="+ str(page-1)
            next = "/?page="+ str(page+1)
    
        return render_template("searchdate.html", params=params, posts=posts, prev=prev, next=next, date=date)
    else:
        return redirect('/')


@app.route("/")
def index():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    post_with_lang = Posts.query.with_entities(Posts.language).distinct().all()
    # languages = list(post_with_lang)
    # print(type(post_with_lang[0][0]))
    
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']) : ((page-1)*int(params['no_of_posts']) + int(params['no_of_posts']))]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)

    return render_template("index.html", params=params, posts=posts, prev=prev, next=next, page_title="Get Code", options=post_with_lang)

@app.route("/about")
def about():
    return render_template("about.html", params=params, page_title="About")

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    if('user' in session and session['user'] == params['admin-uname']):
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params, posts=posts) 
    
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')
        if( username == params['admin-uname'] and password == params['admin-pass']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params, posts=posts, page_title="Admin Panel") 
        else:
            return render_template("admin.html", params=params, page_title="Admin Panel")
    else:
        return render_template("admin.html", params=params, page_title="Admin Panel")

@app.route("/searchdatedashboardcon", methods = ['GET', 'POST'])
def searchdatedashboardcon():
    if request.method == 'POST':
        date = request.form.get('date')
        posts = Contacts.query.filter_by(date=date).all()
        return render_template("dashboardcontact.html", params=params, posts=posts) 
    else:
        return redirect('/admin', page_title="Admin Panel")

@app.route("/searchtextdashboardcon", methods = ['GET', 'POST'])
def searchtextdashboardcon():
    if request.method == 'POST':
        search = request.form.get('search')
        posts = Contacts.query.filter_by(name=search).all()
        return render_template("dashboardcontact.html", params=params, posts=posts) 
    else:
        return redirect('/admin', page_title="Admin Panel")


@app.route("/searchdatedashboardpos", methods = ['GET', 'POST'])
def searchdatedashboardpos():
    if request.method == 'POST':
        date = request.form.get('date')
        posts = Posts.query.filter_by(date=date).all()
        return render_template("dashboardpost.html", params=params, posts=posts) 
    else:
        return redirect('/admin', page_title="Admin Panel")

@app.route("/searchtextdashboardpos", methods = ['GET', 'POST'])
def searchtextdashboardpos():
    if request.method == 'POST':
        search = request.form.get('search')
        posts = Posts.query.filter_by(lang=search).all()
        return render_template("dashboardpost.html", params=params, posts=posts) 
    else:
        return redirect('/admin', page_title="Admin Panel")

@app.route("/dashboardpost", methods = ['GET', 'POST'])
def dashboardpost():
    posts = Posts.query.all()
    return render_template("dashboardpost.html", params=params, posts=posts)

@app.route("/dashboardcontact", methods = ['GET', 'POST'])
def dashboardcontact():
    posts = Contacts.query.all()
    return render_template("dashboardcontact.html", params=params, posts=posts)

@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html", params=params)

@app.route("/edit/<string:srno>", methods = ['GET', 'POST'])
def edit(srno):
    if('user' in session and session['user'] == params['admin-uname']):
        if(request.method == 'POST'):
            title = request.form.get('title')
            subtitle = request.form.get('subtitle')
            slug = request.form.get('slug')
            codefilename = request.form.get('codefilename')
            lang = request.form.get('lang')
            disc = request.form.get('disc')
            date = datetime.now()

            if srno == '0':
                post = Posts(title=title,subtitle=subtitle,slug=slug,codefilename=codefilename,date=date,lang=lang,disc=disc)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(srno=srno).first()
                post.title = title
                post.subtitle = subtitle
                post.slug = slug
                post.codefilename = codefilename
                post.lang = lang
                post.disc = disc
                post.date = date
                db.session.commit()
                return redirect('/edit/' + srno)
        post = Posts.query.filter_by(srno=srno).first()
        return render_template('edit.html', params=params, post=post)


@app.route("/view/<string:srno>", methods = ['GET', 'POST'])
def view(srno):
    if('user' in session and session['user'] == params['admin-uname']):
        if(request.method == 'POST'):
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            msg = request.form.get('msg')
            date = datetime.now()

            cons = Contacts.query.filter_by(srno=srno).first()
            cons.name = name
            cons.email = email
            cons.phone = phone
            cons.msg = msg
            cons.date = date
            return redirect('/view/' + srno)
        post = Contacts.query.filter_by(srno=srno).first()
        return render_template('view.html', params=params, post=post) 

@app.route("/show/<string:post_slug>", methods=['GET'])
def show(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("show.html", params=params, post=post, page_title=post.title)

@app.route("/post", methods = ['GET', 'POST'])
def post():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        slug = request.form.get('slug')
        lang = request.form.get('lang')
        disc = request.form.get('disc')
        # codefilename = request.form.get('codefilename')
        codefile = request.files['codefile']
        # codefile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(codefile.filename)))

        entry = Posts(name=name, email=email, title=title, slug=slug, subtitle=subtitle, date=datetime.now(), description=disc, language=lang, codefilename=codefile.filename, codefiledata=codefile.read())
        db.session.add(entry)
        db.session.commit()
    
    return render_template("post.html", params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/admin')

@app.route("/delete/<string:srno>", methods = ['GET', 'POST'])
def delete(srno):
    if('user' in session and session['user'] == params['admin-uname']):
        post = Posts.query.filter_by(srno=srno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboardpost')


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = Contacts(name=name, email=email, phone=phone, msg = msg, date = datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html", params=params, page_title="Contact")

@app.route('/download_link/<srno>', methods=['GET', 'POST'])
def download_link(srno):
    down = Posts.query.filter_by(srno=srno).first()
    return send_file(BytesIO(down.codefiledata), download_name=down.codefilename, as_attachment=True)    

# Create the database and the database table
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)