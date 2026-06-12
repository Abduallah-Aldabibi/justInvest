# justInvest System Prototype

A command-line access control prototype for an investment management platform. Implements role-based access control (RBAC), secure password management, and user enrollment with proactive password checking.

## Features

- **User Enrollment** — register users with role assignment and password policy enforcement
- **Secure Authentication** — passwords hashed with PBKDF2-HMAC-SHA256 (100,000 iterations + salt)
- **Role-Based Access Control** — each role has a defined set of permitted operations
- **Proactive Password Checker** — rejects weak, short, or policy-violating passwords at signup
- **Time-Restricted Access** — Teller role is limited to business hours (9:00 AM – 5:00 PM)
- **Built-in Test Suite** — validates password policy, login scenarios, and access control matrix

## Roles & Permissions

| Operation | Client | Premium Client | Financial Advisor | Financial Planner | Teller |
|-----------|:------:|:--------------:|:-----------------:|:-----------------:|:------:|
| View account balance | ✓ | ✓ | ✓ | ✓ | ✓ * |
| View investment portfolio | ✓ | ✓ | ✓ | ✓ | ✓ * |
| Modify investment portfolio | | ✓ | ✓ | ✓ | |
| View Financial Advisor contact info | ✓ | | ✓ | | |
| View Financial Planner contact info | | ✓ | | ✓ | |
| View money market instruments | | | | ✓ | |
| View private consumer instruments | | | ✓ | ✓ | |

\* Teller access is restricted to business hours (9:00 AM – 5:00 PM)

## Password Policy

- 8 to 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit (0–9)
- At least one special character: `!@#$%*&`
- Cannot match the username
- Cannot be a known weak password

## Project Structure

```
justInvest/
├── main.py                  # Entry point and main menu
├── src/
│   ├── common.py            # Shared constants, RBAC matrix, utilities
│   ├── password_manager.py  # Password hashing, storage, and validation
│   ├── user_enrollment.py   # Signup interface and password checker
│   ├── user_login.py        # Login interface and session handling
│   └── access_control.py    # RBAC enforcement
├── data/
│   └── weak_passwords.txt   # List of disallowed passwords
├── requirements.txt
└── .gitignore
```

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/justInvest.git
cd justInvest

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Menu options:
1. **Enroll New User** — create an account with role assignment
2. **Login** — authenticate and access permitted operations
3. **Run Tests** — execute the built-in test suite
4. **View All Users** — list registered users and their roles
5. **Add Weak Password** — append a password to the blocklist
6. **Exit**

## Running Tests

Select option **3** from the main menu to run all tests, which cover:
- Proactive password checker (9 cases)
- Login and authentication scenarios (7 cases)
- Access control matrix validation (6 cases)
