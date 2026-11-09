# calc app
def add(a,b):
   return a+b 

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if (b == 0):
        raise ZeroDivisionError("Can't divide by 0!")
    return a/b 

def power(a,b):
    if a == 0 and b< 0:
        raise ZeroDivisionError("Base and power must be 1 and greater")
    return a**b

def sqaure_root(a):
    if a<0 :
        raise ValueError("Can't find square root for negative numbers.")
    return a**2

def calculate(a,operator,b=None):
    operators = ['+','-','*','/','**','sqrt']
    if operator not in operators:
        raise ValueError("Invalid operator!")
    match operator:
        case '+':
            return add(a,b)
        case '-':
            return subtract(a,b)
        case '*':
            return multiply(a,b)
        case '/':
            return divide(a,b)
        case '**':
            return power(a,b)
        case 'sqrt':
            return sqaure_root(a)


    

