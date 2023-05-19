from flask import Flask,redirect, render_template,request,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, User,Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET_KEY"
app.debug = True
toolbar = DebugToolbarExtension(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    

@app.route('/')
def redirect_register():
    session.clear()
    return redirect('/register')

@app.route('/register', methods = ["GET","POST"])
def register_form():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        hash = bcrypt.generate_password_hash(password)
        hashed_utf8 = hash.decode("utf8")

        new_user = User(username=username,
                        password=hashed_utf8,
                        email = email,
                        first_name = first_name,
                        last_name = last_name)
        
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect('/secret')
    else:
        flash('DIDNT WORK')
        username = form.username.data
        return render_template('register.html', form = form)



@app.route('/login', methods = ["GET","POST"])
def user_login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            session['username'] = u.username
            return redirect("/user/" + username)
        else:
            flash("Please Login")
            return render_template('login-form.html', form = form)
    else:
        return render_template('login-form.html', form = form)
@app.route('/secret')
def secret():
    if session.get('username'):
        
        return redirect('/user/' + session['username'])
    else:
        return "TRY AGAIN"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/user/<username>')
def user_profile(username):
    if session['username'] == username:
        user = User.query.filter_by(username = username).first()
        feeds = Feedback.query.filter_by(user = user).all()
        
        return render_template('user.html', user = user, feeds = feeds)
    else:
        return redirect('/login')
    
@app.route('/user/<username>/feedback/add', methods = ["GET", "POST"])
def addFeed(username):
    
    form = FeedbackForm()
    if session.get('username') and session['username'] == username:
        user = User.query.filter_by(username = username).first()


        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feed =  Feedback(title = title,
                                content = content,
                                user = user)
            
            db.session.add(new_feed)
            db.session.commit()
            return redirect('/user/' + username)
        else:
            return render_template('feedback-form.html', form = form, user = user)
    else:
        return redirect('/login')

@app.route('/feedback/<feedback_id>/update', methods = ["GET","POST"])
def editFeed(feedback_id):
    
    feed = Feedback.query.filter_by(id = feedback_id).first()
    form = FeedbackForm(obj=feed)
    if session.get('username') == feed.user.username:
        if form.validate_on_submit():
            feed.title = form.title.data
            feed.content = form.content.data
            db.session.add(feed)
            db.session.commit()
            return redirect(f"/user/{feed.user.username}")
        else:
            return render_template('edit-feedback-form.html', form = form, user= feed.user, feed = feed)
    else:
        return redirect('/logout')

@app.route('/user/<username>/delete')
def user(username):
    if session.get('username') == username:
        user = User.query.filter_by(username = username).first()
        db.session.delete(user)
        db.session.commit()
        return redirect('/logout')
    
@app.route('/feedback/<feedback_id>/delete', methods = ["GET","POST"])
def deleteFeed(feedback_id):
     
    if Feedback.query.filter_by(id = feedback_id).first() != None:
        feed = Feedback.query.filter_by(id = feedback_id).first()
        if session.get('username') == feed.user.username:
            username = feed.user.username
            db.session.delete(feed)
            db.session.commit()
            return redirect('/user/' + username)
        else:
            return redirect('logout')
    else:
        return redirect('/logout')




 