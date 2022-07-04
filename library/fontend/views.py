#in the views.py  inside the website folder
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import SinhVien, Sach
from . import db
from sqlalchemy import or_
#Blueprint: have a lot of routes (URLs)
views = Blueprint('views', __name__)



@views.route('/')
def home():
	return render_template("home.html",sinhVien=current_user)
@views.route('/404')
def error_404():
    return render_template('404.html'), 404
    
@views.route("/student_info/<int:MSSV>")
@login_required
def student_info(MSSV):
    sinhVien = SinhVien.query.filter_by(MSSV=MSSV).first()

    if not sinhVien:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    return render_template("qlythongtinsv.html", sinhVien=current_user, MSSV=MSSV)
@views.route("/timkiem/<int:MSSV>")
@login_required
def search(MSSV):
    sinhVien = SinhVien.query.filter_by(MSSV=MSSV).first()

    if not sinhVien:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    return render_template("timkiem.html", sinhVien=current_user, MSSV=MSSV)
@views.route("/student_borrow/<int:MSSV>")
@login_required
def student_borrow(MSSV):
    sinhVien = SinhVien.query.filter_by(MSSV=MSSV).first()

    if not sinhVien:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    else:
        query = request.form.get("query")
        # searches in both title and author column to check the like string
        sach = Sach.query.filter(or_(Sach.TenSach.ilike('%{}%'.format(query)), Sach.TenTacGia.ilike('%{}%'.format(query)))).all()
        print(sach)

    return render_template("qlymuontra.html", sinhVien=current_user, MSSV=MSSV, sach = sach, length = len(sach))
