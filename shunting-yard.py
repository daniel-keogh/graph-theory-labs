# The Shunting Yard Algorithm for regular expressions

# Input
infix = "(a|b).c*"
print("Input is:", infix)
# Expected output: "ab|c*."
print("Expected:", "ab|c*.")

# Convert input to a stack-ish list
infix = list(infix)[::-1]

# Operator stack
opers = []

# Output list
postfix = []

# Operator precedence
prec = {'*': 100, '.': 80, '|': 60, '(': 40, ')': 20}

# Loop through the input one character at a time
while infix:
    # Pop a character from the input
    c = infix.pop()

    # Decide what to do based on the character
    if c == '(':
        # Push an open bracket to the opers stack
        opers.append(c)
    elif c == ')':
        # Pop the operators stack until you find an open bracket
        while opers[-1] != '(':
            postfix.append(opers.pop())

        # Get rid of the open bracket
        opers.pop()
    elif c in prec:
        # Push any operators on the opers stack with higher prec to the output
        while opers and prec[c] < prec[opers[-1]]:
            postfix.append(opers.push())
        # Push c to the operators stack
        opers.append(c)
    else:
        # Typically we just push the character to the output
        postfix.append(c)

# Pop all the operators to the ouput
while (opers):
    postfix.append(opers.pop())


# Convert output list to a string
postfix = "".join(postfix)

# Print the result
print("Output:", postfix)
