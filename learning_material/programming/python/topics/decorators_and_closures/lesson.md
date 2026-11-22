
# Decorators, Closures and Advanced Python

**Course:** Python  
**Topic ID:** `decorators_and_closures`

## Learning objectives

After completing this topic, learners should be able to:

- Understand the concept of decorators and closures.
- Explain how functions work as first-class objects.
- Understand nested functions and their scope.
- Create and use closures.
- Understand the purpose of decorators.
- Create custom decorators using functions.
- Use the `@` decorator syntax.
- Understand `*args` and `**kwargs`.
- Use `functools.wraps` to preserve function metadata.
- Understand generators, lambda functions and advanced function concepts.
- Apply decorators to practical programming problems.

## Explanation

### 1. Functions as First-Class Objects

In Python, functions are treated as first-class objects. This means functions can be:

- Assigned to variables.
- Passed as arguments to other functions.
- Returned from other functions.
- Stored in lists, dictionaries and other collections.

**Example: Assigning a function to a variable**

```python
def greet():
    print("Hello, Python!")

message = greet

message()
```

Output:

```text
Hello, Python!
```

Here, `message` refers to the same function as `greet`. Parentheses are used to call the function.

**Example: Passing a function as an argument**

```python
def greet():
    return "Hello"

def display(func):
    print(func())

display(greet)
```

Output:

```text
Hello
```

The `greet` function is passed to `display` without calling it first.

### 2. Nested Functions

A nested function is a function defined inside another function.

The inner function can access variables from the outer function.

**Example:**

```python
def outer():
    print("This is the outer function")

    def inner():
        print("This is the inner function")

    inner()

outer()
```

Output:

```text
This is the outer function
This is the inner function
```

Nested functions are useful for:

- Organizing related functionality.
- Hiding helper functions inside another function.
- Creating closures.
- Implementing decorators.

### 3. Variable Scope and the LEGB Rule

Python uses the LEGB rule to determine where a variable is searched for.

LEGB stands for:

1. **Local:** Variables defined inside the current function.
2. **Enclosing:** Variables in the outer function of a nested function.
3. **Global:** Variables defined at the module level.
4. **Built-in:** Names provided by Python, such as `print()`, `len()` and `range()`.

**Example:**

```python
name = "Global"

def outer():
    name = "Enclosing"

    def inner():
        name = "Local"
        print(name)

    inner()

outer()
```

Output:

```text
Local
```

Python finds the variable in the local scope first.

### 4. Closures in Python

A closure is a function that remembers variables from its enclosing scope even after the outer function has finished executing.

A closure is generally created when:

- A function is defined inside another function.
- The inner function uses a variable from the outer function.
- The outer function returns the inner function.

**Example:**

```python
def outer(message):

    def inner():
        print(message)

    return inner

greet = outer("Welcome to Python")

greet()
```

Output:

```text
Welcome to Python
```

Even though `outer()` has finished executing, the returned `inner()` function remembers the value of `message`.

### 5. Closures with Parameters

Closures can be used to create functions with customized behavior.

**Example: Create a multiplier**

```python
def multiplier(factor):

    def multiply(number):
        return number * factor

    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5))
print(triple(5))
```

Output:

```text
10
15
```

Here:

- `double` remembers the factor 2.
- `triple` remembers the factor 3.
- Both functions use the same outer function but retain different values.

### 6. The nonlocal Keyword

The `nonlocal` keyword allows an inner function to modify a variable from its nearest enclosing function scope.

**Example:**

```python
def counter():

    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

count = counter()

print(count())
print(count())
print(count())
```

Output:

```text
1
2
3
```

Without `nonlocal`, assigning to `count` inside `increment()` would create a local variable instead of modifying the enclosing variable.

### 7. What are Decorators?

A decorator is a function that takes another function as input and extends or modifies its behavior without directly changing the original function's code.

Decorators are commonly used for:

- Logging.
- Authentication.
- Measuring execution time.
- Access control.
- Validation.
- Caching.

**Example:**

```python
def my_decorator(func):

    def wrapper():
        print("Before function execution")

        func()

        print("After function execution")

    return wrapper

def greet():
    print("Hello, Student!")

decorated_greet = my_decorator(greet)

decorated_greet()
```

Output:

```text
Before function execution
Hello, Student!
After function execution
```

Explanation:

1. `my_decorator()` receives the original function.
2. It defines a wrapper function.
3. The wrapper executes additional statements.
4. The original function is called inside the wrapper.
5. The wrapper is returned.

### 8. The @ Decorator Syntax

Python provides a convenient `@` syntax for applying decorators.

Instead of writing:

```python
def greet():
    print("Hello!")

greet = my_decorator(greet)
```

We can write:

```python
def my_decorator(func):

    def wrapper():
        print("Starting...")
        func()
        print("Finished!")

    return wrapper

@my_decorator
def greet():
    print("Hello!")

greet()
```

Output:

```text
Starting...
Hello!
Finished!
```

The `@my_decorator` syntax is equivalent to assigning the decorated function back to its original name.

### 9. Decorators with Arguments

A decorator can wrap a function that accepts arguments.

**Example:**

```python
def my_decorator(func):

    def wrapper(name):
        print("Function is starting")
        func(name)
        print("Function is completed")

    return wrapper

@my_decorator
def greet(name):
    print("Hello", name)

greet("Radhika")
```

Output:

```text
Function is starting
Hello Radhika
Function is completed
```

This example works for a function accepting one argument.

### 10. Using *args and **kwargs in Decorators

A general-purpose decorator should be able to work with functions that accept different numbers and types of arguments.

Python provides:

- `*args`: Collects extra positional arguments into a tuple.
- `**kwargs`: Collects extra keyword arguments into a dictionary.

**Example:**

```python
def my_decorator(func):

    def wrapper(*args, **kwargs):
        print("Before execution")

        result = func(*args, **kwargs)

        print("After execution")

        return result

    return wrapper

@my_decorator
def add(a, b):
    return a + b

@my_decorator
def greet(name, message="Welcome"):
    print(message, name)

print(add(10, 20))
greet("Riya")
```

Output:

```text
Before execution
After execution
30
Before execution
Welcome Riya
After execution
```

Using `*args` and `**kwargs` makes the decorator flexible enough to handle different function signatures.

### 11. The functools.wraps Decorator

When a decorator replaces a function with a wrapper, the decorated function may lose some of its original metadata, such as its name and documentation string.

Python provides `functools.wraps` to preserve this metadata.

**Example:**

```python
from functools import wraps

def my_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Executing function")
        return func(*args, **kwargs)

    return wrapper

@my_decorator
def greet():
    """This function greets the user."""
    print("Hello!")

greet()

print(greet.__name__)
print(greet.__doc__)
```

Output:

```text
Executing function
Hello!
greet
This function greets the user.
```

`@wraps(func)` copies important metadata from the original function to the wrapper.

### 12. Multiple Decorators

Python allows multiple decorators to be applied to one function.

**Example:**

```python
def decorator_one(func):

    def wrapper():
        print("Decorator One - Before")
        func()
        print("Decorator One - After")

    return wrapper

def decorator_two(func):

    def wrapper():
        print("Decorator Two - Before")
        func()
        print("Decorator Two - After")

    return wrapper

@decorator_one
@decorator_two
def greet():
    print("Hello!")

greet()
```

Output:

```text
Decorator One - Before
Decorator Two - Before
Hello!
Decorator Two - After
Decorator One - After
```

Decorators are applied from bottom to top.

### 13. Decorators with Their Own Arguments

Sometimes we need to pass arguments to the decorator itself.

This requires an additional outer function.

**Example:**

```python
def repeat(times):

    def decorator(func):

        def wrapper(*args, **kwargs):

            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator

@repeat(3)
def greet():
    print("Hello!")

greet()
```

Output:

```text
Hello!
Hello!
Hello!
```

Here:

- `repeat(3)` configures the decorator.
- `decorator()` receives the original function.
- `wrapper()` executes the function three times.

### 14. Lambda Functions

A lambda function is a small anonymous function created using the `lambda` keyword.

**Syntax:**

```python
lambda arguments: expression
```

**Example:**

```python
square = lambda number: number ** 2

print(square(5))
```

Output:

```text
25
```

Lambda functions are useful for short operations.

**Example: Using lambda with sorted()**

```python
students = [
    ("Aman", 85),
    ("Riya", 92),
    ("Neha", 78)
]

students.sort(key=lambda student: student[1])

print(students)
```

Output:

```text
[('Neha', 78), ('Aman', 85), ('Riya', 92)]
```

The `key` argument tells `sort()` to sort according to the marks.

### 15. Generators and yield

A generator is a special type of iterator that produces values one at a time.

Generators use the `yield` keyword instead of returning all values at once.

**Example:**

```python
def generate_numbers():

    yield 1
    yield 2
    yield 3

numbers = generate_numbers()

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

Output:

```text
1
2
3
```

Important points:

- `yield` produces a value and pauses the function.
- The function resumes from where it paused when the next value is requested.
- Generators are memory-efficient for large sequences.

### 16. Generator Expressions

Generator expressions provide a concise way to create generators.

**Syntax:**

```python
generator = (expression for item in iterable)
```

**Example:**

```python
numbers = (number ** 2 for number in range(1, 6))

for number in numbers:
    print(number)
```

Output:

```text
1
4
9
16
25
```

Unlike a list comprehension, a generator expression does not create the entire collection immediately.

### 17. Caching with functools.lru_cache

Caching stores the results of previous function calls so that repeated calls with the same arguments can be faster.

Python provides `functools.lru_cache` for this purpose.

**Example:**

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def square(number):
    print("Calculating...")
    return number ** 2

print(square(5))
print(square(5))
```

Output:

```text
Calculating...
25
25
```

The second call uses the cached result, so the function does not need to calculate the square again.

### 18. Recursion

Recursion occurs when a function calls itself to solve a smaller version of a problem.

**Example: Factorial**

```python
def factorial(number):

    if number == 0 or number == 1:
        return 1

    return number * factorial(number - 1)

print(factorial(5))
```

Output:

```text
120
```

The base condition prevents the function from calling itself indefinitely.

### 19. Type Hints

Type hints allow developers to indicate the expected types of function arguments and return values.

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

Type hints improve readability and help development tools detect potential mistakes. Python does not automatically enforce ordinary type hints at runtime.

### 20. Context Managers

A context manager manages resources such as files and ensures that cleanup happens appropriately.

The `with` statement is commonly used with context managers.

**Example:**

```python
with open("sample.txt", "w") as file:
    file.write("Learning Python")

print("File operation completed")
```

Output:

```text
File operation completed
```

The file is automatically closed when the `with` block finishes.

## Key concepts

1. **First-class functions:** Functions can be assigned, passed and returned like other objects.
2. **Nested functions:** Functions defined inside other functions.
3. **LEGB rule:** Local, Enclosing, Global and Built-in variable lookup.
4. **Closure:** A function that remembers variables from its enclosing scope.
5. **nonlocal:** Allows modification of a variable in an enclosing function scope.
6. **Decorator:** A function that extends another function's behavior.
7. **Wrapper:** An inner function used to add behavior around the original function.
8. **@ syntax:** A convenient way to apply decorators.
9. **\*args:** Collects extra positional arguments.
10. **\*\*kwargs:** Collects extra keyword arguments.
11. **functools.wraps:** Preserves important function metadata.
12. **Lambda:** A small anonymous function.
13. **Generator:** Produces values one at a time.
14. **yield:** Produces a value from a generator and pauses execution.
15. **Caching:** Stores previous results to avoid repeated calculations.
16. **Recursion:** A function calling itself.
17. **Type hints:** Indicate expected argument and return types.
18. **Context manager:** Manages resources and cleanup.

## Examples

### Example 1: Create a closure-based counter

```python
def create_counter():

    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

counter = create_counter()

print(counter())
print(counter())
print(counter())
```

Output:

```text
1
2
3
```

### Example 2: Create a logging decorator

```python
from functools import wraps

def log_function(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling:", func.__name__)

        result = func(*args, **kwargs)

        print("Execution completed")

        return result

    return wrapper

@log_function
def multiply(a, b):
    return a * b

print(multiply(4, 5))
```

Output:

```text
Calling: multiply
Execution completed
20
```

### Example 3: Measure execution time

```python
import time
from functools import wraps

def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print("Execution time:", end - start)

        return result

    return wrapper

@timer
def calculate():
    total = sum(range(100000))
    return total

print(calculate())
```

Output:

```text
Execution time: [time varies]
4999950000
```

### Example 4: Validate function arguments using a decorator

```python
from functools import wraps

def positive_only(func):

    @wraps(func)
    def wrapper(number):

        if number < 0:
            return "Negative numbers are not allowed"

        return func(number)

    return wrapper

@positive_only
def square(number):
    return number ** 2

print(square(5))
print(square(-3))
```

Output:

```text
25
Negative numbers are not allowed
```

### Example 5: Create a generator for even numbers

```python
def even_numbers(limit):

    for number in range(2, limit + 1, 2):
        yield number

for value in even_numbers(10):
    print(value)
```

Output:

```text
2
4
6
8
10
```

### Example 6: Use caching with Fibonacci

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(number):

    if number <= 1:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)

print(fibonacci(10))
```

Output:

```text
55
```

## Common mistakes

1. **Forgetting to return the wrapper**
   - A decorator should return the wrapper function.
   - Otherwise, the decorated function may become `None`.

2. **Calling a function instead of passing it**
   - Use `my_decorator(func)`, not `my_decorator(func())`, when passing a function object.

3. **Forgetting to call the original function**
   - The wrapper should call `func(*args, **kwargs)` if the original function is meant to execute.

4. **Forgetting to return the original result**
   - If the original function returns a value, the wrapper should normally return that value too.

5. **Not using `*args` and `**kwargs`**
   - A wrapper that accepts no arguments cannot directly wrap functions requiring arguments.

6. **Ignoring function metadata**
   - Use `@wraps(func)` to preserve the original function's name and documentation.

7. **Forgetting the nonlocal keyword**
   - Assigning to an enclosing variable inside a nested function requires `nonlocal`, unless a different approach is used.

8. **Confusing local and global scope**
   - Understand the LEGB rule before changing variables inside nested functions.

9. **Using yield incorrectly**
   - `yield` is used to produce generator values. It is not the same as returning a complete collection.

10. **Creating infinite recursion**
    - Recursive functions need a base condition to stop.

11. **Expecting type hints to validate values automatically**
    - Standard Python type hints are not runtime enforcement.

12. **Using complicated decorators unnecessarily**
    - Prefer a simple function when additional behavior is not required.

## Quick summary

- Functions are first-class objects in Python.
- Nested functions are defined inside other functions.
- Python follows the LEGB rule for variable scope.
- Closures remember values from their enclosing scope.
- `nonlocal` allows modification of enclosing variables.
- Decorators extend the behavior of existing functions.
- The `@` symbol provides convenient decorator syntax.
- `*args` and `**kwargs` support flexible function arguments.
- `functools.wraps` preserves function metadata.
- Lambda functions create small anonymous functions.
- Generators use `yield` to produce values one at a time.
- Generator expressions use parentheses.
- `lru_cache` can improve performance by caching results.
- Recursion occurs when a function calls itself.
- Type hints document expected types.
- Context managers manage resources safely.

## Practice

### Beginner Level

1. Create a nested function that prints a message.
2. Write a function that returns another function.
3. Create a closure that remembers a person's name.
4. Write a lambda function that calculates the square of a number.
5. Create a generator that produces numbers from 1 to 5.

### Intermediate Level

6. Create a closure-based counter using `nonlocal`.
7. Write a decorator that prints a message before and after function execution.
8. Create a decorator that accepts functions with different arguments.
9. Use `functools.wraps` in a custom decorator.
10. Create a generator that returns even numbers up to a given limit.

### Advanced Level

11. Create a decorator that measures function execution time.
12. Create a decorator that repeats a function a specified number of times.
13. Create a decorator that checks whether a number is positive.
14. Use `lru_cache` to optimize a recursive Fibonacci function.
15. Create multiple decorators and apply them to the same function.
16. Write a closure that maintains a running total.
17. Create a generator that reads values from a list one at a time.
18. Create a context manager using a class or `contextlib`.

### Practice Solutions

**Solution 1: Nested function**

```python
def outer():

    def inner():
        print("Hello from inner function")

    inner()

outer()
```

Output:

```text
Hello from inner function
```

**Solution 2: Closure**

```python
def greeting(message):

    def display():
        print(message)

    return display

hello = greeting("Welcome to Python")

hello()
```

Output:

```text
Welcome to Python
```

**Solution 3: Lambda function**

```python
square = lambda number: number ** 2

print(square(6))
```

Output:

```text
36
```

**Solution 4: Basic decorator**

```python
def decorator(func):

    def wrapper():
        print("Before execution")
        func()
        print("After execution")

    return wrapper

@decorator
def greet():
    print("Hello!")

greet()
```

Output:

```text
Before execution
Hello!
After execution
```

**Solution 5: Counter using nonlocal**

```python
def counter():

    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

c = counter()

print(c())
print(c())
```

Output:

```text
1
2
```

**Solution 6: Generator**

```python
def numbers():

    for number in range(1, 6):
        yield number

for value in numbers():
    print(value)
```

Output:

```text
1
2
3
4
5
```

## Learning resources

- **PDF:** [Open the supplied PDF resource](https://drive.google.com/file/d/18RdDS5oTQIPyj55rOjZF0ZOpHFi2q-3x/view?usp=drive_link)
- **YouTube:** Temporary testing link. Replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc