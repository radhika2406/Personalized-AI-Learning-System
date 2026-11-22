
# Variables and Data Types

**Course:** Python  
**Topic ID:** `variables`

## Learning objectives

After completing this topic, learners should be able to:

- Understand variables and their purpose in Python.
- Create and assign values to variables.
- Understand Python's dynamic typing.
- Follow variable naming rules and conventions.
- Identify different built-in Python data types.
- Understand numeric, string, Boolean, and collection data types.
- Use the `type()` function to identify data types.
- Use the `isinstance()` function to check data types.
- Understand mutable and immutable data types.
- Perform type conversion and type casting.
- Differentiate between implicit and explicit type conversion.
- Take user input using the `input()` function.
- Display output using the `print()` function.
- Use multiple assignment and chained assignment.
- Understand constants and naming conventions.
- Apply variables and data types in practical Python programs.

## Explanation

# Part 1: Variables in Python

## 1. What is a Variable?

A variable is a name used to refer to a value stored in a program.

Variables allow us to store information and use it whenever required.

For example, if we want to store a student's name and age, we can create variables.

```python
name = "Riya"
age = 20

print(name)
print(age)
```

Output:

```text
Riya
20
```

Here:

- `name` is a variable storing the string `"Riya"`.
- `age` is a variable storing the integer `20`.
- `=` is the assignment operator.
- `print()` displays the values.

### How Does Variable Assignment Work?

Consider:

```python
marks = 85
```

Python evaluates the value `85` and binds the variable name `marks` to that value.

We can use the variable multiple times.

```python
marks = 85

print(marks)
print(marks + 5)
print(marks * 2)
```

Output:

```text
85
90
170
```

The original value of `marks` remains 85 because the calculations do not reassign it.

## 2. Creating Variables

Python does not require us to declare a variable's data type before assigning a value.

We can create a variable simply by assigning a value to it.

```python
name = "Aman"
age = 21
height = 5.8
is_student = True

print(name)
print(age)
print(height)
print(is_student)
```

Output:

```text
Aman
21
5.8
True
```

Python automatically determines the type of each value.

## 3. Variable Naming Rules

Python has certain rules for naming variables.

### Valid Variable Names

- A variable name can contain letters.
- A variable name can contain numbers.
- A variable name can contain underscores (`_`).
- A variable name must start with a letter or underscore.
- Variable names are case-sensitive.
- Variable names cannot be Python keywords.

Examples:

```python
name = "Riya"
student_age = 20
marks1 = 85
_total = 500
firstName = "Aman"
```

All these are valid variable names.

### Invalid Variable Names

```python
1name = "Riya"
student-age = 20
my name = "Aman"
class = "Python"
```

These are invalid because:

- `1name` starts with a number.
- `student-age` contains a hyphen.
- `my name` contains a space.
- `class` is a reserved Python keyword.

### Variable Naming Conventions

Python recommends using `snake_case` for ordinary variable names.

Example:

```python
student_name = "Riya"
total_marks = 450
average_score = 90
```

Avoid unclear names such as:

```python
x = 100
a = 200
b = 300
```

Prefer meaningful names:

```python
total_price = 100
discount = 200
final_amount = 300
```

Meaningful names make programs easier to understand.

## 4. Python is Dynamically Typed

Python is a dynamically typed language.

This means we do not need to specify a variable's data type explicitly when creating it.

Python determines the type based on the assigned value.

Example:

```python
value = 10

print(value)
print(type(value))
```

Output:

```text
10
<class 'int'>
```

We can assign a different type of value to the same variable later.

```python
value = 10
print(type(value))

value = "Python"
print(type(value))

value = 10.5
print(type(value))
```

Output:

```text
<class 'int'>
<class 'str'>
<class 'float'>
```

The variable name can refer to values of different types at different times.

**Important:** Dynamic typing does not mean Python ignores data types. Every value still has a type.

## 5. Multiple Variable Assignment

Python allows multiple variables to be assigned in one statement.

### A. Assigning Different Values

```python
name, age, city = "Riya", 20, "Bhopal"

print(name)
print(age)
print(city)
```

Output:

```text
Riya
20
Bhopal
```

Each variable receives the corresponding value.

### B. Assigning the Same Value to Multiple Variables

```python
a = b = c = 100

print(a)
print(b)
print(c)
```

Output:

```text
100
100
100
```

All three names refer to the same integer value.

### C. Swapping Variables

Python allows variables to be swapped easily.

```python
a = 10
b = 20

a, b = b, a

print(a)
print(b)
```

Output:

```text
20
10
```

This is called multiple assignment or tuple-based unpacking.

## 6. Reassigning Variables

A variable can be assigned a new value whenever required.

```python
score = 50

print(score)

score = 80

print(score)
```

Output:

```text
50
80
```

The variable `score` refers to the new value after reassignment.

## 7. Deleting Variables

The `del` keyword removes a variable name.

```python
name = "Riya"

print(name)

del name
```

After deletion, trying to access `name` raises a `NameError` because the name is no longer defined.

```python
print(name)
```

Output:

```text
NameError
```

**Important:** `del` removes a name binding. It does not necessarily immediately destroy the underlying object if other references to that object still exist.

# Part 2: Data Types in Python

## 8. What is a Data Type?

A data type defines the kind of value stored in a variable.

It determines what operations can be performed on that value.

For example:

- Integers represent whole numbers.
- Floats represent decimal numbers.
- Strings represent text.
- Booleans represent truth values.

Python provides several built-in data types.

### Main Categories of Python Data Types

| Category | Data Type | Example |
|---|---|---|
| Numeric | `int` | `10` |
| Numeric | `float` | `10.5` |
| Numeric | `complex` | `2 + 3j` |
| Boolean | `bool` | `True` |
| Text | `str` | `"Python"` |
| Sequence | `list` | `[10, 20, 30]` |
| Sequence | `tuple` | `(10, 20, 30)` |
| Sequence | `range` | `range(5)` |
| Set | `set` | `{10, 20, 30}` |
| Set | `frozenset` | `frozenset({1, 2})` |
| Mapping | `dict` | `{"name": "Riya"}` |
| Binary | `bytes` | `b"Hello"` |
| Binary | `bytearray` | `bytearray(5)` |
| Binary | `memoryview` | `memoryview(b"abc")` |
| Special | `NoneType` | `None` |

## 9. Numeric Data Types

Numeric data types are used to store numbers.

Python provides three main numeric types:

1. Integer (`int`)
2. Floating-point (`float`)
3. Complex (`complex`)

### A. Integer (int)

An integer represents a whole number without a decimal point.

Examples:

```python
age = 20
marks = 95
temperature = -5

print(age)
print(marks)
print(temperature)
```

Output:

```text
20
95
-5
```

Integers can be positive, negative, or zero.

Python integers can represent arbitrarily large values, limited by available memory.

Example:

```python
number = 123456789012345678901234567890

print(number)
```

### B. Floating-Point (float)

A float represents a number with a decimal point.

Examples:

```python
price = 99.99
height = 5.8
percentage = 85.5

print(price)
print(height)
print(percentage)
```

Output:

```text
99.99
5.8
85.5
```

Floats are commonly used for:

- Prices
- Measurements
- Percentages
- Scientific calculations

**Important:** Floating-point numbers use finite binary precision. Some decimal values cannot be represented exactly.

Example:

```python
print(0.1 + 0.2)
```

Output:

```text
0.30000000000000004
```

This is a floating-point precision effect.

### C. Complex Numbers (complex)

Complex numbers contain a real part and an imaginary part.

Python uses `j` to represent the imaginary component.

Example:

```python
number = 2 + 3j

print(number)
print(type(number))
```

Output:

```text
(2+3j)
<class 'complex'>
```

We can access the real and imaginary parts.

```python
number = 2 + 3j

print(number.real)
print(number.imag)
```

Output:

```text
2.0
3.0
```

Complex numbers are used in areas such as mathematics, engineering, and signal processing.

## 10. Boolean Data Type (bool)

A Boolean represents one of two values:

- `True`
- `False`

Booleans are commonly used in conditions and decision-making.

Example:

```python
is_student = True
is_employed = False

print(is_student)
print(is_employed)

print(type(is_student))
```

Output:

```text
True
False
<class 'bool'>
```

### Boolean Expressions

Comparison operators produce Boolean results.

```python
a = 10
b = 20

print(a > b)
print(a < b)
print(a == b)
print(a != b)
```

Output:

```text
False
True
False
True
```

### Boolean Operators

Python provides three main logical operators:

| Operator | Meaning |
|---|---|
| `and` | True when both conditions are true |
| `or` | True when at least one condition is true |
| `not` | Reverses the truth value |

Example:

```python
age = 20

print(age >= 18 and age <= 60)
print(age < 18 or age > 60)
print(not age < 18)
```

Output:

```text
True
False
True
```

## 11. String Data Type (str)

A string is a sequence of characters used to store text.

Strings are enclosed within single, double, or triple quotes.

Example:

```python
name = "Riya"
city = 'Bhopal'
message = """Welcome to Python"""

print(name)
print(city)
print(message)
```

Output:

```text
Riya
Bhopal
Welcome to Python
```

### Important String Properties

- Strings are ordered.
- Strings are immutable.
- Strings support indexing.
- Strings support slicing.
- Strings can contain letters, numbers, symbols, and spaces.

Example:

```python
text = "Python"

print(text[0])
print(text[-1])
print(text[0:3])
```

Output:

```text
P
n
Pyt
```

### String Concatenation

The `+` operator joins strings.

```python
first_name = "Riya"
last_name = "Patel"

full_name = first_name + " " + last_name

print(full_name)
```

Output:

```text
Riya Patel
```

### String Repetition

The `*` operator repeats strings.

```python
word = "Python "

print(word * 3)
```

Output:

```text
Python Python Python
```

## 12. Sequence Data Types

Sequence data types store multiple elements in an ordered collection.

Python provides:

- List
- Tuple
- Range
- String

### A. List (list)

A list is an ordered and mutable collection.

Mutable means its elements can be added, removed, or modified.

Lists are created using square brackets `[]`.

Example:

```python
fruits = ["apple", "banana", "mango"]

print(fruits)
```

Output:

```text
['apple', 'banana', 'mango']
```

Lists allow duplicate values and different data types.

```python
data = [10, "Python", 20.5, True, 10]

print(data)
```

Output:

```text
[10, 'Python', 20.5, True, 10]
```

Modifying a list:

```python
numbers = [10, 20, 30]

numbers[0] = 100

print(numbers)
```

Output:

```text
[100, 20, 30]
```

Adding an element:

```python
numbers = [10, 20, 30]

numbers.append(40)

print(numbers)
```

Output:

```text
[10, 20, 30, 40]
```

### B. Tuple (tuple)

A tuple is an ordered and immutable collection.

Tuples are created using parentheses `()`.

Example:

```python
numbers = (10, 20, 30)

print(numbers)
print(type(numbers))
```

Output:

```text
(10, 20, 30)
<class 'tuple'>
```

Tuples allow duplicate values and support indexing and slicing.

```python
numbers = (10, 20, 30, 40)

print(numbers[0])
print(numbers[1:3])
```

Output:

```text
10
(20, 30)
```

A single-element tuple requires a comma.

```python
data = (10,)

print(type(data))
```

Output:

```text
<class 'tuple'>
```

### C. Range (range)

The `range` type represents an immutable sequence of integers.

It is commonly used in loops.

Syntax:

```python
range(start, stop, step)
```

Where:

- `start` is the starting number.
- `stop` is the ending boundary, which is excluded.
- `step` is the interval between numbers.

Example:

```python
numbers = range(1, 6)

print(list(numbers))
```

Output:

```text
[1, 2, 3, 4, 5]
```

Example with a step:

```python
numbers = range(2, 11, 2)

print(list(numbers))
```

Output:

```text
[2, 4, 6, 8, 10]
```

Using range in a loop:

```python
for i in range(1, 6):
    print(i)
```

Output:

```text
1
2
3
4
5
```

## 13. Set Data Types

Sets store unique elements without a guaranteed positional order.

Python provides:

- `set`
- `frozenset`

### A. Set (set)

A set is a mutable collection of unique elements.

Example:

```python
numbers = {10, 20, 30, 10}

print(numbers)
```

The set contains:

```text
10, 20, 30
```

Duplicate elements are automatically removed.

Sets do not support indexing.

Adding an element:

```python
numbers = {10, 20, 30}

numbers.add(40)

print(numbers)
```

The set contains:

```text
10, 20, 30, 40
```

### B. Frozenset (frozenset)

A frozenset is an immutable set.

Its elements cannot be added or removed after creation.

Example:

```python
numbers = frozenset([10, 20, 30])

print(numbers)
print(type(numbers))
```

Output contains:

```text
10, 20, 30
<class 'frozenset'>
```

## 14. Mapping Data Type: Dictionary (dict)

A dictionary stores data in key-value pairs.

Dictionaries are created using curly braces with keys and values separated by colons.

Example:

```python
student = {
    "name": "Riya",
    "age": 20,
    "city": "Bhopal"
}

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 20, 'city': 'Bhopal'}
```

### Accessing Dictionary Values

We can access values using their keys.

```python
student = {
    "name": "Riya",
    "age": 20
}

print(student["name"])
print(student["age"])
```

Output:

```text
Riya
20
```

### Adding or Updating Values

```python
student = {"name": "Riya", "age": 20}

student["city"] = "Bhopal"
student["age"] = 21

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 21, 'city': 'Bhopal'}
```

### Important Dictionary Properties

- Stores key-value pairs.
- Mutable.
- Keys must be hashable.
- Values can be of different data types.
- Keys are unique.
- In modern Python, dictionaries preserve insertion order.

## 15. Binary Data Types

Binary data types are used to work with binary data, such as bytes.

Python provides:

1. `bytes`
2. `bytearray`
3. `memoryview`

### A. bytes

A `bytes` object stores an immutable sequence of bytes.

Example:

```python
data = b"Hello"

print(data)
print(type(data))
```

Output:

```text
b'Hello'
<class 'bytes'>
```

Each byte has a value between 0 and 255.

Accessing an element:

```python
data = b"ABC"

print(data[0])
```

Output:

```text
65
```

The number 65 is the byte value representing the character `A` in ASCII.

### B. bytearray

A `bytearray` stores a mutable sequence of bytes.

Example:

```python
data = bytearray([65, 66, 67])

print(data)
```

Output:

```text
bytearray(b'ABC')
```

Modifying an element:

```python
data = bytearray([65, 66, 67])

data[0] = 68

print(data)
```

Output:

```text
bytearray(b'DBC')
```

### C. memoryview

A memoryview provides access to the memory of an existing bytes-like object without creating a copied data buffer for the view.

Example:

```python
data = bytearray(b"Python")

view = memoryview(data)

print(view[0])
```

Output:

```text
80
```

Memoryviews are useful when working with binary data efficiently.

## 16. None Data Type (NoneType)

`None` represents the absence of a value.

It is commonly used when:

- A variable has no assigned meaningful value yet.
- A function does not return a value explicitly.
- We want to represent a missing or unavailable value.

Example:

```python
result = None

print(result)
print(type(result))
```

Output:

```text
None
<class 'NoneType'>
```

Checking for None:

```python
value = None

if value is None:
    print("No value available")
```

Output:

```text
No value available
```

**Important:** Use `is None` or `is not None` when checking for `None`.

## 17. Checking Data Types

Python provides built-in functions to identify and check data types.

### A. type()

The `type()` function returns the type of an object.

Syntax:

```python
type(value)
```

Example:

```python
a = 10
b = 10.5
c = "Python"
d = True

print(type(a))
print(type(b))
print(type(c))
print(type(d))
```

Output:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

### B. isinstance()

The `isinstance()` function checks whether an object belongs to a particular type or one of its subclasses.

Example:

```python
age = 20

print(isinstance(age, int))
print(isinstance(age, str))
```

Output:

```text
True
False
```

It can also check multiple types.

```python
value = 10.5

print(isinstance(value, (int, float)))
```

Output:

```text
True
```

### Difference Between type() and isinstance()

| type() | isinstance() |
|---|---|
| Returns the object's type | Checks whether the object is an instance of a type |
| Useful for identifying exact types | Useful for type checking |
| Does not treat subclasses as their parent type in direct equality checks | Recognizes inheritance relationships |

Example:

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

print(type(dog) == Animal)
print(isinstance(dog, Animal))
```

Output:

```text
False
True
```

## 18. Type Conversion and Type Casting

Type conversion means changing a value from one data type to another.

Python supports two main types:

1. Implicit type conversion
2. Explicit type conversion

### A. Implicit Type Conversion

Implicit conversion happens automatically when Python converts one compatible numeric type into another during an operation.

Example:

```python
a = 10
b = 5.5

result = a + b

print(result)
print(type(result))
```

Output:

```text
15.5
<class 'float'>
```

Here:

- `a` is an integer.
- `b` is a float.
- Python converts the integer to a float for the operation.
- The result is a float.

Another example:

```python
a = 5
b = 2

result = a / b

print(result)
print(type(result))
```

Output:

```text
2.5
<class 'float'>
```

The `/` operator produces a float result in Python.

### B. Explicit Type Conversion

Explicit conversion means converting a value into another data type using built-in functions.

Common conversion functions:

| Function | Conversion |
|---|---|
| `int()` | Converts a suitable value to integer |
| `float()` | Converts a suitable value to float |
| `str()` | Converts a value to string |
| `bool()` | Converts a value to Boolean |
| `list()` | Converts an iterable to a list |
| `tuple()` | Converts an iterable to a tuple |
| `set()` | Converts an iterable to a set |
| `dict()` | Creates a dictionary from a suitable mapping or iterable of key-value pairs |
| `complex()` | Creates a complex number |
| `bytes()` | Creates a bytes object |
| `bytearray()` | Creates a bytearray |

### Example 1: int()

```python
number = "100"

result = int(number)

print(result)
print(type(result))
```

Output:

```text
100
<class 'int'>
```

### Example 2: float()

```python
number = "10.5"

result = float(number)

print(result)
print(type(result))
```

Output:

```text
10.5
<class 'float'>
```

### Example 3: str()

```python
number = 100

result = str(number)

print(result)
print(type(result))
```

Output:

```text
100
<class 'str'>
```

### Example 4: bool()

```python
print(bool(0))
print(bool(1))
print(bool(""))
print(bool("Python"))
```

Output:

```text
False
True
False
True
```

### Example 5: list()

```python
numbers = (10, 20, 30)

result = list(numbers)

print(result)
```

Output:

```text
[10, 20, 30]
```

### Example 6: tuple()

```python
numbers = [10, 20, 30]

result = tuple(numbers)

print(result)
```

Output:

```text
(10, 20, 30)
```

### Example 7: set()

```python
numbers = [10, 20, 10, 30]

result = set(numbers)

print(result)
```

The result contains:

```text
10, 20, 30
```

### Example 8: complex()

```python
number = complex(2, 3)

print(number)
```

Output:

```text
(2+3j)
```

**Important:** Not every conversion is possible. For example, `int("hello")` raises a `ValueError`.

## 19. Mutable and Immutable Data Types

Python objects can be classified according to whether their contents can be changed after creation.

### A. Mutable Data Types

Mutable objects can be modified after creation.

Common mutable built-in types:

- `list`
- `dict`
- `set`
- `bytearray`

Example:

```python
numbers = [10, 20, 30]

numbers[0] = 100

print(numbers)
```

Output:

```text
[100, 20, 30]
```

The original list is modified.

### B. Immutable Data Types

Immutable objects cannot be modified after creation.

Common immutable built-in types:

- `int`
- `float`
- `complex`
- `bool`
- `str`
- `tuple`
- `range`
- `bytes`
- `frozenset`
- `NoneType`

Example:

```python
name = "Python"

name = name + " Programming"

print(name)
```

Output:

```text
Python Programming
```

The original string was not modified. A new string was created and assigned to `name`.

### Difference Between Mutable and Immutable Types

| Mutable | Immutable |
|---|---|
| Can be modified after creation | Cannot be modified after creation |
| List | Tuple |
| Dictionary | String |
| Set | Integer |
| Bytearray | Float |
| Can change contents | Operations create new objects when a different value is needed |

## 20. User Input in Python

The `input()` function allows users to enter information while a program is running.

**Syntax:**

```python
variable = input("Enter something: ")
```

Example:

```python
name = input("Enter your name: ")

print("Welcome", name)
```

Example interaction:

```text
Enter your name: Riya
Welcome Riya
```

### Important: input() Returns a String

Even when the user enters a number, `input()` returns a string.

Example:

```python
age = input("Enter your age: ")

print(type(age))
```

If the user enters 20, output is:

```text
<class 'str'>
```

### Converting User Input to Integer

```python
age = int(input("Enter your age: "))

print(age)
print(type(age))
```

If the user enters 20, output is:

```text
20
<class 'int'>
```

### Converting User Input to Float

```python
price = float(input("Enter price: "))

print(price)
```

Example input:

```text
99.5
```

Output:

```text
99.5
```

Invalid input can cause a `ValueError`, so real applications should validate user input.

## 21. Output Using print()

The `print()` function displays information on the screen.

### A. Printing Multiple Values

```python
name = "Riya"
age = 20

print(name, age)
```

Output:

```text
Riya 20
```

By default, `print()` separates multiple values with a space.

### B. Using sep

The `sep` parameter specifies the separator between printed values.

```python
print("2026", "11", "22", sep="-")
```

Output:

```text
2026-11-22
```

### C. Using end

The `end` parameter specifies what is printed after the output.

```python
print("Hello", end=" ")
print("Python")
```

Output:

```text
Hello Python
```

By default, `print()` ends with a newline.

### D. Printing Variables with f-Strings

```python
name = "Riya"
age = 20

print(f"My name is {name} and I am {age} years old.")
```

Output:

```text
My name is Riya and I am 20 years old.
```

## 22. Constants in Python

A constant is a value that should not change during program execution.

Python does not enforce constants through a special declaration keyword.

Instead, programmers use uppercase variable names by convention.

Example:

```python
PI = 3.14159
MAX_USERS = 100
COLLEGE_NAME = "LNCT"

print(PI)
print(MAX_USERS)
print(COLLEGE_NAME)
```

Output:

```text
3.14159
100
LNCT
```

The uppercase naming convention indicates that these values should be treated as constants.

**Important:** Python does not prevent reassignment of these names.

## 23. Variable Scope: Local and Global Variables

Scope determines where a variable can be accessed.

### A. Local Variable

A local variable is created inside a function and is normally accessible only within that function.

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

Trying to access `message` outside the function raises a `NameError`.

### B. Global Variable

A global variable is defined outside functions and can be accessed inside them.

```python
name = "Riya"

def greet():
    print(name)

greet()
print(name)
```

Output:

```text
Riya
Riya
```

### C. Using the global Keyword

The `global` keyword allows a function to reassign a global variable.

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

**Important:** Avoid unnecessary use of global variables. Passing values through function arguments often makes programs easier to test and maintain.

## Key concepts

- **Variable:** A name that refers to a value.
- **Assignment operator (`=`):** Assigns a value to a variable.
- **Dynamic typing:** Python determines the type of a value at runtime.
- **Variable naming:** Rules and conventions for naming variables.
- **Multiple assignment:** Assigning values to multiple variables in one statement.
- **Reassignment:** Giving a variable a new value.
- **Integer (`int`):** Stores whole numbers.
- **Float (`float`):** Stores floating-point numbers.
- **Complex (`complex`):** Stores complex numbers.
- **Boolean (`bool`):** Stores `True` or `False`.
- **String (`str`):** Stores text.
- **List (`list`):** An ordered, mutable collection.
- **Tuple (`tuple`):** An ordered, immutable collection.
- **Range (`range`):** An immutable sequence of integers.
- **Set (`set`):** A mutable collection of unique elements.
- **Frozenset:** An immutable set.
- **Dictionary (`dict`):** Stores key-value pairs.
- **Bytes (`bytes`):** An immutable sequence of bytes.
- **Bytearray:** A mutable sequence of bytes.
- **Memoryview:** Provides access to the memory of a bytes-like object.
- **None (`NoneType`):** Represents the absence of a value.
- **type():** Returns an object's type.
- **isinstance():** Checks whether an object belongs to a specified type.
- **Type conversion:** Changes a value from one type to another.
- **Implicit conversion:** Conversion performed automatically by Python.
- **Explicit conversion:** Conversion performed using functions such as `int()`, `float()`, and `str()`.
- **Mutable:** An object whose contents can be changed.
- **Immutable:** An object whose contents cannot be changed.
- **input():** Accepts user input as a string.
- **print():** Displays output.
- **Constant:** A value intended to remain unchanged.
- **Scope:** Defines where a variable can be accessed.

## Common mistakes

1. **Using a variable before assigning a value**

   Incorrect:

   ```python
   print(age)
   ```

   Correct:

   ```python
   age = 20
   print(age)
   ```

2. **Using invalid variable names**

   Incorrect:

   ```python
   1name = "Riya"
   ```

   Correct:

   ```python
   name1 = "Riya"
   ```

3. **Using Python keywords as variable names**

   Incorrect:

   ```python
   class = "Python"
   ```

   Correct:

   ```python
   class_name = "Python"
   ```

4. **Ignoring case sensitivity**

   ```python
   name = "Riya"
   Name = "Aman"

   print(name)
   print(Name)
   ```

   These are two different variable names.

5. **Confusing assignment and comparison operators**

   - `=` assigns a value.
   - `==` compares two values.

   Example:

   ```python
   age = 20

   print(age == 20)
   ```

6. **Assuming input() returns an integer**

   Incorrect:

   ```python
   age = input("Enter age: ")
   print(age + 5)
   ```

   Correct:

   ```python
   age = int(input("Enter age: "))
   print(age + 5)
   ```

7. **Converting invalid text into an integer**

   ```python
   number = int("Python")
   ```

   This raises a `ValueError`.

   Only convert strings containing valid integer representations.

8. **Confusing integer division and ordinary division**

   ```python
   print(5 / 2)
   print(5 // 2)
   ```

   Output:

   ```text
   2.5
   2
   ```

9. **Confusing list and tuple**

   - Lists use `[]` and are mutable.
   - Tuples use `()` and are immutable.

10. **Creating an empty set using `{}`**

    Incorrect:

    ```python
    data = {}
    ```

    This creates an empty dictionary.

    Correct:

    ```python
    data = set()
    ```

11. **Assuming strings can be modified directly**

    Strings are immutable.

    Create a new string instead.

12. **Assuming constants are enforced by Python**

    Uppercase names indicate constants by convention, but Python still allows reassignment.

13. **Confusing None with zero or an empty string**

    `None`, `0`, and `""` are different values.

14. **Using is instead of == for ordinary value comparison**

    - `==` checks value equality.
    - `is` checks object identity.

    Use `==` for ordinary value comparisons and `is None` when checking for None.

15. **Assuming all data types support the same operations**

    For example, strings support concatenation, while dictionaries use key-based access.

16. **Ignoring floating-point precision**

    Some decimal calculations produce small precision differences. Use appropriate rounding or decimal arithmetic when exact decimal representation is required.

## Quick summary

- Variables are names used to refer to values.
- Python does not require explicit variable declarations.
- Python is dynamically typed.
- Variable names are case-sensitive.
- Variable names cannot start with numbers or use reserved keywords.
- Use meaningful `snake_case` variable names.
- Multiple variables can be assigned in one statement.
- Python provides numeric, Boolean, text, sequence, set, mapping, binary, and special data types.
- `int` stores whole numbers.
- `float` stores floating-point numbers.
- `complex` stores complex numbers.
- `bool` stores `True` or `False`.
- `str` stores text.
- `list` is ordered and mutable.
- `tuple` is ordered and immutable.
- `range` represents an immutable sequence of integers.
- `set` stores unique elements.
- `frozenset` is an immutable set.
- `dict` stores key-value pairs.
- `bytes` is immutable, while `bytearray` is mutable.
- `memoryview` provides access to a bytes-like object's memory.
- `None` represents the absence of a value.
- `type()` identifies the type of an object.
- `isinstance()` checks whether an object belongs to a type.
- Type conversion can be implicit or explicit.
- `input()` returns a string.
- `print()` displays output.
- Mutable objects can be modified after creation.
- Immutable objects cannot be modified after creation.
- Constants are represented using uppercase names by convention.
- Local and global variables have different scopes.

## Practice

### Beginner Level

**1. Create Variables**

Create variables to store your name, age, and city. Print all three values.

**2. Check Data Types**

Create an integer, float, string, and Boolean variable. Print their data types using `type()`.

**3. Add Two Numbers**

Create two integer variables and print their sum.

**4. Swap Variables**

Swap the values of two variables without using a third variable.

**5. Multiple Assignment**

Assign values to three variables in a single statement.

**6. Reassign a Variable**

Create a variable containing an integer, then assign a string to the same variable.

**7. User Input**

Take the user's name as input and print a welcome message.

**8. Convert Input**

Take two numbers as input, convert them to integers, and print their sum.

**9. Boolean Expressions**

Create two numeric variables and check which one is greater.

**10. Constants**

Create variables representing PI and the maximum number of students using uppercase names.

### Intermediate Level

**11. Data Type Conversion**

Convert a string into an integer, an integer into a float, and a number into a string.

**12. Mutable and Immutable**

Create a list and a tuple. Try modifying an element in each and observe the difference.

**13. Dictionary Creation**

Create a dictionary containing a student's name, age, and marks. Display each value.

**14. Set Conversion**

Convert a list containing duplicate numbers into a set.

**15. Range Practice**

Generate numbers from 1 to 20 using `range()`.

**16. Check Data Type**

Use `isinstance()` to check whether a value is an integer or float.

**17. Local and Global Variables**

Create one global variable and one local variable inside a function.

**18. String and Number Conversion**

Take a user's age as input and display their age after five years.

**19. Calculate Average**

Take three marks as input and calculate their average.

**20. Check None**

Create a variable containing `None` and check whether it is None.

### Advanced Level

**21. Student Information System**

Take a student's name, age, marks, and city as input. Store the information in a dictionary and display it.

**22. Simple Calculator**

Take two numbers and perform addition, subtraction, multiplication, and division.

**23. Data Type Identification**

Create a list containing values of different data types. Print the type of each element.

**24. Number Conversion**

Take a number as input and display its integer, float, string, and Boolean representations.

**25. Temperature Converter**

Take temperature in Celsius and convert it into Fahrenheit.

Formula:

```text
Fahrenheit = (Celsius * 9/5) + 32
```

**26. Area Calculator**

Take the radius of a circle and calculate its area.

Formula:

```text
Area = 3.14159 * radius * radius
```

**27. Bill Calculator**

Take the price and quantity of a product. Calculate the total bill.

**28. Personal Profile**

Take the user's name, age, city, and course. Display the information using an f-string.

**29. Variable Scope**

Create a global variable and modify it inside a function using the `global` keyword.

**30. Type Validation**

Take user input and check whether it contains a valid integer using exception handling.

### Sample Solutions

**Solution 1: Create Variables**

```python
name = "Riya"
age = 20
city = "Bhopal"

print(name)
print(age)
print(city)
```

Output:

```text
Riya
20
Bhopal
```

**Solution 2: Check Data Types**

```python
a = 10
b = 10.5
c = "Python"
d = True

print(type(a))
print(type(b))
print(type(c))
print(type(d))
```

Output:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

**Solution 3: Add Two Numbers**

```python
a = 10
b = 20

print("Sum:", a + b)
```

Output:

```text
Sum: 30
```

**Solution 4: Swap Variables**

```python
a = 10
b = 20

a, b = b, a

print("a:", a)
print("b:", b)
```

Output:

```text
a: 20
b: 10
```

**Solution 5: Multiple Assignment**

```python
a, b, c = 10, 20, 30

print(a, b, c)
```

Output:

```text
10 20 30
```

**Solution 6: Reassign a Variable**

```python
value = 100

print(value)

value = "Python"

print(value)
```

Output:

```text
100
Python
```

**Solution 7: User Input**

```python
name = input("Enter your name: ")

print(f"Welcome, {name}!")
```

Example interaction:

```text
Enter your name: Riya
Welcome, Riya!
```

**Solution 8: Convert Input**

```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Sum:", a + b)
```

Example interaction:

```text
Enter first number: 10
Enter second number: 20
Sum: 30
```

**Solution 9: Boolean Expressions**

```python
a = 50
b = 30

print(a > b)
print(a < b)
print(a == b)
```

Output:

```text
True
False
False
```

**Solution 10: Constants**

```python
PI = 3.14159
MAX_STUDENTS = 100

print(PI)
print(MAX_STUDENTS)
```

Output:

```text
3.14159
100
```

**Solution 11: Data Type Conversion**

```python
a = "100"
b = 20
c = 30

x = int(a)
y = float(b)
z = str(c)

print(x, type(x))
print(y, type(y))
print(z, type(z))
```

Output:

```text
100 <class 'int'>
20.0 <class 'float'>
30 <class 'str'>
```

**Solution 12: Mutable and Immutable**

```python
numbers = [10, 20, 30]

numbers[0] = 100

print(numbers)
```

Output:

```text
[100, 20, 30]
```

Tuple example:

```python
numbers = (10, 20, 30)

numbers[0] = 100
```

This raises a `TypeError` because tuples are immutable.

**Solution 13: Dictionary Creation**

```python
student = {
    "name": "Riya",
    "age": 20,
    "marks": 90
}

print(student["name"])
print(student["age"])
print(student["marks"])
```

Output:

```text
Riya
20
90
```

**Solution 14: Set Conversion**

```python
numbers = [10, 20, 10, 30, 20]

unique_numbers = set(numbers)

print(unique_numbers)
```

The set contains:

```text
10, 20, 30
```

**Solution 15: Range Practice**

```python
numbers = range(1, 21)

for num in numbers:
    print(num)
```

Output:

```text
1
2
3
...
20
```

**Solution 16: Check Data Type**

```python
value = 10.5

if isinstance(value, (int, float)):
    print("Numeric value")
else:
    print("Not a numeric value")
```

Output:

```text
Numeric value
```

**Solution 17: Local and Global Variables**

```python
name = "Riya"

def display():
    age = 20
    print(name)
    print(age)

display()
```

Output:

```text
Riya
20
```

**Solution 18: String and Number Conversion**

```python
age = int(input("Enter your age: "))

future_age = age + 5

print(f"Your age after 5 years will be {future_age}.")
```

Example interaction:

```text
Enter your age: 20
Your age after 5 years will be 25.
```

**Solution 19: Calculate Average**

```python
a = float(input("Enter first mark: "))
b = float(input("Enter second mark: "))
c = float(input("Enter third mark: "))

average = (a + b + c) / 3

print("Average:", average)
```

Example interaction:

```text
Enter first mark: 80
Enter second mark: 90
Enter third mark: 70
Average: 80.0
```

**Solution 20: Check None**

```python
value = None

if value is None:
    print("Value is empty")
else:
    print("Value is available")
```

Output:

```text
Value is empty
```

**Solution 21: Student Information System**

```python
name = input("Enter name: ")
age = int(input("Enter age: "))
marks = float(input("Enter marks: "))
city = input("Enter city: ")

student = {
    "name": name,
    "age": age,
    "marks": marks,
    "city": city
}

print(student)
```

**Solution 22: Simple Calculator**

```python
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)

if b != 0:
    print("Division:", a / b)
else:
    print("Division by zero is not allowed")
```

**Solution 23: Data Type Identification**

```python
data = [10, 10.5, "Python", True, [1, 2], (3, 4)]

for item in data:
    print(item, ":", type(item))
```

Output:

```text
10 : <class 'int'>
10.5 : <class 'float'>
Python : <class 'str'>
True : <class 'bool'>
[1, 2] : <class 'list'>
(3, 4) : <class 'tuple'>
```

**Solution 24: Number Conversion**

```python
number = int(input("Enter a number: "))

print("Integer:", int(number))
print("Float:", float(number))
print("String:", str(number))
print("Boolean:", bool(number))
```

**Solution 25: Temperature Converter**

```python
celsius = float(input("Enter temperature in Celsius: "))

fahrenheit = (celsius * 9 / 5) + 32

print("Temperature in Fahrenheit:", fahrenheit)
```

Example interaction:

```text
Enter temperature in Celsius: 25
Temperature in Fahrenheit: 77.0
```

**Solution 26: Area Calculator**

```python
PI = 3.14159

radius = float(input("Enter radius: "))

area = PI * radius * radius

print("Area:", area)
```

**Solution 27: Bill Calculator**

```python
price = float(input("Enter product price: "))
quantity = int(input("Enter quantity: "))

total = price * quantity

print("Total bill:", total)
```

**Solution 28: Personal Profile**

```python
name = input("Enter name: ")
age = int(input("Enter age: "))
city = input("Enter city: ")
course = input("Enter course: ")

print(f"My name is {name}. I am {age} years old.")
print(f"I live in {city} and study {course}.")
```

**Solution 29: Variable Scope**

```python
count = 10

def update():
    global count
    count = 50

update()

print(count)
```

Output:

```text
50
```

**Solution 30: Type Validation**

```python
value = input("Enter an integer: ")

try:
    number = int(value)
    print("Valid integer:", number)
except ValueError:
    print("Invalid input. Please enter a whole number.")
```

Example interaction:

```text
Enter an integer: 25
Valid integer: 25
```

## Learning resources

- **PDF:** [Variables and Data Types](https://drive.google.com/file/d/1hjJ3v4n5l68pUbe9eulaMCfpQFkZxN-M/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)