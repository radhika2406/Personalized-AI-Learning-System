
# Iterators and Generators

**Course:** Python
**Topic ID:** `iterators_and_generators`

## Learning objectives

After completing this topic, learners should be able to:

- Understand iteration and iterables in Python.
- Explain the difference between iterables and iterators.
- Understand the `iter()` and `next()` functions.
- Create custom iterators using classes.
- Understand the `__iter__()` and `__next__()` methods.
- Use the `StopIteration` exception.
- Understand generators and how they work.
- Create generators using functions and the `yield` keyword.
- Understand the difference between `yield` and `return`.
- Use generator expressions.
- Understand lazy evaluation and memory efficiency.
- Use `send()`, `close()` and `throw()` with generators.
- Understand generator pipelines.
- Apply iterators and generators to real-world programming problems.

## Explanation

### 1. What is Iteration?

Iteration means repeating a process or accessing elements one by one.

In Python, iteration is commonly performed using loops such as `for` and `while`.

**Example:**

```python
numbers = [10, 20, 30, 40]

for number in numbers:
    print(number)
```

Output:

```text
10
20
30
40
```

Here, the loop accesses each element of the list one at a time.

### 2. What is an Iterable?

An iterable is an object that can return its elements one at a time.

Examples of iterables include:

- Lists
- Tuples
- Strings
- Dictionaries
- Sets
- Files
- Ranges

An iterable can be used in a `for` loop.

**Example:**

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Output:

```text
10
20
30
```

The list is an iterable because Python can access its elements one by one.

### 3. What is an Iterator?

An iterator is an object that represents a stream of values and produces one value at a time.

An iterator maintains its current position while iterating.

Python iterators implement two important methods:

- `__iter__()`
- `__next__()`

An iterator can be created from an iterable using the `iter()` function.

**Example:**

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
10
20
30
```

Here:

- `numbers` is an iterable.
- `iter(numbers)` creates an iterator.
- `next()` retrieves the next available value.

### 4. Difference Between Iterable and Iterator

| Iterable | Iterator |
|---|---|
| Can provide an iterator | Produces values one at a time |
| Can be used in a `for` loop | Can be used in a `for` loop |
| May be traversed again by creating a new iterator | Maintains its current iteration state |
| Example: list, tuple, string | Example: object returned by `iter()` |

**Example:**

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(type(numbers))
print(type(iterator))
```

Output:

```text
<class 'list'>
<class 'list_iterator'>
```

### 5. The iter() Function

The `iter()` function returns an iterator from an iterable object.

**Syntax:**

```python
iterator = iter(iterable)
```

**Example:**

```python
fruits = ["Apple", "Banana", "Mango"]

fruit_iterator = iter(fruits)

print(next(fruit_iterator))
print(next(fruit_iterator))
print(next(fruit_iterator))
```

Output:

```text
Apple
Banana
Mango
```

### 6. The next() Function

The `next()` function retrieves the next item from an iterator.

**Syntax:**

```python
next(iterator)
```

**Example:**

```python
numbers = [1, 2, 3]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
1
2
3
```

Calling `next()` again after all values have been consumed raises `StopIteration`.

```python
numbers = [1, 2]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
1
2
StopIteration
```

### 7. The StopIteration Exception

`StopIteration` is a built-in exception that indicates that an iterator has no more values to provide.

Python uses it internally to stop iteration.

**Example:**

```python
numbers = [10, 20]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))

try:
    print(next(iterator))

except StopIteration:
    print("No more elements.")
```

Output:

```text
10
20
No more elements.
```

The `for` loop automatically handles `StopIteration`, so programmers usually do not need to handle it manually when using normal loops.

### 8. How a for Loop Works Internally

A `for` loop uses the iterator protocol internally.

Consider:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Conceptually, Python performs operations similar to:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

while True:
    try:
        number = next(iterator)
        print(number)

    except StopIteration:
        break
```

Output:

```text
10
20
30
```

This shows that `for` loops use `iter()` and `next()` internally.

### 9. Creating a Custom Iterator

Python allows programmers to create their own iterator classes.

A custom iterator generally implements:

1. `__iter__()` – Returns the iterator object.
2. `__next__()` – Returns the next value.

**Example:**

```python
class Count:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration

counter = Count(5)

for number in counter:
    print(number)
```

Output:

```text
1
2
3
4
5
```

Explanation:

- `Count` is a custom iterator class.
- `__iter__()` returns the iterator itself.
- `__next__()` returns the next number.
- `StopIteration` signals that iteration has finished.

### 10. Creating a Custom Iterator for Even Numbers

**Example:**

```python
class EvenNumbers:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 2
            return value

        raise StopIteration

numbers = EvenNumbers(10)

for number in numbers:
    print(number)
```

Output:

```text
0
2
4
6
8
10
```

### 11. What is a Generator?

A generator is a special type of iterator that produces values one at a time.

Generators are created using:

- Generator functions with `yield`.
- Generator expressions.

Unlike a normal function that returns a value and finishes, a generator function can pause its execution and continue later.

Generators are useful when working with large amounts of data because they do not need to create and store the entire result in memory at once.

### 12. Creating a Generator Function

A generator function looks like a normal function but uses the `yield` keyword.

**Syntax:**

```python
def generator_name():
    yield value
```

**Example:**

```python
def numbers():
    yield 10
    yield 20
    yield 30

result = numbers()

print(next(result))
print(next(result))
print(next(result))
```

Output:

```text
10
20
30
```

Here:

- `numbers()` returns a generator object.
- Each `next()` call resumes the function.
- `yield` produces a value and pauses execution.

### 13. Understanding the yield Keyword

The `yield` keyword returns a value from a generator function while preserving its execution state.

When the generator is requested again, execution continues from where it paused.

**Example:**

```python
def demo():
    print("First step")
    yield 10

    print("Second step")
    yield 20

    print("Third step")
    yield 30

result = demo()

print(next(result))
print(next(result))
print(next(result))
```

Output:

```text
First step
10
Second step
20
Third step
30
```

This demonstrates that the generator pauses at each `yield` statement and resumes when the next value is requested.

### 14. Difference Between return and yield

| return | yield |
|---|---|
| Returns a value and ends the function call | Produces a value and pauses generator execution |
| Does not preserve the function's execution state for another call | Preserves the generator's execution state |
| A normal function uses return | A generator function uses yield |
| Function execution finishes at return | Generator execution can continue after yield |

**Example using return:**

```python
def get_number():
    return 10

result = get_number()

print(result)
```

Output:

```text
10
```

**Example using yield:**

```python
def get_numbers():
    yield 10
    yield 20

result = get_numbers()

print(next(result))
print(next(result))
```

Output:

```text
10
20
```

### 15. Using a Generator with a for Loop

Generators can be used directly in `for` loops.

**Example:**

```python
def count():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5

for number in count():
    print(number)
```

Output:

```text
1
2
3
4
5
```

The `for` loop automatically requests values until the generator is exhausted.

### 16. Generator Expressions

A generator expression is a concise way to create a generator.

It looks similar to a list comprehension but uses parentheses instead of square brackets.

**Syntax:**

```python
generator = (expression for item in iterable)
```

**Example:**

```python
squares = (number ** 2 for number in range(1, 6))

for square in squares:
    print(square)
```

Output:

```text
1
4
9
16
25
```

**Difference between List Comprehension and Generator Expression:**

```python
# List comprehension
numbers_list = [x * x for x in range(5)]

# Generator expression
numbers_generator = (x * x for x in range(5))

print(numbers_list)
print(numbers_generator)
```

The list comprehension creates a list containing all results.

The generator expression creates a generator that produces results when requested.

### 17. Lazy Evaluation

Lazy evaluation means values are calculated only when they are needed.

Generators use lazy evaluation.

**Example:**

```python
def numbers():
    print("Generating 1")
    yield 1

    print("Generating 2")
    yield 2

    print("Generating 3")
    yield 3

result = numbers()

print("Generator created.")

print(next(result))
print(next(result))
```

Output:

```text
Generator created.
Generating 1
1
Generating 2
2
```

Notice that the generator does not calculate all values immediately.

It produces values only when requested.

### 18. Memory Efficiency of Generators

Generators can save memory when processing large sequences.

**List example:**

```python
numbers = [x for x in range(1000000)]

print(numbers[0])
```

This creates a list containing all one million values.

**Generator example:**

```python
numbers = (x for x in range(1000000))

print(next(numbers))
```

Output:

```text
0
```

The generator produces values as needed instead of storing the entire sequence.

Generators are particularly useful for:

- Processing large files.
- Reading large datasets.
- Streaming information.
- Processing records one at a time.
- Working with potentially large sequences.

### 19. Generator Functions with Conditions

Generators can contain conditions and loops.

**Example: Generate even numbers**

```python
def even_numbers(limit):
    for number in range(limit + 1):
        if number % 2 == 0:
            yield number

for number in even_numbers(10):
    print(number)
```

Output:

```text
0
2
4
6
8
10
```

### 20. The send() Method

The `send()` method allows a value to be sent into a paused generator.

The sent value becomes the result of the suspended `yield` expression.

A generator must be started before sending a non-`None` value. This is commonly done using `next()`.

**Example:**

```python
def receive():
    value = yield "Ready"
    print("Received:", value)

generator = receive()

print(next(generator))

generator.send("Hello")
```

Output:

```text
Ready
Received: Hello
```

Explanation:

- The first `next()` starts the generator.
- The generator pauses at `yield "Ready"`.
- `send("Hello")` sends a value into the paused generator.
- The value is assigned to `value`.

### 21. The close() Method

The `close()` method tells a generator to stop.

It raises `GeneratorExit` inside the generator at its current suspension point.

**Example:**

```python
def numbers():
    try:
        yield 10
        yield 20
        yield 30

    finally:
        print("Generator closed.")

generator = numbers()

print(next(generator))

generator.close()
```

Output:

```text
10
Generator closed.
```

The generator does not produce the remaining values after being closed.

### 22. The throw() Method

The `throw()` method injects an exception into a generator at its current suspension point.

The generator can handle the exception using `try` and `except`.

**Example:**

```python
def generator():
    try:
        yield 10

    except ValueError:
        yield "ValueError handled"

result = generator()

print(next(result))
print(result.throw(ValueError))
```

Output:

```text
10
ValueError handled
```

### 23. Returning a Value from a Generator

A generator can use `return` to signal that it has finished.

The return value becomes the value associated with `StopIteration`.

**Example:**

```python
def numbers():
    yield 10
    yield 20
    return "Finished"

generator = numbers()

print(next(generator))
print(next(generator))

try:
    next(generator)

except StopIteration as error:
    print(error.value)
```

Output:

```text
10
20
Finished
```

### 24. yield from

The `yield from` expression delegates yielding values to another iterable or generator.

It is useful when combining multiple generators.

**Example:**

```python
def first():
    yield 1
    yield 2

def second():
    yield 3
    yield 4

def combined():
    yield from first()
    yield from second()

for number in combined():
    print(number)
```

Output:

```text
1
2
3
4
```

### 25. Generator Pipelines

A generator pipeline is a sequence of generators in which the output of one generator is used as the input of another.

This is useful for processing large amounts of data in stages.

**Example:**

```python
def numbers():
    for number in range(1, 11):
        yield number

def even_numbers(values):
    for number in values:
        if number % 2 == 0:
            yield number

def squares(values):
    for number in values:
        yield number ** 2

result = squares(even_numbers(numbers()))

for value in result:
    print(value)
```

Output:

```text
4
16
36
64
100
```

The processing happens in stages:

1. Generate numbers from 1 to 10.
2. Select even numbers.
3. Calculate their squares.

### 26. Iterators vs Generators

| Iterator | Generator |
|---|---|
| Any object implementing the iterator protocol | A special kind of iterator |
| Can be created using classes | Can be created using `yield` or generator expressions |
| Requires `__iter__()` and `__next__()` for a custom iterator | Python manages the iterator protocol automatically |
| May require more code to implement | Usually requires less code |
| Can maintain custom iteration logic | Automatically preserves function execution state |

Every generator is an iterator, but not every iterator is a generator.

### 27. When Should You Use Iterators and Generators?

Use iterators when:

- You need to define custom iteration behavior.
- You are building an object that produces values one at a time.
- You want to control how a collection is traversed.

Use generators when:

- You want to produce values lazily.
- You need to process large data.
- You want to avoid creating large intermediate lists.
- You want simple code for sequential data generation.
- You are building data-processing pipelines.

## Key concepts

1. **Iteration:** Accessing elements one by one.
2. **Iterable:** An object capable of returning an iterator.
3. **Iterator:** An object that produces values one at a time.
4. **iter():** Creates an iterator from an iterable.
5. **next():** Retrieves the next value from an iterator.
6. **StopIteration:** Signals that no more iterator values are available.
7. **Iterator protocol:** The protocol based on `__iter__()` and `__next__()`.
8. **Custom iterator:** A programmer-defined iterator class.
9. **Generator:** A special type of iterator.
10. **yield:** Produces a value and pauses generator execution.
11. **Generator expression:** A compact way to create a generator.
12. **Lazy evaluation:** Calculates values only when requested.
13. **send():** Sends a value into a paused generator.
14. **close():** Stops a generator.
15. **throw():** Injects an exception into a generator.
16. **yield from:** Delegates values to another iterable or generator.
17. **Generator pipeline:** A sequence of generators used for staged processing.
18. **Memory efficiency:** Generators can avoid storing all generated values at once.

## Examples

### Example 1: Create an iterator from a list

```python
fruits = ["Apple", "Banana", "Mango"]

iterator = iter(fruits)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
Apple
Banana
Mango
```

### Example 2: Create a custom iterator

```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration

counter = Counter(3)

for number in counter:
    print(number)
```

Output:

```text
1
2
3
```

### Example 3: Generate squares

```python
def squares(limit):
    for number in range(1, limit + 1):
        yield number ** 2

for value in squares(5):
    print(value)
```

Output:

```text
1
4
9
16
25
```

### Example 4: Generate Fibonacci numbers

```python
def fibonacci(limit):
    a, b = 0, 1

    for _ in range(limit):
        yield a
        a, b = b, a + b

for number in fibonacci(7):
    print(number)
```

Output:

```text
0
1
1
2
3
5
8
```

### Example 5: Generator expression

```python
numbers = (x * 2 for x in range(1, 6))

for number in numbers:
    print(number)
```

Output:

```text
2
4
6
8
10
```

### Example 6: Read a file line by line

```python
def read_lines(filename):
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()

for line in read_lines("data.txt"):
    print(line)
```

This generator reads and produces one line at a time instead of loading the entire file into memory.

### Example 7: Filter even numbers

```python
def even_numbers(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number

values = [1, 2, 3, 4, 5, 6]

for number in even_numbers(values):
    print(number)
```

Output:

```text
2
4
6
```

### Example 8: Use yield from

```python
def group_one():
    yield 10
    yield 20

def group_two():
    yield 30
    yield 40

def all_numbers():
    yield from group_one()
    yield from group_two()

print(list(all_numbers()))
```

Output:

```text
[10, 20, 30, 40]
```

### Example 9: Generator pipeline

```python
def numbers():
    for i in range(1, 6):
        yield i

def multiply_by_two(values):
    for value in values:
        yield value * 2

def add_five(values):
    for value in values:
        yield value + 5

result = add_five(multiply_by_two(numbers()))

print(list(result))
```

Output:

```text
[7, 9, 11, 13, 15]
```

### Example 10: Generate an infinite sequence

```python
def infinite_counter():
    number = 1

    while True:
        yield number
        number += 1

counter = infinite_counter()

for _ in range(5):
    print(next(counter))
```

Output:

```text
1
2
3
4
5
```

The generator is infinite, but the loop requests only five values.

## Common mistakes

1. **Confusing an iterable with an iterator**
   - A list is an iterable.
   - `iter(list)` creates an iterator.

2. **Calling next() on a non-iterator**
   - Convert the iterable using `iter()` before calling `next()`.

3. **Forgetting StopIteration**
   - An iterator raises `StopIteration` when no more values are available.
   - Use a `for` loop or handle the exception when calling `next()` manually.

4. **Trying to reuse an exhausted iterator**
   - Iterators are generally consumed as values are requested.
   - Create a new iterator if you need to iterate again.

5. **Forgetting __iter__() in a custom iterator**
   - A custom iterator should implement the iterator protocol.

6. **Forgetting __next__()**
   - A custom iterator must define how the next value is produced.

7. **Not raising StopIteration**
   - A custom iterator should raise `StopIteration` when its values are exhausted.

8. **Confusing yield with return**
   - `return` ends the function call.
   - `yield` pauses a generator and allows it to resume later.

9. **Expecting a generator to execute immediately**
   - Calling a generator function creates a generator object.
   - Its body starts executing when values are requested.

10. **Trying to print a generator object expecting all values**
    - Use `next()`, a `for` loop or `list()` to retrieve generated values.

11. **Using a generator more than once without recreating it**
    - Once exhausted, a generator does not restart automatically.
    - Call the generator function again to obtain a new generator.

12. **Sending a value before starting a generator**
    - Start a generator using `next()` or `send(None)` before sending a non-`None` value.

13. **Creating an infinite generator without controlling consumption**
    - Use a stopping condition or limit the number of requested values.

14. **Assuming generators always make a program faster**
    - Generators can reduce memory usage, but performance depends on the task and implementation.

15. **Using list() on a very large or infinite generator**
    - `list()` consumes all generated values and may require too much memory.
    - Process values incrementally instead.

## Quick summary

- Iteration means accessing elements one at a time.
- An iterable can return an iterator.
- An iterator produces values one by one.
- `iter()` creates an iterator.
- `next()` retrieves the next value.
- `StopIteration` indicates that iteration has finished.
- Custom iterators implement `__iter__()` and `__next__()`.
- Generators are special types of iterators.
- Generator functions use `yield`.
- `yield` pauses execution and preserves generator state.
- `return` ends a function call.
- Generator expressions use parentheses.
- Lazy evaluation produces values only when needed.
- Generators can improve memory efficiency for large sequences.
- `send()` sends values into a paused generator.
- `close()` stops a generator.
- `throw()` injects an exception into a generator.
- `yield from` delegates values to another iterable or generator.
- Generator pipelines combine multiple processing stages.
- Every generator is an iterator, but not every iterator is a generator.

## Practice

### Beginner Level

1. Create a list and convert it into an iterator.
2. Use `next()` to retrieve three values from an iterator.
3. Write a program that handles `StopIteration`.
4. Create a generator that produces numbers from 1 to 5.
5. Write a generator that produces even numbers.
6. Create a generator that produces squares of numbers.

### Intermediate Level

7. Create a custom iterator class that counts from 1 to 10.
8. Create an iterator that produces odd numbers.
9. Write a generator that produces Fibonacci numbers.
10. Create a generator expression for cubes of numbers.
11. Read a text file line by line using a generator.
12. Create a generator that filters positive numbers from a list.
13. Demonstrate the difference between `return` and `yield`.
14. Create a generator that uses `yield from`.

### Advanced Level

15. Create a generator that produces an infinite sequence of numbers.
16. Implement a generator that accepts values using `send()`.
17. Create a generator that handles an exception using `throw()`.
18. Demonstrate how `close()` works.
19. Build a generator pipeline that filters and transforms numbers.
20. Create a custom iterator for traversing a collection.
21. Build a program that processes a large file line by line.
22. Compare the memory behavior of a list comprehension and a generator expression.

### Practice Solutions

**Solution 1: Create an iterator**

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
10
20
30
```

**Solution 2: Handle StopIteration**

```python
numbers = [1, 2]

iterator = iter(numbers)

try:
    while True:
        print(next(iterator))

except StopIteration:
    print("Iteration completed.")
```

Output:

```text
1
2
Iteration completed.
```

**Solution 3: Create a simple generator**

```python
def numbers():
    yield 1
    yield 2
    yield 3

for number in numbers():
    print(number)
```

Output:

```text
1
2
3
```

**Solution 4: Generate even numbers**

```python
def even_numbers(limit):
    for number in range(0, limit + 1, 2):
        yield number

print(list(even_numbers(10)))
```

Output:

```text
[0, 2, 4, 6, 8, 10]
```

**Solution 5: Generate Fibonacci numbers**

```python
def fibonacci(limit):
    a, b = 0, 1

    for _ in range(limit):
        yield a
        a, b = b, a + b

print(list(fibonacci(6)))
```

Output:

```text
[0, 1, 1, 2, 3, 5]
```

**Solution 6: Generator expression**

```python
squares = (x ** 2 for x in range(1, 6))

print(list(squares))
```

Output:

```text
[1, 4, 9, 16, 25]
```

**Solution 7: Custom iterator**

```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration

counter = Counter(5)

print(list(counter))
```

Output:

```text
[1, 2, 3, 4, 5]
```

**Solution 8: Use send()**

```python
def receiver():
    value = yield "Waiting"
    yield f"Received {value}"

generator = receiver()

print(next(generator))
print(generator.send("Hello"))
```

Output:

```text
Waiting
Received Hello
```

**Solution 9: Use yield from**

```python
def first():
    yield 1
    yield 2

def second():
    yield 3
    yield 4

def combined():
    yield from first()
    yield from second()

print(list(combined()))
```

Output:

```text
[1, 2, 3, 4]
```

**Solution 10: Generator pipeline**

```python
def numbers():
    for number in range(1, 11):
        yield number

def filter_even(values):
    for number in values:
        if number % 2 == 0:
            yield number

def square(values):
    for number in values:
        yield number ** 2

result = square(filter_even(numbers()))

print(list(result))
```

Output:

```text
[4, 16, 36, 64, 100]
```

## Learning resources

- **PDF:** [Iterators and Generators PDF](https://drive.google.com/file/d/1du-a8Meb1JXXm5Gh4ffRTwIu-00dJv18/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc