
# Exceptions and Error Handling

**Course:** Python
**Topic ID:** `exception_handling`

## Learning objectives

After completing this topic, learners should be able to:

- Understand errors and exceptions in Python.
- Identify different types of errors.
- Understand the difference between syntax errors and runtime errors.
- Explain why exception handling is important.
- Use `try` and `except` blocks.
- Handle multiple exceptions.
- Use `else` and `finally` blocks.
- Raise exceptions using the `raise` keyword.
- Create custom exceptions.
- Use `assert` statements.
- Understand exception propagation.
- Apply exception handling to real-world programs.

## Explanation

### 1. What are Errors in Python?

An error is a problem in a program that prevents it from working correctly.

Errors can occur because of incorrect syntax, invalid operations, missing files, incorrect input or unexpected situations.

Python errors are commonly classified into two main categories:

1. Syntax errors
2. Exceptions (runtime errors)

### 2. Syntax Errors

A syntax error occurs when Python code does not follow the language's grammar rules.

Python cannot execute code containing a syntax error.

**Example:**

```python
if 10 > 5
    print("Ten is greater")
```

Output:

```text
SyntaxError: expected ':'
```

The problem is the missing colon after the `if` condition.

**Correct code:**

```python
if 10 > 5:
    print("Ten is greater")
```

Output:

```text
Ten is greater
```

Other common syntax mistakes include:

- Missing brackets.
- Missing quotation marks.
- Incorrect indentation.
- Missing colons.
- Incorrectly written keywords.

### 3. What are Exceptions?

An exception is an error that occurs during program execution and interrupts the normal flow of the program.

Unlike syntax errors, many exceptions can be handled using Python's exception-handling mechanism.

**Example:**

```python
a = 10
b = 0

result = a / b

print(result)
```

Output:

```text
ZeroDivisionError: division by zero
```

The program attempts to divide a number by zero, which is not allowed.

Without exception handling, the program stops at the error.

### 4. Common Types of Exceptions

Python provides many built-in exception types.

| Exception | Meaning |
|---|---|
| `ZeroDivisionError` | Division by zero |
| `ValueError` | Correct data type but invalid value |
| `TypeError` | Operation applied to an incompatible type |
| `NameError` | Variable or name is not defined |
| `IndexError` | List or sequence index is out of range |
| `KeyError` | Dictionary key does not exist |
| `FileNotFoundError` | Requested file does not exist |
| `AttributeError` | Object does not have the requested attribute |
| `ImportError` | Import operation fails |
| `ModuleNotFoundError` | Requested module cannot be found |
| `OverflowError` | Numeric operation produces a result too large for the supported representation |
| `RecursionError` | Maximum recursion depth is exceeded |

**Examples:**

**A. ZeroDivisionError**

```python
print(10 / 0)
```

Output:

```text
ZeroDivisionError: division by zero
```

**B. ValueError**

```python
number = int("hello")
```

Output:

```text
ValueError: invalid literal for int()
```

**C. TypeError**

```python
result = "Hello" + 10
```

Output:

```text
TypeError: can only concatenate str (not "int") to str
```

**D. NameError**

```python
print(age)
```

Output:

```text
NameError: name 'age' is not defined
```

**E. IndexError**

```python
numbers = [10, 20, 30]

print(numbers[5])
```

Output:

```text
IndexError: list index out of range
```

**F. KeyError**

```python
student = {
    "name": "Riya",
    "age": 20
}

print(student["marks"])
```

Output:

```text
KeyError: 'marks'
```

### 5. What is Exception Handling?

Exception handling is a mechanism used to detect and manage runtime errors without allowing the program to terminate unexpectedly.

It helps programs continue executing or display meaningful error messages.

Python uses the following keywords for exception handling:

- `try`
- `except`
- `else`
- `finally`
- `raise`

### 6. The try and except Blocks

The `try` block contains code that may produce an exception.

The `except` block contains code that executes if a matching exception occurs.

**Syntax:**

```python
try:
    # Code that may produce an exception

except:
    # Code that handles the exception
```

**Example:**

```python
try:
    number = 10 / 0

except:
    print("Something went wrong!")
```

Output:

```text
Something went wrong!
```

The program does not terminate with an unhandled division error.

**Better approach: Handle a specific exception**

```python
try:
    number = 10 / 0

except ZeroDivisionError:
    print("Cannot divide by zero!")
```

Output:

```text
Cannot divide by zero!
```

Handling specific exceptions is generally better than using a bare `except` because it avoids hiding unrelated programming errors.

### 7. Handling Multiple Exceptions

A program may produce different types of exceptions.

Python allows multiple `except` blocks to handle them separately.

**Example:**

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number

    print("Result:", result)

except ValueError:
    print("Please enter a valid integer.")

except ZeroDivisionError:
    print("Number cannot be zero.")
```

If the user enters `abc`:

```text
Please enter a valid integer.
```

If the user enters `0`:

```text
Number cannot be zero.
```

If the user enters `5`:

```text
Result: 20.0
```

### 8. Handling Multiple Exceptions in One Block

Multiple exception types can also be handled in a single `except` block.

**Example:**

```python
try:
    number = int("hello")

except (ValueError, TypeError):
    print("Invalid input or operation.")
```

Output:

```text
Invalid input or operation.
```

This is useful when different exceptions require the same handling logic.

### 9. The else Block

The `else` block executes only when no exception occurs in the `try` block.

**Syntax:**

```python
try:
    # Risky code

except:
    # Executes if an exception occurs

else:
    # Executes if no exception occurs
```

**Example:**

```python
try:
    number = int("100")

except ValueError:
    print("Invalid number.")

else:
    print("Conversion successful!")
    print(number)
```

Output:

```text
Conversion successful!
100
```

If an exception occurs, the `else` block is skipped.

### 10. The finally Block

The `finally` block always executes whether an exception occurs or not.

It is commonly used for cleanup operations, such as closing files or releasing resources.

**Example:**

```python
try:
    number = 10 / 2
    print(number)

except ZeroDivisionError:
    print("Cannot divide by zero.")

finally:
    print("Program execution completed.")
```

Output:

```text
5.0
Program execution completed.
```

**Example when an exception occurs:**

```python
try:
    number = 10 / 0

except ZeroDivisionError:
    print("Division error.")

finally:
    print("Finally block executed.")
```

Output:

```text
Division error.
Finally block executed.
```

### 11. Difference Between try, except, else and finally

| Keyword | Purpose |
|---|---|
| `try` | Contains code that may cause an exception |
| `except` | Handles a matching exception |
| `else` | Executes when no exception occurs |
| `finally` | Executes whether an exception occurs or not |

**Complete example:**

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number

except ValueError:
    print("Enter a valid integer.")

except ZeroDivisionError:
    print("Cannot divide by zero.")

else:
    print("Result:", result)

finally:
    print("Execution finished.")
```

### 12. The raise Keyword

The `raise` keyword is used to manually generate an exception.

It is useful when a program needs to reject invalid input or enforce certain conditions.

**Syntax:**

```python
raise ExceptionType("Error message")
```

**Example:**

```python
age = 15

if age < 18:
    raise ValueError("Age must be at least 18.")

print("Eligible")
```

Output:

```text
ValueError: Age must be at least 18.
```

The `print()` statement is not executed because the exception is raised first.

**Example: Raise and handle an exception**

```python
try:
    age = 15

    if age < 18:
        raise ValueError("You must be 18 or older.")

except ValueError as error:
    print("Error:", error)
```

Output:

```text
Error: You must be 18 or older.
```

### 13. The as Keyword in Exception Handling

The `as` keyword stores the exception object in a variable.

This allows the program to access the exception message.

**Example:**

```python
try:
    result = 10 / 0

except ZeroDivisionError as error:
    print("Error occurred:", error)
```

Output:

```text
Error occurred: division by zero
```

Here, `error` contains information about the exception.

### 14. Custom Exceptions

Python allows programmers to create their own exception classes.

A custom exception is useful when built-in exceptions do not clearly describe a particular application error.

Custom exceptions are generally created by inheriting from the built-in `Exception` class.

**Syntax:**

```python
class MyException(Exception):
    pass
```

**Example:**

```python
class InvalidAgeError(Exception):
    pass


age = 15

try:
    if age < 18:
        raise InvalidAgeError("Age must be 18 or above.")

    print("Access granted.")

except InvalidAgeError as error:
    print("Error:", error)
```

Output:

```text
Error: Age must be 18 or above.
```

**Example: Custom exception with a validation function**

```python
class InsufficientBalanceError(Exception):
    pass


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(
            "Insufficient account balance."
        )

    return balance - amount


try:
    remaining = withdraw(1000, 1500)
    print("Remaining balance:", remaining)

except InsufficientBalanceError as error:
    print(error)
```

Output:

```text
Insufficient account balance.
```

### 15. Exception Propagation

Exception propagation means an exception moves from one function to its calling function when it is not handled in the current function.

Python searches for a matching exception handler as the program moves back through the function call stack.

**Example:**

```python
def divide():
    return 10 / 0


def calculate():
    return divide()


try:
    calculate()

except ZeroDivisionError:
    print("Exception handled in the calling function.")
```

Output:

```text
Exception handled in the calling function.
```

The exception occurs inside `divide()`, moves through `calculate()`, and is handled by the outer `try` block.

### 16. Assertions in Python

An assertion is a statement used to check whether a condition is true.

The `assert` keyword is mainly used for debugging and checking assumptions during development.

**Syntax:**

```python
assert condition, "Error message"
```

If the condition is true, execution continues.

If the condition is false, Python raises an `AssertionError`.

**Example:**

```python
age = 20

assert age >= 18, "Age must be at least 18"

print("Eligible")
```

Output:

```text
Eligible
```

**Example when the condition is false:**

```python
age = 15

assert age >= 18, "Age must be at least 18"
```

Output:

```text
AssertionError: Age must be at least 18
```

Assertions should not be used as the only validation mechanism for important user input because Python can disable them when running with optimization.

### 17. Exception Handling with Files

File operations may produce exceptions if a file does not exist or cannot be accessed.

**Example:**

```python
try:
    file = open("data.txt", "r")

    content = file.read()

    print(content)

    file.close()

except FileNotFoundError:
    print("The requested file does not exist.")
```

Output when the file is missing:

```text
The requested file does not exist.
```

A better approach is to use the `with` statement. It automatically closes the file after the block finishes.

**Example:**

```python
try:
    with open("data.txt", "r") as file:
        content = file.read()
        print(content)

except FileNotFoundError:
    print("File not found.")
```

### 18. Exception Chaining

Exception chaining allows one exception to be raised while preserving information about an earlier exception.

Python supports this using `raise ... from ...`.

**Example:**

```python
try:
    number = int("hello")

except ValueError as error:
    raise RuntimeError("Unable to process the input.") from error
```

Here:

- The original exception is `ValueError`.
- The new exception is `RuntimeError`.
- The original error is retained as the cause.

Exception chaining is useful when converting low-level errors into meaningful application-level errors.

### 19. Best Practices for Exception Handling

1. Handle specific exceptions whenever possible.
2. Avoid using empty or bare `except` blocks.
3. Do not silently ignore important errors.
4. Display meaningful error messages.
5. Keep `try` blocks limited to operations that may fail.
6. Use `finally` or context managers for cleanup.
7. Create custom exceptions when application-specific errors need clear representation.
8. Do not use exceptions as a replacement for ordinary conditional checks.
9. Avoid exposing sensitive information in error messages.
10. Use assertions for debugging, not critical input validation.

## Key concepts

1. **Error:** A problem that prevents a program from working correctly.
2. **SyntaxError:** An error caused by incorrect Python syntax.
3. **Exception:** An event that interrupts normal program execution.
4. **Exception handling:** Managing runtime exceptions to prevent unexpected program termination.
5. **try:** Defines the block containing potentially risky code.
6. **except:** Handles matching exceptions.
7. **else:** Executes when no exception occurs.
8. **finally:** Executes whether an exception occurs or not.
9. **raise:** Manually generates an exception.
10. **Custom exception:** A programmer-defined exception class.
11. **Assertion:** Checks whether a condition is true.
12. **Exception propagation:** Movement of an unhandled exception through the function call stack.
13. **Exception chaining:** Preserves the relationship between related exceptions.
14. **Context manager:** Manages resources automatically, commonly using the `with` statement.

## Examples

### Example 1: Safe division calculator

```python
try:
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    result = a / b

    print("Result:", result)

except ValueError:
    print("Please enter valid numbers.")

except ZeroDivisionError:
    print("Cannot divide by zero.")
```

Sample input:

```text
Enter first number: 20
Enter second number: 4
```

Output:

```text
Result: 5.0
```

### Example 2: Check valid age

```python
try:
    age = int(input("Enter your age: "))

    if age < 0:
        raise ValueError("Age cannot be negative.")

    print("Your age is:", age)

except ValueError as error:
    print("Invalid age:", error)
```

Sample input:

```text
Enter your age: -5
```

Output:

```text
Invalid age: Age cannot be negative.
```

### Example 3: Handle list index errors

```python
numbers = [10, 20, 30]

try:
    index = int(input("Enter an index: "))

    print(numbers[index])

except ValueError:
    print("Enter an integer index.")

except IndexError:
    print("Index does not exist.")
```

Sample input:

```text
Enter an index: 5
```

Output:

```text
Index does not exist.
```

### Example 4: Handle dictionary key errors

```python
student = {
    "name": "Riya",
    "age": 20
}

try:
    print(student["marks"])

except KeyError:
    print("Marks information is unavailable.")
```

Output:

```text
Marks information is unavailable.
```

### Example 5: Custom exception for login

```python
class InvalidPasswordError(Exception):
    pass


def login(password):
    if len(password) < 8:
        raise InvalidPasswordError(
            "Password must contain at least 8 characters."
        )

    return "Login successful!"


try:
    result = login("abc123")
    print(result)

except InvalidPasswordError as error:
    print(error)
```

Output:

```text
Password must contain at least 8 characters.
```

### Example 6: File handling with exceptions

```python
try:
    with open("student.txt", "r") as file:
        data = file.read()
        print(data)

except FileNotFoundError:
    print("Student file not found.")

except PermissionError:
    print("You do not have permission to access this file.")
```

### Example 7: Using finally

```python
try:
    number = int("50")

    print("Number:", number)

except ValueError:
    print("Invalid conversion.")

finally:
    print("Program completed.")
```

Output:

```text
Number: 50
Program completed.
```

### Example 8: Multiple exceptions in a program

```python
try:
    numbers = [10, 20, 30]

    index = int(input("Enter index: "))

    value = numbers[index]

    result = 100 / value

    print("Result:", result)

except ValueError:
    print("Invalid input.")

except IndexError:
    print("Invalid list index.")

except ZeroDivisionError:
    print("Cannot divide by zero.")

else:
    print("Operation successful.")

finally:
    print("Program ended.")
```

## Common mistakes

1. **Using try without except or finally**
   - A `try` statement must be followed by at least one `except` or a `finally` clause.

2. **Using a bare except unnecessarily**
   - A bare `except` can hide unexpected errors.
   - Handle specific exception types instead.

3. **Writing except blocks in the wrong order**
   - More specific exceptions should be handled before broader exception classes.
   - Otherwise, a broad handler may catch an exception before its specific handler can.

4. **Confusing syntax errors with exceptions**
   - Syntax errors occur when code is incorrectly written.
   - Exceptions generally occur during execution.

5. **Forgetting to use the as keyword correctly**
   - Use `except ValueError as error:` to access the exception object.

6. **Putting normal code inside finally**
   - The `finally` block is best suited for cleanup operations.
   - Do not use it as a substitute for ordinary program logic.

7. **Using raise without an appropriate exception**
   - Raise a meaningful exception type with a useful message.

8. **Not handling invalid user input**
   - Input received using `input()` is a string.
   - Convert it carefully and handle possible `ValueError` exceptions.

9. **Ignoring exceptions**
   - Empty exception handlers can make debugging difficult.
   - Log, handle or report errors meaningfully.

10. **Using assert for user input validation**
    - Assertions may be disabled with optimization.
    - Use normal conditions and raise appropriate exceptions for required validation.

11. **Forgetting to close files**
    - Use the `with` statement to manage files safely.

12. **Assuming finally never gets skipped**
    - `finally` normally executes during normal exception handling and control flow, but it is not guaranteed in situations such as abrupt process termination.

## Quick summary

- Errors are problems that affect program execution.
- Syntax errors occur because of incorrect Python syntax.
- Exceptions are generally runtime events that interrupt normal execution.
- Python provides built-in exceptions such as `ValueError`, `TypeError`, `IndexError` and `ZeroDivisionError`.
- `try` contains potentially risky code.
- `except` handles matching exceptions.
- Multiple exceptions can be handled using separate or grouped `except` blocks.
- `else` runs when no exception occurs.
- `finally` normally executes whether an exception occurs or not.
- `raise` manually generates an exception.
- Custom exceptions are created by inheriting from `Exception`.
- Assertions are used to check assumptions during development.
- Exception propagation moves unhandled exceptions through the function call stack.
- Exception chaining preserves the original cause of an exception.
- The `with` statement helps manage resources such as files safely.

## Practice

### Beginner Level

1. Write a program that handles division by zero.
2. Write a program that converts a string into an integer and handles `ValueError`.
3. Create a program that handles an invalid list index.
4. Write a program using `try` and `except`.
5. Demonstrate the use of the `finally` block.
6. Write a program that handles a missing dictionary key.

### Intermediate Level

7. Write a calculator that handles invalid input and division by zero.
8. Write a program that uses multiple `except` blocks.
9. Demonstrate the use of `else` and `finally`.
10. Write a program that checks whether a person's age is valid using `raise`.
11. Write a program that handles `FileNotFoundError`.
12. Demonstrate exception propagation using two functions.

### Advanced Level

13. Create a custom exception called `InvalidAgeError`.
14. Create a banking program that raises an exception for insufficient balance.
15. Write a program that uses exception chaining.
16. Create a login system that handles invalid passwords using a custom exception.
17. Write a program that uses assertions to validate assumptions.
18. Create a program that handles multiple exceptions while processing student records.

### Practice Solutions

**Solution 1: Division by zero**

```python
try:
    a = 10
    b = 0

    print(a / b)

except ZeroDivisionError:
    print("Cannot divide by zero.")
```

Output:

```text
Cannot divide by zero.
```

**Solution 2: Handle invalid integer input**

```python
try:
    number = int("hello")
    print(number)

except ValueError:
    print("Invalid integer.")
```

Output:

```text
Invalid integer.
```

**Solution 3: Handle list index error**

```python
numbers = [10, 20, 30]

try:
    print(numbers[5])

except IndexError:
    print("Invalid index.")
```

Output:

```text
Invalid index.
```

**Solution 4: Use else and finally**

```python
try:
    number = int("100")

except ValueError:
    print("Invalid input.")

else:
    print("Conversion successful:", number)

finally:
    print("Execution completed.")
```

Output:

```text
Conversion successful: 100
Execution completed.
```

**Solution 5: Raise an exception**

```python
age = 16

try:
    if age < 18:
        raise ValueError("Not eligible.")

    print("Eligible.")

except ValueError as error:
    print(error)
```

Output:

```text
Not eligible.
```

**Solution 6: Custom exception**

```python
class InvalidAgeError(Exception):
    pass


try:
    age = 15

    if age < 18:
        raise InvalidAgeError("Age must be 18 or above.")

except InvalidAgeError as error:
    print(error)
```

Output:

```text
Age must be 18 or above.
```

**Solution 7: Handle a missing file**

```python
try:
    with open("unknown.txt", "r") as file:
        print(file.read())

except FileNotFoundError:
    print("File does not exist.")
```

Output when the file is missing:

```text
File does not exist.
```

**Solution 8: Banking exception**

```python
class InsufficientBalanceError(Exception):
    pass


balance = 5000
withdrawal = 6000

try:
    if withdrawal > balance:
        raise InsufficientBalanceError(
            "Insufficient balance."
        )

    balance -= withdrawal
    print("Remaining balance:", balance)

except InsufficientBalanceError as error:
    print(error)
```

Output:

```text
Insufficient balance.
```

## Learning resources

- **PDF:** [Exceptions and Error Handling PDF](https://drive.google.com/file/d/1vgfW_adSnZ-h06IiPlUGM1j2jZnSyqw5/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc