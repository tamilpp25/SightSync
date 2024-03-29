from flask import Flask, send_from_directory, jsonify,redirect,url_for,render_template,request
import os
from flask_login import UserMixin,LoginManager,login_user,current_user, logout_user, login_required
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo

app = Flask(__name__)

app.config['SECRET_KEY']  = "mysecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return signup.query.get(id)



class signup(db.Model,UserMixin):
    
    __tablename__ = "signup"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    GuardianName = db.Column(db.String)
    UserName = db.Column(db.String)
    
    def __init__(self,email,password,GuardianName,UserName):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.GuardianName = GuardianName
        self.UserName = UserName
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class SignupForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    guardianName = StringField("Guardian Name ")
    userName = StringField("User's Name ")
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_pass',message='Password doesnot match')])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("SignUp")
    
    def validate_email(self,field):
        if signup.query.filter_by(email=field.data).first():
            flash("This Email has already been registered")
            raise ValidationError("Email is already registered")
        
class LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/')
def index():
    return redirect(url_for('login'))        

@app.route('/gps_coordinates')
def gps_coordinates():
    latitude = 12.970946
    longitude = 79.163305
    return jsonify({'latitude': latitude, 'longitude': longitude})

# @login_required
# @app.route('/test')
# def test():
#     return send_from_directory('.', 'index.html')


@app.route('/signup',methods=['GET','POST'])
def Signup():
    
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        guardianName = form.guardianName.data
        userName = form.userName.data
        user = signup(email,password,guardianName,userName)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = signup.query.filter_by(email = form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next==None or not next[0]=='/':
                    next = url_for('map')
                return redirect(next)
            else:
                flash("Password is incorrect")
    return render_template('login.html',form=form)


@app.route('/map')
@login_required
def map():
    guardianName = current_user.GuardianName
    return render_template('index.html',guardianName=guardianName)


@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)