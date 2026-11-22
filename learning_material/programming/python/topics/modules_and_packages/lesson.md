
# Modules, Packages and Imports

**Course:** Python  
**Topic ID:** `modules_and_packages`

## Learning objectives

After completing this topic, learners should be able to:

- Understand what modules and packages are in Python.
- Explain why modules and packages are useful.
- Create and use custom Python modules.
- Import built-in and external modules.
- Use different import statements.
- Understand the difference between `import` and `from ... import`.
- Use aliases with the `as` keyword.
- Understand the purpose of `__name__` and `__main__`.
- Create Python packages using folders and `__init__.py`.
- Import modules from packages and subpackages.
- Understand absolute and relative imports.
- Install and use external Python libraries using `pip`.
- Understand Python's module search path.
- Organize Python programs into reusable files.
- Avoid common errors related to imports and modules.

## Explanation

### 1. What is a Module in Python?

A module is a Python file containing code that can be reused in other Python programs.

A module can contain:
- Variables
- Functions
- Classes
- Statements
- Other reusable code

Every Python file with a `.py` extension can be used as a module.

Instead of writing all the code in one large file, we can divide a program into smaller files called modules.

**Example:**

Suppose we have a file named `calculator.py`.

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
```

This file contains three functions.

We can use these functions in another Python file without rewriting them.

**Advantages of Modules:**

1. Code Reusability: Write code once and use it in multiple programs.
2. Organization: Divide large programs into smaller files.
3. Maintainability: Make changes to one module without modifying unrelated code.
4. Readability: Keep programs clean and understandable.
5. Collaboration: Different developers can work on different modules.

### 2. Creating and Using a Custom Module

Let's create two Python files in the same folder.

**Folder structure:**

```text
my_project/
│
├── calculator.py
└── main.py
```

**File 1: calculator.py**

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

**File 2: main.py**

```python
import calculator

result1 = calculator.add(10, 5)
result2 = calculator.subtract(10, 5)

print("Addition:", result1)
print("Subtraction:", result2)
```

**Output:**

```text
Addition: 15
Subtraction: 5
```

Explanation:

- `calculator.py` is the module.
- `main.py` imports the calculator module.
- `calculator.add()` calls the add function.
- `calculator.subtract()` calls the subtract function.

Both files should be in the same directory for this simple example to work directly.

### 3. What is Importing?

Importing means bringing code from another module into the current Python program so that it can be accessed and reused.

Python provides different ways to import modules and their contents.

### 4. Different Ways to Import Modules

**Method 1: import module**

This imports the complete module.

```python
import math

print(math.sqrt(25))
print(math.pi)
```

Output:

```text
5.0
3.141592653589793
```

We access module members using the dot operator.

**Method 2: from module import function**

This imports a particular function or object from a module.

```python
from math import sqrt

print(sqrt(36))
```

Output:

```text
6.0
```

We can use `sqrt()` directly without writing `math.sqrt()`.

**Method 3: Import Multiple Functions**

We can import multiple objects from the same module.

```python
from math import sqrt, factorial, pi

print(sqrt(49))
print(factorial(5))
print(pi)
```

Output:

```text
7.0
120
3.141592653589793
```

**Method 4: Import with an Alias**

An alias is an alternative name given to a module or imported object.

The `as` keyword is used to create an alias.

```python
import math as m

print(m.sqrt(64))
print(m.pi)
```

Output:

```text
8.0
3.141592653589793
```

**Method 5: Import Everything Using * **

The asterisk imports names exposed by a module according to its import rules.

```python
from math import *

print(sqrt(25))
print(factorial(4))
```

Output:

```text
5.0
24
```

However, using `from module import *` is generally discouraged because it can:
- Make it difficult to identify where a name came from.
- Cause naming conflicts.
- Reduce code readability.

Prefer importing the required functions explicitly.

### 5. Built-in Python Modules

Python provides many modules as part of its standard library.

These modules provide ready-made functions and features.

Some commonly used modules are:

| Module | Purpose |
|---|---|
| math | Mathematical operations |
| random | Random number generation |
| datetime | Working with dates and times |
| os | Operating system operations |
| sys | Python interpreter and system information |
| json | Working with JSON data |
| re | Regular expressions |
| statistics | Statistical calculations |
| pathlib | Working with file paths |
| collections | Specialized data structures |

**Example 1: math Module**

```python
import math

print(math.sqrt(100))
print(math.factorial(5))
print(math.ceil(4.2))
print(math.floor(4.8))
```

Output:

```text
10.0
120
5
4
```

**Example 2: random Module**

```python
import random

print(random.randint(1, 10))
```

Output:

```text
A random integer between 1 and 10
```

The exact output changes each time the program runs.

**Example 3: datetime Module**

```python
import datetime

today = datetime.date.today()

print(today)
```

Output:

```text
The current date
```

The actual output depends on the date when the program runs.

**Example 4: os Module**

```python
import os

print(os.getcwd())
```

Output:

```text
The current working directory
```

**Example 5: statistics Module**

```python
import statistics

numbers = [10, 20, 30, 40, 50]

print(statistics.mean(numbers))
print(statistics.median(numbers))
```

Output:

```text
30
30
```

### 6. What is a Package in Python?

A package is a way to organize related Python modules into a directory structure.

A package helps manage large applications by grouping related modules together.

For example, an application may have separate modules for:
- User management
- Payment processing
- Authentication
- Database operations

These modules can be grouped into packages.

**Example folder structure:**

```text
my_project/
│
├── main.py
│
└── student/
    ├── __init__.py
    ├── details.py
    └── marks.py
```

Here:
- `student` is a package.
- `__init__.py` is the package initialization file.
- `details.py` is a module.
- `marks.py` is another module.

Traditionally, `__init__.py` marks a directory as a regular Python package and can contain initialization code.

Modern Python also supports namespace packages that do not require an `__init__.py` file.

### 7. Creating a Package

Let's create a package named `student`.

**Step 1: Create a folder**

Create a folder named:

```text
student
```

**Step 2: Create __init__.py**

Inside the folder, create:

```text
__init__.py
```

It can be empty.

**Step 3: Create details.py**

```python
def student_name():
    return "Riya"

def student_age():
    return 20
```

**Step 4: Create marks.py**

```python
def student_marks():
    return 90
```

**Complete folder structure:**

```text
my_project/
│
├── main.py
│
└── student/
    ├── __init__.py
    ├── details.py
    └── marks.py
```

**Step 5: Import the Package Modules**

Inside `main.py`:

```python
from student import details, marks

print("Name:", details.student_name())
print("Age:", details.student_age())
print("Marks:", marks.student_marks())
```

Output:

```text
Name: Riya
Age: 20
Marks: 90
```

### 8. Different Ways to Import from Packages

**Method 1: Import a Module from a Package**

```python
import student.details

print(student.details.student_name())
```

**Method 2: Using from ... import**

```python
from student.details import student_name

print(student_name())
```

**Method 3: Importing Multiple Modules**

```python
from student import details, marks

print(details.student_name())
print(marks.student_marks())
```

**Method 4: Using Aliases**

```python
from student import details as d

print(d.student_name())
```

### 9. Understanding __init__.py

The `__init__.py` file is used to initialize a regular Python package.

It can:
- Contain initialization code.
- Define package-level variables.
- Expose selected functions or classes.
- Control convenient imports from the package.

**Example:**

Folder structure:

```text
my_project/
│
├── main.py
│
└── calculator/
    ├── __init__.py
    ├── addition.py
    └── subtraction.py
```

**addition.py**

```python
def add(a, b):
    return a + b
```

**subtraction.py**

```python
def subtract(a, b):
    return a - b
```

**__init__.py**

```python
from .addition import add
from .subtraction import subtract
```

Now we can import the functions directly from the package.

**main.py**

```python
from calculator import add, subtract

print(add(10, 5))
print(subtract(10, 5))
```

Output:

```text
15
5
```

The leading dot in `.addition` and `.subtraction` indicates a relative import within the package.

### 10. Absolute Imports

An absolute import uses the full path from the top-level package or import root to identify the module.

**Example:**

```python
from student.details import student_name

print(student_name())
```

Here:
- `student` is the package.
- `details` is the module.
- `student_name` is the function.

Absolute imports are often easier to understand because the complete module path is visible.

### 11. Relative Imports

Relative imports are used to import modules from the same package or nearby packages.

They use dots to indicate the location.

Example structure:

```text
my_project/
│
└── student/
    ├── __init__.py
    ├── details.py
    └── marks.py
```

Inside `marks.py`:

```python
from .details import student_name

def display_marks():
    print(student_name())
    print(90)
```

Here:
- `.` means the current package.
- `..` means the parent package.
- `...` means the package one level above the parent.

Relative imports are generally used within packages and normally require the module to be executed as part of the package.

### 12. Difference Between Modules and Packages

| Module | Package |
|---|---|
| A single Python file | A directory organizing Python modules and possibly subpackages |
| Contains reusable code | Groups related modules |
| Usually has a `.py` extension | Usually represented by a directory |
| Example: `calculator.py` | Example: `student/` |
| Suitable for smaller units of functionality | Useful for organizing larger applications |

### 13. What is __name__?

`__name__` is a special built-in variable in Python.

Its value depends on how a module is being used.

When a Python file is executed directly, its `__name__` value is:

```python
"__main__"
```

When the file is imported as a module, its `__name__` is usually the module's name.

**Example:**

Create a file named `test.py`.

```python
print(__name__)
```

If we execute it directly:

```text
__main__
```

If we import it from another file:

```python
import test
```

The module prints:

```text
test
```

### 14. Understanding if __name__ == "__main__"

This condition checks whether a Python file is being executed directly rather than imported as a module.

It is commonly used to separate reusable code from code that should run only when the file is executed directly.

**Example:**

File: `calculator.py`

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("Calculator Program")

    print(add(10, 5))
    print(subtract(10, 5))
```

If we execute `calculator.py` directly, the output is:

```text
Calculator Program
15
5
```

If another file imports `calculator`, the functions become available, but the code inside the `if` block does not run automatically.

This is useful for creating reusable modules that can also be tested independently.

### 15. External Modules and pip

Python also supports external libraries developed by the community.

These libraries are not necessarily included in the Python standard library.

We can install many of them using `pip`.

`pip` is Python's package installer.

**Example: Installing NumPy**

Open the terminal or CMD and run:

```cmd
python -m pip install numpy
```

**Using NumPy:**

```python
import numpy as np

numbers = np.array([10, 20, 30, 40])

print(numbers)
print(numbers.mean())
```

Output:

```text
[10 20 30 40]
25.0
```

**Other commonly used external libraries:**

| Library | Purpose |
|---|---|
| NumPy | Numerical computing |
| Pandas | Data analysis and manipulation |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Machine learning |
| TensorFlow | Deep learning |
| Requests | Making HTTP requests |
| Flask | Web application development |
| Django | Web application framework |

### 16. Useful pip Commands

**Install a Package**

```cmd
python -m pip install package_name
```

**Example:**

```cmd
python -m pip install requests
```

**Check Installed Packages**

```cmd
python -m pip list
```

**Display Package Information**

```cmd
python -m pip show numpy
```

**Upgrade a Package**

```cmd
python -m pip install --upgrade numpy
```

**Uninstall a Package**

```cmd
python -m pip uninstall numpy
```

**Save Installed Dependencies**

```cmd
python -m pip freeze > requirements.txt
```

**Install Dependencies from a File**

```cmd
python -m pip install -r requirements.txt
```

### 17. Understanding Python's Module Search Path

When importing a module, Python searches for it in locations specified by its module search path.

This search path is available through `sys.path`.

**Example:**

```python
import sys

for path in sys.path:
    print(path)
```

Output:

```text
Python module search directories
```

The exact paths depend on the Python installation and execution environment.

Common search locations include:
- The directory containing the input script.
- Directories listed in `PYTHONPATH`.
- Standard library directories.
- Installed package directories such as `site-packages`.

Understanding the module search path helps troubleshoot `ModuleNotFoundError`.

### 18. Practical Example: Organizing a Student Management Program

Let's build a small application using modules.

**Folder structure:**

```text
student_project/
│
├── main.py
│
└── student/
    ├── __init__.py
    ├── details.py
    └── marks.py
```

**File: details.py**

```python
def get_name():
    return "Riya"

def get_age():
    return 20
```

**File: marks.py**

```python
def get_marks():
    return [85, 90, 95]

def calculate_average(marks):
    return sum(marks) / len(marks)
```

**File: main.py**

```python
from student.details import get_name, get_age
from student.marks import get_marks, calculate_average

name = get_name()
age = get_age()

marks = get_marks()
average = calculate_average(marks)

print("Student Name:", name)
print("Student Age:", age)
print("Marks:", marks)
print("Average Marks:", average)
```

Output:

```text
Student Name: Riya
Student Age: 20
Marks: [85, 90, 95]
Average Marks: 90.0
```

This example demonstrates how a program can be divided into separate modules and organized into a package.

## Key concepts

- **Module:** A Python file containing reusable code.
- **Package:** A directory that organizes related Python modules and subpackages.
- **Import:** Making code from another module available.
- **import:** Imports a module.
- **from ... import:** Imports selected objects from a module.
- **as:** Creates an alias for an imported module or object.
- **Built-in module:** A module included with Python.
- **External library:** A separately installed Python package or library.
- **pip:** Python's package installer.
- **__init__.py:** Package initialization file traditionally used to mark regular packages.
- **__name__:** A special variable identifying a module's execution name.
- **__main__:** The special name assigned to a file executed as the main program.
- **Absolute import:** Imports using a complete package path.
- **Relative import:** Imports using dot notation relative to the current package.
- **sys.path:** List of locations Python searches for modules.
- **requirements.txt:** A file commonly used to record project dependencies.

## Common mistakes

1. **Incorrect module name**

   Incorrect:

   ```python
   import calulator
   ```

   Correct:

   ```python
   import calculator
   ```

   Make sure the module name matches the filename.

2. **Forgetting the module location**

   If a module is in another directory, Python may not find it automatically.

   Keep your project structure organized and use proper package imports.

3. **Naming a file after a built-in module**

   Avoid naming your own files:

   ```text
   random.py
   math.py
   json.py
   ```

   These names can shadow standard library modules and cause confusing import errors.

4. **Using the wrong import syntax**

   Incorrect:

   ```python
   import math

   print(sqrt(25))
   ```

   Correct:

   ```python
   import math

   print(math.sqrt(25))
   ```

   Alternatively:

   ```python
   from math import sqrt

   print(sqrt(25))
   ```

5. **Confusing a module with a package**

   A module is generally a Python file, whereas a package organizes modules in directories.

6. **Forgetting __init__.py in a regular package**

   For traditional regular packages, include an `__init__.py` file. Namespace packages are an exception and can work without it.

7. **Using relative imports incorrectly**

   Relative imports are intended for package modules. Running an individual package file directly may cause an import error.

   Run the application from the appropriate project root, using package-aware execution where necessary.

8. **Circular imports**

   A circular import happens when two modules depend on each other directly or indirectly.

   Example:

   ```text
   module_a imports module_b
   module_b imports module_a
   ```

   This can cause partially initialized module errors.

   Avoid unnecessary circular dependencies by reorganizing shared functionality into another module.

9. **Using import * everywhere**

   This can create naming conflicts and make code difficult to understand.

   Prefer explicit imports.

10. **Installing a package in the wrong Python environment**

    A package may be installed for a different Python interpreter or virtual environment.

    Use:

    ```cmd
    python -m pip install package_name
    ```

    from the environment in which you run your program.

11. **Confusing standard library modules with external libraries**

    Modules such as `math` and `random` are included with Python. Libraries such as NumPy generally need to be installed separately.

12. **Using incorrect capitalization**

    Python module and package names are case-sensitive on many operating systems.

    Match the exact filename and import name.

## Quick summary

- A module is a Python file containing reusable code.
- A package organizes related modules into directories.
- The `import` keyword is used to import modules.
- `from ... import` imports selected objects.
- The `as` keyword creates aliases.
- Python provides built-in modules such as `math`, `random`, and `datetime`.
- External libraries can be installed using `pip`.
- The `__init__.py` file can initialize a regular package and expose package-level functionality.
- Absolute imports use complete module paths.
- Relative imports use dots to identify locations within packages.
- `__name__` identifies the module's execution name.
- `if __name__ == "__main__"` separates direct execution from imported use.
- `sys.path` contains locations Python searches for modules.
- `requirements.txt` records project dependencies.
- Modules and packages help make applications reusable, organized, and maintainable.

## Practice

### Beginner Level

**1. Create a Module**

Create a Python file named `greeting.py` with a function that prints "Welcome to Python".

Import it into another file and call the function.

**2. Use the Math Module**

Import the `math` module and calculate:
- Square root of 144.
- Factorial of 5.
- Value of pi.

**3. Import Using an Alias**

Import the `random` module using the alias `r`.

Generate a random integer between 1 and 100.

**4. Import Specific Functions**

Import `sqrt` and `pow` from the `math` module and use them.

**5. Create a Calculator Module**

Create a module containing functions for addition, subtraction, multiplication, and division.

Import and use these functions in another file.

### Intermediate Level

**6. Create a Student Package**

Create a package named `student` containing:
- `details.py`
- `marks.py`
- `__init__.py`

Store student information and marks in separate modules.

**7. Use the datetime Module**

Write a program to display the current date and time.

**8. Install and Use NumPy**

Install NumPy using pip and create an array containing five numbers.

Calculate its sum and average.

**9. Use __name__**

Create a module containing a function and an `if __name__ == "__main__"` block.

Import it into another Python file and observe the difference.

**10. Create a Utility Package**

Create a package named `utilities` with separate modules for:
- Mathematical operations.
- String operations.
- Number operations.

Import and use the functions from `main.py`.

### Advanced Level

**11. Create a Banking Package**

Create a package named `banking` containing:
- `account.py`
- `transactions.py`
- `__init__.py`

Implement deposit, withdrawal, and balance-checking functions.

**12. Create a Nested Package**

Create the following structure:

```text
project/
│
├── main.py
│
└── college/
    ├── __init__.py
    │
    ├── students/
    │   ├── __init__.py
    │   └── details.py
    │
    └── teachers/
        ├── __init__.py
        └── details.py
```

Import and use functions from both subpackages.

**13. Create a Package with Aliases**

Create a package containing mathematical functions and import them using aliases.

**14. Create requirements.txt**

Install two external libraries and generate a `requirements.txt` file using pip.

**15. Build a Mini Project**

Create a student management application using separate modules for:
- Student details.
- Student marks.
- Attendance.
- Result calculation.
- Main program.

### Sample Solutions

**Solution 1: Create a Module**

File: `greeting.py`

```python
def greet():
    print("Welcome to Python")
```

File: `main.py`

```python
import greeting

greeting.greet()
```

Output:

```text
Welcome to Python
```

**Solution 2: Use the Math Module**

```python
import math

print(math.sqrt(144))
print(math.factorial(5))
print(math.pi)
```

Output:

```text
12.0
120
3.141592653589793
```

**Solution 3: Import Using an Alias**

```python
import random as r

number = r.randint(1, 100)

print(number)
```

Output:

```text
A random integer between 1 and 100
```

**Solution 4: Import Specific Functions**

```python
from math import sqrt, pow

print(sqrt(25))
print(pow(2, 3))
```

Output:

```text
5.0
8.0
```

**Solution 5: Create a Calculator Module**

File: `calculator.py`

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
```

File: `main.py`

```python
import calculator

print(calculator.add(10, 5))
print(calculator.subtract(10, 5))
print(calculator.multiply(10, 5))
print(calculator.divide(10, 5))
```

Output:

```text
15
5
50
2.0
```

**Solution 6: Create a Student Package**

Folder structure:

```text
project/
│
├── main.py
│
└── student/
    ├── __init__.py
    ├── details.py
    └── marks.py
```

File: `student/details.py`

```python
def get_name():
    return "Riya"

def get_age():
    return 20
```

File: `student/marks.py`

```python
def get_marks():
    return [85, 90, 95]
```

File: `main.py`

```python
from student.details import get_name, get_age
from student.marks import get_marks

print("Name:", get_name())
print("Age:", get_age())
print("Marks:", get_marks())
```

Output:

```text
Name: Riya
Age: 20
Marks: [85, 90, 95]
```

**Solution 7: Use datetime Module**

```python
import datetime

now = datetime.datetime.now()

print("Current Date and Time:", now)
print("Current Date:", now.date())
print("Current Time:", now.time())
```

The output depends on the system date and time.

**Solution 8: Install and Use NumPy**

First install NumPy:

```cmd
python -m pip install numpy
```

Python program:

```python
import numpy as np

numbers = np.array([10, 20, 30, 40, 50])

print("Array:", numbers)
print("Sum:", numbers.sum())
print("Average:", numbers.mean())
```

Output:

```text
Array: [10 20 30 40 50]
Sum: 150
Average: 30.0
```

**Solution 9: Use __name__**

File: `calculator.py`

```python
def add(a, b):
    return a + b

if __name__ == "__main__":
    print("Running calculator directly")
    print(add(10, 20))
```

File: `main.py`

```python
import calculator

print(calculator.add(5, 5))
```

When `calculator.py` is executed directly, its main block runs.

When `main.py` imports it, the main block in `calculator.py` does not run.

Output from `main.py`:

```text
10
```

**Solution 10: Create a Utility Package**

Folder structure:

```text
project/
│
├── main.py
│
└── utilities/
    ├── __init__.py
    ├── math_operations.py
    ├── string_operations.py
    └── number_operations.py
```

File: `utilities/math_operations.py`

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

File: `utilities/string_operations.py`

```python
def reverse_string(text):
    return text[::-1]

def uppercase(text):
    return text.upper()
```

File: `utilities/number_operations.py`

```python
def is_even(num):
    return num % 2 == 0

def square(num):
    return num ** 2
```

File: `main.py`

```python
from utilities import math_operations
from utilities import string_operations
from utilities import number_operations

print(math_operations.add(10, 5))
print(string_operations.reverse_string("Python"))
print(string_operations.uppercase("python"))
print(number_operations.is_even(10))
print(number_operations.square(5))
```

Output:

```text
15
nohtyP
PYTHON
True
25
```

**Solution 11: Create a Banking Package**

Folder structure:

```text
project/
│
├── main.py
│
└── banking/
    ├── __init__.py
    ├── account.py
    └── transactions.py
```

File: `banking/account.py`

```python
balance = 1000

def get_balance():
    return balance
```

File: `banking/transactions.py`

```python
from . import account

def deposit(amount):
    if amount <= 0:
        return "Enter a positive amount"

    account.balance += amount
    return account.balance

def withdraw(amount):
    if amount <= 0:
        return "Enter a positive amount"

    if amount > account.balance:
        return "Insufficient balance"

    account.balance -= amount
    return account.balance
```

File: `main.py`

```python
from banking.account import get_balance
from banking.transactions import deposit, withdraw

print("Initial Balance:", get_balance())

print("After Deposit:", deposit(500))
print("After Withdrawal:", withdraw(200))

print("Final Balance:", get_balance())
```

Output:

```text
Initial Balance: 1000
After Deposit: 1500
After Withdrawal: 1300
Final Balance: 1300
```

This is a basic learning example. A real banking application would need stronger validation, data persistence, and security.

**Solution 12: Create a Nested Package**

File: `college/students/details.py`

```python
def student_name():
    return "Riya"
```

File: `college/teachers/details.py`

```python
def teacher_name():
    return "Mr. Sharma"
```

File: `main.py`

```python
from college.students.details import student_name
from college.teachers.details import teacher_name

print("Student:", student_name())
print("Teacher:", teacher_name())
```

Output:

```text
Student: Riya
Teacher: Mr. Sharma
```

**Solution 13: Create a Package with Aliases**

```python
from utilities import math_operations as m

print(m.add(10, 20))
print(m.multiply(5, 4))
```

Output:

```text
30
20
```

**Solution 14: Create requirements.txt**

Run these commands in the terminal:

```cmd
python -m pip install numpy
python -m pip install requests
python -m pip freeze > requirements.txt
```

The generated `requirements.txt` records installed packages and versions from the active environment.

**Solution 15: Student Management Mini Project**

Folder structure:

```text
student_project/
│
├── main.py
│
└── student/
    ├── __init__.py
    ├── details.py
    ├── marks.py
    └── attendance.py
```

File: `student/details.py`

```python
def get_student_details():
    return {
        "name": "Riya",
        "age": 20,
        "course": "Python"
    }
```

File: `student/marks.py`

```python
def get_marks():
    return [85, 90, 95]

def calculate_average(marks):
    return sum(marks) / len(marks)
```

File: `student/attendance.py`

```python
def get_attendance():
    return 92
```

File: `main.py`

```python
from student.details import get_student_details
from student.marks import get_marks, calculate_average
from student.attendance import get_attendance

details = get_student_details()
marks = get_marks()

average = calculate_average(marks)
attendance = get_attendance()

print("Student Details:", details)
print("Marks:", marks)
print("Average Marks:", average)
print("Attendance:", attendance, "%")
```

Output:

```text
Student Details: {'name': 'Riya', 'age': 20, 'course': 'Python'}
Marks: [85, 90, 95]
Average Marks: 90.0
Attendance: 92 %
```

## Learning resources

- **PDF:** [Modules, Packages and Imports](https://drive.google.com/file/d/1lCqN9AyJEvziRXtqg4P3Bp5L6cb88ceJ/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)