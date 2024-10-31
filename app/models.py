from . import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
    phone_number=db.column(db.Integer,nullable=False)
    role=db.column(db.String, nullable=False)
    status=db.column(db.String, nullable=False)
    gate_no=db.column(db.Integer, nullable=False)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}', {self.role})"
