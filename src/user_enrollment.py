"""
User enrollment with proactive password checking
"""
from .password_manager import PasswordManager
from .common import ROLES, validate_username, ALLOWED_SPECIAL_CHARS


class UserEnrollment:
    def __init__(self):
        self.password_manager = PasswordManager()

    def display_signup_interface(self):
        """
        Simple signup user interface
        """
        print("\n" + "=" * 50)
        print("justInvest - New User Enrollment")
        print("=" * 50)

        # Get username
        while True:
            username = input("Enter username: ").strip()
            is_valid, message = validate_username(username)
            if is_valid:
                # Check if username already exists
                if self.password_manager.user_exists(username):
                    print(f"Error: Username '{username}' already exists. Please choose another.")
                else:
                    break
            else:
                print(f"Error: {message}")

        # Get password
        while True:
            print("\nPassword Requirements:")
            print(f"- 8 to 12 characters")
            print(f"- At least one uppercase letter")
            print(f"- At least one lowercase letter")
            print(f"- At least one digit (0-9)")
            print(f"- At least one special character: {ALLOWED_SPECIAL_CHARS}")
            print("- Cannot be the same as username")
            print("- Cannot be a common/weak password")

            password = input("\nEnter password: ").strip()
            confirm = input("Confirm password: ").strip()

            if password != confirm:
                print("Error: Passwords do not match. Please try again.")
                continue

            # Validate password policy
            is_valid, message = self.password_manager.validate_password_policy(username, password)
            if not is_valid:
                print(f"Error: {message}")
                continue

            # Password meets all requirements
            break

        # Get role
        print("\nAvailable Roles:")
        role_options = list(ROLES.values())
        for i, role in enumerate(role_options, 1):
            print(f"{i}. {role}")

        while True:
            try:
                choice = int(input(f"\nSelect role (1-{len(role_options)}): "))
                if 1 <= choice <= len(role_options):
                    selected_role = role_options[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(role_options)}")
            except ValueError:
                print("Please enter a valid number")

        # Confirm enrollment
        print("\n" + "=" * 50)
        print("Enrollment Summary:")
        print(f"Username: {username}")
        print(f"Role: {selected_role}")
        print("=" * 50)

        confirm = input("\nConfirm enrollment? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            # Add user to password file
            success, message = self.password_manager.add_user(username, selected_role, password)
            if success:
                print(f"\n✓ {message}")
                print("✓ Enrollment completed successfully!")
                return True, username, selected_role
            else:
                print(f"\n✗ Error: {message}")
                return False, None, None
        else:
            print("\nEnrollment cancelled.")
            return False, None, None

    def test_proactive_password_checker(self):
        """
        Test the proactive password checker
        """
        test_cases = [
            # (password, username, should_pass, reason)
            ("Short1!", "user1", False, "Too short"),
            ("ValidPass123!", "user2", True, "Valid password"),
            ("nouppercase123!", "user3", False, "No uppercase"),
            ("NOLOWERCASE123!", "user4", False, "No lowercase"),
            ("NoDigitsHere!", "user5", False, "No digits"),
            ("NoSpecial123", "user6", False, "No special chars"),
            ("user7user7", "user7", False, "Same as username"),
            ("password", "user8", False, "Common weak password"),
            ("ThisIsTooLong123!", "user9", False, "Too long"),
        ]

        print("\n" + "=" * 60)
        print("Testing Proactive Password Checker")
        print("=" * 60)

        passed_tests = 0
        failed_tests = 0

        for password, username, should_pass, reason in test_cases:
            is_valid, message = self.password_manager.validate_password_policy(username, password)

            if (should_pass and is_valid) or (not should_pass and not is_valid):
                status = "✓ PASS"
                passed_tests += 1
            else:
                status = "✗ FAIL"
                failed_tests += 1

            print(f"\nTest: {reason}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Expected: {'Accept' if should_pass else 'Reject'}")
            print(f"Actual: {'Accept' if is_valid else 'Reject'}")
            if not is_valid:
                print(f"Reason: {message}")
            print(f"Status: {status}")

        print("\n" + "=" * 60)
        print(f"Test Results: {passed_tests} passed, {failed_tests} failed")
        print("=" * 60)

        return passed_tests, failed_tests