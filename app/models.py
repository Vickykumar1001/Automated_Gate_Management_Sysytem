from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    gate_no = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "status": self.status,
            "gate_no": self.gate_no
        }
        
    # def __repr__(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "email": self.email,
    #         "phone_number": self.phone_number,
    #         "role": self.role,
    #         "status": self.status,
    #         "gate_no": self.gate_no
    #     }
