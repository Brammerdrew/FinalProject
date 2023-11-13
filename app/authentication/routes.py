from forms import SignUpForm, LoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            print(email, password)

            user = User(first_name,last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful in your initiation', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed your attempt', 'auth-failed')
    except:
        raise Exception("Invalid form data")
    return render_template('signin.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))





