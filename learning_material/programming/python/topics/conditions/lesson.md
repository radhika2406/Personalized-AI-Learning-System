
# Conditional Statements

**Course:** Python
**Topic ID:** `conditions`

## Learning objectives

After completing this topic, learners should be able to:

- Understand the concept of conditional statements in Python.
- Explain how decision-making works in programming.
- Use if, elif and else statements.
- Apply comparison and logical operators in conditions.
- Write nested if statements.
- Use shorthand conditional expressions.
- Combine multiple conditions using logical operators.
- Solve real-world problems using conditional statements.

## Explanation

### 1. What are Conditional Statements?

Conditional statements are used to make decisions in a program.

They allow Python to execute different blocks of code depending on whether a condition is True or False.

For example, a program can check whether a person is eligible to vote based on their age.

**Example:**

```python
age = 20

if age >= 18:
    print("You are eligible to vote")
```

Output:

```text
You are eligible to vote
```

Here, Python checks whether the age is greater than or equal to 18. Since the condition is True, the print statement executes.

### 2. The if Statement

The `if` statement executes a block of code only when its condition is True.

**Syntax:**

```python
if condition:
    statement
```

Important points:

- The condition must evaluate to True or False.
- A colon (`:`) is required after the condition.
- The code inside the if block must be indented.
- If the condition is False, the block is skipped.

**Example:**

```python
temperature = 35

if temperature > 30:
    print("It is a hot day")

print("Program completed")
```

Output:

```text
It is a hot day
Program completed
```

### 3. The if-else Statement

The `if-else` statement provides two possible paths.

- If the condition is True, the if block executes.
- If the condition is False, the else block executes.

**Syntax:**

```python
if condition:
    statement_if_true
else:
    statement_if_false
```

**Example:**

```python
number = 7

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")
```

Output:

```text
Odd number
```

The modulo operator (`%`) returns the remainder after division. An even number has a remainder of zero when divided by 2.

### 4. The if-elif-else Statement

The `elif` statement means "else if".

It is used when multiple conditions need to be checked.

Python checks the conditions from top to bottom. The first True condition executes, and the remaining conditions are skipped.

**Syntax:**

```python
if condition1:
    statement1
elif condition2:
    statement2
elif condition3:
    statement3
else:
    default_statement
```

**Example: grading system**

```python
marks = 85

if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 60:
    print("Grade C")
elif marks >= 40:
    print("Grade D")
else:
    print("Fail")
```

Output:

```text
Grade B
```

The conditions are checked in order. Since 85 is greater than or equal to 75, Grade B is printed.

### 5. Comparison Operators in Conditions

Comparison operators compare two values and return either True or False.

| Operator | Meaning | Example |
|---|---|---|
| `==` | Equal to | `5 == 5` |
| `!=` | Not equal to | `5 != 3` |
| `>` | Greater than | `10 > 5` |
| `<` | Less than | `3 < 8` |
| `>=` | Greater than or equal to | `5 >= 5` |
| `<=` | Less than or equal to | `4 <= 6` |

**Example:**

```python
age = 21

print(age >= 18)
print(age == 21)
print(age < 18)
```

Output:

```text
True
True
False
```

### 6. Logical Operators in Conditions

Logical operators combine multiple conditions.

Python provides three main logical operators.

#### A. AND Operator

The `and` operator returns True only when both conditions are True.

```python
age = 22
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")
else:
    print("Entry denied")
```

Output:

```text
Entry allowed
```

#### B. OR Operator

The `or` operator returns True when at least one condition is True.

```python
day = "Sunday"

if day == "Saturday" or day == "Sunday":
    print("It is a weekend")
else:
    print("It is a working day")
```

Output:

```text
It is a weekend
```

#### C. NOT Operator

The `not` operator reverses a Boolean value.

```python
is_raining = False

if not is_raining:
    print("You can go outside")
```

Output:

```text
You can go outside
```

### 7. Nested if Statements

A nested if statement means placing one if statement inside another if statement.

It is useful when a second decision depends on the first decision.

**Syntax:**

```python
if condition1:
    if condition2:
        statement
    else:
        statement
else:
    statement
```

**Example:**

```python
age = 20
has_license = True

if age >= 18:
    if has_license:
        print("You can drive")
    else:
        print("You need a driving license")
else:
    print("You are underage")
```

Output:

```text
You can drive
```

The program first checks the age. If the person is at least 18, it checks whether they have a driving license.

### 8. Short-Hand if Statement

Python allows a simple if statement to be written on one line.

**Example:**

```python
age = 20

if age >= 18: print("Adult")
```

Output:

```text
Adult
```

This is suitable only for simple statements. For longer logic, use normal indentation.

### 9. Ternary Conditional Expression

A ternary conditional expression is a short way to write an if-else expression.

**Syntax:**

```python
value_if_true if condition else value_if_false
```

**Example:**

```python
age = 17

result = "Adult" if age >= 18 else "Minor"

print(result)
```

Output:

```text
Minor
```

This expression selects one of two values depending on the condition.

### 10. The pass Statement

The `pass` statement is used when a statement is syntactically required but no action needs to be performed yet.

**Example:**

```python
age = 20

if age >= 18:
    pass
else:
    print("Underage")
```

The program does nothing inside the if block because it contains `pass`.

### 11. Truthy and Falsy Values

Python conditions can use values other than True and False.

Some values are considered False when evaluated in a condition. These are called falsy values.

Common falsy values:

- `False`
- `None`
- `0`
- `0.0`
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dictionary)
- `set()` (empty set)

Most other values are truthy.

**Example:**

```python
name = ""

if name:
    print("Name is provided")
else:
    print("Name is empty")
```

Output:

```text
Name is empty
```

### 12. Multiple Conditions and Operator Precedence

Python evaluates logical operators in this order:

1. `not`
2. `and`
3. `or`

Parentheses can be used to make conditions easier to understand.

**Example:**

```python
age = 25
has_id = True
is_member = False

if age >= 18 and (has_id or is_member):
    print("Access granted")
else:
    print("Access denied")
```

Output:

```text
Access granted
```

## Key concepts

1. **Conditional statement:** A statement that controls program execution based on a condition.
2. **if:** Executes code when a condition is True.
3. **else:** Executes code when the if condition is False.
4. **elif:** Checks additional conditions.
5. **Nested if:** An if statement inside another if statement.
6. **Comparison operators:** Compare values using operators such as `==`, `!=`, `>`, and `<`.
7. **Logical operators:** Combine conditions using `and`, `or`, and `not`.
8. **Ternary expression:** A compact if-else expression.
9. **Truthy values:** Values treated as True in conditions.
10. **Falsy values:** Values treated as False in conditions.
11. **pass:** A placeholder statement that performs no action.
12. **Indentation:** Defines which statements belong to a conditional block.

## Examples

### Example 1: Check whether a number is positive, negative or zero

```python
number = -5

if number > 0:
    print("Positive number")
elif number < 0:
    print("Negative number")
else:
    print("Zero")
```

Output:

```text
Negative number
```

### Example 2: Find the largest of two numbers

```python
a = 25
b = 40

if a > b:
    print("A is greater")
elif b > a:
    print("B is greater")
else:
    print("Both are equal")
```

Output:

```text
B is greater
```

### Example 3: Check voting eligibility

```python
age = 19

if age >= 18:
    print("Eligible to vote")
else:
    print("Not eligible to vote")
```

Output:

```text
Eligible to vote
```

### Example 4: Check leap year

```python
year = 2024

if year % 400 == 0:
    print("Leap year")
elif year % 100 == 0:
    print("Not a leap year")
elif year % 4 == 0:
    print("Leap year")
else:
    print("Not a leap year")
```

Output:

```text
Leap year
```

### Example 5: Simple login validation

```python
username = "admin"
password = "12345"

if username == "admin" and password == "12345":
    print("Login successful")
else:
    print("Invalid username or password")
```

Output:

```text
Login successful
```

### Example 6: Electricity bill category

```python
units = 250

if units <= 100:
    print("Low consumption")
elif units <= 300:
    print("Medium consumption")
else:
    print("High consumption")
```

Output:

```text
Medium consumption
```

## Common mistakes

1. **Forgetting the colon**

Incorrect:

```python
if age >= 18
    print("Adult")
```

Correct:

```python
if age >= 18:
    print("Adult")
```

2. **Incorrect indentation**

Incorrect:

```python
if age >= 18:
print("Adult")
```

Correct:

```python
if age >= 18:
    print("Adult")
```

3. **Using = instead of ==**

- `=` assigns a value.
- `==` compares two values.

Incorrect:

```python
if age = 18:
    print("Adult")
```

Correct:

```python
if age == 18:
    print("Age is 18")
```

4. **Incorrect condition order**

When using multiple conditions, more specific conditions may need to be checked first.

5. **Using multiple independent if statements unnecessarily**

Use `if-elif-else` when only one branch should execute.

6. **Forgetting the else block is optional**

An if statement does not always require an else statement.

7. **Incorrect use of logical operators**

Understand the difference between `and`, `or`, and `not`.

8. **Comparing incompatible data types**

For example, comparing a number directly with a string may cause a TypeError.

## Quick summary

- Conditional statements allow programs to make decisions.
- `if` executes code when a condition is True.
- `else` executes when the if condition is False.
- `elif` checks additional conditions.
- Nested if statements allow decisions inside decisions.
- Comparison operators compare values.
- Logical operators combine conditions.
- Ternary expressions provide a shorter if-else form.
- Python uses indentation to define conditional blocks.
- Truthy and falsy values can be used directly in conditions.
- The `pass` statement acts as a placeholder.

## Practice

### Beginner Level

1. Write a program to check whether a number is positive or negative.
2. Write a program to check whether a number is even or odd.
3. Check whether a person is eligible to vote.
4. Check whether a number is equal to zero.
5. Find the larger of two numbers.

### Intermediate Level

6. Write a program to find the largest of three numbers.
7. Create a grading system using if-elif-else.
8. Check whether a year is a leap year.
9. Check whether a character is a vowel or consonant.
10. Create a simple login validation program.

### Advanced Level

11. Create a calculator using conditional statements.
12. Check whether a triangle is valid using its three sides.
13. Create a discount calculator based on purchase amount.
14. Write a program to check whether a number is divisible by both 5 and 11.
15. Create a nested conditional program to check eligibility for a scholarship.

### Practice Solutions

**Solution 1: Positive or Negative**

```python
number = -10

if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")
```

Output:

```text
Negative
```

**Solution 2: Even or Odd**

```python
number = 12

if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

Output:

```text
Even
```

**Solution 3: Largest of Three Numbers**

```python
a = 10
b = 25
c = 15

if a >= b and a >= c:
    print("A is largest")
elif b >= a and b >= c:
    print("B is largest")
else:
    print("C is largest")
```

Output:

```text
B is largest
```

**Solution 4: Vowel or Consonant**

```python
character = "a"

if character.lower() in "aeiou":
    print("Vowel")
else:
    print("Consonant")
```

Output:

```text
Vowel
```

**Solution 5: Divisibility by 5 and 11**

```python
number = 55

if number % 5 == 0 and number % 11 == 0:
    print("Divisible by both 5 and 11")
else:
    print("Not divisible by both")
```

Output:

```text
Divisible by both 5 and 11
```

## Learning resources

- **PDF:** [Conditional Statements PDF](https://drive.google.com/file/d/1Wd8kTCajaucx5Mq9oSbkBM78cgWf3wrI/view?usp=drive_link)
- **YouTube:** Temporary testing link. Replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc
