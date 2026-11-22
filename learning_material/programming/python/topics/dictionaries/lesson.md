
# Dictionaries and Key-Value Pairs

**Course:** Python  
**Topic ID:** `dictionaries`

## Learning objectives

After completing this topic, learners should be able to:

- Understand dictionaries and their purpose in Python.
- Explain the concept of key-value pairs.
- Create dictionaries using different methods.
- Access, add, update and delete dictionary elements.
- Use dictionary methods such as `keys()`, `values()`, `items()` and `get()`.
- Iterate through dictionaries using loops.
- Understand nested dictionaries.
- Apply dictionary operations to real-world problems.
- Use dictionary comprehensions.
- Understand dictionary membership and common operations.

## Explanation

### 1. What is a Dictionary?

A dictionary is a built-in Python data structure used to store data in the form of key-value pairs.

Each item in a dictionary contains:

- **Key:** Identifies an item.
- **Value:** Stores the information associated with that key.

Dictionaries are written using curly braces `{}`.

**Syntax:**

```python
dictionary = {
    "key1": "value1",
    "key2": "value2"
}
```

**Example:**

```python
student = {
    "name": "Riya",
    "age": 20,
    "course": "Python"
}

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 20, 'course': 'Python'}
```

Here:

- `"name"` is a key and `"Riya"` is its value.
- `"age"` is a key and `20` is its value.
- `"course"` is a key and `"Python"` is its value.

### 2. Features of Dictionaries

Important characteristics of Python dictionaries:

1. Store information as key-value pairs.
2. Keys must be unique.
3. Values can be duplicated.
4. Dictionaries are mutable, meaning they can be modified.
5. Values can have different data types.
6. Keys must be hashable. Common immutable types such as strings, integers and tuples containing hashable elements can be used as keys.
7. Dictionaries preserve insertion order in modern Python.
8. Dictionaries can contain other dictionaries.

**Example:**

```python
data = {
    "name": "Aman",
    "age": 21,
    "marks": 85,
    "passed": True
}

print(data)
```

Output:

```text
{'name': 'Aman', 'age': 21, 'marks': 85, 'passed': True}
```

### 3. Creating Dictionaries

There are different ways to create dictionaries.

**Method 1: Using curly braces**

```python
student = {
    "name": "Aman",
    "age": 20
}

print(student)
```

**Method 2: Using the dict() constructor**

```python
student = dict(name="Aman", age=20)

print(student)
```

Output:

```text
{'name': 'Aman', 'age': 20}
```

**Method 3: Creating an empty dictionary**

```python
student = {}

print(student)
```

Output:

```text
{}
```

**Method 4: Using dict() with pairs**

```python
student = dict([
    ("name", "Riya"),
    ("age", 21)
])

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 21}
```

### 4. Accessing Dictionary Elements

Dictionary values can be accessed using their keys.

**Method 1: Using square brackets**

```python
student = {
    "name": "Riya",
    "age": 20,
    "course": "Python"
}

print(student["name"])
print(student["age"])
```

Output:

```text
Riya
20
```

If the requested key does not exist, square-bracket access raises a `KeyError`.

**Method 2: Using get()**

The `get()` method accesses a value without raising a `KeyError` when the key is missing.

```python
student = {
    "name": "Riya",
    "age": 20
}

print(student.get("name"))
print(student.get("marks"))
print(student.get("marks", 0))
```

Output:

```text
Riya
None
0
```

The second argument of `get()` provides a default value.

### 5. Adding Elements to a Dictionary

New key-value pairs can be added using assignment.

**Example:**

```python
student = {
    "name": "Aman",
    "age": 20
}

student["course"] = "Python"
student["marks"] = 90

print(student)
```

Output:

```text
{'name': 'Aman', 'age': 20, 'course': 'Python', 'marks': 90}
```

If the key does not exist, Python creates a new entry.

### 6. Updating Dictionary Elements

Existing values can be modified by assigning a new value to their keys.

**Example:**

```python
student = {
    "name": "Aman",
    "age": 20,
    "marks": 75
}

student["marks"] = 95

print(student)
```

Output:

```text
{'name': 'Aman', 'age': 20, 'marks': 95}
```

**Using update():**

The `update()` method adds new entries or updates existing entries.

```python
student = {
    "name": "Riya",
    "age": 20
}

student.update({
    "age": 21,
    "course": "Python"
})

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 21, 'course': 'Python'}
```

### 7. Removing Elements from a Dictionary

Python provides several methods to remove dictionary elements.

**A. Using pop()**

Removes a specified key and returns its value.

```python
student = {
    "name": "Aman",
    "age": 20,
    "marks": 85
}

removed = student.pop("age")

print(removed)
print(student)
```

Output:

```text
20
{'name': 'Aman', 'marks': 85}
```

**B. Using popitem()**

Removes and returns the last inserted key-value pair.

```python
student = {
    "name": "Riya",
    "age": 20,
    "course": "Python"
}

removed = student.popitem()

print(removed)
print(student)
```

Output:

```text
('course', 'Python')
{'name': 'Riya', 'age': 20}
```

**C. Using del**

Deletes a specified key-value pair.

```python
student = {
    "name": "Aman",
    "age": 20
}

del student["age"]

print(student)
```

Output:

```text
{'name': 'Aman'}
```

**D. Using clear()**

Removes all elements from the dictionary.

```python
student = {
    "name": "Riya",
    "age": 20
}

student.clear()

print(student)
```

Output:

```text
{}
```

### 8. Dictionary Methods

Python provides built-in methods for working with dictionaries.

| Method | Description |
|---|---|
| `keys()` | Returns a view of all keys |
| `values()` | Returns a view of all values |
| `items()` | Returns a view of key-value pairs |
| `get()` | Retrieves a value safely |
| `update()` | Adds or updates entries |
| `pop()` | Removes a specified key |
| `popitem()` | Removes the last inserted pair |
| `clear()` | Removes all entries |
| `copy()` | Creates a shallow copy |
| `setdefault()` | Returns a value or inserts a default |
| `fromkeys()` | Creates a dictionary from given keys |

**Example: keys(), values() and items()**

```python
student = {
    "name": "Aman",
    "age": 20,
    "marks": 90
}

print(student.keys())
print(student.values())
print(student.items())
```

Output:

```text
dict_keys(['name', 'age', 'marks'])
dict_values(['Aman', 20, 90])
dict_items([('name', 'Aman'), ('age', 20), ('marks', 90)])
```

**Example: setdefault()**

```python
student = {
    "name": "Riya",
    "age": 20
}

student.setdefault("course", "Python")
student.setdefault("age", 25)

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 20, 'course': 'Python'}
```

`setdefault()` inserts the default value only if the key is missing. It does not overwrite an existing value.

**Example: fromkeys()**

```python
keys = ["name", "age", "course"]

student = dict.fromkeys(keys, "Not provided")

print(student)
```

Output:

```text
{'name': 'Not provided', 'age': 'Not provided', 'course': 'Not provided'}
```

### 9. Iterating Through Dictionaries

A dictionary can be processed using loops.

**A. Iterating through keys**

```python
student = {
    "name": "Aman",
    "age": 20,
    "marks": 85
}

for key in student:
    print(key)
```

Output:

```text
name
age
marks
```

**B. Iterating through values**

```python
for value in student.values():
    print(value)
```

Output:

```text
Aman
20
85
```

**C. Iterating through key-value pairs**

```python
for key, value in student.items():
    print(key, ":", value)
```

Output:

```text
name : Aman
age : 20
marks : 85
```

### 10. Checking Whether a Key Exists

The `in` operator checks whether a key exists in a dictionary.

**Example:**

```python
student = {
    "name": "Riya",
    "age": 20
}

print("name" in student)
print("marks" in student)
```

Output:

```text
True
False
```

The `in` operator checks keys by default, not values.

To check values, use:

```python
print(20 in student.values())
```

Output:

```text
True
```

### 11. Nested Dictionaries

A nested dictionary is a dictionary containing another dictionary as its value.

It is useful for storing structured information.

**Example:**

```python
students = {
    "student1": {
        "name": "Aman",
        "age": 20,
        "marks": 85
    },
    "student2": {
        "name": "Riya",
        "age": 21,
        "marks": 92
    }
}

print(students["student1"]["name"])
print(students["student2"]["marks"])
```

Output:

```text
Aman
92
```

Nested dictionaries are commonly used for:

- Student records.
- Employee information.
- Product details.
- Application settings.
- Structured API responses.

### 12. Dictionary Length

The `len()` function returns the number of key-value pairs.

**Example:**

```python
student = {
    "name": "Aman",
    "age": 20,
    "marks": 85
}

print(len(student))
```

Output:

```text
3
```

### 13. Copying Dictionaries

The `copy()` method creates a shallow copy of a dictionary.

**Example:**

```python
original = {
    "name": "Riya",
    "age": 20
}

copied = original.copy()

copied["age"] = 22

print(original)
print(copied)
```

Output:

```text
{'name': 'Riya', 'age': 20}
{'name': 'Riya', 'age': 22}
```

A shallow copy creates a new outer dictionary, but nested mutable objects are still shared.

For deeply nested structures, `copy.deepcopy()` can be used when an independent recursive copy is needed.

### 14. Dictionary Comprehensions

Dictionary comprehensions provide a short way to create dictionaries.

**Syntax:**

```python
new_dict = {
    key_expression: value_expression
    for item in iterable
}
```

**Example: create a dictionary of squares**

```python
numbers = [1, 2, 3, 4, 5]

squares = {
    number: number ** 2
    for number in numbers
}

print(squares)
```

Output:

```text
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

**Example: dictionary comprehension with a condition**

```python
numbers = [1, 2, 3, 4, 5, 6]

even_squares = {
    number: number ** 2
    for number in numbers
    if number % 2 == 0
}

print(even_squares)
```

Output:

```text
{2: 4, 4: 16, 6: 36}
```

### 15. Merging Dictionaries

Dictionaries can be combined in different ways.

**Using update():**

```python
first = {"name": "Aman", "age": 20}
second = {"course": "Python", "marks": 90}

first.update(second)

print(first)
```

Output:

```text
{'name': 'Aman', 'age': 20, 'course': 'Python', 'marks': 90}
```

**Using the | operator (Python 3.9 and later):**

```python
first = {"name": "Aman", "age": 20}
second = {"course": "Python", "marks": 90}

combined = first | second

print(combined)
```

Output:

```text
{'name': 'Aman', 'age': 20, 'course': 'Python', 'marks': 90}
```

If the same key appears in both dictionaries, the value from the right-hand dictionary takes precedence.

## Key concepts

1. **Dictionary:** A Python collection that stores key-value pairs.
2. **Key:** A unique identifier used to access a value.
3. **Value:** Data associated with a key.
4. **Mutable:** A property that allows a dictionary to be modified.
5. **Key uniqueness:** A dictionary cannot contain duplicate keys.
6. **get():** Retrieves a value and can provide a default if the key is missing.
7. **keys():** Returns a view of dictionary keys.
8. **values():** Returns a view of dictionary values.
9. **items():** Returns a view of key-value pairs.
10. **update():** Adds or updates dictionary entries.
11. **pop():** Removes a specified key.
12. **popitem():** Removes the last inserted key-value pair.
13. **Nested dictionary:** A dictionary stored inside another dictionary.
14. **Dictionary comprehension:** A concise way to create dictionaries.
15. **Shallow copy:** Creates a new outer dictionary but shares nested objects.
16. **Membership:** Checks whether a key or value exists.

## Examples

### Example 1: Student information system

```python
student = {
    "name": "Riya",
    "roll_number": 101,
    "course": "Python",
    "marks": 92
}

print("Student:", student["name"])
print("Roll Number:", student["roll_number"])
print("Marks:", student["marks"])
```

Output:

```text
Student: Riya
Roll Number: 101
Marks: 92
```

### Example 2: Count the frequency of characters

```python
text = "banana"

frequency = {}

for character in text:
    frequency[character] = frequency.get(character, 0) + 1

print(frequency)
```

Output:

```text
{'b': 1, 'a': 3, 'n': 2}
```

The `get()` method returns the existing count or zero when the character is first encountered.

### Example 3: Find the student with the highest marks

```python
students = {
    "Aman": 85,
    "Riya": 95,
    "Neha": 88
}

top_student = max(students, key=students.get)

print("Top student:", top_student)
print("Marks:", students[top_student])
```

Output:

```text
Top student: Riya
Marks: 95
```

### Example 4: Product inventory

```python
inventory = {
    "Laptop": 10,
    "Mouse": 25,
    "Keyboard": 15
}

inventory["Mouse"] -= 5
inventory["Monitor"] = 8

for product, quantity in inventory.items():
    print(product, ":", quantity)
```

Output:

```text
Laptop : 10
Mouse : 20
Keyboard : 15
Monitor : 8
```

### Example 5: Filter students who passed

```python
marks = {
    "Aman": 85,
    "Riya": 45,
    "Neha": 92,
    "Rahul": 55
}

passed = {
    name: score
    for name, score in marks.items()
    if score >= 60
}

print(passed)
```

Output:

```text
{'Aman': 85, 'Neha': 92}
```

### Example 6: Nested dictionary access

```python
employees = {
    "employee1": {
        "name": "Aman",
        "department": "IT"
    },
    "employee2": {
        "name": "Riya",
        "department": "HR"
    }
}

print(employees["employee1"]["department"])
print(employees["employee2"]["name"])
```

Output:

```text
IT
Riya
```

## Common mistakes

1. **Accessing a missing key using square brackets**
   - This raises a `KeyError`.
   - Use `get()` when a missing key is possible.

2. **Using duplicate keys**
   - Dictionary keys must be unique.
   - A later value for the same key replaces the earlier value.

3. **Using mutable objects as keys**
   - Lists and dictionaries cannot be used as dictionary keys.
   - Use hashable objects such as strings, integers or suitable tuples.

4. **Confusing keys and values**
   - Keys identify entries, while values store the associated data.

5. **Forgetting dictionary syntax**
   - Separate key-value pairs using commas.
   - Separate each key from its value using a colon.

6. **Assuming `in` checks values**
   - `in` checks dictionary keys by default.
   - Use `dictionary.values()` to check values.

7. **Confusing pop() and popitem()**
   - `pop(key)` removes a specified key.
   - `popitem()` removes the last inserted pair.

8. **Modifying a dictionary while iterating over it**
   - Adding or removing entries during iteration can cause a `RuntimeError`.
   - Iterate over a copy or collect changes before modifying the dictionary.

9. **Assuming copy() performs a deep copy**
   - `copy()` creates a shallow copy.
   - Use `copy.deepcopy()` when nested mutable objects must also be copied.

10. **Confusing update() with creating a new dictionary**
    - `update()` modifies the existing dictionary.
    - The `|` operator creates a merged dictionary.

## Quick summary

- Dictionaries store information in key-value pairs.
- Dictionaries are created using curly braces or `dict()`.
- Keys must be unique and hashable.
- Dictionaries are mutable and preserve insertion order.
- Values can be accessed using square brackets or `get()`.
- New entries can be added using assignment.
- Existing entries can be updated using assignment or `update()`.
- `pop()`, `popitem()` and `del` remove entries.
- `keys()`, `values()` and `items()` help access dictionary contents.
- Dictionaries can be processed using loops.
- Nested dictionaries store structured information.
- Dictionary comprehensions create dictionaries concisely.
- `copy()` creates a shallow copy.
- Dictionaries can be merged using `update()` or `|`.

## Practice

### Beginner Level

1. Create a dictionary containing your name, age and course.
2. Access the name and age from a student dictionary.
3. Add a new key called `marks` to an existing dictionary.
4. Update the age of a student.
5. Remove an entry using `pop()`.
6. Find the number of entries using `len()`.

### Intermediate Level

7. Create a dictionary of five students and their marks.
8. Iterate through a dictionary and print all keys and values.
9. Count the frequency of each character in a string.
10. Find the student with the highest marks.
11. Create a dictionary containing only students who scored at least 60.
12. Create a dictionary from two lists using `zip()`.

### Advanced Level

13. Create a nested dictionary for three employees.
14. Update a product inventory dictionary after a sale.
15. Merge two dictionaries and handle duplicate keys.
16. Create a dictionary of squares using dictionary comprehension.
17. Find all keys that have a particular value.
18. Build a simple contact book using dictionaries.

### Practice Solutions

**Solution 1: Create a student dictionary**

```python
student = {
    "name": "Riya",
    "age": 20,
    "course": "Python"
}

print(student)
```

Output:

```text
{'name': 'Riya', 'age': 20, 'course': 'Python'}
```

**Solution 2: Add and update values**

```python
student = {
    "name": "Aman",
    "age": 20
}

student["marks"] = 85
student["age"] = 21

print(student)
```

Output:

```text
{'name': 'Aman', 'age': 21, 'marks': 85}
```

**Solution 3: Count character frequency**

```python
text = "hello"

frequency = {}

for character in text:
    frequency[character] = frequency.get(character, 0) + 1

print(frequency)
```

Output:

```text
{'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

**Solution 4: Find the highest marks**

```python
marks = {
    "Aman": 80,
    "Riya": 95,
    "Neha": 88
}

topper = max(marks, key=marks.get)

print(topper)
```

Output:

```text
Riya
```

**Solution 5: Filter passing students**

```python
marks = {
    "Aman": 85,
    "Riya": 40,
    "Neha": 90
}

passed = {
    name: score
    for name, score in marks.items()
    if score >= 60
}

print(passed)
```

Output:

```text
{'Aman': 85, 'Neha': 90}
```

**Solution 6: Create a dictionary using zip()**

```python
names = ["Aman", "Riya", "Neha"]
marks = [85, 90, 78]

students = dict(zip(names, marks))

print(students)
```

Output:

```text
{'Aman': 85, 'Riya': 90, 'Neha': 78}
```

## Learning resources

- **PDF:** [Dictionaries and Key-Value Pairs PDF](https://drive.google.com/file/d/1Nv3hpUnpGfDdBn4NC6TV8mWk8XFFp_7s/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc