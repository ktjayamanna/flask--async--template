# relative path: business_logic.py
def perform_addition(x, y):
    """
    This function performs addition on two input parameters x and y and returns the result.
    """
    return x + y

def perform_division(x, y):
    """
    A function that performs division between two numbers.

    Parameters:
    x (int or float): The numerator.
    y (int or float): The denominator. Must not be zero.

    Returns:
    float: The result of x divided by y.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y
