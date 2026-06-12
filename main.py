"""
Main application for justInvest system prototype
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.user_enrollment import UserEnrollment
from src.user_login import UserLogin
from src.access_control import AccessControl
from src.password_manager import PasswordManager
from src.common import load_weak_passwords


def main_menu():
    """Display main menu"""
    print("\n" + "=" * 50)
    print("justInvest System Prototype")
    print("=" * 50)
    print("1. Enroll New User")
    print("2. Login")
    print("3. Run Tests")
    print("4. View All Users")
    print("5. Add Weak Password")
    print("6. Exit")
    print("=" * 50)

    try:
        choice = int(input("\nEnter your choice (1-6): "))
        return choice
    except ValueError:
        print("Please enter a valid number")
        return None


def run_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Running Comprehensive Tests")
    print("=" * 60)

    # Test enrollment and password checker
    print("\n1. Testing Enrollment and Password Checker...")
    enrollment = UserEnrollment()
    passed1, failed1 = enrollment.test_proactive_password_checker()

    # Test login and access control
    print("\n2. Testing Login and Access Control...")
    login = UserLogin()
    passed2, failed2 = login.test_login_scenarios()

    # Test access control directly
    print("\n3. Testing Access Control Matrix...")
    access_control = AccessControl()
    test_cases = [
        ("Client", 1, True, "Client can view balance"),
        ("Client", 3, False, "Client cannot modify portfolio"),
        ("Premium Client", 3, True, "Premium client can modify portfolio"),
        ("Financial Advisor", 7, True, "FA can view private instruments"),
        ("Financial Planner", 6, True, "FP can view money market"),
        ("Financial Planner", 4, False, "FP cannot view FA contact"),
    ]

    passed3 = 0
    failed3 = 0

    for role, operation, should_allow, description in test_cases:
        allowed = access_control.can_perform_operation(role, operation, check_time=False)

        if allowed == should_allow:
            status = "✓ PASS"
            passed3 += 1
        else:
            status = "✗ FAIL"
            failed3 += 1

        print(f"\nTest: {description}")
        print(f"Role: {role}, Operation: {operation}")
        print(f"Expected: {'Allowed' if should_allow else 'Denied'}")
        print(f"Actual: {'Allowed' if allowed else 'Denied'}")
        print(f"Status: {status}")

    # Summary
    total_passed = passed1 + passed2 + passed3
    total_failed = failed1 + failed2 + failed3

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Password Checker Tests: {passed1} passed, {failed1} failed")
    print(f"Login Tests: {passed2} passed, {failed2} failed")
    print(f"Access Control Tests: {passed3} passed, {failed3} failed")
    print("-" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print("=" * 60)

    return total_passed, total_failed


def main():
    """Main application loop"""

    # Create necessary directories
    os.makedirs("data", exist_ok=True)

    # Initialize components
    enrollment = UserEnrollment()
    login = UserLogin()
    password_manager = PasswordManager()

    while True:
        choice = main_menu()

        if choice == 1:
            # Enroll new user
            enrollment.display_signup_interface()

        elif choice == 2:
            # Login
            success, user_data, allowed_ops = login.display_login_interface()
            if success and allowed_ops:
                login.simulate_operation_selection(
                    user_data['username'],
                    user_data['role'],
                    allowed_ops
                )

        elif choice == 3:
            # Run tests
            run_tests()

        elif choice == 4:
            # View all users
            users = password_manager.get_all_users()
            print("\n" + "=" * 50)
            print("Registered Users")
            print("=" * 50)
            if not users:
                print("No users registered yet.")
            else:
                for user in users:
                    print(f"Username: {user['username']}")
                    print(f"Role: {user['role']}")
                    print(f"Created: {user['created_at']}")
                    print("-" * 30)

        elif choice == 5:
            # Add weak password
            weak_pwd = input("\nEnter password to add to weak list: ").strip()
            if weak_pwd:
                password_manager.add_weak_password(weak_pwd)
                print(f"✓ Added '{weak_pwd}' to weak passwords list")

        elif choice == 6:
            # Exit
            print("\nThank you for using justInvest System. Goodbye!")
            break

        elif choice is None:
            continue

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()