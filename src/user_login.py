"""
User login and access control display
"""
from .password_manager import PasswordManager
from .access_control import AccessControl
from .common import display_operations


class UserLogin:
    def __init__(self):
        self.password_manager = PasswordManager()
        self.access_control = AccessControl()

    def display_login_interface(self):
        """
        Simple login user interface
        """
        print("\n" + "=" * 50)
        print("justInvest System")
        print("=" * 50)

        # Show available operations (for reference)
        from .common import OPERATIONS
        print("\nOperations available on the system:")
        for op_num, op_name in sorted(OPERATIONS.items()):
            print(f"{op_num}. {op_name}")

        # Get credentials
        print("\n" + "-" * 50)
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        # Verify credentials
        success, message, user_data = self.password_manager.verify_user(username, password)

        if success:
            print("\n" + "=" * 50)
            print("ACCESS GRANTED!")
            print("=" * 50)

            # Display user permissions
            allowed_ops = self.access_control.display_user_permissions(
                user_data['username'],
                user_data['role']
            )

            return True, user_data, allowed_ops
        else:
            print(f"\n✗ ACCESS DENIED: {message}")
            return False, None, None

    def simulate_operation_selection(self, username, role, allowed_operations):
        """
        Simulate operation selection after login
        """
        if not allowed_operations:
            print("\nNo operations available. Exiting...")
            return

        while True:
            try:
                print("\n" + "-" * 50)
                operation = input("Which operation would you like to perform? (Enter number, or 'q' to quit): ").strip()

                if operation.lower() == 'q':
                    print("Goodbye!")
                    break

                operation_num = int(operation)

                # Check if operation is allowed
                allowed, message = self.access_control.validate_access(username, role, operation_num)

                if allowed:
                    from .common import OPERATIONS
                    op_name = OPERATIONS.get(operation_num, f"Operation {operation_num}")
                    print(f"\n✓ Executing: {op_name}")
                    print("✓ Operation completed successfully!")
                else:
                    print(f"\n✗ {message}")

            except ValueError:
                print("Please enter a valid operation number or 'q' to quit")

    def test_login_scenarios(self):
        """
        Test various login scenarios
        """
        test_users = [
            # Pre-populated test users
            {"username": "sasha_kim", "role": "Client", "password": "ValidPass1!"},
            {"username": "noor_abbasi", "role": "Premium Client", "password": "Premium123!"},
            {"username": "mikael_chen", "role": "Financial Advisor", "password": "Advisor123!"},
            {"username": "ellis_nakamura", "role": "Financial Planner", "password": "Planner123!"},
            {"username": "alex_hayes", "role": "Teller", "password": "Teller123!"},
        ]

        print("\n" + "=" * 60)
        print("Testing Login and Access Control")
        print("=" * 60)

        # First, add test users if they don't exist
        password_manager = PasswordManager()
        for user in test_users:
            if not password_manager.user_exists(user["username"]):
                password_manager.add_user(
                    user["username"],
                    user["role"],
                    user["password"]
                )

        test_scenarios = [
            # (username, password, should_succeed, description)
            ("sasha_kim", "ValidPass1!", True, "Valid client login"),
            ("sasha_kim", "wrongpass", False, "Wrong password"),
            ("nonexistent", "somepass", False, "Non-existent user"),
            ("noor_abbasi", "Premium123!", True, "Valid premium client login"),
            ("mikael_chen", "Advisor123!", True, "Valid financial advisor login"),
            ("ellis_nakamura", "Planner123!", True, "Valid financial planner login"),
            ("alex_hayes", "Teller123!", True, "Valid teller login"),
        ]

        passed = 0
        failed = 0

        for username, password, should_succeed, description in test_scenarios:
            print(f"\nTest: {description}")
            print(f"Username: {username}")

            success, message, _ = password_manager.verify_user(username, password)

            if (should_succeed and success) or (not should_succeed and not success):
                status = "✓ PASS"
                passed += 1
            else:
                status = "✗ FAIL"
                failed += 1

            print(f"Expected: {'Success' if should_succeed else 'Failure'}")
            print(f"Actual: {'Success' if success else 'Failure'}")
            if not success and message:
                print(f"Message: {message}")
            print(f"Status: {status}")

        print("\n" + "=" * 60)
        print(f"Test Results: {passed} passed, {failed} failed")
        print("=" * 60)

        return passed, failed