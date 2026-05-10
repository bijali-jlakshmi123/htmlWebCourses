def add(num1, num2):
    return num1+num2

def sub(num1, num2):
    return num1-num2

def mul(num1, num2):
    return num1*num2

def div(num1, num2):
    return num1/num2
while True:
    
    print("#######################")
    print("Calculator")
    print("#######################")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
    print("#######################")
    option = input("Select your option: 1,2,3,4,5: ")

    if option == '5':
        print("Exiting...")
        break
    if option in ('1','2','3','4'):
        num1 = float(input("Enter your first number:"))
        num2 = float(input("Enter your second number:"))
        if option=='1':
            print("Result:",add(num1,num2))
        elif option=='2':
            print("Result:",sub(num1,num2))
        elif option=='3':
            print("Result:",mul(num1,num2))
        elif option=='4':
            print("Result:",div(num1,num2))
    else:
        print("Selected Invalid option. Please try again.")
