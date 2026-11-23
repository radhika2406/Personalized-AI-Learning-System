
# Tuples and Sets

**Course:** Python
**Topic ID:** `tuples_and_sets`

## Learning objectives

After completing this topic, learners should be able to:

- Understand tuples and sets in Python.
- Create tuples and sets using different methods.
- Understand the differences between lists, tuples, and sets.
- Access tuple elements using positive and negative indexing.
- Extract elements from tuples using slicing.
- Understand tuple immutability.
- Perform tuple packing and unpacking.
- Use built-in tuple methods such as `count()` and `index()`.
- Create sets and understand their properties.
- Add, remove, and update elements in sets.
- Perform mathematical set operations such as union, intersection, difference, and symmetric difference.
- Check subsets, supersets, and disjoint sets.
- Understand the difference between mutable sets and immutable frozensets.
- Use tuples and sets in practical Python programs.
- Choose the appropriate data structure for different programming problems.

## Explanation

# Part 1: Tuples in Python

## 1. What is a Tuple?

A tuple is an ordered collection of elements in Python.

It is used to store multiple values in a single variable.

A tuple can contain different types of data, such as:

- Integers
- Strings
- Floating-point numbers
- Boolean values
- Other tuples
- Lists
- Other Python objects

Tuples are written using parentheses `()` with elements separated by commas.

**Example:**

```python
student = ("Riya", 20, "Bhopal", 85.5)

print(student)
```

Output:

```text
('Riya', 20, 'Bhopal', 85.5)
```

Here, the tuple contains four elements:

- `"Riya"` is a string.
- `20` is an integer.
- `"Bhopal"` is a string.
- `85.5` is a float.

### Important properties of tuples

1. Ordered: Elements maintain their position.
2. Immutable: Elements cannot be changed directly after creation.
3. Allow duplicates: The same value can appear multiple times.
4. Allow different data types: A tuple can store different types of values.
5. Support indexing and slicing.
6. Can be nested: A tuple can contain another tuple.

## 2. Creating Tuples

Python provides different ways to create tuples.

### A. Using Parentheses

The most common way is to use parentheses.

```python
numbers = (10, 20, 30, 40)

print(numbers)
```

Output:

```text
(10, 20, 30, 40)
```

### B. Creating a Tuple Without Parentheses

Python also supports tuple packing without parentheses.

```python
numbers = 10, 20, 30, 40

print(numbers)
```

Output:

```text
(10, 20, 30, 40)
```

### C. Creating an Empty Tuple

An empty tuple contains no elements.

```python
empty = ()

print(empty)
print(type(empty))
```

Output:

```text
()
<class 'tuple'>
```

### D. Creating a Single-Element Tuple

A single-element tuple must contain a trailing comma.

Correct:

```python
number = (10,)

print(number)
print(type(number))
```

Output:

```text
(10,)
<class 'tuple'>
```

Incorrect:

```python
number = (10)

print(type(number))
```

Output:

```text
<class 'int'>
```

Without the comma, Python treats `(10)` as an ordinary integer expression.

### E. Using the tuple() Constructor

The `tuple()` function converts an iterable into a tuple.

```python
numbers = tuple([10, 20, 30])

print(numbers)
```

Output:

```text
(10, 20, 30)
```

Converting a string into a tuple:

```python
text = "Python"

result = tuple(text)

print(result)
```

Output:

```text
('P', 'y', 't', 'h', 'o', 'n')
```

## 3. Accessing Tuple Elements

Tuples are ordered, so we can access individual elements using indexes.

Python supports positive and negative indexing.

### A. Positive Indexing

Positive indexing starts from 0 and moves from left to right.

```python
fruits = ("apple", "banana", "mango", "orange")

print(fruits[0])
print(fruits[1])
print(fruits[2])
```

Output:

```text
apple
banana
mango
```

Index positions:

| Element | apple | banana | mango | orange |
|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 |

### B. Negative Indexing

Negative indexing starts from -1 and moves from right to left.

```python
fruits = ("apple", "banana", "mango", "orange")

print(fruits[-1])
print(fruits[-2])
print(fruits[-3])
```

Output:

```text
orange
mango
banana
```

Index positions:

| Element | apple | banana | mango | orange |
|---|---|---|---|---|
| Negative index | -4 | -3 | -2 | -1 |

**Important:** Accessing an index outside the valid range raises an `IndexError`.

## 4. Tuple Slicing

Slicing is used to extract a portion of a tuple.

**Syntax:**

```python
tuple_name[start:stop:step]
```

Where:

- `start`: Starting index, included.
- `stop`: Ending index, excluded.
- `step`: Number of positions to move.

### Example 1: Basic Slicing

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[1:4])
```

Output:

```text
(20, 30, 40)
```

### Example 2: Omitting the Start Index

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[:3])
```

Output:

```text
(10, 20, 30)
```

### Example 3: Omitting the Stop Index

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[2:])
```

Output:

```text
(30, 40, 50)
```

### Example 4: Using Step

```python
numbers = (10, 20, 30, 40, 50, 60)

print(numbers[::2])
```

Output:

```text
(10, 30, 50)
```

### Example 5: Reversing a Tuple

```python
numbers = (10, 20, 30, 40)

print(numbers[::-1])
```

Output:

```text
(40, 30, 20, 10)
```

## 5. Tuple Immutability

Tuples are immutable.

Immutability means that once a tuple is created, its elements cannot be directly changed, added, or removed.

**Incorrect Example:**

```python
numbers = (10, 20, 30)

numbers[0] = 100
```

Output:

```text
TypeError
```

Python does not allow direct modification of tuple elements.

### How to Modify Tuple Data

If you need to change a tuple, you can create a new tuple.

```python
numbers = (10, 20, 30)

new_numbers = (100,) + numbers[1:]

print(new_numbers)
```

Output:

```text
(100, 20, 30)
```

The original tuple remains unchanged.

### Important: Tuples Can Contain Mutable Objects

A tuple cannot have its elements reassigned, but it can contain mutable objects such as lists.

```python
data = (10, 20, [30, 40])

data[2].append(50)

print(data)
```

Output:

```text
(10, 20, [30, 40, 50])
```

The list inside the tuple can be modified.

However, you cannot replace the list itself:

```python
data[2] = [100, 200]
```

This raises a `TypeError`.

**Remember:** Tuple immutability prevents changing its element references, but it does not make every object stored inside the tuple immutable.

## 6. Tuple Packing and Unpacking

### A. Tuple Packing

Tuple packing means combining multiple values into a single tuple.

```python
student = "Riya", 20, "Bhopal"

print(student)
```

Output:

```text
('Riya', 20, 'Bhopal')
```

Python automatically packs the values into a tuple.

### B. Tuple Unpacking

Tuple unpacking means assigning tuple elements to separate variables.

```python
student = ("Riya", 20, "Bhopal")

name, age, city = student

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

The number of variables must match the number of elements unless extended unpacking is used.

### C. Extended Unpacking Using *

The `*` operator collects multiple remaining values into a list.

```python
numbers = (10, 20, 30, 40, 50)

first, *middle, last = numbers

print(first)
print(middle)
print(last)
```

Output:

```text
10
[20, 30, 40]
50
```

### D. Swapping Variables Using Tuple Unpacking

Python allows two variables to be swapped without using a temporary variable.

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

This technique is commonly used in Python programming.

## 7. Tuple Methods

Tuples have only two main built-in methods because they are immutable.

### A. count()

The `count()` method returns the number of times a specified element appears.

**Syntax:**

```python
tuple_name.count(value)
```

Example:

```python
numbers = (10, 20, 10, 30, 10, 40)

print(numbers.count(10))
```

Output:

```text
3
```

### B. index()

The `index()` method returns the index of the first occurrence of an element.

**Syntax:**

```python
tuple_name.index(value)
```

Example:

```python
fruits = ("apple", "banana", "mango", "banana")

print(fruits.index("banana"))
```

Output:

```text
1
```

If the element does not exist, Python raises a `ValueError`.

An optional start and stop position can also be provided.

```python
numbers = (10, 20, 30, 20, 40)

print(numbers.index(20, 2))
```

Output:

```text
3
```

The search starts at index 2.

## 8. Useful Built-in Functions with Tuples

Python provides several built-in functions that can be used with tuples.

### A. len()

Returns the total number of elements.

```python
numbers = (10, 20, 30, 40)

print(len(numbers))
```

Output:

```text
4
```

### B. max()

Returns the largest element.

```python
numbers = (10, 50, 20, 40)

print(max(numbers))
```

Output:

```text
50
```

### C. min()

Returns the smallest element.

```python
numbers = (10, 50, 20, 40)

print(min(numbers))
```

Output:

```text
10
```

### D. sum()

Returns the sum of numeric elements.

```python
numbers = (10, 20, 30, 40)

print(sum(numbers))
```

Output:

```text
100
```

### E. sorted()

Returns a sorted list from the tuple elements. It does not modify the original tuple.

```python
numbers = (40, 10, 30, 20)

result = sorted(numbers)

print(result)
print(numbers)
```

Output:

```text
[10, 20, 30, 40]
(40, 10, 30, 20)
```

### F. tuple()

Creates a tuple from an iterable.

```python
numbers = tuple([1, 2, 3])

print(numbers)
```

Output:

```text
(1, 2, 3)
```

## 9. Iterating Through Tuples

A tuple is iterable, so we can use loops to access its elements.

### A. Using a for Loop

```python
fruits = ("apple", "banana", "mango")

for fruit in fruits:
    print(fruit)
```

Output:

```text
apple
banana
mango
```

### B. Using a while Loop

```python
numbers = (10, 20, 30)

i = 0

while i < len(numbers):
    print(numbers[i])
    i += 1
```

Output:

```text
10
20
30
```

### C. Using enumerate()

The `enumerate()` function returns both the index and the element.

```python
fruits = ("apple", "banana", "mango")

for index, fruit in enumerate(fruits):
    print(index, fruit)
```

Output:

```text
0 apple
1 banana
2 mango
```

## 10. Nested Tuples

A nested tuple is a tuple that contains one or more tuples.

**Example:**

```python
students = (
    ("Riya", 20),
    ("Aman", 21),
    ("Neha", 19)
)

print(students)
```

Output:

```text
(('Riya', 20), ('Aman', 21), ('Neha', 19))
```

Accessing nested elements:

```python
print(students[0])
print(students[0][0])
print(students[1][1])
```

Output:

```text
('Riya', 20)
Riya
21
```

## 11. When Should We Use Tuples?

Tuples are useful when:

- Data should remain unchanged.
- We need to store fixed collections of values.
- We want to return multiple values from a function.
- We need immutable sequences.
- We want to use suitable tuples as dictionary keys or set elements.

**Example: Storing Coordinates**

```python
location = (23.2599, 77.4126)

print("Latitude:", location[0])
print("Longitude:", location[1])
```

Output:

```text
Latitude: 23.2599
Longitude: 77.4126
```

# Part 2: Sets in Python

## 12. What is a Set?

A set is an unordered collection of unique elements in Python.

It is used when we want to store multiple values without duplicates.

Sets are created using curly braces `{}` or the `set()` constructor.

**Example:**

```python
numbers = {10, 20, 30, 40}

print(numbers)
```

Output contains:

```text
10, 20, 30, 40
```

The display order is not guaranteed.

### Important properties of sets

1. Unordered: Elements do not have fixed positions.
2. Unique: Duplicate values are automatically removed.
3. Mutable: Elements can be added or removed.
4. No indexing: Elements cannot be accessed using positions.
5. Support mathematical set operations.
6. Elements must be hashable.
7. A set can contain different hashable data types.

## 13. Creating Sets

### A. Using Curly Braces

```python
fruits = {"apple", "banana", "mango"}

print(fruits)
```

Output contains:

```text
apple, banana, mango
```

### B. Creating an Empty Set

An empty set must be created using `set()`.

```python
empty = set()

print(empty)
print(type(empty))
```

Output:

```text
set()
<class 'set'>
```

**Important:** `{}` creates an empty dictionary, not an empty set.

```python
data = {}

print(type(data))
```

Output:

```text
<class 'dict'>
```

### C. Creating a Set with Duplicate Elements

Sets automatically remove duplicate values.

```python
numbers = {10, 20, 10, 30, 20, 40}

print(numbers)
```

The set contains:

```text
10, 20, 30, 40
```

Each unique value is stored only once.

### D. Using the set() Constructor

The `set()` function converts an iterable into a set.

```python
numbers = set([10, 20, 30, 20])

print(numbers)
```

Output contains:

```text
10, 20, 30
```

Converting a string into a set:

```python
text = "banana"

result = set(text)

print(result)
```

The result contains the unique characters:

```text
b, a, n
```

The order may vary.

## 14. Accessing Set Elements

Sets are unordered collections.

Therefore, we cannot access their elements using indexing or slicing.

Incorrect:

```python
numbers = {10, 20, 30}

print(numbers[0])
```

This raises a `TypeError`.

### How to Access Set Elements

We can use a loop to access elements.

```python
numbers = {10, 20, 30, 40}

for number in numbers:
    print(number)
```

Output contains all four elements, but their order is not guaranteed.

### Checking Membership

The `in` operator checks whether an element exists in a set.

```python
fruits = {"apple", "banana", "mango"}

print("apple" in fruits)
print("orange" in fruits)
```

Output:

```text
True
False
```

The `not in` operator checks whether an element is absent.

```python
print("orange" not in fruits)
```

Output:

```text
True
```

## 15. Adding Elements to a Set

Python provides two main methods for adding elements.

### A. add()

The `add()` method adds a single element.

**Syntax:**

```python
set_name.add(element)
```

Example:

```python
fruits = {"apple", "banana"}

fruits.add("mango")

print(fruits)
```

The set contains:

```text
apple, banana, mango
```

Adding an element that already exists does not create a duplicate.

```python
numbers = {10, 20, 30}

numbers.add(20)

print(numbers)
```

The set still contains only:

```text
10, 20, 30
```

### B. update()

The `update()` method adds multiple elements from an iterable.

**Syntax:**

```python
set_name.update(iterable)
```

Example:

```python
numbers = {10, 20}

numbers.update([30, 40, 50])

print(numbers)
```

The set contains:

```text
10, 20, 30, 40, 50
```

We can also update a set using another set.

```python
a = {1, 2, 3}
b = {3, 4, 5}

a.update(b)

print(a)
```

The result contains:

```text
1, 2, 3, 4, 5
```

## 16. Removing Elements from a Set

Python provides several methods to remove elements.

### A. remove()

Removes the specified element.

```python
numbers = {10, 20, 30, 40}

numbers.remove(20)

print(numbers)
```

The set contains:

```text
10, 30, 40
```

If the element does not exist, `remove()` raises a `KeyError`.

### B. discard()

Removes the specified element if it exists.

```python
numbers = {10, 20, 30, 40}

numbers.discard(20)
numbers.discard(100)

print(numbers)
```

The set contains:

```text
10, 30, 40
```

Unlike `remove()`, `discard()` does not raise an error when the element is absent.

### C. pop()

Removes and returns an arbitrary element from the set.

```python
numbers = {10, 20, 30}

removed = numbers.pop()

print("Removed:", removed)
print("Remaining:", numbers)
```

The removed element is not predictable because sets are unordered.

### D. clear()

Removes all elements from the set.

```python
numbers = {10, 20, 30}

numbers.clear()

print(numbers)
```

Output:

```text
set()
```

### Difference Between Set Removal Methods

| Method | Description | If element is absent |
|---|---|---|
| `remove()` | Removes a specified element | Raises `KeyError` |
| `discard()` | Removes a specified element if present | Does nothing |
| `pop()` | Removes and returns an arbitrary element | Raises `KeyError` if empty |
| `clear()` | Removes all elements | No error |

## 17. Mathematical Set Operations

Python supports mathematical operations between sets.

These operations are useful for comparing collections of data.

Consider two sets:

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
```

### A. Union

Union combines all unique elements from both sets.

It is represented by the `|` operator or `union()` method.

**Syntax:**

```python
A | B
```

Example:

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A.union(B))
print(A | B)
```

Output contains:

```text
1, 2, 3, 4, 5, 6
```

Duplicate elements appear only once.

### B. Intersection

Intersection returns elements that are common to both sets.

It is represented by the `&` operator or `intersection()` method.

Example:

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A.intersection(B))
print(A & B)
```

Output:

```text
{3, 4}
```

### C. Difference

Difference returns elements that exist in the first set but not in the second set.

It is represented by the `-` operator or `difference()` method.

Example:

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A.difference(B))
print(A - B)
```

Output:

```text
{1, 2}
```

Reverse difference:

```python
print(B - A)
```

Output:

```text
{5, 6}
```

**Important:** Difference is directional. `A - B` and `B - A` can produce different results.

### D. Symmetric Difference

Symmetric difference returns elements that exist in either set but not in both.

It is represented by the `^` operator or `symmetric_difference()` method.

Example:

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A.symmetric_difference(B))
print(A ^ B)
```

Output contains:

```text
1, 2, 5, 6
```

### Summary of Set Operations

| Operation | Symbol | Meaning |
|---|---|---|
| Union | `A \| B` | All unique elements from both sets |
| Intersection | `A & B` | Common elements |
| Difference | `A - B` | Elements in A but not B |
| Symmetric Difference | `A ^ B` | Elements in either set, but not both |

## 18. Updating Sets Using Set Operations

Python provides methods that directly modify the original set.

### A. update()

Adds all unique elements from another iterable.

```python
A = {1, 2, 3}
B = {3, 4, 5}

A.update(B)

print(A)
```

Result contains:

```text
1, 2, 3, 4, 5
```

### B. intersection_update()

Keeps only common elements.

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

A.intersection_update(B)

print(A)
```

Output:

```text
{3, 4}
```

### C. difference_update()

Removes elements that are also present in another set.

```python
A = {1, 2, 3, 4}
B = {3, 4, 5}

A.difference_update(B)

print(A)
```

Output:

```text
{1, 2}
```

### D. symmetric_difference_update()

Keeps elements that are present in exactly one of the sets.

```python
A = {1, 2, 3}
B = {3, 4, 5}

A.symmetric_difference_update(B)

print(A)
```

Output contains:

```text
1, 2, 4, 5
```

**Important:** These update methods modify the original set rather than returning a new set as their primary result.

## 19. Subsets and Supersets

### A. Subset

A set A is a subset of set B if every element of A is also present in B.

The `issubset()` method checks this condition.

The `<=` operator can also be used.

Example:

```python
A = {1, 2}
B = {1, 2, 3, 4}

print(A.issubset(B))
print(A <= B)
```

Output:

```text
True
True
```

### B. Superset

A set A is a superset of set B if A contains every element of B.

The `issuperset()` method checks this condition.

The `>=` operator can also be used.

Example:

```python
A = {1, 2, 3, 4}
B = {1, 2}

print(A.issuperset(B))
print(A >= B)
```

Output:

```text
True
True
```

### C. Proper Subset and Proper Superset

A proper subset is a subset that is not equal to the other set.

The `<` operator checks proper subset relationships.

The `>` operator checks proper superset relationships.

```python
A = {1, 2}
B = {1, 2, 3}

print(A < B)
print(B > A)
```

Output:

```text
True
True
```

## 20. Disjoint Sets

Two sets are disjoint if they have no common elements.

The `isdisjoint()` method checks whether two sets have an empty intersection.

Example:

```python
A = {1, 2, 3}
B = {4, 5, 6}

print(A.isdisjoint(B))
```

Output:

```text
True
```

Example with common elements:

```python
A = {1, 2, 3}
B = {3, 4, 5}

print(A.isdisjoint(B))
```

Output:

```text
False
```

## 21. Frozen Sets

A frozenset is an immutable version of a set.

Once created, its elements cannot be added or removed.

It is created using the `frozenset()` constructor.

**Example:**

```python
numbers = frozenset([10, 20, 30, 40])

print(numbers)
print(type(numbers))
```

Output contains:

```text
10, 20, 30, 40
<class 'frozenset'>
```

The display order is not guaranteed.

### Properties of Frozensets

- Immutable.
- Stores unique elements.
- Unordered.
- Supports mathematical set operations.
- Cannot use methods such as `add()` or `remove()`.
- Can be used as a dictionary key or as an element of another set, provided its elements are hashable.

**Example:**

```python
A = frozenset([1, 2, 3])
B = frozenset([3, 4, 5])

print(A | B)
print(A & B)
```

Output contains:

```text
1, 2, 3, 4, 5
3
```

### Difference Between Set and Frozenset

| Set | Frozenset |
|---|---|
| Mutable | Immutable |
| Elements can be added | Elements cannot be added |
| Elements can be removed | Elements cannot be removed |
| Cannot be used as a dictionary key | Can be used as a dictionary key if its elements are hashable |
| Created using `{}` or `set()` | Created using `frozenset()` |

## 22. Set Comprehension

Set comprehension provides a short way to create sets using an expression and an iterable.

**Syntax:**

```python
{expression for item in iterable if condition}
```

### Example 1: Squares of Numbers

```python
numbers = {1, 2, 3, 4, 5}

squares = {num ** 2 for num in numbers}

print(squares)
```

Output contains:

```text
1, 4, 9, 16, 25
```

### Example 2: Even Numbers

```python
numbers = {1, 2, 3, 4, 5, 6}

even_numbers = {num for num in numbers if num % 2 == 0}

print(even_numbers)
```

Output:

```text
{2, 4, 6}
```

### Example 3: Convert Strings to Uppercase

```python
names = {"riya", "aman", "neha"}

result = {name.upper() for name in names}

print(result)
```

Output contains:

```text
RIYA, AMAN, NEHA
```

The order is not guaranteed.

## 23. Hashable Elements in Sets

Set elements must be hashable.

A hashable object has a hash value that remains stable during its lifetime and can be compared for equality.

Common hashable objects include:

- Integers
- Strings
- Floats
- Booleans
- Tuples containing only hashable elements
- Frozensets

Lists, dictionaries, and ordinary sets are mutable and cannot be directly stored as set elements.

**Incorrect Example:**

```python
data = {[1, 2], [3, 4]}
```

This raises a `TypeError` because lists are unhashable.

**Correct Example:**

```python
data = {(1, 2), (3, 4)}

print(data)
```

The set contains two tuples.

A tuple is hashable only when all its elements are hashable.

## 24. Converting Between Lists, Tuples, and Sets

Python allows conversion between common collection types.

### A. List to Tuple

```python
numbers = [10, 20, 30]

result = tuple(numbers)

print(result)
```

Output:

```text
(10, 20, 30)
```

### B. Tuple to List

```python
numbers = (10, 20, 30)

result = list(numbers)

print(result)
```

Output:

```text
[10, 20, 30]
```

### C. List to Set

```python
numbers = [10, 20, 10, 30, 20]

result = set(numbers)

print(result)
```

The set contains:

```text
10, 20, 30
```

### D. Set to List

```python
numbers = {10, 20, 30}

result = list(numbers)

print(result)
```

Output contains all three elements, but their order is not guaranteed.

### E. Tuple to Set

```python
numbers = (10, 20, 10, 30)

result = set(numbers)

print(result)
```

The set contains:

```text
10, 20, 30
```

**Important:** Converting a collection to a set removes duplicate elements and does not preserve a guaranteed positional order.

## 25. Difference Between List, Tuple, and Set

| Feature | List | Tuple | Set |
|---|---|---|---|
| Syntax | `[]` | `()` | `{}` |
| Ordered | Yes | Yes | No |
| Mutable | Yes | No | Yes |
| Allows duplicates | Yes | Yes | No |
| Indexing | Yes | Yes | No |
| Slicing | Yes | Yes | No |
| Mathematical set operations | No direct set operations | No direct set operations | Yes |
| Can store mixed types | Yes | Yes | Yes, if elements are hashable |

**Examples:**

```python
my_list = [10, 20, 10]
my_tuple = (10, 20, 10)
my_set = {10, 20, 10}

print(my_list)
print(my_tuple)
print(my_set)
```

Output:

```text
[10, 20, 10]
(10, 20, 10)
{10, 20}
```

## 26. Practical Applications of Tuples and Sets

### A. Tuples for Fixed Student Records

```python
student = ("Riya", 20, "Computer Science")

name, age, course = student

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Course: {course}")
```

Output:

```text
Name: Riya
Age: 20
Course: Computer Science
```

### B. Sets for Removing Duplicate Values

```python
marks = [80, 90, 80, 70, 90, 85]

unique_marks = set(marks)

print(unique_marks)
```

The set contains:

```text
70, 80, 85, 90
```

### C. Finding Common Students

```python
python_students = {"Riya", "Aman", "Neha"}
java_students = {"Aman", "Neha", "Rahul"}

common = python_students & java_students

print(common)
```

Output contains:

```text
Aman, Neha
```

### D. Finding Students Enrolled in Either Course

```python
python_students = {"Riya", "Aman", "Neha"}
java_students = {"Aman", "Neha", "Rahul"}

all_students = python_students | java_students

print(all_students)
```

Output contains:

```text
Riya, Aman, Neha, Rahul
```

### E. Finding Students Enrolled Only in Python

```python
python_students = {"Riya", "Aman", "Neha"}
java_students = {"Aman", "Neha", "Rahul"}

only_python = python_students - java_students

print(only_python)
```

Output:

```text
{'Riya'}
```

## Key concepts

### Tuple Concepts

- **Tuple:** An ordered collection of elements.
- **Immutability:** Tuple elements cannot be directly changed after creation.
- **Indexing:** Accessing tuple elements using positions.
- **Slicing:** Extracting a portion of a tuple.
- **Tuple packing:** Combining multiple values into one tuple.
- **Tuple unpacking:** Assigning tuple elements to separate variables.
- **Extended unpacking:** Using `*` to collect remaining elements into a list.
- **count():** Counts occurrences of an element.
- **index():** Finds the first occurrence of an element.
- **Nested tuple:** A tuple containing other tuples.

### Set Concepts

- **Set:** An unordered collection of unique elements.
- **Uniqueness:** Duplicate elements are automatically removed.
- **add():** Adds one element.
- **update():** Adds multiple elements.
- **remove():** Removes an element and raises an error if absent.
- **discard():** Removes an element without raising an error if absent.
- **pop():** Removes and returns an arbitrary element.
- **clear():** Removes all elements.
- **Union:** Combines unique elements from two sets.
- **Intersection:** Returns common elements.
- **Difference:** Returns elements present in one set but absent in another.
- **Symmetric difference:** Returns elements present in either set but not both.
- **Subset:** A set whose elements are all present in another set.
- **Superset:** A set containing all elements of another set.
- **Disjoint sets:** Sets with no common elements.
- **Frozenset:** An immutable set.
- **Set comprehension:** A concise method for creating sets.
- **Hashable:** An object suitable for use as a set element.

## Common mistakes

1. **Forgetting the comma in a single-element tuple**

   Incorrect:

   ```python
   number = (10)
   ```

   This creates an integer, not a tuple.

   Correct:

   ```python
   number = (10,)
   ```

2. **Trying to modify tuple elements**

   Tuples are immutable.

   Create a new tuple if you need different values.

3. **Assuming tuples cannot contain mutable objects**

   A tuple can contain a list, and that list can still be modified.

4. **Unpacking the wrong number of elements**

   Incorrect:

   ```python
   data = (10, 20, 30)

   a, b = data
   ```

   Correct:

   ```python
   a, b, c = data
   ```

   Alternatively, use extended unpacking with `*`.

5. **Using an invalid tuple index**

   Tuple indexing starts at 0. Accessing an invalid index raises `IndexError`.

6. **Confusing tuple methods with list methods**

   Tuples provide `count()` and `index()` as their main methods. They do not have `append()`, `remove()`, or `sort()` methods.

7. **Creating an empty set using `{}`**

   Incorrect:

   ```python
   data = {}
   ```

   This creates a dictionary.

   Correct:

   ```python
   data = set()
   ```

8. **Trying to access set elements using indexing**

   Incorrect:

   ```python
   numbers = {10, 20, 30}
   print(numbers[0])
   ```

   Sets do not support indexing.

   Use a loop or membership testing instead.

9. **Expecting set elements to appear in a fixed order**

   Sets are unordered. Do not rely on their display or iteration order.

10. **Expecting duplicate elements in a set**

    Sets automatically remove duplicates.

11. **Using remove() when an element may not exist**

    `remove()` raises `KeyError` if the element is missing.

    Use `discard()` when you want to avoid this error.

12. **Assuming pop() removes a specific element**

    Set `pop()` removes an arbitrary element, not necessarily the first or last one.

13. **Confusing union and intersection**

    - Union combines all unique elements.
    - Intersection returns only common elements.

14. **Confusing difference and symmetric difference**

    - `A - B` returns elements only in A.
    - `A ^ B` returns elements in either set but not both.

15. **Trying to store a list or dictionary inside a set**

    Mutable lists and dictionaries are unhashable and cannot be set elements.

    Use suitable immutable elements such as tuples containing hashable values.

16. **Confusing set and frozenset**

    A set is mutable, whereas a frozenset is immutable.

17. **Assuming sorted() changes the original tuple or set**

    `sorted()` returns a new list. It does not modify the original collection.

## Quick summary

- Tuples and sets are collection data types in Python.
- A tuple is ordered and immutable.
- A set is unordered, mutable, and stores unique elements.
- Tuples are created using `()` or `tuple()`.
- A single-element tuple requires a trailing comma.
- Tuple elements can be accessed using positive and negative indexing.
- Tuple slicing extracts a portion of a tuple.
- Tuple packing combines values into a tuple.
- Tuple unpacking assigns elements to variables.
- Tuple methods include `count()` and `index()`.
- Sets are created using `{}` or `set()`.
- An empty set must be created using `set()`.
- Sets do not support indexing or slicing.
- `add()` adds one element.
- `update()` adds multiple elements.
- `remove()` and `discard()` remove specified elements.
- `pop()` removes an arbitrary element.
- `clear()` removes all elements.
- Union combines unique elements.
- Intersection returns common elements.
- Difference returns elements present in one set but not the other.
- Symmetric difference returns elements present in either set but not both.
- Subsets and supersets describe relationships between sets.
- Disjoint sets have no common elements.
- Frozensets are immutable sets.
- Set comprehension provides a short way to create sets.
- Set elements must be hashable.
- Lists, tuples, and sets can be converted into one another where appropriate.

## Practice

### Beginner Level

**1. Create a Tuple**

Create a tuple containing five numbers and print it.

**2. Create an Empty Tuple**

Create an empty tuple and check its data type.

**3. Single-Element Tuple**

Create a tuple containing only one element.

**4. Tuple Indexing**

Print the first, third, and last elements of a tuple.

**5. Negative Indexing**

Access the last two elements using negative indexing.

**6. Tuple Slicing**

Extract the first three elements from a tuple.

**7. Tuple Length**

Find the number of elements using `len()`.

**8. Tuple Count**

Count how many times the number 10 appears in a tuple.

**9. Tuple Index**

Find the index of a particular element using `index()`.

**10. Create a Set**

Create a set containing five numbers and print it.

### Intermediate Level

**11. Remove Duplicates**

Convert a list containing duplicate elements into a set.

**12. Add Elements**

Add one element using `add()` and multiple elements using `update()`.

**13. Remove Elements**

Remove elements using `remove()` and `discard()`.

**14. Tuple Unpacking**

Create a tuple containing a person's name, age, and city. Assign its values to separate variables.

**15. Swap Variables**

Swap two variables using tuple unpacking.

**16. Set Union**

Find the union of two sets.

**17. Set Intersection**

Find the common elements between two sets.

**18. Set Difference**

Find elements that are present in the first set but not in the second.

**19. Symmetric Difference**

Find elements that are present in either set but not both.

**20. Check Subset**

Check whether one set is a subset of another.

### Advanced Level

**21. Find Unique Elements**

Write a program to find unique elements in a list using sets.

**22. Find Common Elements in Three Sets**

Find the elements that are common to three sets.

**23. Remove Duplicate Words**

Given a sentence, find all unique words using a set.

**24. Find Missing Elements**

Given a set of numbers from 1 to 10 with some missing values, identify the missing numbers.

**25. Find Students in Only One Course**

Given two sets of students enrolled in different courses, find students who are enrolled in exactly one course.

**26. Set Comprehension**

Create a set of squares of even numbers from 1 to 20.

**27. Character Uniqueness**

Check whether all characters in a string are unique using a set.

**28. Anagram Using Sets**

Understand why comparing sets alone is insufficient for checking anagrams when character frequencies matter. Write a correct solution using character counts.

**29. Frozenset**

Create a frozenset and demonstrate that it cannot be modified.

**30. Tuple-Based Student Records**

Store student information in nested tuples and display each student's name and marks.

### Sample Solutions

**Solution 1: Create a Tuple**

```python
numbers = (10, 20, 30, 40, 50)

print(numbers)
```

Output:

```text
(10, 20, 30, 40, 50)
```

**Solution 2: Create an Empty Tuple**

```python
empty = ()

print(empty)
print(type(empty))
```

Output:

```text
()
<class 'tuple'>
```

**Solution 3: Single-Element Tuple**

```python
number = (10,)

print(number)
print(type(number))
```

Output:

```text
(10,)
<class 'tuple'>
```

**Solution 4: Tuple Indexing**

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[0])
print(numbers[2])
print(numbers[-1])
```

Output:

```text
10
30
50
```

**Solution 5: Negative Indexing**

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[-2:])
```

Output:

```text
(40, 50)
```

**Solution 6: Tuple Slicing**

```python
numbers = (10, 20, 30, 40, 50)

print(numbers[:3])
```

Output:

```text
(10, 20, 30)
```

**Solution 7: Tuple Length**

```python
numbers = (10, 20, 30, 40, 50)

print(len(numbers))
```

Output:

```text
5
```

**Solution 8: Tuple Count**

```python
numbers = (10, 20, 10, 30, 10)

print(numbers.count(10))
```

Output:

```text
3
```

**Solution 9: Tuple Index**

```python
numbers = (10, 20, 30, 40)

print(numbers.index(30))
```

Output:

```text
2
```

**Solution 10: Create a Set**

```python
numbers = {10, 20, 30, 40, 50}

print(numbers)
```

The set contains all five numbers. Their order is not guaranteed.

**Solution 11: Remove Duplicates**

```python
numbers = [10, 20, 10, 30, 20, 40]

unique_numbers = set(numbers)

print(unique_numbers)
```

The set contains:

```text
10, 20, 30, 40
```

**Solution 12: Add Elements**

```python
numbers = {10, 20, 30}

numbers.add(40)
numbers.update([50, 60])

print(numbers)
```

The set contains:

```text
10, 20, 30, 40, 50, 60
```

**Solution 13: Remove Elements**

```python
numbers = {10, 20, 30, 40, 50}

numbers.remove(20)
numbers.discard(100)

print(numbers)
```

The set contains:

```text
10, 30, 40, 50
```

**Solution 14: Tuple Unpacking**

```python
student = ("Riya", 20, "Bhopal")

name, age, city = student

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

**Solution 15: Swap Variables**

```python
a = 10
b = 20

a, b = b, a

print("a =", a)
print("b =", b)
```

Output:

```text
a = 20
b = 10
```

**Solution 16: Set Union**

```python
A = {1, 2, 3}
B = {3, 4, 5}

print(A | B)
```

The result contains:

```text
1, 2, 3, 4, 5
```

**Solution 17: Set Intersection**

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A & B)
```

Output:

```text
{3, 4}
```

**Solution 18: Set Difference**

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A - B)
```

Output:

```text
{1, 2}
```

**Solution 19: Symmetric Difference**

```python
A = {1, 2, 3}
B = {3, 4, 5}

print(A ^ B)
```

The result contains:

```text
1, 2, 4, 5
```

**Solution 20: Check Subset**

```python
A = {1, 2}
B = {1, 2, 3, 4}

if A.issubset(B):
    print("A is a subset of B")
else:
    print("A is not a subset of B")
```

Output:

```text
A is a subset of B
```

**Solution 21: Find Unique Elements**

```python
numbers = [1, 2, 2, 3, 4, 4, 5]

unique = set(numbers)

print(unique)
```

The set contains:

```text
1, 2, 3, 4, 5
```

**Solution 22: Common Elements in Three Sets**

```python
A = {1, 2, 3, 4}
B = {2, 3, 4, 5}
C = {3, 4, 5, 6}

common = A & B & C

print(common)
```

Output:

```text
{3, 4}
```

**Solution 23: Remove Duplicate Words**

```python
sentence = "python is easy and python is powerful"

words = sentence.split()

unique_words = set(words)

print(unique_words)
```

The set contains the unique words:

```text
python, is, easy, and, powerful
```

The order is not guaranteed.

**Solution 24: Find Missing Elements**

```python
numbers = {1, 2, 4, 6, 7, 9, 10}

complete = set(range(1, 11))

missing = complete - numbers

print(missing)
```

Output:

```text
{3, 5, 8}
```

**Solution 25: Students in Only One Course**

```python
python_students = {"Riya", "Aman", "Neha"}
java_students = {"Aman", "Rahul", "Neha"}

result = python_students ^ java_students

print(result)
```

Output contains:

```text
Riya, Rahul
```

**Solution 26: Set Comprehension**

```python
squares = {
    num ** 2
    for num in range(1, 21)
    if num % 2 == 0
}

print(squares)
```

The set contains:

```text
4, 16, 36, 64, 100, 144, 196, 256, 324, 400
```

**Solution 27: Character Uniqueness**

```python
text = "python"

if len(text) == len(set(text)):
    print("All characters are unique")
else:
    print("Duplicate characters found")
```

Output:

```text
All characters are unique
```

**Solution 28: Anagram Checker**

Two strings are anagrams when they contain the same characters with the same frequencies.

```python
text1 = "listen"
text2 = "silent"

if sorted(text1.lower()) == sorted(text2.lower()):
    print("Anagrams")
else:
    print("Not anagrams")
```

Output:

```text
Anagrams
```

**Why not compare sets alone?**

```python
print(set("aab") == set("abb"))
```

Output:

```text
True
```

Both sets contain only `a` and `b`, but the character frequencies are different.

Therefore, comparing sets alone is not sufficient for checking anagrams.

**Solution 29: Frozenset**

```python
numbers = frozenset([10, 20, 30])

print(numbers)
print(type(numbers))
```

Trying to modify it:

```python
numbers.add(40)
```

This raises an `AttributeError` because frozensets do not support `add()`.

**Solution 30: Nested Tuple Student Records**

```python
students = (
    ("Riya", 85),
    ("Aman", 90),
    ("Neha", 88)
)

for name, marks in students:
    print(f"Name: {name}, Marks: {marks}")
```

Output:

```text
Name: Riya, Marks: 85
Name: Aman, Marks: 90
Name: Neha, Marks: 88
```

## Learning resources

- **PDF:** [Tuples and Sets](https://drive.google.com/file/d/1ZV21sjPNL6dGVoaRN-VTQkyptjTQUB1q/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)