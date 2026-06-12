"""
Common utilities and constants for the justInvest system
"""
from datetime import datetime, time
import json
import os

# User roles
ROLES = {
    "client": "Client",
    "premium_client": "Premium Client",
    "financial_advisor": "Financial Advisor",
    "financial_planner": "Financial Planner",
    "teller": "Teller"
}

# System operations (numbered as in assignment)
OPERATIONS = {
    1: "View account balance",
    2: "View investment portfolio",
    3: "Modify investment portfolio",
    4: "View Financial Advisor contact info",
    5: "View Financial Planner contact info",
    6: "View money market instruments",
    7: "View private consumer instruments"
}

# Role-based access control matrix
RBAC_MATRIX = {
    ROLES["client"]: [1, 2, 4],  # Operations 1, 2, 4
    ROLES["premium_client"]: [1, 2, 3, 5],  # Operations 1, 2, 3, 5
    ROLES["financial_advisor"]: [1, 2, 3, 4, 7],  # Operations 1, 2, 3, 4, 7
    ROLES["financial_planner"]: [1, 2, 3, 5, 6, 7],  # Operations 1, 2, 3, 5, 6, 7
    ROLES["teller"]: [1, 2]  # Operations 1, 2 (time-restricted)
}

# Business hours (9am to 5pm)
BUSINESS_HOURS = {
    "start": time(9, 0, 0),  # 9:00 AM
    "end": time(17, 0, 0)  # 5:00 PM
}

# Special characters allowed in passwords
ALLOWED_SPECIAL_CHARS = "!@#$%*&"

# Password policy constants
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 12


def is_within_business_hours():
    """
    Check if current time is within business hours (9am-5pm)
    Returns True if within business hours, False otherwise
    """
    current_time = datetime.now().time()
    return BUSINESS_HOURS["start"] <= current_time <= BUSINESS_HOURS["end"]


def get_operations_for_role(role, check_time=True):
    """
    Get list of allowed operations for a given role
    """
    operations = RBAC_MATRIX.get(role, [])

    # Apply time restriction for Tellers
    if role == ROLES["teller"] and check_time and not is_within_business_hours():
        return []  # No access outside business hours

    return operations


def display_operations(operations):
    """
    Display operations in a user-friendly format
    """
    if not operations:
        print("No operations available at this time.")
        return

    print("\n" + "=" * 50)
    print("Available Operations:")
    print("=" * 50)
    for op_num in sorted(operations):
        print(f"{op_num}. {OPERATIONS[op_num]}")
    print("=" * 50)


def validate_username(username):
    """
    Validate username format
    """
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if ':' in username:
        return False, "Username cannot contain ':' character"

    return True, ""


def load_weak_passwords(file_path="data/weak_passwords.txt"):
    """
    Load list of weak passwords from file
    """
    weak_passwords = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                password = line.strip()
                if password:
                    weak_passwords.add(password)
    except FileNotFoundError:
        # Create default weak passwords file
        default_weak = [
            "password", "12345678", "qwerty123", "admin123",
            "letmein", "welcome", "password123", "abc123"
        ]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            for pwd in default_weak:
                f.write(pwd + "\n")
        weak_passwords = set(default_weak)

    return weak_passwords