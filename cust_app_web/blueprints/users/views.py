from flask import request, Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from peewee import IntegretyError
from models.user import User
from flask_login import current_user, login_required, logout_user, login_user

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/', methods=['GET'])
@login_required
def index():
    if current_user.is_active:
        return render_template('userpage.html', username=current_user.name)
    else:
        return render_template(url_for('user.login'))

@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    if current_user.is_active:
        return redirect(url_for('home'))
    return render_template('signup form.html')


@users_blueprint.route('/sign_up_form', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    new_user = User(username=username, password=password, email=email)

    try:
        new_user.save():
        flash("Successfully Created")
        login_user(new_user)
        return redirect(url_for("users.show", username=current_user.name))

    except IntegrityError as e:
        if 'username' in str(e):
            return render_template('signup form.html', username=request.form['username'], errors='Username is taken')
        if 'email' in str(e):
            return render_template('signup form.html', email=request.form['email'], errors='Email is taken')

@users_blueprint.route('/sign_in', methods=['GET'])
def sign_in():
    if current_user.is_active:
        return redirect(url_for("users.show", username=current_user.name))
    return render_template('signin form.html')

@users_blueprint.route('/sign_in_form', methods=['POST'])
def user_show():
    current_username = request.form.get('username')
    current_password = request.form.get('password')
    current_person = User.get_or_none(User.name == current_username)

    if current_person != None:
        if current_person.login_validate(current_password):
            login_user(current_person)
            flash('Successfully signed in')
            return redirect(url_for('users.show', username=current_username))
        else:
            return render_template('signin form.html', errors=current_person.errors)
    else:
        flash('Username not found! Please sign up for an account.')
        return render_template('signin form.html')

@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    if current_user.is_active:
        return render_template('userpage.html', username=current_user.name)
    else:
        return render_template(url_for('user.login'))

@users_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('home'))