"""
Password file management with secure hashing
"""
import hashlib
import secrets
import os
from datetime import datetime
from .common import validate_username, load_weak_passwords, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH


class PasswordManager:
    def __init__(self, password_file="data/passwd.txt"):
        self.password_file = password_file
        self.weak_passwords = load_weak_passwords()

    def _generate_salt(self, length=16):
        """Generate cryptographically secure salt"""
        return secrets.token_hex(length)

    def _hash_password(self, password, salt):
        """
        Hash password using PBKDF2-HMAC-SHA256
        This is a secure key derivation function
        """
        # Use PBKDF2 with 100,000 iterations (NIST recommended)
        iterations = 100000
        dk = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        )
        return dk.hex()

    def _parse_record(self, record):
        """Parse a password file record"""
        parts = record.strip().split(':')
        if len(parts) != 5:
            return None

        return {
            'username': parts[0],
            'role': parts[1],
            'salt': parts[2],
            'hashed_password': parts[3],
            'created_at': parts[4]
        }

    def _format_record(self, username, role, salt, hashed_password):
        """Format a record for storage"""
        created_at = datetime.now().isoformat()
        return f"{username}:{role}:{salt}:{hashed_password}:{created_at}\n"

    def add_user(self, username, role, password):
        """
        Add a new user to the password file
        """
        # Validate username
        is_valid, message = validate_username(username)
        if not is_valid:
            return False, message

        # Check if user already exists
        if self.user_exists(username):
            return False, f"User '{username}' already exists"

        # Generate salt and hash password
        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt)

        # Format and write record
        record = self._format_record(username, role, salt, hashed_password)

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.password_file), exist_ok=True)

        # Append to password file
        with open(self.password_file, 'a') as f:
            f.write(record)

        return True, f"User '{username}' added successfully"

    def verify_user(self, username, password):
        """
        Verify user credentials
        Returns (success, message, user_data)
        """
        # Check if user exists
        user_record = self._find_user(username)
        if not user_record:
            return False, "Invalid username or password", None

        # Hash provided password with stored salt
        test_hash = self._hash_password(password, user_record['salt'])

        # Compare hashes
        if test_hash == user_record['hashed_password']:
            return True, "Authentication successful", user_record
        else:
            return False, "Invalid username or password", None

    def user_exists(self, username):
        """Check if a user exists in the password file"""
        return self._find_user(username) is not None

    def _find_user(self, username):
        """Find a user record by username"""
        if not os.path.exists(self.password_file):
            return None

        with open(self.password_file, 'r') as f:
            for line in f:
                record = self._parse_record(line)
                if record and record['username'] == username:
                    return record

        return None

    def get_all_users(self):
        """Get all user records"""
        users = []
        if not os.path.exists(self.password_file):
            return users

        with open(self.password_file, 'r') as f:
            for line in f:
                record = self._parse_record(line)
                if record:
                    users.append(record)

        return users

    def validate_password_policy(self, username, password):
        """
        Validate password against policy
        Returns (is_valid, error_message)
        """
        # Check length
        if len(password) < MIN_PASSWORD_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
            return False, f"Password must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH} characters"

        # Check character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%*&" for c in password)

        if not all([has_upper, has_lower, has_digit, has_special]):
            return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%*&)"

        # Check if password matches username
        if password.lower() == username.lower():
            return False, "Password cannot be the same as username"

        # Check against weak passwords list
        if password in self.weak_passwords:
            return False, "Password is too common/weak. Please choose a different password"

        return True, "Password meets policy requirements"

    def add_weak_password(self, password):
        """Add a password to the weak passwords list"""
        self.weak_passwords.add(password)

        # Update the file
        weak_file = "data/weak_passwords.txt"
        os.makedirs(os.path.dirname(weak_file), exist_ok=True)

        with open(weak_file, 'a') as f:
            f.write(password + "\n")

        return True