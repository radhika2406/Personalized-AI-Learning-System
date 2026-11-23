
# List, Dict and Set Comprehensions

**Course:** Python
**Topic ID:** `comprehensions`

## Learning objectives

After completing this topic, learners should be able to:

- Understand the concept and purpose of comprehensions.
- Create lists using list comprehensions.
- Create dictionaries using dictionary comprehensions.
- Create sets using set comprehensions.
- Apply conditions to filter elements.
- Use conditional expressions to transform values.
- Work with nested comprehensions.
- Convert simple loops into comprehensions.

## Explanation

### 1. What are Comprehensions?

Comprehensions are a concise way of creating new collections from existing iterables such as lists, tuples, strings, and ranges.

They combine loops and expressions into a single statement, making code shorter and often easier to read.

**Example using a normal loop:**

```python
numbers = [1, 2, 3, 4, 5]
squares = []

for number in numbers:
    squares.append(number ** 2)

print(squares)
```

Output:

```text
[1, 4, 9, 16, 25]
```

**The same example using list comprehension:**

```python
numbers = [1, 2, 3, 4, 5]
squares = [number ** 2 for number in numbers]

print(squares)
```

Output:

```text
[1, 4, 9, 16, 25]
```

Both approaches produce the same result, but the comprehension requires fewer lines.

### 2. List Comprehensions

A list comprehension creates a new list using an existing iterable.

**Syntax:**

```python
new_list = [expression for item in iterable]
```

Where:

- Expression: Value to be added.
- Item: Variable representing each element.
- Iterable: Collection being processed.

**Example:**

```python
numbers = [1, 2, 3, 4, 5]

doubled = [number * 2 for number in numbers]

print(doubled)
```

Output:

```text
[2, 4, 6, 8, 10]
```

### 3. List Comprehensions with Conditions

We can use conditions to select only specific elements.

**Syntax:**

```python
new_list = [expression for item in iterable if condition]
```

**Example:**

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

even_numbers = [
    number for number in numbers
    if number % 2 == 0
]

print(even_numbers)
```

Output:

```text
[2, 4, 6, 8]
```

Only even numbers are included because they satisfy the condition.

### 4. Conditional Expressions in List Comprehensions

We can use if-else expressions to select a value for every element.

**Syntax:**

```python
new_list = [
    value_if_true if condition else value_if_false
    for item in iterable
]
```

**Example:**

```python
numbers = [1, 2, 3, 4, 5]

result = [
    "Even" if number % 2 == 0 else "Odd"
    for number in numbers
]

print(result)
```

Output:

```text
['Odd', 'Even', 'Odd', 'Even', 'Odd']
```

### 5. Dictionary Comprehensions

Dictionary comprehensions create dictionaries using key-value pairs.

**Syntax:**

```python
new_dict = {
    key_expression: value_expression
    for item in iterable
}
```

**Example:**

```python
numbers = [1, 2, 3, 4]

squares = {
    number: number ** 2
    for number in numbers
}

print(squares)
```

Output:

```text
{1: 1, 2: 4, 3: 9, 4: 16}
```

Here, each number is the key and its square is the value.

### 6. Dictionary Comprehensions with Conditions

We can filter dictionary elements using conditions.

**Example:**

```python
students = {
    "Aman": 85,
    "Riya": 45,
    "Rahul": 90,
    "Neha": 55
}

passed = {
    name: marks
    for name, marks in students.items()
    if marks >= 60
}

print(passed)
```

Output:

```text
{'Aman': 85, 'Rahul': 90}
```

Only students scoring at least 60 are included.

### 7. Set Comprehensions

Set comprehensions create sets containing unique elements.

**Syntax:**

```python
new_set = {expression for item in iterable}
```

**Example:**

```python
numbers = [1, 2, 2, 3, 3, 4]

squares = {
    number ** 2
    for number in numbers
}

print(squares)
```

Possible output:

```text
{16, 1, 4, 9}
```

Duplicate values are automatically removed.

### 8. Set Comprehensions with Conditions

**Example:**

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

odd_squares = {
    number ** 2
    for number in numbers
    if number % 2 != 0
}

print(odd_squares)
```

Possible output:

```text
{1, 9, 25, 49}
```

### 9. Nested Comprehensions

Nested comprehensions contain multiple for clauses.

They are useful for processing nested collections.

**Example:**

```python
matrix = [
    [1, 2],
    [3, 4],
    [5, 6]
]

flattened = [
    number
    for row in matrix
    for number in row
]

print(flattened)
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

### 10. Types of Comprehensions

| Type | Collection Created | Brackets |
|---|---|---|
| List comprehension | List | `[ ]` |
| Dictionary comprehension | Dictionary | `{ }` with key-value pairs |
| Set comprehension | Set | `{ }` |
| Generator expression | Generator | `( )` |

## Key concepts

1. Comprehension: A short way of creating collections.
2. Iterable: An object that can be iterated over.
3. Expression: The value calculated for each element.
4. Filtering: Selecting elements using conditions.
5. List comprehension: Creates a list.
6. Dictionary comprehension: Creates key-value pairs.
7. Set comprehension: Creates unique elements.
8. Nested comprehension: Uses multiple loops.
9. Conditional expression: Uses if-else to choose a value.
10. Generator expression: Produces values lazily.

## Examples

### Example 1: Create cubes of numbers

```python
numbers = [1, 2, 3, 4, 5]

cubes = [number ** 3 for number in numbers]

print(cubes)
```

Output:

```text
[1, 8, 27, 64, 125]
```

### Example 2: Filter names starting with A

```python
names = ["Aman", "Riya", "Ankit", "Neha"]

result = [
    name for name in names
    if name.startswith("A")
]

print(result)
```

Output:

```text
['Aman', 'Ankit']
```

### Example 3: Create a dictionary of word lengths

```python
words = ["Python", "Java", "C++"]

lengths = {
    word: len(word)
    for word in words
}

print(lengths)
```

Output:

```text
{'Python': 6, 'Java': 4, 'C++': 3}
```

### Example 4: Generate coordinate pairs

```python
x_values = [1, 2]
y_values = [10, 20]

pairs = [
    (x, y)
    for x in x_values
    for y in y_values
]

print(pairs)
```

Output:

```text
[(1, 10), (1, 20), (2, 10), (2, 20)]
```

### Example 5: Convert Celsius to Fahrenheit

```python
celsius = [0, 10, 20, 30]

fahrenheit = [
    (temperature * 9 / 5) + 32
    for temperature in celsius
]

print(fahrenheit)
```

Output:

```text
[32.0, 50.0, 68.0, 86.0]
```

## Common mistakes

1. Using incorrect brackets for different comprehensions.
2. Forgetting the expression before the for clause.
3. Confusing filtering conditions with if-else expressions.
4. Forgetting the key-value structure in dictionary comprehensions.
5. Expecting sets to preserve order.
6. Expecting sets to contain duplicate elements.
7. Writing overly complicated nested comprehensions.
8. Using incorrect variable names.
9. Assuming a comprehension modifies the original collection.
10. Using comprehensions when normal loops would be easier to understand.

## Quick summary

- Comprehensions provide a concise way to create collections.
- List comprehensions use square brackets.
- Dictionary comprehensions use key-value pairs.
- Set comprehensions store unique elements.
- Conditions can filter elements.
- If-else expressions can transform elements.
- Nested comprehensions can process nested collections.
- Generator expressions produce values lazily.
- Normal loops are often clearer for complicated logic.

## Practice

### Beginner Level

1. Create a list of squares from 1 to 10.
2. Create a list containing only even numbers from a given list.
3. Find the length of every word in a list.
4. Create a set of unique vowels from a string.

### Intermediate Level

5. Replace even numbers with "Even" and odd numbers with "Odd".
6. Create a dictionary mapping student names to marks.
7. Filter students who scored at least 60.
8. Create a set containing unique squares of numbers.

### Advanced Level

9. Flatten a nested list using a list comprehension.
10. Generate all possible pairs from two lists.
11. Convert a normal for loop into a list comprehension.
12. Create a dictionary containing each word and its length.

### Practice Solutions

**Solution 1:**

```python
squares = [number ** 2 for number in range(1, 11)]
print(squares)
```

Output:

```text
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

**Solution 2:**

```python
numbers = [3, 8, 12, 5, 7, 10]

even_numbers = [
    number for number in numbers
    if number % 2 == 0
]

print(even_numbers)
```

Output:

```text
[8, 12, 10]
```

**Solution 5:**

```python
numbers = [1, 2, 3, 4]

result = [
    "Even" if number % 2 == 0 else "Odd"
    for number in numbers
]

print(result)
```

Output:

```text
['Odd', 'Even', 'Odd', 'Even']
```

**Solution 6:**

```python
names = ["Aman", "Riya", "Neha"]
marks = [85, 90, 78]

students = {
    name: mark
    for name, mark in zip(names, marks)
}

print(students)
```

Output:

```text
{'Aman': 85, 'Riya': 90, 'Neha': 78}
```

**Solution 9:**

```python
nested = [[1, 2], [3, 4], [5, 6]]

flat = [
    item
    for row in nested
    for item in row
]

print(flat)
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

## Learning resources

- **PDF:** [Open the supplied PDF](https://drive.google.com/file/d/1Udv1KJmycivTJ0TLl-kyLKp-Ak-rpTEc/view?usp=drive_link)
- **YouTube:** Temporary testing link. Replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc
