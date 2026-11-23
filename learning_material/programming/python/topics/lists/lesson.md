
# Lists and List Operations

**Course:** Python
**Topic ID:** `lists`

## Learning objectives

After completing this topic, learners should be able to:

- Understand what a list is and why lists are used in Python.
- Create lists using square brackets `[]`.
- Store multiple values of different data types in a list.
- Access list elements using positive and negative indexing.
- Extract elements using list slicing.
- Add elements using `append()`, `insert()`, and `extend()`.
- Remove elements using `remove()`, `pop()`, `clear()`, and `del`.
- Modify and update existing list elements.
- Use built-in functions such as `len()`, `min()`, `max()`, and `sum()`.
- Sort and reverse lists.
- Iterate through lists using loops.
- Understand nested lists and common list operations.
- Identify common list errors and avoid them.

## Explanation

### 1. What is a List in Python?

A list is a built-in Python data structure used to store multiple items in a single variable.

Instead of creating separate variables for every value, we can store all the values together inside a list.

Lists are written using square brackets `[]`, and individual elements are separated by commas.

**Example:**

```python
fruits = ["apple", "banana", "mango", "orange"]

print(fruits)
```

**Output:**

```text
['apple', 'banana', 'mango', 'orange']
```

Here:
- `fruits` is the list variable.
- `"apple"`, `"banana"`, `"mango"`, and `"orange"` are list elements.
- Each element is separated by a comma.

### 2. Features of Lists

Python lists have the following important characteristics:

**1. Ordered**

Lists maintain the order in which elements are inserted.

```python
numbers = [10, 20, 30, 40]

print(numbers)
```

Output:

```text
[10, 20, 30, 40]
```

**2. Mutable**

Lists are mutable, which means their elements can be changed after creation.

```python
fruits = ["apple", "banana", "mango"]

fruits[1] = "orange"

print(fruits)
```

Output:

```text
['apple', 'orange', 'mango']
```

**3. Allow Duplicate Elements**

A list can contain the same value multiple times.

```python
numbers = [10, 20, 10, 30, 20]

print(numbers)
```

Output:

```text
[10, 20, 10, 30, 20]
```

**4. Allow Different Data Types**

A single list can store integers, strings, floats, and Boolean values.

```python
data = [10, "Python", 3.14, True]

print(data)
```

Output:

```text
[10, 'Python', 3.14, True]
```

**5. Can Contain Nested Lists**

A list can also contain other lists.

```python
matrix = [[1, 2], [3, 4], [5, 6]]

print(matrix)
```

Output:

```text
[[1, 2], [3, 4], [5, 6]]
```

### 3. Creating Lists

There are different ways to create lists in Python.

**Method 1: Using Square Brackets**

```python
numbers = [10, 20, 30, 40]

print(numbers)
```

**Method 2: Creating an Empty List**

```python
my_list = []

print(my_list)
```

Output:

```text
[]
```

**Method 3: Using the `list()` Constructor**

The `list()` constructor converts an iterable into a list.

```python
numbers = list((10, 20, 30))

print(numbers)
```

Output:

```text
[10, 20, 30]
```

**Method 4: Converting a String into a List**

```python
word = "Python"

letters = list(word)

print(letters)
```

Output:

```text
['P', 'y', 't', 'h', 'o', 'n']
```

### 4. Accessing List Elements (Indexing)

Indexing means accessing an individual element using its position in the list.

Python uses zero-based indexing, which means the first element has index `0`.

**Example:**

```python
fruits = ["apple", "banana", "mango", "orange"]

print(fruits[0])
print(fruits[1])
print(fruits[2])
print(fruits[3])
```

Output:

```text
apple
banana
mango
orange
```

**Positive Indexing**

Positive indexing starts from the beginning of the list.

| Element | Positive Index |
|---|---:|
| apple | 0 |
| banana | 1 |
| mango | 2 |
| orange | 3 |

**Negative Indexing**

Negative indexing starts from the end of the list.

- `-1` represents the last element.
- `-2` represents the second-last element.
- `-3` represents the third-last element.

```python
fruits = ["apple", "banana", "mango", "orange"]

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

### 5. List Slicing

Slicing is used to access a specific portion of a list.

**Syntax:**

```python
list_name[start:stop:step]
```

Where:
- `start`: Starting index (included).
- `stop`: Ending index (excluded).
- `step`: Number of positions to move each time.

**Example 1: Basic Slicing**

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[1:4])
```

Output:

```text
[20, 30, 40]
```

The elements at indexes 1, 2, and 3 are selected. Index 4 is excluded.

**Example 2: Slicing from the Beginning**

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[:3])
```

Output:

```text
[10, 20, 30]
```

**Example 3: Slicing to the End**

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[2:])
```

Output:

```text
[30, 40, 50]
```

**Example 4: Using Step**

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[::2])
```

Output:

```text
[10, 30, 50]
```

**Example 5: Reversing a List Using Slicing**

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[::-1])
```

Output:

```text
[50, 40, 30, 20, 10]
```

### 6. Updating List Elements

Since lists are mutable, we can change their elements after creating them.

```python
colors = ["red", "blue", "green"]

colors[1] = "yellow"

print(colors)
```

Output:

```text
['red', 'yellow', 'green']
```

We can also update multiple elements using slicing.

```python
numbers = [10, 20, 30, 40]

numbers[1:3] = [200, 300]

print(numbers)
```

Output:

```text
[10, 200, 300, 40]
```

### 7. Adding Elements to a List

Python provides several methods to add elements.

**1. append()**

The `append()` method adds one element at the end of the list.

```python
fruits = ["apple", "banana"]

fruits.append("mango")

print(fruits)
```

Output:

```text
['apple', 'banana', 'mango']
```

**2. insert()**

The `insert()` method adds an element at a specified position.

Syntax:

```python
list_name.insert(index, element)
```

Example:

```python
fruits = ["apple", "banana", "mango"]

fruits.insert(1, "orange")

print(fruits)
```

Output:

```text
['apple', 'orange', 'banana', 'mango']
```

**3. extend()**

The `extend()` method adds multiple elements from another iterable to the end of a list.

```python
numbers = [10, 20, 30]

numbers.extend([40, 50, 60])

print(numbers)
```

Output:

```text
[10, 20, 30, 40, 50, 60]
```

**Difference between append() and extend():**

```python
a = [1, 2, 3]
a.append([4, 5])

print(a)

b = [1, 2, 3]
b.extend([4, 5])

print(b)
```

Output:

```text
[1, 2, 3, [4, 5]]
[1, 2, 3, 4, 5]
```

Remember:
- `append()` adds its argument as one element.
- `extend()` adds the elements of an iterable individually.

### 8. Removing Elements from a List

Python provides different methods to remove elements.

**1. remove()**

The `remove()` method removes the first matching value.

```python
numbers = [10, 20, 30, 20, 40]

numbers.remove(20)

print(numbers)
```

Output:

```text
[10, 30, 20, 40]
```

Only the first occurrence of `20` is removed.

**2. pop()**

The `pop()` method removes and returns an element.

```python
numbers = [10, 20, 30, 40]

removed = numbers.pop()

print(removed)
print(numbers)
```

Output:

```text
40
[10, 20, 30]
```

We can also provide an index.

```python
numbers = [10, 20, 30, 40]

removed = numbers.pop(1)

print(removed)
print(numbers)
```

Output:

```text
20
[10, 30, 40]
```

**3. clear()**

The `clear()` method removes all elements from the list.

```python
numbers = [10, 20, 30]

numbers.clear()

print(numbers)
```

Output:

```text
[]
```

**4. del Statement**

The `del` statement can remove an element, a slice, or the entire list variable.

```python
numbers = [10, 20, 30, 40]

del numbers[1]

print(numbers)
```

Output:

```text
[10, 30, 40]
```

Removing a slice:

```python
numbers = [10, 20, 30, 40, 50]

del numbers[1:3]

print(numbers)
```

Output:

```text
[10, 40, 50]
```

**Difference between remove(), pop(), clear(), and del:**

| Method | Purpose |
|---|---|
| remove(value) | Removes the first matching value |
| pop(index) | Removes and returns an element |
| pop() | Removes and returns the last element |
| clear() | Removes all elements |
| del | Deletes an element, slice, or list variable |

### 9. Finding the Length of a List

The `len()` function returns the total number of elements in a list.

```python
fruits = ["apple", "banana", "mango", "orange"]

print(len(fruits))
```

Output:

```text
4
```

### 10. Useful Built-in Functions for Lists

Python provides built-in functions that make list operations easier.

**1. min()**

Returns the smallest element.

```python
numbers = [10, 5, 30, 2, 20]

print(min(numbers))
```

Output:

```text
2
```

**2. max()**

Returns the largest element.

```python
numbers = [10, 5, 30, 2, 20]

print(max(numbers))
```

Output:

```text
30
```

**3. sum()**

Returns the sum of numeric elements.

```python
numbers = [10, 20, 30, 40]

print(sum(numbers))
```

Output:

```text
100
```

**4. sorted()**

Returns a new sorted list without changing the original list.

```python
numbers = [40, 10, 30, 20]

new_list = sorted(numbers)

print(new_list)
print(numbers)
```

Output:

```text
[10, 20, 30, 40]
[40, 10, 30, 20]
```

**5. any()**

Returns `True` if at least one element is truthy.

```python
values = [0, False, 5, 0]

print(any(values))
```

Output:

```text
True
```

**6. all()**

Returns `True` if every element is truthy. It also returns `True` for an empty iterable.

```python
values = [1, 2, 3, 4]

print(all(values))
```

Output:

```text
True
```

### 11. Important List Methods

**1. sort()**

Sorts the original list in ascending order by default.

```python
numbers = [40, 10, 30, 20]

numbers.sort()

print(numbers)
```

Output:

```text
[10, 20, 30, 40]
```

For descending order:

```python
numbers = [40, 10, 30, 20]

numbers.sort(reverse=True)

print(numbers)
```

Output:

```text
[40, 30, 20, 10]
```

**2. reverse()**

Reverses the order of elements in the original list. It does not sort them.

```python
numbers = [10, 30, 20, 40]

numbers.reverse()

print(numbers)
```

Output:

```text
[40, 20, 30, 10]
```

**3. index()**

Returns the index of the first occurrence of a value.

```python
fruits = ["apple", "banana", "mango"]

print(fruits.index("banana"))
```

Output:

```text
1
```

**4. count()**

Returns the number of times a value appears.

```python
numbers = [10, 20, 10, 30, 10]

print(numbers.count(10))
```

Output:

```text
3
```

**5. copy()**

Creates a shallow copy of a list.

```python
original = [10, 20, 30]

copied = original.copy()

copied.append(40)

print(original)
print(copied)
```

Output:

```text
[10, 20, 30]
[10, 20, 30, 40]
```

### 12. Checking Whether an Element Exists

The `in` and `not in` operators check whether a value exists in a list.

**Using in:**

```python
fruits = ["apple", "banana", "mango"]

print("banana" in fruits)
```

Output:

```text
True
```

**Using not in:**

```python
fruits = ["apple", "banana", "mango"]

print("orange" not in fruits)
```

Output:

```text
True
```

### 13. Iterating Through a List

Iteration means accessing list elements one by one.

**Method 1: Using a for Loop**

```python
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)
```

Output:

```text
apple
banana
mango
```

**Method 2: Using a while Loop**

```python
numbers = [10, 20, 30, 40]

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
40
```

**Method 3: Using enumerate()**

The `enumerate()` function provides both the index and the value during iteration.

```python
fruits = ["apple", "banana", "mango"]

for index, fruit in enumerate(fruits):
    print(index, fruit)
```

Output:

```text
0 apple
1 banana
2 mango
```

We can also start the index from a different number.

```python
fruits = ["apple", "banana", "mango"]

for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
```

Output:

```text
1 apple
2 banana
3 mango
```

### 14. Nested Lists

A nested list is a list that contains one or more lists as its elements.

Nested lists are useful for representing tables, matrices, and grouped information.

**Example:**

```python
students = [
    ["Riya", 85],
    ["Aman", 90],
    ["Rahul", 78]
]

print(students)
```

Output:

```text
[['Riya', 85], ['Aman', 90], ['Rahul', 78]]
```

**Accessing Nested List Elements:**

```python
students = [
    ["Riya", 85],
    ["Aman", 90],
    ["Rahul", 78]
]

print(students[0])
print(students[0][0])
print(students[1][1])
```

Output:

```text
['Riya', 85]
Riya
90
```

Here:
- `students[0]` accesses the first inner list.
- `students[0][0]` accesses the first value of the first inner list.
- `students[1][1]` accesses the second value of the second inner list.

### 15. List Concatenation and Repetition

**List Concatenation (+)**

The `+` operator joins two lists and returns a new list.

```python
a = [1, 2, 3]
b = [4, 5, 6]

result = a + b

print(result)
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

**List Repetition (*)**

The `*` operator repeats list elements.

```python
numbers = [1, 2]

result = numbers * 3

print(result)
```

Output:

```text
[1, 2, 1, 2, 1, 2]
```

### 16. List Assignment and Copying

It is important to understand the difference between assigning a list and copying it.

**Example 1: Normal Assignment**

```python
a = [10, 20, 30]

b = a

b.append(40)

print(a)
print(b)
```

Output:

```text
[10, 20, 30, 40]
[10, 20, 30, 40]
```

Why?

Because `b = a` does not create a new list. Both variables refer to the same list object.

**Example 2: Using copy()**

```python
a = [10, 20, 30]

b = a.copy()

b.append(40)

print(a)
print(b)
```

Output:

```text
[10, 20, 30]
[10, 20, 30, 40]
```

Now `b` is a separate shallow copy of the original list.

**Important:** A shallow copy does not recursively copy nested objects. If a list contains other mutable lists, those inner lists are still shared. The `copy` module's `deepcopy()` can be used when a fully independent nested copy is required.

### 17. List Comprehension (Introduction)

List comprehension provides a shorter way to create a new list from an iterable.

**Syntax:**

```python
new_list = [expression for item in iterable]
```

Example:

```python
numbers = [1, 2, 3, 4, 5]

squares = [x * x for x in numbers]

print(squares)
```

Output:

```text
[1, 4, 9, 16, 25]
```

List comprehensions can also include conditions.

```python
numbers = [1, 2, 3, 4, 5, 6]

even_numbers = [x for x in numbers if x % 2 == 0]

print(even_numbers)
```

Output:

```text
[2, 4, 6]
```

Note: List comprehensions are introduced here. They are covered in greater detail in the separate Comprehensions topic.

### 18. Practical Example: Student Marks Management

Let's create a simple program that stores student marks and performs basic list operations.

```python
marks = [85, 90, 78, 92, 88]

print("Student Marks:", marks)

print("Total Marks:", sum(marks))
print("Highest Marks:", max(marks))
print("Lowest Marks:", min(marks))
print("Number of Subjects:", len(marks))

average = sum(marks) / len(marks)

print("Average Marks:", average)

marks.append(95)

print("After Adding New Marks:", marks)

marks.sort()

print("Sorted Marks:", marks)
```

Output:

```text
Student Marks: [85, 90, 78, 92, 88]
Total Marks: 433
Highest Marks: 92
Lowest Marks: 78
Number of Subjects: 5
Average Marks: 86.6
After Adding New Marks: [85, 90, 78, 92, 88, 95]
Sorted Marks: [78, 85, 88, 90, 92, 95]
```

This example demonstrates:
- Creating a list.
- Displaying list elements.
- Calculating the sum and average.
- Finding the maximum and minimum values.
- Finding the length of a list.
- Adding an element.
- Sorting the list.

## Key concepts

- **List:** A collection used to store multiple elements in one variable.
- **Square brackets `[]`:** Used to create lists.
- **Element:** An individual value stored inside a list.
- **Indexing:** Accessing an element using its position.
- **Positive indexing:** Starts from index `0`.
- **Negative indexing:** Starts from index `-1` at the end.
- **Slicing:** Extracting a portion of a list.
- **Mutable:** List elements can be changed after creation.
- **append():** Adds one element at the end.
- **insert():** Adds an element at a specified position.
- **extend():** Adds elements from another iterable.
- **remove():** Removes the first matching value.
- **pop():** Removes and returns an element.
- **clear():** Removes all elements.
- **sort():** Sorts the original list.
- **reverse():** Reverses the original list.
- **index():** Finds the position of the first matching element.
- **count():** Counts occurrences of an element.
- **len():** Returns the number of elements.
- **Nested list:** A list containing other lists.
- **List comprehension:** A concise way to create lists.

## Common mistakes

1. **Using the wrong index**

   Incorrect:

   ```python
   fruits = ["apple", "banana", "mango"]

   print(fruits[3])
   ```

   This produces an `IndexError` because valid indexes are `0`, `1`, and `2`.

   Correct:

   ```python
   print(fruits[2])
   ```

2. **Forgetting that indexing starts from zero**

   The first element is at index `0`, not index `1`.

3. **Confusing append() and extend()**

   `append([4, 5])` adds the entire list as one nested element, whereas `extend([4, 5])` adds the two elements separately.

4. **Using remove() with an element that does not exist**

   ```python
   numbers = [10, 20, 30]

   numbers.remove(50)
   ```

   This raises a `ValueError`.

   Check first:

   ```python
   if 50 in numbers:
       numbers.remove(50)
   ```

5. **Confusing sort() and sorted()**

   - `sort()` changes the original list and returns `None`.
   - `sorted()` returns a new sorted list.

6. **Expecting reverse() to sort a list**

   `reverse()` only changes the order of existing elements. It does not arrange them in ascending or descending order.

7. **Assigning one list to another and expecting an independent copy**

   ```python
   a = [1, 2, 3]
   b = a
   ```

   Both variables refer to the same list. Use `a.copy()` for a shallow copy.

8. **Using an invalid slicing assumption**

   The stop index in slicing is excluded.

   ```python
   numbers = [10, 20, 30, 40]

   print(numbers[1:3])
   ```

   Output:

   ```text
   [20, 30]
   ```

9. **Modifying a list while iterating over it**

   Removing elements directly from a list while looping over it can cause elements to be skipped.

   Safer approach:

   ```python
   numbers = [1, 2, 3, 4, 5]

   numbers = [x for x in numbers if x % 2 != 0]

   print(numbers)
   ```

   Output:

   ```text
   [1, 3, 5]
   ```

10. **Calling list methods incorrectly**

    Methods such as `append()`, `insert()`, `extend()`, and `sort()` modify the list and generally return `None`.

    Incorrect:

    ```python
    numbers = [1, 2, 3]

    numbers = numbers.append(4)

    print(numbers)
    ```

    Correct:

    ```python
    numbers = [1, 2, 3]

    numbers.append(4)

    print(numbers)
    ```

## Quick summary

- Lists store multiple values in a single variable.
- Lists are created using square brackets `[]`.
- Lists are ordered, mutable, and allow duplicate values.
- Lists can store different data types.
- Positive indexing starts at `0`.
- Negative indexing starts at `-1`.
- Slicing extracts a portion of a list.
- `append()` adds one element.
- `insert()` adds an element at a particular position.
- `extend()` adds multiple elements from an iterable.
- `remove()` removes the first matching value.
- `pop()` removes and returns an element.
- `clear()` removes all elements.
- `len()` returns the number of elements.
- `min()`, `max()`, and `sum()` perform useful calculations.
- `sort()` sorts a list, while `reverse()` reverses its current order.
- `index()` finds an element's position.
- `count()` counts how often an element occurs.
- `copy()` creates a shallow copy.
- Nested lists can store lists inside other lists.
- List comprehensions provide a shorter way to create lists.

## Practice

### Beginner Level

**1. Create a List**

Create a list containing five different fruits and print it.

**2. Access Elements**

Given:

```python
numbers = [10, 20, 30, 40, 50]
```

Print:
- The first element.
- The last element.
- The third element.

**3. Find the Length**

Write a program to find the total number of elements in a list.

**4. Update an Element**

Given:

```python
colors = ["red", "blue", "green"]
```

Replace `"blue"` with `"yellow"`.

**5. Add Elements**

Create a list of three numbers and add two more numbers using `append()`.

### Intermediate Level

**6. Find the Sum and Average**

Given:

```python
marks = [75, 80, 90, 85, 70]
```

Find the total and average marks.

**7. Find Even Numbers**

Given:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

Create a new list containing only even numbers.

**8. Remove Duplicates**

Given:

```python
numbers = [10, 20, 10, 30, 20, 40]
```

Create a new list containing unique values while preserving their original order.

**9. Find the Second Largest Element**

Write a program to find the second-largest distinct number in a list.

**10. Reverse a List**

Reverse a list using:
- The `reverse()` method.
- Slicing.

### Advanced Level

**11. Find Common Elements**

Given:

```python
a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]
```

Create a list containing the common elements.

**12. Separate Positive and Negative Numbers**

Given:

```python
numbers = [-5, 10, -2, 8, 0, -7, 3]
```

Create separate lists for positive numbers, negative numbers, and zeros.

**13. Flatten a Nested List**

Given:

```python
nested = [[1, 2], [3, 4], [5, 6]]
```

Convert it into:

```text
[1, 2, 3, 4, 5, 6]
```

**14. Rotate a List**

Write a program to rotate a list to the right by two positions.

Example:

```text
Input:  [1, 2, 3, 4, 5]
Output: [4, 5, 1, 2, 3]
```

**15. Student Marks Analysis**

Create a program that:
- Stores marks of five students.
- Calculates the average.
- Finds the highest and lowest marks.
- Displays marks in ascending order.
- Adds a new student's marks.
- Counts how many students scored above 75.

### Sample Solutions

**Solution 1: Create a List**

```python
fruits = ["apple", "banana", "mango", "orange", "grapes"]

print(fruits)
```

**Solution 2: Access Elements**

```python
numbers = [10, 20, 30, 40, 50]

print("First:", numbers[0])
print("Last:", numbers[-1])
print("Third:", numbers[2])
```

**Solution 3: Find the Length**

```python
numbers = [10, 20, 30, 40, 50]

print("Length:", len(numbers))
```

**Solution 4: Update an Element**

```python
colors = ["red", "blue", "green"]

colors[1] = "yellow"

print(colors)
```

**Solution 5: Add Elements**

```python
numbers = [10, 20, 30]

numbers.append(40)
numbers.append(50)

print(numbers)
```

**Solution 6: Find the Sum and Average**

```python
marks = [75, 80, 90, 85, 70]

total = sum(marks)
average = total / len(marks)

print("Total:", total)
print("Average:", average)
```

**Solution 7: Find Even Numbers**

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)

print(even_numbers)
```

**Solution 8: Remove Duplicates**

```python
numbers = [10, 20, 10, 30, 20, 40]

unique = []

for num in numbers:
    if num not in unique:
        unique.append(num)

print(unique)
```

**Solution 9: Find the Second Largest Distinct Element**

```python
numbers = [10, 40, 20, 40, 30]

unique = sorted(set(numbers), reverse=True)

if len(unique) >= 2:
    print("Second largest:", unique[1])
else:
    print("Second largest element does not exist")
```

**Solution 10: Reverse a List**

```python
numbers = [1, 2, 3, 4, 5]

# Using reverse()
a = numbers.copy()
a.reverse()

print(a)

# Using slicing
b = numbers[::-1]

print(b)
```

**Solution 11: Find Common Elements**

```python
a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]

common = []

for num in a:
    if num in b:
        common.append(num)

print(common)
```

**Solution 12: Separate Positive and Negative Numbers**

```python
numbers = [-5, 10, -2, 8, 0, -7, 3]

positive = []
negative = []
zeros = []

for num in numbers:
    if num > 0:
        positive.append(num)
    elif num < 0:
        negative.append(num)
    else:
        zeros.append(num)

print("Positive:", positive)
print("Negative:", negative)
print("Zeros:", zeros)
```

**Solution 13: Flatten a Nested List**

```python
nested = [[1, 2], [3, 4], [5, 6]]

flat = []

for sublist in nested:
    for num in sublist:
        flat.append(num)

print(flat)
```

**Solution 14: Rotate a List to the Right**

```python
numbers = [1, 2, 3, 4, 5]

k = 2

if numbers:
    k = k % len(numbers)
    rotated = numbers[-k:] + numbers[:-k]
else:
    rotated = []

print(rotated)
```

Output:

```text
[4, 5, 1, 2, 3]
```

**Solution 15: Student Marks Analysis**

```python
marks = [75, 80, 90, 85, 70]

print("Original Marks:", marks)

average = sum(marks) / len(marks)

print("Average:", average)
print("Highest:", max(marks))
print("Lowest:", min(marks))

marks.sort()

print("Ascending Order:", marks)

marks.append(95)

print("After Adding New Marks:", marks)

count = 0

for mark in marks:
    if mark > 75:
        count += 1

print("Students scoring above 75:", count)
```

## Learning resources

- **PDF:** [Lists and List Operations](https://drive.google.com/file/d/1NYlEhvdiMGyOLDn78zMG3g-y9GFQIXYU/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)