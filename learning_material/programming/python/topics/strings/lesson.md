
# String Manipulation and Formatting

**Course:** Python  
**Topic ID:** `strings`

## Learning objectives

After completing this topic, learners should be able to:

- Understand what strings are in Python.
- Create strings using single, double, and triple quotes.
- Understand string indexing and slicing.
- Access individual characters from a string.
- Perform string concatenation and repetition.
- Understand that strings are immutable.
- Use built-in string methods to modify and analyze text.
- Remove unwanted spaces using string methods.
- Search for characters and substrings.
- Replace, split, and join strings.
- Understand escape characters and special characters.
- Format strings using different formatting techniques.
- Use f-strings, `format()`, and formatted string literals.
- Validate strings using built-in methods.
- Write programs to reverse strings, count characters, and check palindromes.
- Apply string manipulation to real-world text-processing problems.

## Explanation

### 1. What is a String in Python?

A string is a sequence of characters enclosed within quotation marks.

Strings are used to store and process text, such as:

- Names
- Addresses
- Email IDs
- Messages
- Passwords
- Sentences
- Website URLs

In Python, strings are represented using the `str` data type.

**Example:**

```python
name = "Riya"
message = 'Welcome to Python'
city = "Bhopal"

print(name)
print(message)
print(city)
```

Output:

```text
Riya
Welcome to Python
Bhopal
```

Here, `name`, `message`, and `city` are string variables.

### 2. Creating Strings in Python

Python supports three common ways to create strings.

**A. Single Quotes**

```python
name = 'Riya'
print(name)
```

Output:

```text
Riya
```

**B. Double Quotes**

```python
name = "Riya"
print(name)
```

Output:

```text
Riya
```

Both single and double quotes can be used to create ordinary strings.

**C. Triple Quotes**

Triple quotes are used for multiline strings and documentation strings.

```python
message = """Welcome to Python.
Python is easy to learn.
Python is widely used."""

print(message)
```

Output:

```text
Welcome to Python.
Python is easy to learn.
Python is widely used.
```

Triple single quotes can also be used:

```python
message = '''This is
a multiline
string.'''

print(message)
```

### 3. Checking the Data Type of a String

We can use the `type()` function to identify the data type of a variable.

```python
name = "Riya"

print(type(name))
```

Output:

```text
<class 'str'>
```

The `str` data type represents strings in Python.

### 4. String Indexing

Indexing means accessing an individual character from a string using its position.

Python supports:

1. Positive indexing
2. Negative indexing

**A. Positive Indexing**

Positive indexing starts from 0, moving from left to right.

Example:

```python
word = "PYTHON"

print(word[0])
print(word[1])
print(word[2])
```

Output:

```text
P
Y
T
```

Index positions:

| Character | P | Y | T | H | O | N |
|---|---|---|---|---|---|---|
| Positive index | 0 | 1 | 2 | 3 | 4 | 5 |

**B. Negative Indexing**

Negative indexing starts from -1, moving from right to left.

```python
word = "PYTHON"

print(word[-1])
print(word[-2])
print(word[-3])
```

Output:

```text
N
O
H
```

Index positions:

| Character | P | Y | T | H | O | N |
|---|---|---|---|---|---|---|
| Negative index | -6 | -5 | -4 | -3 | -2 | -1 |

**Important:** Accessing an index outside the valid range raises an `IndexError`.

### 5. String Slicing

Slicing is used to extract a portion of a string.

**Syntax:**

```python
string[start:stop:step]
```

Where:

- `start`: Starting index, included.
- `stop`: Ending index, excluded.
- `step`: Number of positions to move between selected characters.

**Example 1: Basic Slicing**

```python
word = "PYTHON"

print(word[0:3])
```

Output:

```text
PYT
```

Characters from index 0 up to, but not including, index 3 are selected.

**Example 2: Omitting the Start Index**

```python
word = "PYTHON"

print(word[:3])
```

Output:

```text
PYT
```

The default starting index is 0.

**Example 3: Omitting the Stop Index**

```python
word = "PYTHON"

print(word[2:])
```

Output:

```text
THON
```

The slice continues to the end of the string.

**Example 4: Negative Slicing**

```python
word = "PYTHON"

print(word[-4:-1])
```

Output:

```text
THO
```

**Example 5: Using Step**

```python
word = "PYTHON"

print(word[::2])
```

Output:

```text
PTO
```

Every second character is selected.

**Example 6: Reverse a String Using Slicing**

```python
word = "PYTHON"

print(word[::-1])
```

Output:

```text
NOHTYP
```

A step of `-1` moves backward through the string.

### 6. String Concatenation

Concatenation means joining two or more strings together.

The `+` operator is used for concatenation.

**Example:**

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

We can also concatenate multiple strings.

```python
a = "Python"
b = " is"
c = " powerful"

result = a + b + c

print(result)
```

Output:

```text
Python is powerful
```

**Important:** The `+` operator concatenates strings, but it does not automatically convert numbers into strings.

Incorrect:

```python
age = 20

print("Age: " + age)
```

This raises a `TypeError`.

Correct:

```python
age = 20

print("Age: " + str(age))
```

Output:

```text
Age: 20
```

### 7. String Repetition

The `*` operator repeats a string a specified number of times.

**Example:**

```python
word = "Python "

print(word * 3)
```

Output:

```text
Python Python Python
```

Another example:

```python
print("*" * 5)
```

Output:

```text
*****
```

### 8. Strings Are Immutable

Strings in Python are immutable.

This means that once a string is created, its individual characters cannot be changed directly.

**Incorrect Example:**

```python
word = "Python"

word[0] = "J"
```

This raises a `TypeError`.

**Correct Example:**

Create a new string instead.

```python
word = "Python"

new_word = "J" + word[1:]

print(new_word)
```

Output:

```text
Jython
```

The original string remains unchanged.

**Important points:**

- Strings cannot be modified character by character.
- String methods generally return new strings rather than changing the original.
- You can assign a new string to the same variable name.

### 9. Finding the Length of a String

The `len()` function returns the total number of characters in a string.

Spaces and punctuation are also counted.

**Example:**

```python
word = "Python"

print(len(word))
```

Output:

```text
6
```

Another example:

```python
message = "Hello World"

print(len(message))
```

Output:

```text
11
```

The space between the words is counted as one character.

## 10. Important String Methods

Python provides many built-in string methods to process text.

### A. upper()

Converts all alphabetic characters to uppercase.

```python
text = "hello python"

print(text.upper())
```

Output:

```text
HELLO PYTHON
```

### B. lower()

Converts all alphabetic characters to lowercase.

```python
text = "HELLO PYTHON"

print(text.lower())
```

Output:

```text
hello python
```

### C. capitalize()

Converts the first character to uppercase and the remaining characters to lowercase.

```python
text = "hello PYTHON"

print(text.capitalize())
```

Output:

```text
Hello python
```

### D. title()

Converts the first character of each word to uppercase according to Python's title-casing rules.

```python
text = "welcome to python programming"

print(text.title())
```

Output:

```text
Welcome To Python Programming
```

### E. swapcase()

Converts uppercase characters to lowercase and lowercase characters to uppercase.

```python
text = "Hello PYTHON"

print(text.swapcase())
```

Output:

```text
hELLO python
```

### F. strip()

Removes leading and trailing whitespace.

```python
text = "   Hello Python   "

print(text.strip())
```

Output:

```text
Hello Python
```

### G. lstrip()

Removes whitespace from the left side.

```python
text = "   Hello"

print(text.lstrip())
```

Output:

```text
Hello
```

### H. rstrip()

Removes whitespace from the right side.

```python
text = "Hello   "

print(text.rstrip())
```

Output:

```text
Hello
```

### I. replace()

Replaces occurrences of one substring with another.

**Syntax:**

```python
string.replace(old, new, count)
```

The `count` argument is optional and limits the number of replacements.

```python
text = "I like Java"

result = text.replace("Java", "Python")

print(result)
```

Output:

```text
I like Python
```

Example with count:

```python
text = "apple apple apple"

print(text.replace("apple", "mango", 2))
```

Output:

```text
mango mango apple
```

### J. find()

Returns the lowest index where the specified substring is found.

If the substring is not found, it returns `-1`.

```python
text = "Hello Python"

print(text.find("Python"))
print(text.find("Java"))
```

Output:

```text
6
-1
```

### K. index()

Returns the lowest index where the specified substring is found.

If the substring is not found, it raises a `ValueError`.

```python
text = "Hello Python"

print(text.index("Python"))
```

Output:

```text
6
```

**Difference between find() and index():**

| find() | index() |
|---|---|
| Returns the index when found | Returns the index when found |
| Returns -1 when not found | Raises ValueError when not found |
| Useful when absence is expected | Useful when absence should be treated as an error |

### L. count()

Counts how many times a substring occurs.

```python
text = "banana"

print(text.count("a"))
print(text.count("an"))
```

Output:

```text
3
2
```

### M. startswith()

Checks whether a string starts with a specified prefix.

```python
text = "Python Programming"

print(text.startswith("Python"))
print(text.startswith("Java"))
```

Output:

```text
True
False
```

### N. endswith()

Checks whether a string ends with a specified suffix.

```python
text = "report.pdf"

print(text.endswith(".pdf"))
print(text.endswith(".txt"))
```

Output:

```text
True
False
```

## 11. Splitting and Joining Strings

### A. split()

The `split()` method divides a string into a list of substrings.

**Syntax:**

```python
string.split(separator, maxsplit)
```

The separator and maximum number of splits are optional.

**Example 1: Splitting by Spaces**

```python
text = "Python is easy"

result = text.split()

print(result)
```

Output:

```text
['Python', 'is', 'easy']
```

**Example 2: Splitting by Commas**

```python
text = "apple,banana,mango"

result = text.split(",")

print(result)
```

Output:

```text
['apple', 'banana', 'mango']
```

**Example 3: Using maxsplit**

```python
text = "Python is easy to learn"

result = text.split(" ", 2)

print(result)
```

Output:

```text
['Python', 'is', 'easy to learn']
```

### B. join()

The `join()` method combines elements of an iterable of strings into a single string.

The string on which `join()` is called acts as the separator.

**Example 1: Joining with Spaces**

```python
words = ["Python", "is", "easy"]

result = " ".join(words)

print(result)
```

Output:

```text
Python is easy
```

**Example 2: Joining with Hyphens**

```python
words = ["2026", "11", "22"]

result = "-".join(words)

print(result)
```

Output:

```text
2026-11-22
```

**Example 3: Joining with Commas**

```python
fruits = ["apple", "banana", "mango"]

result = ", ".join(fruits)

print(result)
```

Output:

```text
apple, banana, mango
```

**Important:** All elements passed to `join()` must be strings.

### Difference Between split() and join()

| split() | join() |
|---|---|
| Divides a string into parts | Combines strings into one string |
| Returns a list | Returns a string |
| Example: `"a b".split()` | Example: `" ".join(["a", "b"])` |

## 12. Escape Characters

Escape characters are special sequences beginning with a backslash (`\`).

They are used to represent special characters inside strings.

Common escape characters:

| Escape Character | Meaning |
|---|---|
| `\n` | New line |
| `\t` | Horizontal tab |
| `\\` | Backslash |
| `\'` | Single quotation mark |
| `\"` | Double quotation mark |
| `\r` | Carriage return |
| `\b` | Backspace |

**Example 1: New Line**

```python
print("Hello\nPython")
```

Output:

```text
Hello
Python
```

**Example 2: Tab**

```python
print("Name\tAge")
print("Riya\t20")
```

Output:

```text
Name    Age
Riya    20
```

**Example 3: Quotation Marks**

```python
print("She said, \"Hello!\"")
```

Output:

```text
She said, "Hello!"
```

**Example 4: Backslash**

```python
print("C:\\Users\\HP")
```

Output:

```text
C:\Users\HP
```

## 13. Raw Strings

A raw string treats backslashes as ordinary characters rather than interpreting most backslash escape sequences.

Raw strings are useful for Windows paths and regular expression patterns.

They are created by placing `r` before the opening quotation mark.

**Example:**

```python
path = r"C:\Users\HP\Documents"

print(path)
```

Output:

```text
C:\Users\HP\Documents
```

**Important:** A raw string cannot end with an odd number of consecutive backslashes because the final backslash would escape the closing quotation mark.

## 14. String Formatting

String formatting allows us to insert variable values into a string.

Python provides several methods:

1. Using the `%` operator.
2. Using the `format()` method.
3. Using f-strings.

### A. Formatting Using the % Operator

This is an older string formatting technique.

Common format specifiers:

| Specifier | Meaning |
|---|---|
| `%s` | String |
| `%d` | Integer |
| `%f` | Floating-point number |
| `%.2f` | Floating-point number with two decimal places |

**Example:**

```python
name = "Riya"
age = 20

print("My name is %s and I am %d years old." % (name, age))
```

Output:

```text
My name is Riya and I am 20 years old.
```

Example with decimal formatting:

```python
price = 99.5678

print("Price: %.2f" % price)
```

Output:

```text
Price: 99.57
```

### B. Formatting Using format()

The `format()` method inserts values into placeholders.

**Example 1:**

```python
name = "Riya"
age = 20

message = "My name is {} and I am {} years old.".format(name, age)

print(message)
```

Output:

```text
My name is Riya and I am 20 years old.
```

**Example 2: Using Positional Indexes**

```python
message = "My name is {0} and I am {1} years old."

print(message.format("Riya", 20))
```

Output:

```text
My name is Riya and I am 20 years old.
```

**Example 3: Using Named Placeholders**

```python
message = "Name: {name}, Age: {age}"

print(message.format(name="Riya", age=20))
```

Output:

```text
Name: Riya, Age: 20
```

**Example 4: Formatting Decimal Values**

```python
price = 99.5678

print("Price: {:.2f}".format(price))
```

Output:

```text
Price: 99.57
```

### C. f-Strings

F-strings are formatted string literals introduced in Python 3.6.

They allow expressions and variables to be inserted directly inside curly braces.

Place the letter `f` before the opening quotation mark.

**Example 1: Basic f-String**

```python
name = "Riya"
age = 20

print(f"My name is {name} and I am {age} years old.")
```

Output:

```text
My name is Riya and I am 20 years old.
```

**Example 2: Expressions Inside f-Strings**

```python
a = 10
b = 20

print(f"Sum: {a + b}")
```

Output:

```text
Sum: 30
```

**Example 3: Decimal Formatting**

```python
price = 99.5678

print(f"Price: {price:.2f}")
```

Output:

```text
Price: 99.57
```

**Example 4: Percentage Formatting**

```python
score = 0.875

print(f"Percentage: {score:.1%}")
```

Output:

```text
Percentage: 87.5%
```

**Example 5: Alignment and Width**

```python
name = "Riya"

print(f"|{name:<10}|")
print(f"|{name:>10}|")
print(f"|{name:^10}|")
```

Output:

```text
|Riya      |
|      Riya|
|   Riya   |
```

Here:

- `<` aligns text to the left.
- `>` aligns text to the right.
- `^` centers text.
- `10` specifies the field width.

### Difference Between String Formatting Methods

| Method | Example | Description |
|---|---|---|
| `%` formatting | `"%s" % name` | Older formatting method |
| `format()` | `"{}".format(name)` | Uses placeholders |
| f-string | `f"{name}"` | Inserts expressions directly |

F-strings are generally preferred for clear and readable formatting in modern Python.

## 15. Checking String Content

Python provides methods that check the content of strings and return Boolean values (`True` or `False`).

### A. isalpha()

Returns `True` if all characters are alphabetic and the string is non-empty.

```python
text = "Python"

print(text.isalpha())
```

Output:

```text
True
```

### B. isdigit()

Returns `True` if all characters are digits and the string is non-empty.

```python
text = "12345"

print(text.isdigit())
```

Output:

```text
True
```

### C. isalnum()

Returns `True` if all characters are alphanumeric and the string is non-empty.

```python
text = "Python123"

print(text.isalnum())
```

Output:

```text
True
```

### D. isspace()

Returns `True` if all characters are whitespace and the string is non-empty.

```python
text = "   "

print(text.isspace())
```

Output:

```text
True
```

### E. islower()

Checks whether all cased alphabetic characters are lowercase.

```python
text = "python"

print(text.islower())
```

Output:

```text
True
```

### F. isupper()

Checks whether all cased alphabetic characters are uppercase.

```python
text = "PYTHON"

print(text.isupper())
```

Output:

```text
True
```

### G. istitle()

Checks whether the string follows title-case rules.

```python
text = "Hello Python"

print(text.istitle())
```

Output:

```text
True
```

**Important:** Many of these methods return `False` for an empty string because they require at least one character.

## 16. String Comparison

Strings can be compared using comparison operators.

Common operators:

- `==` checks equality.
- `!=` checks inequality.
- `<` checks lexicographical ordering.
- `>` checks lexicographical ordering.

**Example:**

```python
a = "Python"
b = "Python"
c = "Java"

print(a == b)
print(a == c)
print(a != c)
```

Output:

```text
True
False
True
```

String comparisons are case-sensitive.

```python
print("python" == "Python")
```

Output:

```text
False
```

For case-insensitive comparison, convert both strings to the same case.

```python
a = "Python"
b = "PYTHON"

print(a.lower() == b.lower())
```

Output:

```text
True
```

## 17. Iterating Through Strings

A string is an iterable sequence of characters.

We can use a `for` loop to process its characters one by one.

**Example:**

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

**Example: Display Characters with Indexes**

```python
word = "Python"

for index, character in enumerate(word):
    print(index, character)
```

Output:

```text
0 P
1 y
2 t
3 h
4 o
5 n
```

## 18. Important Practical String Programs

### Example 1: Reverse a String

```python
text = "Python"

reverse = text[::-1]

print("Reversed:", reverse)
```

Output:

```text
Reversed: nohtyP
```

### Example 2: Count Vowels

```python
text = "Hello Python"

count = 0

for character in text.lower():
    if character in "aeiou":
        count += 1

print("Vowels:", count)
```

Output:

```text
Vowels: 3
```

### Example 3: Count Consonants

```python
text = "Hello Python"

count = 0

for character in text.lower():
    if character.isalpha() and character not in "aeiou":
        count += 1

print("Consonants:", count)
```

Output:

```text
Consonants: 7
```

### Example 4: Count Words

```python
text = "Python is easy to learn"

words = text.split()

print("Number of words:", len(words))
```

Output:

```text
Number of words: 5
```

### Example 5: Check Palindrome String

A palindrome is a string that reads the same forward and backward.

```python
text = "madam"

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not a palindrome")
```

Output:

```text
Palindrome
```

For case-insensitive checking:

```python
text = "Madam"

cleaned = text.lower()

if cleaned == cleaned[::-1]:
    print("Palindrome")
else:
    print("Not a palindrome")
```

Output:

```text
Palindrome
```

### Example 6: Count Character Frequency

```python
text = "banana"

for character in set(text):
    print(character, ":", text.count(character))
```

Output order may vary:

```text
b : 1
a : 3
n : 2
```

### Example 7: Remove Spaces

```python
text = "Python is easy"

result = text.replace(" ", "")

print(result)
```

Output:

```text
Pythoniseasy
```

### Example 8: Replace Vowels with *

```python
text = "education"

result = ""

for character in text:
    if character.lower() in "aeiou":
        result += "*"
    else:
        result += character

print(result)
```

Output:

```text
*d*c*t**n
```

### Example 9: Find the Longest Word

```python
sentence = "Python is a powerful programming language"

words = sentence.split()

longest = ""

for word in words:
    if len(word) > len(longest):
        longest = word

print("Longest word:", longest)
```

Output:

```text
Longest word: programming
```

### Example 10: Check Whether a String Contains Only Digits

```python
text = "12345"

if text.isdigit():
    print("Only digits")
else:
    print("Contains other characters")
```

Output:

```text
Only digits
```

## Key concepts

- **String:** A sequence of characters represented using the `str` data type.
- **Indexing:** Accessing an individual character by its position.
- **Positive indexing:** Indexing from left to right, starting at 0.
- **Negative indexing:** Indexing from right to left, starting at -1.
- **Slicing:** Extracting a portion of a string.
- **Concatenation:** Joining strings using the `+` operator.
- **Repetition:** Repeating strings using the `*` operator.
- **Immutability:** Strings cannot be modified character by character.
- **len():** Returns the number of characters.
- **upper():** Converts alphabetic characters to uppercase.
- **lower():** Converts alphabetic characters to lowercase.
- **strip():** Removes leading and trailing whitespace.
- **replace():** Replaces occurrences of a substring.
- **find():** Searches for a substring and returns -1 when absent.
- **split():** Divides a string into a list.
- **join():** Combines an iterable of strings into one string.
- **Escape characters:** Special sequences such as `\n` and `\t`.
- **Raw string:** A string literal that treats backslashes literally for most escape sequences.
- **String formatting:** Inserts values into a string.
- **f-string:** A modern way to format strings using expressions inside curly braces.
- **isalpha():** Checks whether all characters are alphabetic.
- **isdigit():** Checks whether all characters are digits.
- **isalnum():** Checks whether all characters are alphanumeric.

## Common mistakes

1. **Forgetting that indexing starts from zero**

   Incorrect:

   ```python
   word = "Python"
   print(word[6])
   ```

   This raises an `IndexError`.

   Correct:

   ```python
   word = "Python"
   print(word[5])
   ```

   Output:

   ```text
   n
   ```

2. **Using an invalid index**

   An index must be within the valid range of the string.

3. **Confusing slicing with indexing**

   - `text[0]` accesses one character.
   - `text[0:3]` extracts a portion of the string.

4. **Forgetting that the stop index is excluded**

   ```python
   text = "Python"
   print(text[0:3])
   ```

   Output:

   ```text
   Pyt
   ```

5. **Trying to modify an individual character**

   Strings are immutable.

   Create a new string instead of assigning to an indexed character.

6. **Concatenating a string and an integer directly**

   Incorrect:

   ```python
   age = 20
   print("Age: " + age)
   ```

   Correct:

   ```python
   age = 20
   print("Age: " + str(age))
   ```

   An f-string is another convenient solution:

   ```python
   print(f"Age: {age}")
   ```

7. **Confusing upper() and lower()**

   - `upper()` converts letters to uppercase.
   - `lower()` converts letters to lowercase.

8. **Forgetting that string methods return new strings**

   Incorrect:

   ```python
   text = "hello"
   text.upper()

   print(text)
   ```

   Output:

   ```text
   hello
   ```

   Correct:

   ```python
   text = "hello"
   text = text.upper()

   print(text)
   ```

   Output:

   ```text
   HELLO
   ```

9. **Confusing find() and index()**

   - `find()` returns `-1` when the substring is absent.
   - `index()` raises `ValueError` when the substring is absent.

10. **Using join() with non-string elements**

    Incorrect:

    ```python
    numbers = [1, 2, 3]
    print("-".join(numbers))
    ```

    Correct:

    ```python
    numbers = [1, 2, 3]

    result = "-".join(str(num) for num in numbers)

    print(result)
    ```

    Output:

    ```text
    1-2-3
    ```

11. **Confusing split() and join()**

    - `split()` converts a string into a list.
    - `join()` combines strings into a single string.

12. **Ignoring case sensitivity**

    `"Python"` and `"python"` are different strings when compared directly.

13. **Forgetting spaces in concatenation**

    Use `" "` when a space is required between joined words.

14. **Misunderstanding strip()**

    `strip()` removes leading and trailing whitespace, not all spaces inside the string.

15. **Using an incorrect f-string**

    Incorrect:

    ```python
    name = "Riya"
    print("Hello {name}")
    ```

    Correct:

    ```python
    name = "Riya"
    print(f"Hello {name}")
    ```

## Quick summary

- A string is a sequence of characters.
- Strings can use single, double, or triple quotes.
- Python uses the `str` data type for strings.
- Positive indexing starts from 0.
- Negative indexing starts from -1.
- Slicing extracts part of a string.
- The `+` operator joins strings.
- The `*` operator repeats strings.
- Strings are immutable.
- `len()` returns the length of a string.
- `upper()`, `lower()`, `capitalize()`, and `title()` change letter casing.
- `strip()`, `lstrip()`, and `rstrip()` remove surrounding whitespace.
- `replace()` replaces substrings.
- `find()` and `index()` search for substrings.
- `split()` divides a string into a list.
- `join()` combines strings.
- Escape characters represent special characters.
- Raw strings are useful for paths and regular expressions.
- `%`, `format()`, and f-strings are string formatting techniques.
- Methods such as `isalpha()`, `isdigit()`, and `isalnum()` validate string content.
- Strings can be processed using loops and conditional statements.

## Practice

### Beginner Level

**1. Create a String**

Create a string containing your name and print it.

**2. Find String Length**

Write a program to calculate the length of a string using `len()`.

**3. Convert to Uppercase**

Convert a given string into uppercase.

**4. Convert to Lowercase**

Convert a given string into lowercase.

**5. Access Characters**

Print the first, third, and last characters of a string.

**6. String Slicing**

Extract the first five characters of a string.

**7. Concatenation**

Join your first name and last name with a space.

**8. Repetition**

Print the word "Python" five times using the repetition operator.

### Intermediate Level

**9. Reverse a String**

Write a program to reverse a string without using a loop.

**10. Count Vowels**

Count the total number of vowels in a string.

**11. Count Consonants**

Count the total number of consonants in a string.

**12. Count Words**

Count the total number of words in a sentence.

**13. Replace a Word**

Replace every occurrence of "Java" with "Python" in a sentence.

**14. Remove Spaces**

Remove all ordinary space characters from a string.

**15. Character Frequency**

Count how many times a given character occurs in a string.

**16. Check Palindrome**

Check whether a given string is a palindrome.

**17. String Formatting**

Create a sentence using an f-string containing a person's name, age, and city.

### Advanced Level

**18. Find the Longest Word**

Find the longest word in a sentence.

**19. Character Frequency Dictionary**

Create a dictionary containing each character and its frequency.

**20. Remove Duplicate Characters**

Remove repeated characters from a string while preserving the first occurrence of each character.

**21. Anagram Checker**

Check whether two strings contain the same characters with the same frequencies, ignoring case.

**22. Reverse Each Word**

Reverse each word in a sentence while keeping the word order unchanged.

**23. Count Uppercase and Lowercase Characters**

Count uppercase letters, lowercase letters, digits, and special characters separately.

**24. Email Validation**

Write a basic program to check whether an email string contains an `@` symbol and a domain portion.

**25. Word Frequency Counter**

Count how many times each word occurs in a sentence.

### Sample Solutions

**Solution 1: Create a String**

```python
name = "Riya"

print(name)
```

Output:

```text
Riya
```

**Solution 2: Find String Length**

```python
text = "Python Programming"

print("Length:", len(text))
```

Output:

```text
Length: 18
```

**Solution 3: Convert to Uppercase**

```python
text = "hello python"

print(text.upper())
```

Output:

```text
HELLO PYTHON
```

**Solution 4: Convert to Lowercase**

```python
text = "HELLO PYTHON"

print(text.lower())
```

Output:

```text
hello python
```

**Solution 5: Access Characters**

```python
text = "Python"

print("First:", text[0])
print("Third:", text[2])
print("Last:", text[-1])
```

Output:

```text
First: P
Third: t
Last: n
```

**Solution 6: String Slicing**

```python
text = "Programming"

print(text[:5])
```

Output:

```text
Progr
```

**Solution 7: Concatenation**

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

**Solution 8: Repetition**

```python
word = "Python "

print(word * 5)
```

Output:

```text
Python Python Python Python Python
```

**Solution 9: Reverse a String**

```python
text = "Python"

reverse = text[::-1]

print(reverse)
```

Output:

```text
nohtyP
```

**Solution 10: Count Vowels**

```python
text = "Hello Python"

count = 0

for ch in text.lower():
    if ch in "aeiou":
        count += 1

print("Vowels:", count)
```

Output:

```text
Vowels: 3
```

**Solution 11: Count Consonants**

```python
text = "Hello Python"

count = 0

for ch in text.lower():
    if ch.isalpha() and ch not in "aeiou":
        count += 1

print("Consonants:", count)
```

Output:

```text
Consonants: 7
```

**Solution 12: Count Words**

```python
sentence = "Python is easy to learn"

words = sentence.split()

print("Words:", len(words))
```

Output:

```text
Words: 5
```

**Solution 13: Replace a Word**

```python
text = "I am learning Java"

result = text.replace("Java", "Python")

print(result)
```

Output:

```text
I am learning Python
```

**Solution 14: Remove Spaces**

```python
text = "Python is easy"

result = text.replace(" ", "")

print(result)
```

Output:

```text
Pythoniseasy
```

**Solution 15: Character Frequency**

```python
text = "programming"
character = "m"

count = text.count(character)

print("Frequency:", count)
```

Output:

```text
Frequency: 2
```

**Solution 16: Check Palindrome**

```python
text = "madam"

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not a palindrome")
```

Output:

```text
Palindrome
```

**Solution 17: String Formatting**

```python
name = "Riya"
age = 20
city = "Bhopal"

print(f"My name is {name}, I am {age} years old, and I live in {city}.")
```

Output:

```text
My name is Riya, I am 20 years old, and I live in Bhopal.
```

**Solution 18: Find the Longest Word**

```python
sentence = "Python is a powerful programming language"

words = sentence.split()

longest = ""

for word in words:
    if len(word) > len(longest):
        longest = word

print("Longest word:", longest)
```

Output:

```text
Longest word: programming
```

**Solution 19: Character Frequency Dictionary**

```python
text = "banana"

frequency = {}

for ch in text:
    if ch in frequency:
        frequency[ch] += 1
    else:
        frequency[ch] = 1

print(frequency)
```

Output:

```text
{'b': 1, 'a': 3, 'n': 2}
```

**Solution 20: Remove Duplicate Characters**

```python
text = "programming"

result = ""

for ch in text:
    if ch not in result:
        result += ch

print(result)
```

Output:

```text
progamin
```

**Solution 21: Anagram Checker**

An anagram is formed when two strings contain the same characters with the same frequencies, possibly in a different order.

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

This simple version includes spaces and punctuation in the comparison. They would need to be removed if the requirement is to ignore them.

**Solution 22: Reverse Each Word**

```python
sentence = "Python is easy"

words = sentence.split()

result = []

for word in words:
    result.append(word[::-1])

print(" ".join(result))
```

Output:

```text
nohtyP si ysae
```

**Solution 23: Count Different Character Types**

```python
text = "Python123@"

uppercase = 0
lowercase = 0
digits = 0
special = 0

for ch in text:
    if ch.isupper():
        uppercase += 1
    elif ch.islower():
        lowercase += 1
    elif ch.isdigit():
        digits += 1
    else:
        special += 1

print("Uppercase:", uppercase)
print("Lowercase:", lowercase)
print("Digits:", digits)
print("Special characters:", special)
```

Output:

```text
Uppercase: 1
Lowercase: 5
Digits: 3
Special characters: 1
```

**Solution 24: Basic Email Validation**

```python
email = input("Enter email: ").strip()

if email.count("@") == 1:
    username, domain = email.split("@")

    if username and "." in domain and not domain.startswith(".") and not domain.endswith("."):
        print("Basic email format looks valid")
    else:
        print("Invalid email format")
else:
    print("Invalid email format")
```

This is a basic educational check, not complete email validation.

**Solution 25: Word Frequency Counter**

```python
sentence = "python is easy and python is powerful"

words = sentence.lower().split()

frequency = {}

for word in words:
    frequency[word] = frequency.get(word, 0) + 1

print(frequency)
```

Output:

```text
{'python': 2, 'is': 2, 'easy': 1, 'and': 1, 'powerful': 1}
```

## Learning resources

- **PDF:** [String Manipulation and Formatting](https://drive.google.com/file/d/1VtUH0XovMZCfTReRlObwH1e1mrg-7v4R/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)