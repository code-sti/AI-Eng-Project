# Learning Guide: CLI Calculator with Error Handling

This file walks through exactly how this project was built, step by step, with every concept explained. If you're following this as part of the Zero-to-Senior AI Engineer + Solutions Architect path, build this project yourself using the steps below before looking at the final code.

---

## Goal

Build a command-line calculator that takes two numbers and an operator, performs the calculation, and doesn't crash when given bad input.

---

## Step 1 — Get input from the user

```python
num1_input = input("Enter first number: ")
operator = input("Enter operator (+, -, *, /): ")
num2_input = input("Enter second number: ")
```

**What's happening:** `input()` shows a prompt and waits for the user to type something, then returns whatever they typed **as text (a string)** — even if it looks like a number. We store each answer in a variable.

**Why it matters:** Every program that takes input from a real user (not just test data) starts here. Getting comfortable with `input()` and knowing that it *always* returns a string (never a number) prevents a very common beginner bug.

---

## Step 2 — Convert the text into real numbers

```python
try:
    num1 = float(num1_input)
    num2 = float(num2_input)
except ValueError:
    print("Error: Please enter valid numbers.")
    exit()
```

**What's happening:** `float()` converts text like `"5"` into an actual number `5.0` so math can be performed. If the user typed something that isn't a number (like `"five"`), `float()` raises a `ValueError` — normally this crashes the program.

**Why it matters:** `try` means "attempt this code." `except ValueError:` means "if that specific error happens, run this instead of crashing." This is the single most important habit in this whole project: **never trust user input**. `exit()` stops the program immediately so it doesn't try to do math on bad data.

---

## Step 3 — Do the math based on the operator

```python
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
```

**What's happening:** We check the `operator` variable against each possible symbol using `if`/`elif`. Only one branch runs — `elif` means "else if," so Python stops checking once it finds a match.

**Why it matters:** Division gets its *own* `try`/`except` because it's the only operation that can fail even with two perfectly valid numbers (dividing by zero). `ZeroDivisionError` is the specific error Python raises for that case. The final `else` catches any operator that isn't one of the four we support — this is called a **guard clause**, and it prevents silent failures (imagine if we just skipped an unrecognized operator instead of telling the user).

---

## Step 4 — Show the result

```python
print(f"Result: {num1} {operator} {num2} = {result}")
```

**What's happening:** An f-string (the `f` before the quotes) lets you insert variable values directly into text using `{}`.

**Why it matters:** This is cleaner and less error-prone than building strings with `+` concatenation, and it's the standard way to format output in modern Python.

---

## Full Program

```python
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
```

---

## Topics Covered

| Topic | Where it's used |
|---|---|
| `input()` and string vs. number types | Step 1 |
| Type conversion with `float()` | Step 2 |
| `try`/`except` error handling | Steps 2 & 3 |
| Specific exception types (`ValueError`, `ZeroDivisionError`) | Steps 2 & 3 |
| `if`/`elif`/`else` control flow | Step 3 |
| Guard clauses / early exits (`exit()`) | Steps 2 & 3 |
| f-strings for output formatting | Step 4 |

---

## Soft Skills Built

**Anticipating failure before it happens.** The entire point of this project wasn't the arithmetic — it was thinking through every way a user could break the program *before* writing the happy-path code. This is the same instinct behind writing test cases, designing APIs defensively, and (later in this path) designing enterprise systems that don't fall over when a client does something unexpected.

**Technical writing.** Documenting *why* each decision was made (not just what the code does) is a skill that transfers directly to writing design docs, BRDs, and HLDs later in this path.

---

## Test It Yourself

Run the program and try all four of these cases — this is how you *prove* the error handling works, rather than assuming it does:

1. `5`, `+`, `3` → `Result: 5.0 + 3.0 = 8.0`
2. `five`, `+`, `3` → `Error: Please enter valid numbers.`
3. `5`, `/`, `0` → `Error: Cannot divide by zero.`
4. `5`, `%`, `3` → `Error: Invalid operator. Use +, -, *, or /`

## What's Next

**Project 2: To-Do List App (File-Based Storage)** — introduces persistent state (data that survives closing the program), file I/O, and JSON.