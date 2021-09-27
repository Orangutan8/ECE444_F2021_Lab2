from flask import Flask, render_template, flash, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import re
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Regexp
from wtforms.validators import Email

class NameForm(Form):    
    name = StringField('What is your name?', validators=[DataRequired()])    
    email=StringField("What is your UofT Email address?", validators=[DataRequired(), Email()])#I bet I could have done this like I tried below. It seemed hard to have a good regex for email and also check for utoronto though.
    #email=StringField("What is your UofT Email address?", validators=[DataRequired(), Regexp(".*@.*\.utoronto\.ca"), Email()])#I think this is fine but I'm worried about the @utoronto.ca case, is it real? Is it not? I have no idea
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am a hacker now :)'
bootstrap=Bootstrap(app)
moment=Moment(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        if(re.match(".*@.*\.utoronto\.ca", form.email.data)):
            session['email']=form.email.data
        else:
            session['email']="INVALID_EMAIL"
        return redirect(url_for('index'))
    #else:
        #session['email']=""
        #return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form = form, name = session.get('name'), email=session.get('email'))
    #return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__=='__main__':
    app.run(debug=True)
