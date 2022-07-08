#in the models.py  inside the website folder
#Object: database models for users/ notes
from . import db
#import from __init__.py
from flask_login import UserMixin
#helps user login
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class SinhVien(db.Model, UserMixin):
	__tablename__ = 'SinhVien'  # Case sensitive.
	__table_args__ = (
        CheckConstraint('MSSV>=20150000 AND MSSV<=20219999'),
		CheckConstraint('MucCanhBao>=0 AND MucCanhBao<=3'),
		CheckConstraint('GioiTinhSV="Nam" OR GioiTinhSV="Nữ"'),
    )
	MSSV = db.Column(db.Integer, primary_key=True, nullable=False)
	HoTenSV= db.Column(db.String(100, convert_unicode=True), nullable=False)
	GioiTinhSV = db.Column(db.String(3,  convert_unicode=True))
	Vien = db.Column(db.String(100, convert_unicode=True))
	NgaySinhSV = db.Column(db.String(12))
	EmailSV = db.Column(db.String(100), nullable=False)
	MucCanhBao = db.Column(db.Integer)
	def get_id(self):
		return self.MSSV
@hybrid_property
def date(self):
	# @todo: add python parsing of date and time to produce the result
	str_value = self.NgaySinhSV
	return date.strptime(str_value, "%d/%m/%Y")

@date.expression
def date(cls):
	# @note: query specific value
	dt_column =(func.substr(cls.NgaySinhSV, 7) + "-" +
				func.substr(cls.NgaySinhSV, 4, 2) + "-" +
				func.substr(cls.NgaySinhSV, 1, 2) + " " )
	dt_column = func.date(dt_column)
	return dt_column




class NhanVien(db.Model, UserMixin):
	__tablename__ = 'NhanVien'  # Case sensitive.
	__table_args__ = (
		CheckConstraint('GioiTinhNV="Nam" OR GioiTinhNV="Nữ"'),
    )
	MSNV = db.Column(db.Integer, primary_key=True, nullable=False)
	HoTenNV= db.Column(db.String(100,convert_unicode=True),  nullable=False)
	GioiTinhNV = db.Column(db.String(3, convert_unicode=True))
	CMND = db.Column(db.String(12))
	NgaySinhSV = db.Column(db.TEXT)
	EmailNV = db.Column(db.String(100), nullable=False)
def get_id(self):
	return (str(self.MSNV))
class NXB(db.Model):
	__tablename__ = 'NXB' 
	MaNXB = db.Column(db.String(20, convert_unicode=True), primary_key=True, nullable=False)
	TenNXB = db.Column(db.String(100,convert_unicode=True))
class Sach(db.Model):
	__tablename__ = 'Sach' 
	MaSach = db.Column(db.String(20), primary_key=True, nullable=False)
	TenSach = db.Column(db.String(100,convert_unicode=True), nullable=False)
	TenTacGia = db.Column(db.String(100,convert_unicode=True))
	MaNXB = db.Column(db.String(20),db.ForeignKey('NXB.MaNXB'), nullable=False)
	NamXB = db.Column(db.Integer)
	SoTrang = db.Column(db.Integer)
	SoLuongBanDau = db.Column(db.Integer)
	SoLuongDuocMuon = db.Column(db.Integer)
	SoLuongConLai = db.Column(db.Integer)
	LoaiSach = db.Column(db.String(100, convert_unicode=True))


class MuonTraSach(db.Model):
	__tablename__ = 'MuonTraSach' 
	__table_args__ = (
        CheckConstraint('MSSV>=20150000 AND MSSV<=20219999'),
    )
	MaMuon = db.Column(db.Integer,primary_key=True, nullable=False)
	MSSV = db.Column(db.Integer,db.ForeignKey('SinhVien.MSSV'), nullable=False)
	MSNV = db.Column(db.Integer,db.ForeignKey('NhanVien.MSNV'), nullable=False)
	MaSach = db.Column(db.String(20),db.ForeignKey('Sach.MaSach'), nullable=False)
	NgayMuon = db.Column(db.DateTime, default=func.now())
	ThoiHanMuon = db.Column(db.Integer)
	NgayTraSach = db.Column(db.DateTime, default=func.now())
	TinhTrang = db.Column(db.String(100, convert_unicode=True))
