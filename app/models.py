from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name is mandatory
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email is mandatory and must be unique
    password = db.Column(db.String(100), nullable=False)  # Password is mandatory
    phone_number = db.Column(db.String(15), nullable=False)  # Phone number can be stored as a string to accommodate formatting
    role = db.Column(db.String(20), nullable=False)  # Role is mandatory
    status = db.Column(db.String(20), nullable=False)  # Status is mandatory
    gate_no = db.Column(db.Integer, nullable=True)  # Gate number is optional

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "status": self.status,
            "gate_no": self.gate_no  # This will return None if not assigned
        }

    # String representation of the User object
    def __repr__(self):
        return f"<User {self.name} - Role: {self.role}>"
