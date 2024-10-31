import sys


from flask import Blueprint,render_template
index=Blueprint('index' ,__name__)
@index.route('/')
def home():
    return render_template('index.html')
@index.route('/about')
def about():
	return render_template('about.html')