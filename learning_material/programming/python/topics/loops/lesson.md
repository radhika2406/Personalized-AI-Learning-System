
# Loops and Iteration

**Course:** Python
**Topic ID:** `loops`

## Learning objectives

After completing this topic, learners should be able to:

- Understand the meaning and purpose of loops in Python.
- Explain why loops are used in programming.
- Understand the difference between iteration and repetition.
- Use `for` loops to iterate over sequences.
- Use `while` loops when repetition depends on a condition.
- Understand and use the `range()` function.
- Iterate through strings, lists, tuples, and dictionaries.
- Use `break`, `continue`, and `pass` statements.
- Understand nested loops and their execution.
- Use loops with conditional statements.
- Create multiplication tables and number patterns.
- Avoid infinite loops and common iteration errors.
- Solve basic programming problems using loops.

## Explanation

### 1. What is a Loop in Python?

A loop is a programming structure that allows us to execute a block of code repeatedly.

Instead of writing the same statement many times, we can use a loop to repeat the operation automatically.

**Example without a loop:**

```python
print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")
```

Output:

```text
Hello
Hello
Hello
Hello
Hello
```

**Example using a loop:**

```python
for i in range(5):
    print("Hello")
```

Output:

```text
Hello
Hello
Hello
Hello
Hello
```

Both programs produce the same output, but the second program is shorter and easier to maintain.

### 2. Why Do We Use Loops?

Loops are useful when we need to:

- Repeat a task multiple times.
- Process multiple elements in a list.
- Display multiplication tables.
- Calculate sums and averages.
- Search for values in a collection.
- Process student marks.
- Generate number and star patterns.
- Automate repetitive operations.

**Real-life example:**

Suppose a teacher wants to display the marks of 50 students.

Without loops, the teacher would need to write 50 print statements.

With a loop, the teacher can store the marks in a list and display all of them using just a few lines of code.

### 3. Types of Loops in Python

Python mainly provides two types of loops:

1. `for` loop
2. `while` loop

| For Loop | While Loop |
|---|---|
| Used to iterate over a sequence or iterable | Used to repeat code while a condition is true |
| Common when the items or iteration range are known | Common when repetition depends on a condition |
| Automatically moves to the next item | Usually requires updating a variable or condition |
| Iterates over items directly | Checks the condition before each iteration |

## 4. For Loop

A `for` loop is used to iterate over a sequence or any iterable object, such as a list, tuple, string, dictionary, or range.

**Syntax:**

```python
for variable in sequence:
    # Statements to execute
```

Here:
- `for` is the loop keyword.
- `variable` stores the current item.
- `sequence` is the iterable.
- The indented statements execute for each item.

**Example 1: Printing Numbers**

```python
for i in [1, 2, 3, 4, 5]:
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

**Example 2: Printing Names**

```python
names = ["Riya", "Aman", "Rahul", "Priya"]

for name in names:
    print(name)
```

Output:

```text
Riya
Aman
Rahul
Priya
```

**Example 3: Iterating Through a String**

```python
word = "Python"

for character in word:
    print(character)
```

Output:

```text
P
y
t
h
o
n
```

The loop processes one character at a time.

## 5. The range() Function

The `range()` function generates a sequence of integers. It is commonly used with `for` loops.

**Syntax:**

```python
range(start, stop, step)
```

Where:
- `start`: Starting number (included).
- `stop`: Ending boundary (excluded).
- `step`: Difference between consecutive numbers.

The default values are:
- `start = 0`
- `step = 1`

**Example 1: range(stop)**

```python
for i in range(5):
    print(i)
```

Output:

```text
0
1
2
3
4
```

The sequence starts from 0 and stops before 5.

**Example 2: range(start, stop)**

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

**Example 3: range(start, stop, step)**

```python
for i in range(2, 11, 2):
    print(i)
```

Output:

```text
2
4
6
8
10
```

The step value is 2, so the numbers increase by 2.

**Example 4: Counting Backward**

```python
for i in range(5, 0, -1):
    print(i)
```

Output:

```text
5
4
3
2
1
```

A negative step is used to count backward.

**Important:** The stop value is excluded from the range.

## 6. While Loop

A `while` loop executes a block of code as long as its condition remains `True`.

It is useful when we do not know exactly how many repetitions are required in advance.

**Syntax:**

```python
while condition:
    # Statements
```

The loop:
1. Checks the condition.
2. Executes the code if the condition is `True`.
3. Checks the condition again.
4. Stops when the condition becomes `False`.

**Example 1: Printing Numbers**

```python
i = 1

while i <= 5:
    print(i)
    i += 1
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

- Initially, `i = 1`.
- The condition `i <= 5` is checked.
- The current value of `i` is printed.
- `i += 1` increases its value by 1.
- The process continues until `i` becomes 6.
- The condition becomes false and the loop stops.

**Example 2: Printing Even Numbers**

```python
i = 2

while i <= 10:
    print(i)
    i += 2
```

Output:

```text
2
4
6
8
10
```

**Example 3: Sum of First Five Natural Numbers**

```python
i = 1
total = 0

while i <= 5:
    total += i
    i += 1

print("Sum:", total)
```

Output:

```text
Sum: 15
```

## 7. Difference Between for and while Loops

| Feature | for Loop | while Loop |
|---|---|---|
| Main use | Iterating over an iterable | Repeating while a condition is true |
| Iteration control | Gets the next item automatically | Condition controls repetition |
| Counter update | Often automatic through `range()` | Usually manual |
| Common use | Lists, strings, ranges | Input validation, condition-based repetition |
| Risk of infinite loop | Usually lower for finite iterables | Higher if the condition never becomes false |

**Example using for:**

```python
for i in range(1, 6):
    print(i)
```

**Example using while:**

```python
i = 1

while i <= 5:
    print(i)
    i += 1
```

Both produce:

```text
1
2
3
4
5
```

## 8. Loop Control Statements

Python provides special statements to change the normal execution of loops.

The three important statements are:

1. `break`
2. `continue`
3. `pass`

### A. break Statement

The `break` statement immediately terminates the nearest enclosing loop.

**Example:**

```python
for i in range(1, 10):
    if i == 5:
        break

    print(i)
```

Output:

```text
1
2
3
4
```

When `i` becomes 5, the loop terminates.

**Practical Example: Searching for an Element**

```python
numbers = [10, 20, 30, 40, 50]

for num in numbers:
    if num == 30:
        print("Element found")
        break
```

Output:

```text
Element found
```

### B. continue Statement

The `continue` statement skips the remaining statements in the current iteration and moves to the next iteration.

**Example:**

```python
for i in range(1, 6):
    if i == 3:
        continue

    print(i)
```

Output:

```text
1
2
4
5
```

When `i` becomes 3, the print statement is skipped for that iteration.

**Practical Example: Printing Only Odd Numbers**

```python
for i in range(1, 11):
    if i % 2 == 0:
        continue

    print(i)
```

Output:

```text
1
3
5
7
9
```

### C. pass Statement

The `pass` statement does nothing. It acts as a placeholder when a statement is syntactically required but no action is needed yet.

**Example:**

```python
for i in range(5):
    if i == 3:
        pass

    print(i)
```

Output:

```text
0
1
2
3
4
```

The loop continues normally because `pass` does not stop or skip anything.

**Difference Between break, continue, and pass:**

| Statement | Meaning |
|---|---|
| break | Terminates the nearest enclosing loop |
| continue | Skips the rest of the current iteration |
| pass | Does nothing; acts as a placeholder |

## 9. Nested Loops

A nested loop is a loop placed inside another loop.

The inner loop executes completely for each iteration of the outer loop.

**Syntax:**

```python
for i in sequence:
    for j in sequence:
        # Statements
```

**Example 1: Nested for Loop**

```python
for i in range(1, 4):
    for j in range(1, 3):
        print(i, j)
```

Output:

```text
1 1
1 2
2 1
2 2
3 1
3 2
```

Explanation:

- The outer loop runs three times.
- For every outer iteration, the inner loop runs two times.
- Therefore, the print statement executes six times.

**Example 2: Multiplication Table from 1 to 3**

```python
for i in range(1, 4):
    for j in range(1, 6):
        print(i * j, end=" ")
    print()
```

Output:

```text
1 2 3 4 5
2 4 6 8 10
3 6 9 12 15
```

The `end=" "` argument prints values on the same line with spaces. The empty `print()` moves to the next line.

## 10. Looping Through Different Data Structures

Loops can iterate through different Python data structures.

**A. List**

```python
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)
```

**B. Tuple**

```python
numbers = (10, 20, 30)

for num in numbers:
    print(num)
```

**C. Set**

```python
numbers = {10, 20, 30}

for num in numbers:
    print(num)
```

Note: Sets are unordered collections, so do not depend on a particular iteration order.

**D. Dictionary**

```python
student = {
    "name": "Riya",
    "age": 20,
    "marks": 90
}

for key in student:
    print(key, student[key])
```

Output:

```text
name Riya
age 20
marks 90
```

**Using items():**

```python
student = {
    "name": "Riya",
    "age": 20,
    "marks": 90
}

for key, value in student.items():
    print(key, value)
```

**E. Using enumerate()**

The `enumerate()` function gives both the index and the value.

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

## 11. Using else with Loops

Python allows an `else` block with both `for` and `while` loops.

The `else` block executes when the loop finishes normally, including when a `while` condition becomes false.

It does not execute if the loop is terminated by a `break`.

**Example 1: for-else**

```python
for i in range(1, 4):
    print(i)
else:
    print("Loop completed")
```

Output:

```text
1
2
3
Loop completed
```

**Example 2: break with else**

```python
for i in range(1, 6):
    if i == 3:
        break

    print(i)
else:
    print("Loop completed")
```

Output:

```text
1
2
```

The `else` block does not execute because the loop ended using `break`.

**Practical Example: Searching for a Number**

```python
numbers = [10, 20, 30, 40]

target = 50

for num in numbers:
    if num == target:
        print("Number found")
        break
else:
    print("Number not found")
```

Output:

```text
Number not found
```

## 12. Infinite Loops

An infinite loop is a loop that continues running because its stopping condition never becomes false.

**Example:**

```python
i = 1

while i <= 5:
    print(i)
```

This loop never stops because the value of `i` is not updated.

**Correct Example:**

```python
i = 1

while i <= 5:
    print(i)
    i += 1
```

Output:

```text
1
2
3
4
5
```

Infinite loops can sometimes be intentional, such as in menu-driven applications, but they should include a suitable exit condition.

**Example: Menu Loop**

```python
while True:
    print("1. Start")
    print("2. Exit")

    choice = input("Enter choice: ")

    if choice == "2":
        print("Exiting...")
        break
```

The loop continues until the user selects option 2.

## 13. Using Loops with Conditional Statements

Loops and conditions are often used together to solve programming problems.

**Example 1: Print Even and Odd Numbers**

```python
for i in range(1, 11):
    if i % 2 == 0:
        print(i, "is Even")
    else:
        print(i, "is Odd")
```

**Example 2: Count Positive Numbers**

```python
numbers = [10, -5, 20, -2, 30, 0]

count = 0

for num in numbers:
    if num > 0:
        count += 1

print("Positive numbers:", count)
```

Output:

```text
Positive numbers: 3
```

**Example 3: Find the Largest Number Without max()**

```python
numbers = [10, 50, 20, 80, 30]

largest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num

print("Largest:", largest)
```

Output:

```text
Largest: 80
```

## 14. Pattern Printing Using Loops

Nested loops are commonly used to print patterns.

**Example 1: Square Star Pattern**

```python
for i in range(4):
    for j in range(4):
        print("*", end=" ")
    print()
```

Output:

```text
* * * *
* * * *
* * * *
* * * *
```

**Example 2: Right-Angled Triangle**

```python
for i in range(1, 6):
    for j in range(i):
        print("*", end=" ")
    print()
```

Output:

```text
*
* *
* * *
* * * *
* * * * *
```

**Example 3: Number Triangle**

```python
for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()
```

Output:

```text
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```

**Example 4: Inverted Triangle**

```python
for i in range(5, 0, -1):
    for j in range(i):
        print("*", end=" ")
    print()
```

Output:

```text
* * * * *
* * * *
* * *
* *
*
```

## 15. Important Loop Examples

### Example 1: Sum of First N Natural Numbers

```python
n = 5
total = 0

for i in range(1, n + 1):
    total += i

print("Sum:", total)
```

Output:

```text
Sum: 15
```

### Example 2: Multiplication Table

```python
n = 5

for i in range(1, 11):
    print(n, "x", i, "=", n * i)
```

Output:

```text
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50
```

### Example 3: Factorial of a Number

Factorial is the product of all positive integers from 1 to a given number.

For example:

5! = 5 × 4 × 3 × 2 × 1 = 120

```python
n = 5
factorial = 1

for i in range(1, n + 1):
    factorial *= i

print("Factorial:", factorial)
```

Output:

```text
Factorial: 120
```

### Example 4: Reverse a Number

```python
num = 1234
reverse = 0

while num > 0:
    digit = num % 10
    reverse = reverse * 10 + digit
    num //= 10

print("Reversed number:", reverse)
```

Output:

```text
Reversed number: 4321
```

### Example 5: Count Digits in a Number

```python
num = 12345
count = 0

while num > 0:
    count += 1
    num //= 10

print("Number of digits:", count)
```

Output:

```text
Number of digits: 5
```

For this example, the input is a positive integer. Special handling is needed for zero and negative numbers.

### Example 6: Check Whether a Number Is Prime

A prime number is greater than 1 and has exactly two positive divisors: 1 and itself.

```python
num = 17
is_prime = True

if num <= 1:
    is_prime = False
else:
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

if is_prime:
    print("Prime number")
else:
    print("Not a prime number")
```

Output:

```text
Prime number
```

### Example 7: Fibonacci Series

The Fibonacci series starts with 0 and 1. Each following number is the sum of the previous two numbers.

```python
n = 7

a = 0
b = 1

for i in range(n):
    print(a, end=" ")
    a, b = b, a + b
```

Output:

```text
0 1 1 2 3 5 8
```

### Example 8: Sum of Digits

```python
num = 1234
total = 0

while num > 0:
    digit = num % 10
    total += digit
    num //= 10

print("Sum of digits:", total)
```

Output:

```text
Sum of digits: 10
```

### Example 9: Display List Elements and Their Squares

```python
numbers = [1, 2, 3, 4, 5]

for num in numbers:
    print(num, "Square:", num ** 2)
```

Output:

```text
1 Square: 1
2 Square: 4
3 Square: 9
4 Square: 16
5 Square: 25
```

## Key concepts

- **Loop:** A programming structure used to repeat instructions.
- **Iteration:** One execution of a loop's body.
- **for loop:** Iterates over items in an iterable.
- **while loop:** Repeats while a condition is true.
- **range():** Generates a sequence of integers.
- **start:** Beginning value of a range; included.
- **stop:** Ending boundary of a range; excluded.
- **step:** Difference between consecutive values.
- **break:** Terminates the nearest enclosing loop.
- **continue:** Skips the rest of the current iteration.
- **pass:** Does nothing and acts as a placeholder.
- **Nested loop:** A loop inside another loop.
- **Infinite loop:** A loop that does not reach its stopping condition.
- **enumerate():** Provides both index and item during iteration.
- **Loop else:** Executes when the loop finishes normally without `break`.
- **end parameter:** Controls what `print()` places after printed content.
- **Indentation:** Defines the statements belonging to a loop.

## Common mistakes

1. **Forgetting indentation**

   Incorrect:

   ```python
   for i in range(5):
   print(i)
   ```

   Correct:

   ```python
   for i in range(5):
       print(i)
   ```

   Python uses indentation to identify the loop body.

2. **Forgetting that range() excludes the stop value**

   ```python
   for i in range(1, 5):
       print(i)
   ```

   Output:

   ```text
   1
   2
   3
   4
   ```

   To include 5, use `range(1, 6)`.

3. **Forgetting to update the while loop variable**

   If the condition never becomes false, the loop may run forever.

   Always update the relevant variable when required.

4. **Using the wrong comparison operator**

   Check whether you need `<`, `<=`, `>`, or `>=`.

5. **Confusing break and continue**

   - `break` exits the loop.
   - `continue` skips only the current iteration.

6. **Incorrectly using the step value**

   ```python
   range(10, 1, -1)
   ```

   A negative step is required to count backward.

7. **Modifying a collection while iterating over it**

   Removing elements directly during iteration may cause some elements to be skipped. Consider building a new collection instead.

8. **Using an incorrect nested loop structure**

   Remember that the inner loop completes its iterations for every outer-loop iteration.

9. **Expecting a loop else block to run after break**

   The `else` block does not execute when the loop terminates using `break`.

10. **Confusing assignment and comparison**

    Use `=` for assignment and `==` for equality comparison.

11. **Using an uninitialized variable**

    Initialize counters and totals before using them.

    ```python
    total = 0
    count = 0
    ```

12. **Forgetting to handle special inputs**

    For example, a factorial program should handle zero and negative values correctly.

## Quick summary

- Loops are used to repeat a block of code.
- Python mainly provides `for` and `while` loops.
- A `for` loop iterates over an iterable.
- A `while` loop repeats while its condition is true.
- `range()` generates a sequence of integers.
- The stop value in `range()` is excluded.
- `break` terminates a loop.
- `continue` skips the current iteration.
- `pass` acts as a placeholder.
- Nested loops contain one loop inside another.
- Loops can iterate over strings, lists, tuples, sets, and dictionaries.
- `enumerate()` provides indexes and values.
- A loop's `else` block executes when the loop finishes normally without `break`.
- An infinite loop occurs when the stopping condition is never reached.
- Loops and conditional statements can be combined to solve many programming problems.

## Practice

### Beginner Level

**1. Print Numbers**

Write a program to print numbers from 1 to 10 using a `for` loop.

**2. Print Even Numbers**

Write a program to print all even numbers between 1 and 50.

**3. Print Odd Numbers**

Write a program to print all odd numbers between 1 and 50.

**4. Multiplication Table**

Write a program to display the multiplication table of a number entered by the user.

**5. Sum of Natural Numbers**

Write a program to calculate the sum of the first N natural numbers.

### Intermediate Level

**6. Factorial**

Write a program to calculate the factorial of a number using a loop.

**7. Reverse a Number**

Write a program to reverse a given integer using a `while` loop.

**8. Count Digits**

Write a program to count the number of digits in an integer.

**9. Sum of Digits**

Write a program to calculate the sum of all digits of a number.

**10. Find the Largest Number**

Given a list of numbers, find the largest element without using `max()`.

**11. Count Vowels**

Write a program to count the vowels in a string using a loop.

**12. Search an Element**

Write a program to search for a particular number in a list. Stop searching when the element is found.

### Advanced Level

**13. Prime Number**

Write a program to check whether a number is prime using a loop.

**14. Fibonacci Series**

Write a program to display the first N Fibonacci numbers.

**15. Palindrome Number**

Write a program to check whether a number reads the same forward and backward.

**16. Armstrong Number**

Write a program to check whether a number is an Armstrong number.

Example:

```text
153 = 1³ + 5³ + 3³ = 153
```

**17. Star Pattern**

Print the following pattern using nested loops:

```text
*
* *
* * *
* * * *
* * * * *
```

**18. Number Pattern**

Print the following pattern:

```text
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```

**19. Find Common Elements**

Given two lists, use loops to find their common elements.

**20. Number Guessing Game**

Create a simple number guessing game where the user repeatedly enters a guess until the correct number is entered. Use a `while` loop.

### Sample Solutions

**Solution 1: Print Numbers from 1 to 10**

```python
for i in range(1, 11):
    print(i)
```

**Solution 2: Print Even Numbers**

```python
for i in range(2, 51, 2):
    print(i)
```

**Solution 3: Print Odd Numbers**

```python
for i in range(1, 51, 2):
    print(i)
```

**Solution 4: Multiplication Table**

```python
n = int(input("Enter a number: "))

for i in range(1, 11):
    print(n, "x", i, "=", n * i)
```

**Solution 5: Sum of Natural Numbers**

```python
n = int(input("Enter a number: "))

total = 0

for i in range(1, n + 1):
    total += i

print("Sum:", total)
```

**Solution 6: Factorial**

```python
n = int(input("Enter a number: "))

factorial = 1

if n < 0:
    print("Factorial is not defined for negative integers")
else:
    for i in range(1, n + 1):
        factorial *= i

    print("Factorial:", factorial)
```

**Solution 7: Reverse a Number**

```python
num = int(input("Enter a number: "))

reverse = 0

while num > 0:
    digit = num % 10
    reverse = reverse * 10 + digit
    num //= 10

print("Reverse:", reverse)
```

This version handles non-negative integers. For negative integers, handle the sign separately.

**Solution 8: Count Digits**

```python
num = abs(int(input("Enter a number: ")))

count = 0

if num == 0:
    count = 1
else:
    while num > 0:
        count += 1
        num //= 10

print("Number of digits:", count)
```

**Solution 9: Sum of Digits**

```python
num = abs(int(input("Enter a number: ")))

total = 0

while num > 0:
    digit = num % 10
    total += digit
    num //= 10

print("Sum of digits:", total)
```

**Solution 10: Find the Largest Number**

```python
numbers = [10, 50, 20, 80, 30]

largest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num

print("Largest number:", largest)
```

**Solution 11: Count Vowels**

```python
text = input("Enter a string: ")

count = 0

for ch in text.lower():
    if ch in "aeiou":
        count += 1

print("Number of vowels:", count)
```

**Solution 12: Search an Element**

```python
numbers = [10, 20, 30, 40, 50]

target = 30

for num in numbers:
    if num == target:
        print("Element found")
        break
else:
    print("Element not found")
```

**Solution 13: Prime Number**

```python
num = int(input("Enter a number: "))

is_prime = True

if num <= 1:
    is_prime = False
else:
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

if is_prime:
    print("Prime number")
else:
    print("Not a prime number")
```

**Solution 14: Fibonacci Series**

```python
n = int(input("Enter number of terms: "))

a = 0
b = 1

for i in range(n):
    print(a, end=" ")
    a, b = b, a + b
```

**Solution 15: Palindrome Number**

```python
num = int(input("Enter a number: "))

original = num
reverse = 0

if num < 0:
    print("Not a palindrome")
else:
    while num > 0:
        digit = num % 10
        reverse = reverse * 10 + digit
        num //= 10

    if original == reverse:
        print("Palindrome number")
    else:
        print("Not a palindrome")
```

**Solution 16: Armstrong Number**

```python
num = int(input("Enter a number: "))

if num < 0:
    print("Not an Armstrong number")
else:
    original = num
    digits = len(str(num))
    total = 0

    while num > 0:
        digit = num % 10
        total += digit ** digits
        num //= 10

    if total == original:
        print("Armstrong number")
    else:
        print("Not an Armstrong number")
```

**Solution 17: Star Pattern**

```python
for i in range(1, 6):
    for j in range(i):
        print("*", end=" ")
    print()
```

**Solution 18: Number Pattern**

```python
for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()
```

**Solution 19: Find Common Elements**

```python
a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]

common = []

for num in a:
    if num in b and num not in common:
        common.append(num)

print("Common elements:", common)
```

**Solution 20: Number Guessing Game**

```python
secret_number = 7

while True:
    guess = int(input("Guess the number: "))

    if guess == secret_number:
        print("Correct guess!")
        break
    elif guess < secret_number:
        print("Too low. Try again.")
    else:
        print("Too high. Try again.")
```

## Learning resources

- **PDF:** [Loops and Iteration](https://drive.google.com/file/d/1SgzNcTVXo-cArEyn3O_JRASqoO9ZKmGS/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)