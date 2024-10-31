from flask import Blueprint,request,render_template,session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User
auth = Blueprint('auth', __name__)

@auth.route('/register',methods=['POST'])
def register():
    data = request.json  # Get JSON data from the request
    
    # Extract data
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone')
    role = data.get('role')
    gate_no = data.get('gate')
    
    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user instance
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        phone_number=phone_number,
        role=role,
        gate_no=gate_no,
        status="pending"
    )

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201
@auth.route('/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from the request
    
    # Get email and password from the form data
    email = data.get('email')
    password = data.get('password')
    
    # Query the database to find the user by email
    user = User.query.filter_by(email=email).first()
    if(user):
        print("User is there")
    # Check if user exists and password is correct
    if user and check_password_hash(user.password, password):
        # Store necessary user details in session
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role
        session['user_status'] = user.status
        session['gate_no'] = user.gate_no
        return jsonify({"message": "User logged in successfully!", "user": {"name": user.name, "role": user.role}}), 200
    else:
        # Return JSON response for failed login
        return jsonify({"error": "User not found or incorrect password"}), 401  # 401 Unauthorized status

@auth.route('/logout')
def logout():
    # Clear all session data on logout
    session.clear()
    # Return JSON response for successful logout
    return jsonify({"message": "User logged out successfully!"}), 200  # 200 OK status