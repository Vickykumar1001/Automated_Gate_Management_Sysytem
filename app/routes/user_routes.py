from flask import Blueprint,request,render_template,session, jsonify
from flask_sqlalchemy import pagination
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User
user = Blueprint('user', __name__)

@user.route('/users', methods=['GET'])
def get_user():
    # Get the search term, sort order, pagination parameters, role, and status from the request
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort', 'id')  # Default sort by 'id'
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 users per page
    role = request.args.get('role')  # Filter by role
    status = request.args.get('status')  # Filter by status

    # Query the database
    query = User.query

    # Apply search filter if search term is provided
    if search_term:
        query = query.filter(User.email.ilike(f'%{search_term}%'))

    # Apply role filter if provided
    if role:
        query = query.filter(User.role == role)  # Assuming 'role' is a field in User model

    # Apply status filter if provided
    if status:
        query = query.filter(User.status == status)  # Assuming 'status' is a field in User model

    # Apply sorting
    if sort_by in [ 'email', 'id', 'role', 'status']:
        query = query.order_by(getattr(User, sort_by))

    # Correctly apply pagination
    users = query.paginate(page=page, per_page=per_page, error_out=False)

    # Prepare the JSON response
    user_list = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone':user.phone_number,
            'role': user.role,
            'status': user.status,
            'gate':user.gate_no
        } for user in users.items
    ]

    response = {
        'total': users.total,
        'page': users.page,
        'pages': users.pages,
        'per_page': users.per_page,
        'users': user_list
    }

    return jsonify(response), 200  # Return a 200 OK status code

@user.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Fetch the user by ID
    user = User.query.get(user_id)
    
    if user is None:
        # If user not found, return a 404 error
        return jsonify({'error': 'User not found'}), 404

    # Prepare the JSON response with user details
    response = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone':user.phone_number,
        'role': user.role,
        'status': user.status,
        'gate':user.gate_no
    }

    return jsonify(response), 200  # Return a 200 OK status code

@user.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Fetch the user by ID
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Check if the request is made by an admin or the user themselves
    curr_user_id = session.get('user_id')
    if curr_user_id:
        current_user = User.query.get(curr_user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    # Get updated fields from the request
    data = request.get_json()
    
    if 'role' in data:
        user.role = data['role']  # Change user role

    if 'gate_no' in data:
        user.gate_no = data['gate_no']  # Assign gate number

    if 'name' in data:
        user.name = data['name']  # Update name

    if 'email' in data:
        user.email = data['email']  # Update email

    # Add more fields as necessary
    # Handle other user attributes as needed

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Update failed due to integrity error'}), 400

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'gate_no': user.gate_no
        # Return more fields as necessary
    }), 200  # Return a 200 OK status code

@user.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Fetch the user by ID
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    curr_user_id = session.get('user_id')
    if curr_user_id:
        current_user = User.query.get(curr_user_id)

    # Check if the current user has permission to delete (e.g., only admins can delete users)
    if current_user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

@user.route('/users/<int:user_id>/change_password', methods=['PUT'])
def change_password(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    curr_user_id = session.get('user_id')
    if curr_user_id:
        current_user = User.query.get(curr_user_id)
    if current_user.id != user_id:
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    curr_password = data.get('curr_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if not new_password  or not confirm_password:
        return jsonify({'error': 'Please enter new and confirm password'}), 400
    
    if(confirm_password !=  new_password):
        return  jsonify({'error': 'New password and Confirm password do not match'}), 400
    
    if not check_password_hash(current_user.password, curr_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    user.password = generate_password_hash(new_password)  # Ensure you hash the password
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200
