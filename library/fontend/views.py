#in the views.py  inside the website folder
from flask import Blueprint, render_template

#Blueprint: have a lot of routes (URLs)
views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template("home.html")
