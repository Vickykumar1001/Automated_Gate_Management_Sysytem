from app.models import User

# Creating dummy data
user1 = User(
    name="John Doe",
    email="johndoe@example.com",
    password="password123",
    phone_number=1234567890,
    role="Admin",
    status="Active",
    gate_no=1
)

user2 = User(
    name="Jane Smith",
    email="janesmith@example.com",
    password="password456",
    phone_number=9876543210,
    role="Guard",
    status="Inactive",
    gate_no=2
)

user3 = User(
    name="Alice Johnson",
    email="alicej@example.com",
    password="password789",
    phone_number=5555555555,
    role="User",
    status="Active",
    gate_no=3
)

# Adding users to the session
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Committing the session to save users in the database
db.session.commit()

print("Dummy data inserted successfully.")
