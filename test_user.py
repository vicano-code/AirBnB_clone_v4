#!/usr/bin/python3
# test_user.py

from models.user import User

# Create a new user
user = User(email="test@example.com", password="password123")
print(user.to_dict())  # Should not include the password

# Check that the password is hashed
assert user.password == User.hash_password("password123")

# Save the user to storage and retrieve it
from models import storage
storage.new(user)
storage.save()

retrieved_user = storage.get('User', user.id)
assert retrieved_user.password == User.hash_password("password123")

