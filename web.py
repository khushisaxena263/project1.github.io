from email.message import Message
from hashlib import sha256
from flask import Flask,render_template,request, url_for, redirect,session,logging,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail, Message
from sqlalchemy.orm import scoped_session,sessionmaker
from itsdangerous import URLSafeTimedSerializer,SignatureExpired


app=Flask(__name__)




mail=Mail(app)

engine=create_engine('mysql://root:@localhost/website1')
db=scoped_session(sessionmaker(bind=engine))
app.secret_key="login"


s=URLSafeTimedSerializer('thisissecrete')

@app.route("/")
def Hello():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def test():

    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        repass=request.form.get('confPassword')
        usernamedata=db.execute("SELECT email FROM Log WHERE email=:email",{"email":email}).fetchone()
        try:
            if usernamedata==None:
                if password==repass:
                    db.execute("INSERT INTO Log(name,email,password) VALUES(:name,:email,:password)",{'name':name,'email':email,'password':password})
                    db.commit()
                    return render_template('login.html')
                else:
                    flash('password does not match','danger')
                    return render_template('register.html')
            else:
                flash('user already existed, please login or contact admin','danger')
                return render_template('login.html')
        except Exception:
            return render_template('index.html')
    return render_template('register.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email1=request.form.get('emaillog')
        password1=request.form.get('passwordlog')

        usernamedata=db.execute("SELECT email FROM Log WHERE email=:email",{"email":email1}).fetchone()
        passworddata=db.execute("SELECT password FROM Log WHERE password=:password",{"password":password1}).fetchone()
        if usernamedata is None:
            flash('NO username','danger')
            return render_template('register.html')
        else:
            try:
                for passwor_data in passworddata:
                    if passwor_data==password1:
                        flash('successfully logging')
                        return render_template('after-login.html')
            except Exception:
                    return render_template('login.html')
    return render_template('login.html')


@app.route("/logout")
def logout():
    return render_template('login.html')


app.run(debug=True) 