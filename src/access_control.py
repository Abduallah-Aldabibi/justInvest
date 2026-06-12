"""
Access Control Mechanism using RBAC
"""
from .common import ROLES, get_operations_for_role, display_operations


class AccessControl:
    def __init__(self):
        self.roles_permissions = {
            ROLES["client"]: [1, 2, 4],
            ROLES["premium_client"]: [1, 2, 3, 5],
            ROLES["financial_advisor"]: [1, 2, 3, 4, 7],
            ROLES["financial_planner"]: [1, 2, 3, 5, 6, 7],
            ROLES["teller"]: [1, 2]
        }

    def can_perform_operation(self, role, operation_number, check_time=True):
        """
        Check if a role can perform a specific operation
        """
        allowed_ops = get_operations_for_role(role, check_time)
        return operation_number in allowed_ops

    def get_allowed_operations(self, role, check_time=True):
        """
        Get all allowed operations for a role
        """
        return get_operations_for_role(role, check_time)

    def display_user_permissions(self, username, role):
        """
        Display user permissions in a formatted way
        """
        allowed_ops = self.get_allowed_operations(role)

        print("\n" + "=" * 60)
        print(f"ACCESS GRANTED!")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Role: {role}")

        if allowed_ops:
            ops_str = ", ".join(str(op) for op in sorted(allowed_ops))
            print(f"Authorized operations: {ops_str}")
            print("\nOperations available:")
            for op_num in sorted(allowed_ops):
                from .common import OPERATIONS
                print(f"  {op_num}. {OPERATIONS[op_num]}")
        else:
            print("No operations available at this time.")
            if role == ROLES["teller"]:
                print("Reason: Outside business hours (9:00 AM - 5:00 PM)")

        print("=" * 60)
        return allowed_ops

    def validate_access(self, username, role, operation_number):
        """
        Validate if a user can perform an operation
        Returns (allowed, message)
        """
        allowed = self.can_perform_operation(role, operation_number)

        if allowed:
            return True, f"User '{username}' is allowed to perform operation {operation_number}"
        else:
            from .common import OPERATIONS
            op_name = OPERATIONS.get(operation_number, f"Operation {operation_number}")

            if role == ROLES["teller"]:
                from .common import is_within_business_hours
                if not is_within_business_hours():
                    return False, f"Tellers can only access the system during business hours (9:00 AM - 5:00 PM)"

            return False, f"User '{username}' with role '{role}' is not authorized to {op_name.lower()}"