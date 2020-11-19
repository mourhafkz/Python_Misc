
def validate_ID(employeeID):
    if employeeID:
        if len(employeeID) <= 7 and employeeID.isdigit():
            return True
        else:
            return False


# Validate Employee Name
def validate_name(employeeName):
    if employeeName:
        employeeNameExcludedCharachters = ['!', '"', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=',
                                           '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\']
    for letter in employeeName:
        if letter in employeeNameExcludedCharachters:
            return False
    return True


# Validate Employee Email
def validate_email(employeeEmail):
    if employeeEmail:
        employeeEmailExcludedCharachters = ['!', '"', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+',
                                            ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\']
    for letter in employeeEmail:
        if letter in employeeEmailExcludedCharachters:
            return False
    return True


# Validate Employee Address
def validate_address(employeeAddress):
    if employeeAddress:
        employeeAddressExcludedCharachters = ['!', '"', "'", '@', '$', '%', '^', '&', '*', '_', '=', '+',
                                              '<', '>', '/', '?', ';', ':', '[', ']', '{', '}']
    for letter in employeeAddress:
        if letter in employeeAddressExcludedCharachters:
            return False
    return True


# Print Dictionary Elements

def print_dictionary(list):
    #remmeber to fix this
    # line = "\n"
    # for entry in list:
    #     line = line + "Employee ID: " + entry['employeeID'] + " | Employee Name: " + entry['employeeName'] + " | Employee Email: " + entry['employeeEmail'] + " | Employee Address: " + entry['employeeAddress']
    # line = line + "\n"
    return list


employeeList = []
# Take 5 employees details from users
customers = 1

while customers < 6:
    employeeID = 0  # this returns true by default and stops your program
    employeeName = ""  # this returns true by default and stops your program
    employeeEmail = ""  # this returns true by default and stops your program
    employeeAddress = ""  # this returns true by default and stops your program
    if customers == 6:
        break
    print(f'Enter details for customer number {customers} ')
    print(f'______________________________________________')
    if not validate_ID(employeeID) or employeeID == 0:
        employeeID = input("Enter Employee ID: ")
        validate_ID(employeeID)

    if not validate_name(employeeName) or employeeName == "":
        employeeName = input("Enter Employee Name: ")
        validate_name(employeeName)

    if not validate_email(employeeEmail) or employeeEmail == "":
        employeeEmail = input("Enter Employee Email: ")
        validate_email(employeeEmail)

    if not validate_address(employeeAddress) or employeeAddress == "":
        employeeAddress = input("Enter Employee address: ")
        validate_address(employeeAddress)

    employeeList.append({'employeeID': employeeID,
                         'employeeName': employeeName,
                         'employeeEmail': employeeEmail,
                         'employeeAddress': employeeAddress})
    print(f'______________________________________________')
    customers += 1

print_dictionary(employeeList)
