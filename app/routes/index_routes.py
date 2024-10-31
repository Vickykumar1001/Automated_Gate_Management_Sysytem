import sys

sys.path.insert(0, r"F:\DevSphere\ANPR\app\routes")

from number_recognition import detect_license_plate_from_url


from flask import Blueprint,render_template
index=Blueprint('index' ,__name__)
@index.route('/')
def home():
    number=detect_license_plate_from_url("https://res.cloudinary.com/dlpdm7vye/image/upload/v1730303357/vehicle-database/kdv2kigd3cnwkkobrk68.webp")
    return render_template('index.html',number=number)
@index.route('/about')
def about():
	return render_template('about.html')