#! /usr/bin/env python3

def sqrt(x):
    """
    Calculate the square root of x.
    """

    if x < 0:
        raise ValueError("Error: Negative value supplied.")

    # Initial guess.
    z = x / 2.0

    # Continuously improve the guess.
    # Reference: https://tour.golang.org/flowcontrol/8
    while abs(x - (z * z)) > 0.000001:
        z -= ((z * z) - x) / (2 * z)
        
    return z


val = float(input("Enter number: "))

try:
    print("The square root of", val, "is", sqrt(val))
except ValueError as e:
    print(e)


