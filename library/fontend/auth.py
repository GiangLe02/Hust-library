from pickle import FALSE
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import SinhVien
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emailSV = request.form.get('email')
        password = request.form.get('password')

        sinhVien = SinhVien.query.filter_by(EmailSV=emailSV).first()
        # print(str(sinhVien.MSSV), type(str(sinhVien.MSSV)))
        # print(password, type(password))
        # print(check_password_hash(str(sinhVien.MSSV),password))
        if sinhVien:
            if check_password_hash(str(sinhVien.MSSV),password):
                flash('Logged in successfully!', category='success')
                login_user(sinhVien, remember=True)
                #remember the the member has already logged in 
                print(str(sinhVien.MSSV))
                return redirect(url_for('views.home', _external=True, _scheme='https'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", sinhVien=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        emailSV = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = SinhVien.query.filter_by(emailSV = emailSV).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(emailSV) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = SinhVien(emailSV=emailSV, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)