"""
AccessGuard - Enterprise Identity & Access Management Simulator
"""

from datetime import date

# ==============================================================================
# GLOBAL DATA & CONFIGURATION
# ==============================================================================

TOOLS = ["GitHub", "AWS", "Slack", "Jira", "Production Server", "HR Portal", "Figma", "Docker"]
ROLES = ("intern", "developer", "tester", "manager", "admin")

COMPANY_INFO = ("PythonGuruKool", "Pune", 2018, "ISO 27001 Certified")
COMPANY_NAME, COMPANY_LOCATION, COMPANY_YEAR, COMPANY_SECURITY = COMPANY_INFO

ASSIGNED_ROLES = {
    "intern": ["Slack", "Jira"],
    "developer": ["GitHub", "AWS", "Slack", "Jira"],
    "tester": ["Slack", "Jira", "GitHub", "Docker"],
    "manager": ["GitHub", "Slack", "Jira", "AWS", "HR Portal"],
    "admin": ["GitHub", "AWS", "Slack", "Jira", "Production Server", "HR Portal", "Figma", "Docker"]
}

EMPLOYEES = {
    "E101": {"name": "Aarav Sharma", "role": "developer", "access": ["Slack", "Jira", "GitHub", "AWS"]},
    "E102": {"name": "Sneha Patil", "role": "intern", "access": ["Slack", "Jira"]}
}

ACCESS_LOG = [
    ("E101", "GitHub", "Granted", "2025-01-15"),
    ("E102", "AWS", "Denied", "2025-02-10")
]


# ==============================================================================
# CORE MODULE FUNCTIONS
# ==============================================================================

def display_company_banner():
    """Phase 1: Displays company metadata, tools, role mappings, and current employees."""
    print("\n" + "=" * 80)
    print(f"  {COMPANY_NAME} | HQ: {COMPANY_LOCATION} | Est: {COMPANY_YEAR}")
    print(f"  Security Standard: {COMPANY_SECURITY}")
    print("=" * 80)
    print(f"  Total tools available : {len(TOOLS)}")
    print(f"  Valid Roles           : {len(ROLES)}")
    print(f"  Employees registered  : {len(EMPLOYEES)}")
    print("=" * 80)
    print(f"Available Tools: {TOOLS}\n")
    print(f"Valid Roles    : {ROLES}\n")
    
    print("Role permissions:")
    for role_name, perms in ASSIGNED_ROLES.items():
        print(f"  {role_name:<12} --> {perms}")
        
    print("\nExisting Employees:")
    for emp_id, emp_info in EMPLOYEES.items():
        print(f"  {emp_id} | {emp_info['name']:<16} | {emp_info['role']:<10} | Access: {emp_info['access']}")


def onboard_employee():
    """Phase 2: Validates input, onboards a new employee, and provisions default access."""
    print("\n" + "=" * 55)
    print("--- EMPLOYEE ONBOARDING ---")
    print("=" * 55)

    # 1. Name validation
    while True:
        raw_name = input("Enter Name (First and Last only): ").strip().title()
        parts = raw_name.split()
        if len(parts) == 2 and parts[0].isalpha() and parts[1].isalpha():
            first_name, last_name = parts
            full_name = f"{first_name} {last_name}"
            break
        print("Invalid input. Please enter exactly two alphabetic names (e.g., 'Rohan Gupta').")

    # 2. Sequential ID generation
    new_id = f"E10{len(EMPLOYEES) + 1}"
    email_id = f"{first_name.lower()}.{last_name.lower()}@pythongurukool.com"
    temp_pass = f"{first_name[:3]}{new_id[-3:]}@TN"

    # 3. Role assignment
    while True:
        role = input(f"Enter role {ROLES}: ").strip().lower()
        if role in ROLES:
            break
        print(f"Invalid role. Must be one of: {ROLES}")

    # 4. Experience & seniority assessment
    while True:
        exp_input = input("Enter years of experience: ").strip()
        if exp_input.isdigit():
            exp = int(exp_input)
            break
        print("Invalid number. Please enter a non-negative integer.")

    if exp == 0:
        seniority = "Fresher (Mentor assigned)"
    elif 1 <= exp <= 3:
        seniority = "Junior Level"
    elif 4 <= exp <= 7:
        seniority = "Mid Level"
    else:
        seniority = "Senior Level"

    # 5. Independent copy of permissions to prevent master template mutation
    initial_access = ASSIGNED_ROLES[role].copy()

    EMPLOYEES[new_id] = {
        "name": full_name,
        "role": role,
        "access": initial_access
    }

    audit_stamp = str(date.today())
    permanent_record = (new_id, full_name, role, audit_stamp)

    print("\n" + "-" * 55)
    print("ONBOARDING SUMMARY")
    print("-" * 55)
    print(f"ID               : {new_id}")
    print(f"Name             : {full_name}")
    print(f"Role             : {role} ({seniority})")
    print(f"Corporate Email  : {email_id}")
    print(f"Temporary Pass   : {temp_pass}")
    print(f"Provisioned Tools: {initial_access}")
    print(f"Permanent Record : {permanent_record}")
    print("-" * 55)


def access_request_portal():
    """Phase 3: Validates and grants/denies tool access based on role policies."""
    print("\n" + "=" * 55)
    print("--- ACCESS REQUEST PORTAL ---")
    print("=" * 55)
    print(f"Active Employees: {list(EMPLOYEES.keys())}")

    emp_id = input("Enter Employee ID: ").strip().upper()
    emp_data = EMPLOYEES.get(emp_id)

    if not emp_data:
        print(f"Error: Employee ID '{emp_id}' not found.")
        return

    print(f"\nWelcome, {emp_data['name']}!")
    print(f"Designation: {emp_data['role'].capitalize()}")
    print(f"Current Access: {emp_data['access']}\n")

    req_tool = input("Enter tool to request: ").strip()
    today = str(date.today())

    # Check 1: Tool exists in company master list
    if req_tool not in TOOLS:
        print(f"Error: Tool '{req_tool}' is not an approved company tool.")
        print(f"Approved catalog: {TOOLS}")
        return

    # Check 2: Already has access
    if req_tool in emp_data["access"]:
        idx = emp_data["access"].index(req_tool)
        print(f"Notice: You already have active access to '{req_tool}' (Slot #{idx + 1}).")
        return

    # Check 3: Role policy verification
    permitted_tools = ASSIGNED_ROLES.get(emp_data["role"], [])
    if req_tool not in permitted_tools:
        print(f"Access Denied: Role '{emp_data['role']}' does not have clearance for '{req_tool}'.")
        print(f"Permitted tools for your role: {permitted_tools}")
        
        log_entry = (emp_id, req_tool, "DENIED", today)
        ACCESS_LOG.append(log_entry)
        print(f"Security Log Updated: {log_entry}")
    else:
        emp_data["access"].append(req_tool)
        print(f"Access Granted: '{req_tool}' has been added to your profile.")
        print(f"Updated Access: {emp_data['access']}")
        
        log_entry = (emp_id, req_tool, "GRANTED", today)
        ACCESS_LOG.append(log_entry)
        print(f"Security Log Updated: {log_entry}")


def run_tool_audit():
    """Phase 4: Set-theory analysis across company tooling and employee permissions."""
    print("\n" + "=" * 55)
    print("--- TOOL AUDIT & ACCESS COMPARISON ---")
    print("=" * 55)

    if "E101" not in EMPLOYEES or "E102" not in EMPLOYEES:
        print("Audit requires at least E101 and E102 registered.")
        return

    e1_access = set(EMPLOYEES["E101"]["access"])
    e2_access = set(EMPLOYEES["E102"]["access"])
    master_set = set(TOOLS)

    print(f"E101 ({EMPLOYEES['E101']['name']}) Access: {e1_access}")
    print(f"E102 ({EMPLOYEES['E102']['name']}) Access: {e2_access}\n")

    print(f"Shared Tools (Intersection)          : {e1_access & e2_access}")
    print(f"Unique to E101 (Difference)           : {e1_access - e2_access}")
    print(f"Unique to E102 (Difference)           : {e2_access - e1_access}")
    print(f"Combined Access (Union)               : {e1_access | e2_access}")
    print(f"Non-Overlapping (Symmetric Difference): {e1_access ^ e2_access}")

    # Enterprise-wide unused software licenses
    all_assigned_tools = set().union(*(emp["access"] for emp in EMPLOYEES.values()))
    unused_tools = master_set - all_assigned_tools
    print(f"\nUnused Company Tools (Cost Optimization): {unused_tools}")
    print(f"Company is maintaining {len(unused_tools)} unused tool license(s).")

    # Subset & Superset analysis
    print(f"\nIs E102 access subset of E101?  : {e2_access.issubset(e1_access)}")
    print(f"Is E101 access superset of E102?: {e1_access.issuperset(e2_access)}")
    print(f"Are their permissions disjoint? : {e1_access.isdisjoint(e2_access)}")


def revoke_access():
    """Phase 5: Removes a granted tool from an employee and logs the revocation."""
    print("\n" + "=" * 55)
    print("--- REVOKE ACCESS ---")
    print("=" * 55)

    emp_id = input("Enter Employee ID: ").strip().upper()
    emp_record = EMPLOYEES.get(emp_id)

    if not emp_record:
        print(f"Error: Employee '{emp_id}' not found.")
        return

    print(f"Selected: {emp_record['name']} | Current Access: {emp_record['access']}")
    tool_to_revoke = input("Enter tool name to revoke: ").strip()

    if tool_to_revoke not in emp_record["access"]:
        print(f"Warning: {emp_record['name']} does not have access to '{tool_to_revoke}'.")
        return

    emp_record["access"].remove(tool_to_revoke)
    today = str(date.today())
    log_entry = (emp_id, tool_to_revoke, "REVOKED", today)
    ACCESS_LOG.append(log_entry)

    print(f"Revocation successful.")
    print(f"Updated Access: {emp_record['access']}")
    print(f"Security Log Updated: {log_entry}")


def update_employee_record():
    """Phase 6: Updates employee roles, contacts, or removes custom fields."""
    print("\n" + "=" * 55)
    print("--- UPDATE EMPLOYEE RECORD ---")
    print("=" * 55)

    emp_id = input("Enter Employee ID to update: ").strip().upper()
    emp_record = EMPLOYEES.get(emp_id)

    if not emp_record:
        print(f"Error: Employee '{emp_id}' not found.")
        return

    print(f"\nCurrent Profile for {emp_id}:")
    for key, val in emp_record.items():
        print(f"  {key:<10}: {val}")

    # 1. Optional Role Update
    new_role = input(f"\nEnter new role {ROLES} (Press Enter to skip): ").strip().lower()
    if new_role:
        if new_role in ROLES:
            emp_record["role"] = new_role
            emp_record["access"] = ASSIGNED_ROLES[new_role].copy()
            print(f"Role updated to '{new_role}'. Tool permissions reset to role standard.")
        else:
            print("Invalid role entered. Skipping role change.")

    # 2. Optional Phone Update
    emp_record.setdefault("phone", "Not provided")
    phone = input(f"Enter 10-digit phone number (Current: '{emp_record['phone']}', Enter to skip): ").strip()
    if phone:
        if len(phone) == 10 and phone.isdigit():
            emp_record["phone"] = phone
            print("Phone number updated.")
        else:
            print("Invalid phone format (must be 10 digits). Skipping.")

    # 3. Optional Field Deletion
    field_to_del = input("Enter a field to remove (or Enter to skip): ").strip()
    if field_to_del:
        if field_to_del in ("name", "role", "access"):
            print("Protected field: Cannot delete core identity attributes.")
        else:
            removed = emp_record.pop(field_to_del, None)
            if removed is not None:
                print(f"Field '{field_to_del}' removed (value was '{removed}').")
            else:
                print(f"Field '{field_to_del}' does not exist.")


def inspect_cloning_and_memory():
    """Phase 7: Demonstrates shallow vs. deep copies and reference immutability."""
    print("\n" + "=" * 55)
    print("--- MEMORY MANAGEMENT & RECORD CLONING ---")
    print("=" * 55)

    if "E101" not in EMPLOYEES:
        print("E101 record required for memory inspection demo.")
        return

    original_access = EMPLOYEES["E101"]["access"]
    cloned_access = original_access.copy()
    cloned_access.append("Docker")

    print(f"Original E101 Access : {original_access}")
    print(f"Cloned Modified List : {cloned_access}")
    print(f"Are memory addresses identical? {original_access is cloned_access} (Isolated)")

    # Deep dictionary simulation
    backup_emp = EMPLOYEES["E101"].copy()
    backup_emp["access"] = EMPLOYEES["E101"]["access"].copy()
    backup_emp["access"].append("Kubernetes")

    print(f"\nOriginal E101 Access (Post-mutation): {EMPLOYEES['E101']['access']}")
    print(f"Independent Backup Profile Access   : {backup_emp['access']}")


def generate_final_dashboard():
    """Phase 8: Renders formatted summary reports and the security audit ledger."""
    print("\n" + "=" * 70)
    print("ACCESSGUARD - EXECUTIVE SECURITY DASHBOARD".center(70))
    print("=" * 70)

    # Employee Matrix
    print(f"\n{'ID':<8}{'Name':<18}{'Role':<14}{'Count':<8}{'Granted Access'}")
    print("-" * 70)
    for emp_id, data in EMPLOYEES.items():
        access_str = ", ".join(data["access"])
        print(f"{emp_id:<8}{data['name']:<18}{data['role'].upper():<14}{len(data['access']):<8}{access_str}")
    print("-" * 70)

    # Metric Bar
    print(f"Total Staff: {len(EMPLOYEES)} | Master Tools: {len(TOOLS)} | Audit Entries: {len(ACCESS_LOG)}\n")

    # Security Log Ledger
    print("SECURITY AUDIT TRAIL".center(70, "-"))
    print(f"{'Emp ID':<12}{'Tool':<20}{'Status':<16}{'Date'}")
    print("-" * 70)
    for entry in ACCESS_LOG:
        print(f"{entry[0]:<12}{entry[1]:<20}{entry[2]:<16}{entry[3]}")
    print("-" * 70)
    print("Report generated securely by AccessGuard IAM Engine".center(70))


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================

def main():
    """Application entry point with interactive command loop."""
    menu_actions = {
        "1": ("View Company Directory & Roles", display_company_banner),
        "2": ("Onboard New Employee", onboard_employee),
        "3": ("Request Tool Access", access_request_portal),
        "4": ("Run Tool Audit & Set Analysis", run_tool_audit),
        "5": ("Revoke Tool Access", revoke_access),
        "6": ("Update Employee Record", update_employee_record),
        "7": ("Inspect Memory & Clone Records", inspect_cloning_and_memory),
        "8": ("Generate Security Dashboard", generate_final_dashboard),
    }

    while True:
        print("\n" + "=" * 55)
        print("          ACCESSGUARD CONTROL PANEL")
        print("=" * 55)
        for key, (description, _) in menu_actions.items():
            print(f"  [{key}] {description}")
        print("  [0] Exit System")
        print("=" * 55)

        choice = input("Select an option (0-8): ").strip()

        if choice == "0":
            print("\nShutting down AccessGuard. Session terminated securely.")
            break
        elif choice in menu_actions:
            action_name, action_func = menu_actions[choice]
            action_func()
        else:
            print("\n[!] Invalid selection. Please enter a number between 0 and 8.")


if __name__ == "__main__":
    main()