from flask_login import current_user, login_user, logout_user
from flask import request
from werkzeug.urls import url_parse
import models
from app import app

@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    #The current_user variable comes from Flask_Login
    #This if statement is designed to redirect user to home pg if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('frontPage')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('logIn'))


