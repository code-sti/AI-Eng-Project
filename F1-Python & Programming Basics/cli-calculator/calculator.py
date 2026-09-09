num1_input = input("Enter first number: ")
operator = input("Enter operator (+, -, *, /): ")
num2_input = input("Enter second number: ")

try:
    num1 = float(num1_input)
    num2 = float(num2_input)
except ValueError:
    print("Error: Please enter valid numbers.")
    exit()

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    try:
        result = num1 / num2
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        exit()
else:
    print("Error: Invalid operator. Use +, -, *, or /")
    exit()

print(f"Result: {num1} {operator} {num2} = {result}")