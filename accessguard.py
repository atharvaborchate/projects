# Project 1 - AccessGuard
from datetime import date
#===============================================#
#COMPANY INFO
#===============================================#

tools=["GitHub","AWS","Slack","Jira","Production Server","HR Portal","Figma","Docker"]

roles=("intern","developer","tester","manager","admin")

company_info=("PythonGuruKool","Pune",2018,"ISO 27001 Certified")
company_name,company_location,company_year,company_security=company_info

assined_roles={"intern":["Slack","Jira"],
               "developer":["GitHub","AWS","Slack","Jira"],
               "tester":["Slack","Jira","GitHub","Docker"],
               "manager":["GitHub","Slack","Jira","AWS","HR Portal"],
               "admin":["GitHub","AWS","Slack","Jira","Production Server","HR Portal","Figma","Docker"]}
employees={
    "E101":{"name":"Aarav Sharma","role":"developer","access":["Slack","Jira","GitHub","AWS"]},
    "E102":{"name":"Sneha Patil","role":"intern","access":["Slack","Jira"]}
}
no_of_employees=len(employees)
access_log=[
    ("E101","GitHub","Granted","2025-01-15"),
    ("E102","AWS","Denied","2025-02-10")]


#===============================================#   




#===============================================#
#COMPANY BANNER
#===============================================#
def company_banner():
  print("="*80)
  print(f"  {company_name} | HQ: {company_location} | Est:{company_year}");
  print(f"  Security Standard: {company_security}")
  print("="*80)
  print(f"  Total tools available:{len(tools)}")
  print(f"  Valid Roles:{len(roles)}")
  print(f"  Employees registered:{len(employees)}")
  print("="*80)
  print(f"Available Tools: {tools} \n")
  print(f"Valid Roles: {roles}\n")
  print(f"Role permission:")
  print(f"intern     -->{assined_roles["intern"]}")
  print(f"developer  -->{assined_roles["developer"]}")
  print(f"tester     -->{assined_roles["tester"]}")
  print(f"manager    -->{assined_roles["manager"]}")
  print(f"admin      -->{assined_roles["admin"]}\n")
  print("Existing Employees:\n")
  print(f"E101 | {employees['E101']["name"]} | {employees['E101']["role"]} | Access:{employees['E101']["access"]}")
  print(f"E102 | {employees['E102']["name"]}  | {employees['E102']["role"]}    | Access:{employees['E102']["access"]}")
#===============================================#




#===============================================#
#ONBOARD A NEW EMPLOYEE
#===============================================#
# def onboarding():      
#   print("\n" + "=" * 55)
#   print("--- EMPLOYEE ONBOARDING ---")
#   print("=" * 55)


#   # 1. Name validation
#   while True:
#       new_employee_raw=input("Enter your Name(only First and Last)").strip().title()
#       parts=new_employee_raw.split()
#       if len(parts) == 2 and parts[0].isalpha() and parts[1].isalpha():
#           first_name, last_name = parts[0], parts[1]
#           new_employee = f"{first_name} {last_name}"
#           break
#       print("Invalid input. Please enter exactly two alphabetic names (e.g., 'Atharva Borchate').")
    
#   # 2. Sequential ID generation
#   new_Id = f"E10{len(employees) + 1}"
#   email_id=first_name.lower()+"."+last_name.lower()+"@pythongurukool.com"
#   temp_pass=first_name[:3]+new_Id[-3:]+"@TN"

#   # 3. Role assignment
#   while True:
#     role=input("Enter your role:").strip().lower()
#     if role in roles:
#       break
#     print(f"Invalid Role. Please enter the available role only:{roles}")   


#   # 4. Experience & seniority assessment
#   while True:
#         exp_input = input("Enter years of experience: ").strip()
#         if exp_input.isdigit():
#           experience = int(exp_input)
#           break
#         print("Invalid number. Please enter a non-negative integer.")
          
#   while True:
#       exp_input = input("Enter years of experience: ").strip()
#       if exp_input.isdigit():
#         exp = int(exp_input)
#         break
#       print("Invalid number. Please enter a non-negative integer.")

#   if exp == 0:
#     seniority = "Fresher (Mentor assigned)"
#   elif 1 <= exp <= 3:
#     seniority = "Junior Level"
#   elif 4 <= exp <= 7:
#     seniority = "Mid Level"
#   else:
#     seniority = "Senior Level"

#   # 5. Independent copy of permissions to prevent master template mutation
#   initial_access = assined_roles[role].copy()

#   employees[new_Id] = {
#           "name": new_employee,
#           "role": role,
#           "access": initial_access
#       }

#   audit_stamp = str(date.today())
#   permanent_record = (new_Id, new_employee, role, audit_stamp)

#   print("\n" + "-" * 55)
#   print("ONBOARDING SUMMARY")
#   print("-" * 55)    
#   print(f"Name     :{new_employee}")
#   print(f"ID       :{new_Id}")
#   print(F"Role     :{role}")
#   print(F"Email    :{email_id}")
#   print(F"Password :{temp_pass}")
#   print(F"Access   :{assined_roles}")
#   print("=================================================")
#   print(F"Permanent Record: {permanent_record}")
#   print(F"Record Type: {permanent_record}")
  
    
def access_request_portal():
  print(f"Registered Employee IDs: dict_keys({employees.keys})")
  while True: 
    em_ID=input("ENTER THE YOUR ID").strip().upper()
    if em_ID in employees.keys:
      requested_tool=input("ENTER THE REQUIRED TOOL")
      break
    else:
      print("EMPLOYEE NOT FOUND!")   
