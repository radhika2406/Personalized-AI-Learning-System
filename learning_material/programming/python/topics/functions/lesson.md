
# Functions and Scope

**Course:** Python
**Topic ID:** `functions`

## Learning objectives

After completing this topic, learners should be able to:

- Understand what functions are and why they are used.
- Explain the advantages of using functions.
- Create and call user-defined functions.
- Understand function parameters and arguments.
- Work with positional, keyword and default arguments.
- Use variable-length arguments such as `*args` and `**kwargs`.
- Understand the difference between `return` and `print()`.
- Understand local and global variables.
- Explain Python variable scope and the LEGB rule.
- Use the `global` and `nonlocal` keywords.
- Understand lambda functions.
- Understand recursion and recursive functions.
- Pass functions as arguments to other functions.
- Apply functions to solve real-world programming problems.

## Explanation

### 1. What is a Function?

A function is a reusable block of code designed to perform a particular task.

Instead of writing the same code repeatedly, we can define a function once and call it whenever required.

**Example without a function:**

```python
print("Welcome to Python!")
print("Welcome to Python!")
print("Welcome to Python!")
```

**Example using a function:**

```python
def welcome():
    print("Welcome to Python!")

welcome()
welcome()
welcome()
```

Output:

```text
Welcome to Python!
Welcome to Python!
Welcome to Python!
```

Here:
- `def` is the keyword used to define a function.
- `welcome` is the function name.
- `()` contains parameters, if any.
- The indented statement is the function body.
- `welcome()` calls or executes the function.

### 2. Advantages of Functions

Functions provide several benefits:

1. **Code reusability:** Write code once and use it multiple times.
2. **Modularity:** Divide a large program into smaller parts.
3. **Readability:** Make programs easier to understand.
4. **Maintainability:** Changes can be made in one place.
5. **Debugging:** Individual functions can be tested separately.
6. **Reduced repetition:** Avoid writing the same logic repeatedly.

### 3. Defining and Calling a Function

A function must be defined before it is called during normal program execution.

**Syntax:**

```python
def function_name():
    # Function body
    statements

function_name()
```

**Example:**

```python
def greet():
    print("Hello!")
    print("Welcome to Python programming.")

greet()
```

Output:

```text
Hello!
Welcome to Python programming.
```

A function definition does not execute its body immediately. The body executes when the function is called.

### 4. Functions with Parameters

Parameters are variables written inside the parentheses of a function definition.

They allow a function to receive information.

**Example:**

```python
def greet(name):
    print("Hello", name)

greet("Riya")
greet("Aman")
```

Output:

```text
Hello Riya
Hello Aman
```

Here:
- `name` is a parameter.
- `"Riya"` and `"Aman"` are arguments.

**Difference between Parameters and Arguments:**

| Parameter | Argument |
|---|---|
| Variable in function definition | Actual value passed during function call |
| Receives data | Supplies data |
| Example: `name` | Example: `"Riya"` |

### 5. Functions with Multiple Parameters

A function can accept more than one parameter.

**Example:**

```python
def add(a, b):
    print("Sum:", a + b)

add(10, 20)
```

Output:

```text
Sum: 30
```

Here, `a` and `b` are parameters.

### 6. The return Statement

The `return` statement sends a result back to the place where the function was called.

**Example:**

```python
def add(a, b):
    return a + b

result = add(10, 20)

print(result)
```

Output:

```text
30
```

The returned value can be stored in a variable or used in another expression.

**Difference between print() and return:**

| print() | return |
|---|---|
| Displays information on the screen | Sends a value back to the caller |
| Does not automatically provide the displayed value to the caller | Provides the function result |
| Mainly used for displaying output | Used when a result must be reused |

**Example:**

```python
def show():
    print("Hello")

def get_value():
    return "Hello"

x = show()
y = get_value()

print("x =", x)
print("y =", y)
```

Output:

```text
Hello
x = None
y = Hello
```

A function without an explicit `return` statement returns `None`.

### 7. Types of Function Arguments

Python supports different ways to pass arguments to functions.

#### A. Positional Arguments

Values are passed according to the order of parameters.

**Example:**

```python
def student(name, age):
    print("Name:", name)
    print("Age:", age)

student("Riya", 20)
```

Output:

```text
Name: Riya
Age: 20
```

The first argument is assigned to `name` and the second to `age`.

#### B. Keyword Arguments

Arguments are passed using parameter names.

**Example:**

```python
def student(name, age):
    print("Name:", name)
    print("Age:", age)

student(age=20, name="Riya")
```

Output:

```text
Name: Riya
Age: 20
```

The order does not matter when all arguments are supplied by keyword.

#### C. Default Arguments

A default argument has a predefined value used when the caller does not provide that argument.

**Example:**

```python
def greet(name="Guest"):
    print("Hello", name)

greet()
greet("Riya")
```

Output:

```text
Hello Guest
Hello Riya
```

Default parameters must come after non-default parameters in a function definition.

#### D. Variable-Length Positional Arguments (*args)

`*args` allows a function to accept any number of positional arguments.

The arguments are collected into a tuple.

**Example:**

```python
def add(*numbers):
    total = 0

    for number in numbers:
        total += number

    return total

print(add(10, 20))
print(add(10, 20, 30))
print(add(1, 2, 3, 4, 5))
```

Output:

```text
30
60
15
```

#### E. Variable-Length Keyword Arguments (**kwargs)

`**kwargs` allows a function to accept any number of keyword arguments.

These arguments are collected into a dictionary.

**Example:**

```python
def student(**details):
    for key, value in details.items():
        print(key, ":", value)

student(name="Riya", age=20, course="Python")
```

Output:

```text
name : Riya
age : 20
course : Python
```

### 8. Combining Different Types of Arguments

Python allows different types of parameters in one function, provided they follow the correct parameter-ordering rules.

**Example:**

```python
def display(name, age=20, *args, **kwargs):
    print("Name:", name)
    print("Age:", age)
    print("Extra positional:", args)
    print("Extra keyword:", kwargs)

display("Riya", 21, "Python", "AI", city="Bhopal")
```

Output:

```text
Name: Riya
Age: 21
Extra positional: ('Python', 'AI')
Extra keyword: {'city': 'Bhopal'}
```

### 9. Variable Scope

Scope refers to the region of a program where a variable can be accessed.

Python mainly uses four levels of scope:

1. Local scope
2. Enclosing scope
3. Global scope
4. Built-in scope

These follow the LEGB rule.

### 10. Local Variables

A local variable is created inside a function.

It can normally be accessed only within that function.

**Example:**

```python
def greet():
    message = "Hello Python"
    print(message)

greet()
```

Output:

```text
Hello Python
```

Trying to access `message` outside the function causes a `NameError`.

```python
def greet():
    message = "Hello Python"

greet()

print(message)
```

Output:

```text
NameError: name 'message' is not defined
```

### 11. Global Variables

A global variable is defined outside all functions.

It can be read inside functions.

**Example:**

```python
name = "Riya"

def greet():
    print("Hello", name)

greet()
```

Output:

```text
Hello Riya
```

Here, `name` is a global variable.

### 12. The global Keyword

The `global` keyword allows a function to assign a new value to a variable defined at the module's global scope.

**Example:**

```python
count = 10

def update():
    global count
    count = 20

update()

print(count)
```

Output:

```text
20
```

Without `global`, assigning to `count` inside the function would create a local variable instead.

Use `global` carefully because excessive global-state modification can make programs harder to maintain.

### 13. Enclosing Scope

An enclosing variable is defined inside an outer function and accessed by an inner function.

**Example:**

```python
def outer():
    message = "Hello from outer function"

    def inner():
        print(message)

    inner()

outer()
```

Output:

```text
Hello from outer function
```

The inner function can access variables from its enclosing function.

### 14. The nonlocal Keyword

The `nonlocal` keyword allows an inner function to modify a variable in its nearest enclosing function scope.

**Example:**

```python
def outer():
    count = 10

    def inner():
        nonlocal count
        count = 20

    inner()

    print(count)

outer()
```

Output:

```text
20
```

Difference:

- `global` refers to a variable at the module's global scope.
- `nonlocal` refers to a variable in an enclosing function scope.

### 15. The LEGB Rule

LEGB describes the order Python uses to search for a variable name.

| Letter | Scope | Meaning |
|---|---|---|
| L | Local | Current function |
| E | Enclosing | Outer or enclosing function |
| G | Global | Module-level scope |
| B | Built-in | Names provided by Python |

**Example:**

```python
x = "Global"

def outer():
    x = "Enclosing"

    def inner():
        x = "Local"
        print(x)

    inner()

outer()
```

Output:

```text
Local
```

Python finds the variable in the local scope first.

### 16. Lambda Functions

A lambda function is a small anonymous function created using the `lambda` keyword.

It can contain only one expression.

**Syntax:**

```python
lambda arguments: expression
```

**Example:**

```python
square = lambda x: x * x

print(square(5))
```

Output:

```text
25
```

**Example with multiple arguments:**

```python
add = lambda a, b: a + b

print(add(10, 20))
```

Output:

```text
30
```

Lambda functions are useful for short operations, especially when a small function is needed temporarily.

### 17. Functions as Arguments

In Python, functions are objects. This means one function can be passed as an argument to another function.

**Example:**

```python
def square(number):
    return number * number

def calculate(function, value):
    return function(value)

result = calculate(square, 5)

print(result)
```

Output:

```text
25
```

Here:
- `square` is passed as an argument.
- `calculate()` calls the supplied function.

This concept is useful in callbacks, decorators and functional programming.

### 18. Recursion

Recursion occurs when a function calls itself to solve a smaller version of the same problem.

A recursive function generally needs two important parts:

1. **Base case:** Stops further recursive calls.
2. **Recursive case:** Calls the function again with a smaller or simpler input.

**Example: Factorial using recursion**

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1

    return n * factorial(n - 1)

print(factorial(5))
```

Output:

```text
120
```

Explanation:

```text
factorial(5)
= 5 * factorial(4)
= 5 * 4 * factorial(3)
= 5 * 4 * 3 * factorial(2)
= 5 * 4 * 3 * 2 * factorial(1)
= 120
```

Without a proper base case, recursion may continue until Python raises a `RecursionError`.

### 19. Built-in Functions

Python provides many ready-made functions.

Some commonly used built-in functions are:

| Function | Purpose |
|---|---|
| `print()` | Displays output |
| `len()` | Returns the length |
| `type()` | Returns the object's type |
| `sum()` | Calculates the sum |
| `max()` | Returns the largest item |
| `min()` | Returns the smallest item |
| `abs()` | Returns the absolute value |
| `round()` | Rounds a number |
| `range()` | Generates a sequence of integers |
| `sorted()` | Returns a sorted list |
| `enumerate()` | Provides index-value pairs |
| `zip()` | Combines iterables |

**Example:**

```python
numbers = [10, 20, 30, 40]

print(len(numbers))
print(sum(numbers))
print(max(numbers))
print(min(numbers))
```

Output:

```text
4
100
40
10
```

### 20. Docstrings

A docstring is a string used to describe the purpose of a function, class or module.

It is usually written as the first statement inside the function.

**Example:**

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

print(add(10, 20))
print(add.__doc__)
```

Output:

```text
30
Return the sum of two numbers.
```

Docstrings help developers understand how a function should be used.

### 21. Type Hints in Functions

Type hints indicate the expected types of function parameters and return values.

They improve readability and help development tools detect possible type-related problems.

**Example:**

```python
def add(a: int, b: int) -> int:
    return a + b

result = add(10, 20)

print(result)
```

Output:

```text
30
```

Here:

- `a: int` indicates that `a` is expected to be an integer.
- `b: int` indicates that `b` is expected to be an integer.
- `-> int` indicates the expected return type.

Type hints are not automatically enforced by Python at runtime.

### 22. Function Annotations

Function annotations provide additional information about parameters and return values.

Type hints are a common use of annotations.

**Example:**

```python
def greet(name: str) -> str:
    return "Hello " + name

print(greet("Riya"))
print(greet.__annotations__)
```

Output:

```text
Hello Riya
{'name': <class 'str'>, 'return': <class 'str'>}
```

### 23. Function Composition

Function composition means combining functions so that the output of one function becomes the input of another.

**Example:**

```python
def add_one(number):
    return number + 1

def double(number):
    return number * 2

result = double(add_one(5))

print(result)
```

Output:

```text
12
```

First, `add_one(5)` returns `6`. Then `double(6)` returns `12`.

## Key concepts

1. **Function:** A reusable block of code that performs a particular task.
2. **def:** Keyword used to define a function.
3. **Function call:** Executes a defined function.
4. **Parameter:** A variable in a function definition.
5. **Argument:** A value passed to a function.
6. **return:** Sends a result back to the caller.
7. **Positional arguments:** Arguments assigned according to position.
8. **Keyword arguments:** Arguments assigned using parameter names.
9. **Default arguments:** Parameters with predefined values.
10. **\*args:** Collects additional positional arguments into a tuple.
11. **\*\*kwargs:** Collects additional keyword arguments into a dictionary.
12. **Scope:** The region where a variable can be accessed.
13. **Local variable:** A variable defined inside a function.
14. **Global variable:** A variable defined at module level.
15. **global:** Allows assignment to a module-level global variable.
16. **nonlocal:** Allows assignment to a variable in an enclosing function.
17. **LEGB:** Local, Enclosing, Global and Built-in scope lookup order.
18. **Lambda:** A small anonymous function.
19. **Recursion:** A function calling itself.
20. **Base case:** The condition that stops recursion.
21. **Docstring:** A description of a function.
22. **Type hints:** Annotations describing expected data types.
23. **Function composition:** Combining functions by passing one result into another function.

## Examples

### Example 1: Simple calculator using functions

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"

    return a / b

print("Addition:", add(10, 5))
print("Subtraction:", subtract(10, 5))
print("Multiplication:", multiply(10, 5))
print("Division:", divide(10, 5))
```

Output:

```text
Addition: 15
Subtraction: 5
Multiplication: 50
Division: 2.0
```

### Example 2: Find the largest of three numbers

```python
def largest(a, b, c):
    return max(a, b, c)

print(largest(10, 25, 15))
```

Output:

```text
25
```

### Example 3: Check whether a number is even or odd

```python
def check_number(number):
    if number % 2 == 0:
        return "Even"

    return "Odd"

print(check_number(10))
print(check_number(7))
```

Output:

```text
Even
Odd
```

### Example 4: Calculate factorial using recursion

```python
def factorial(n):
    if n <= 1:
        return 1

    return n * factorial(n - 1)

print(factorial(5))
```

Output:

```text
120
```

### Example 5: Use *args to calculate an average

```python
def average(*numbers):
    if not numbers:
        return 0

    return sum(numbers) / len(numbers)

print(average(10, 20, 30))
print(average(5, 10, 15, 20))
```

Output:

```text
20.0
12.5
```

### Example 6: Use **kwargs for student details

```python
def display_student(**details):
    for key, value in details.items():
        print(key, ":", value)

display_student(
    name="Riya",
    age=20,
    course="Python",
    marks=95
)
```

Output:

```text
name : Riya
age : 20
course : Python
marks : 95
```

### Example 7: Global and local variables

```python
message = "Global message"

def display():
    message = "Local message"
    print(message)

display()

print(message)
```

Output:

```text
Local message
Global message
```

### Example 8: Lambda function to find a square

```python
square = lambda number: number ** 2

print(square(6))
```

Output:

```text
36
```

### Example 9: Use a function as an argument

```python
def square(number):
    return number ** 2

def cube(number):
    return number ** 3

def calculate(function, number):
    return function(number)

print(calculate(square, 4))
print(calculate(cube, 4))
```

Output:

```text
16
64
```

### Example 10: Use functions to calculate student grades

```python
def calculate_average(marks):
    return sum(marks) / len(marks)

def calculate_grade(average):
    if average >= 90:
        return "A"

    elif average >= 75:
        return "B"

    elif average >= 60:
        return "C"

    else:
        return "D"

marks = [85, 90, 80]

average = calculate_average(marks)
grade = calculate_grade(average)

print("Average:", average)
print("Grade:", grade)
```

Output:

```text
Average: 85.0
Grade: B
```

## Common mistakes

1. **Forgetting parentheses when calling a function**
   - Use `greet()` to call a function.
   - Writing only `greet` refers to the function object.

2. **Forgetting indentation**
   - Function body statements must be indented.

3. **Calling a function before it is defined**
   - Define the function before calling it during normal execution.

4. **Confusing parameters and arguments**
   - Parameters are written in the definition.
   - Arguments are supplied during the call.

5. **Using print() instead of return**
   - Use `return` when the function result needs to be reused.

6. **Forgetting the return statement**
   - A function without an explicit return value returns `None`.

7. **Passing the wrong number of arguments**
   - Supply the required arguments or define suitable defaults.

8. **Incorrect parameter order**
   - Required parameters must come before default parameters.
   - Follow Python's rules when combining positional-only, keyword-only and variable-length parameters.

9. **Using mutable objects as default arguments**
   - Avoid defaults such as `items=[]` when a new list is intended for each call.
   - Use `None` and create a new list inside the function.

10. **Confusing local and global variables**
    - Local variables belong to their function.
    - Global variables are defined at module level.

11. **Using global unnecessarily**
    - Prefer returning values instead of modifying global variables when possible.

12. **Using nonlocal without an enclosing binding**
    - A matching variable must exist in an enclosing function scope.

13. **Forgetting the base case in recursion**
    - Every recursive function should have a condition that stops further calls.

14. **Using lambda for complicated logic**
    - Use a normal `def` function for complex operations.

15. **Confusing *args and **kwargs**
    - `*args` collects positional arguments into a tuple.
    - `**kwargs` collects keyword arguments into a dictionary.

16. **Assuming type hints automatically validate values**
    - Type hints provide information to developers and tools but do not enforce types automatically at runtime.

## Quick summary

- Functions are reusable blocks of code.
- `def` defines a function.
- Function calls execute the function body.
- Parameters receive arguments.
- `return` sends a value back to the caller.
- Positional arguments depend on order.
- Keyword arguments use parameter names.
- Default arguments provide predefined values.
- `*args` collects additional positional arguments.
- `**kwargs` collects additional keyword arguments.
- Scope determines where variables can be accessed.
- Local variables are defined inside functions.
- Global variables are defined at module level.
- `global` modifies a module-level variable.
- `nonlocal` modifies an enclosing function variable.
- LEGB means Local, Enclosing, Global and Built-in.
- Lambda functions are small anonymous functions.
- Recursion occurs when a function calls itself.
- A base case stops recursion.
- Docstrings describe functions.
- Type hints describe expected parameter and return types.
- Functions can be passed as arguments to other functions.

## Practice

### Beginner Level

1. Write a function that prints "Hello Python".
2. Create a function that adds two numbers.
3. Write a function that returns the square of a number.
4. Create a function that checks whether a number is even or odd.
5. Write a function that finds the largest of two numbers.
6. Create a function that converts Celsius to Fahrenheit.

### Intermediate Level

7. Write a function that accepts three numbers and returns their average.
8. Create a function using default arguments.
9. Write a function using keyword arguments.
10. Create a function that accepts any number of values using `*args`.
11. Create a function that accepts student details using `**kwargs`.
12. Write a program demonstrating local and global variables.
13. Write a function that returns both the sum and product of two numbers.
14. Create a lambda function to find the cube of a number.

### Advanced Level

15. Write a recursive function to calculate factorial.
16. Write a recursive function to calculate the Fibonacci sequence.
17. Create a function that uses `nonlocal` to modify an enclosing variable.
18. Write a function that accepts another function as an argument.
19. Create a calculator using separate functions for each operation.
20. Build a student grade calculator using multiple functions.
21. Write a recursive function to calculate the sum of digits of a number.
22. Create a function with type hints and a docstring.

### Practice Solutions

**Solution 1: Print a welcome message**

```python
def welcome():
    print("Welcome to Python!")

welcome()
```

Output:

```text
Welcome to Python!
```

**Solution 2: Add two numbers**

```python
def add(a, b):
    return a + b

print(add(10, 20))
```

Output:

```text
30
```

**Solution 3: Check even or odd**

```python
def check(number):
    if number % 2 == 0:
        return "Even"

    return "Odd"

print(check(8))
```

Output:

```text
Even
```

**Solution 4: Use default arguments**

```python
def greet(name="Guest"):
    print("Hello", name)

greet()
greet("Riya")
```

Output:

```text
Hello Guest
Hello Riya
```

**Solution 5: Use *args**

```python
def total(*numbers):
    return sum(numbers)

print(total(10, 20, 30, 40))
```

Output:

```text
100
```

**Solution 6: Use **kwargs**

```python
def details(**data):
    print(data)

details(name="Riya", age=20, course="Python")
```

Output:

```text
{'name': 'Riya', 'age': 20, 'course': 'Python'}
```

**Solution 7: Factorial using recursion**

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1

    return n * factorial(n - 1)

print(factorial(5))
```

Output:

```text
120
```

**Solution 8: Fibonacci using recursion**

```python
def fibonacci(n):
    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(7):
    print(fibonacci(i), end=" ")
```

Output:

```text
0 1 1 2 3 5 8
```

**Solution 9: Demonstrate global scope**

```python
count = 5

def update():
    global count
    count = 15

update()

print(count)
```

Output:

```text
15
```

**Solution 10: Sum of digits using recursion**

```python
def sum_digits(number):
    if number == 0:
        return 0

    return number % 10 + sum_digits(number // 10)

print(sum_digits(1234))
```

Output:

```text
10
```

**Solution 11: Function as an argument**

```python
def square(number):
    return number ** 2

def apply(function, value):
    return function(value)

print(apply(square, 5))
```

Output:

```text
25
```

**Solution 12: Function with type hints and docstring**

```python
def multiply(a: int, b: int) -> int:
    """Return the product of two integers."""
    return a * b

print(multiply(5, 4))
```

Output:

```text
20
```

## Learning resources

- **PDF:** [Functions and Scope PDF](https://drive.google.com/file/d/1nl1lpt-EMMkGGQu_YfbiFwD31yjyBWZc/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc