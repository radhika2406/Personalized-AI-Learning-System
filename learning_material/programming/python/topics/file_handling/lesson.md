
# File Input and Output

**Course:** Python
**Topic ID:** `file_handling`

## Learning objectives

After completing this topic, learners should be able to:

- Understand file handling and why it is important.
- Explain the difference between reading and writing files.
- Open and close files using Python.
- Understand different file opening modes.
- Read file contents using different methods.
- Write and append data to files.
- Work with text and binary files.
- Use the `with` statement for safe file handling.
- Understand file pointers and file positioning.
- Rename and delete files using Python.
- Handle file-related exceptions.
- Work with CSV and JSON files.
- Apply file handling concepts to real-world applications.

## Explanation

### 1. What is File Handling?

File handling is the process of creating, opening, reading, writing, updating and deleting files using a programming language.

Python provides built-in functions and modules to work with files.

Files are useful because they allow programs to store information permanently, even after the program stops running.

For example, file handling is used in:

- Saving student records.
- Storing login information.
- Maintaining application logs.
- Saving user-generated data.
- Reading configuration files.
- Managing reports and documents.

### 2. Types of Files

Files are commonly divided into two main categories.

**A. Text Files**

Text files store information as readable characters.

Examples:

- `.txt`
- `.csv`
- `.json`
- `.py`
- `.html`

Example content of a text file:

```text
Name: Riya
Age: 20
Course: Python
```

**B. Binary Files**

Binary files store information as bytes rather than ordinary readable text.

Examples:

- Images (`.jpg`, `.png`)
- Audio files (`.mp3`)
- Video files (`.mp4`)
- PDF files (`.pdf`)
- Executable files

Binary files are generally handled using binary modes such as `rb` and `wb`.

### 3. Opening a File

Python uses the built-in `open()` function to open a file.

**Syntax:**

```python
file = open("filename", "mode")
```

Here:

- `filename` specifies the file name or path.
- `mode` specifies how the file should be accessed.

**Example:**

```python
file = open("sample.txt", "r")

print(file)

file.close()
```

The `close()` method closes the file after use.

Closing files is important because it releases system resources and ensures pending writes are properly completed.

### 4. File Opening Modes

Python supports different file opening modes.

| Mode | Description |
|---|---|
| `r` | Opens a file for reading |
| `w` | Opens a file for writing; creates it if needed and truncates an existing file |
| `a` | Opens a file for appending; creates it if needed |
| `x` | Creates a new file; raises an error if it already exists |
| `t` | Opens a file in text mode |
| `b` | Opens a file in binary mode |
| `r+` | Opens a file for reading and writing |
| `w+` | Opens a file for reading and writing; truncates existing content |
| `a+` | Opens a file for reading and appending |

**Example:**

```python
file = open("sample.txt", "w")

file.write("Hello Python!")

file.close()
```

This creates the file if it does not exist or replaces its existing content.

### 5. Reading a File

Python provides different methods to read file contents.

**A. read()**

The `read()` method reads the entire file or a specified number of characters.

Example:

```python
file = open("sample.txt", "r")

content = file.read()

print(content)

file.close()
```

Suppose `sample.txt` contains:

```text
Hello Python!
Welcome to file handling.
```

Output:

```text
Hello Python!
Welcome to file handling.
```

To read only a specified number of characters:

```python
file = open("sample.txt", "r")

print(file.read(5))

file.close()
```

Output:

```text
Hello
```

**B. readline()**

The `readline()` method reads one line at a time.

Example:

```python
file = open("sample.txt", "r")

print(file.readline())
print(file.readline())

file.close()
```

Output:

```text
Hello Python!

Welcome to file handling.
```

**C. readlines()**

The `readlines()` method reads all lines and returns them as a list.

Example:

```python
file = open("sample.txt", "r")

lines = file.readlines()

print(lines)

file.close()
```

Output:

```text
['Hello Python!\n', 'Welcome to file handling.']
```

The `\n` character represents a newline.

### 6. Writing to a File

The `write()` method writes a string into a file.

**Example:**

```python
file = open("student.txt", "w")

file.write("Name: Riya\n")
file.write("Course: Python\n")
file.write("Age: 20\n")

file.close()
```

Contents of `student.txt`:

```text
Name: Riya
Course: Python
Age: 20
```

Important: Opening a file in `w` mode removes its previous contents.

### 7. Appending Data to a File

The `a` mode adds new content at the end of an existing file without removing the previous content.

**Example:**

```python
file = open("student.txt", "a")

file.write("Marks: 90\n")

file.close()
```

The file now contains:

```text
Name: Riya
Course: Python
Age: 20
Marks: 90
```

If the file does not exist, append mode creates it.

### 8. The Difference Between Write and Append

| Write Mode (`w`) | Append Mode (`a`) |
|---|---|
| Writes new content | Adds content at the end |
| Removes existing content | Preserves existing content |
| Creates a file if missing | Creates a file if missing |
| Starts writing from the beginning | Writes at the end |

**Example:**

```python
# Write mode
file = open("demo.txt", "w")
file.write("First line")
file.close()

# Append mode
file = open("demo.txt", "a")
file.write("\nSecond line")
file.close()
```

Final file content:

```text
First line
Second line
```

### 9. Using the with Statement

The `with` statement is the recommended way to work with files.

It automatically closes the file when the block finishes, including when an exception occurs.

**Syntax:**

```python
with open("filename", "mode") as file:
    # File operations
```

**Example:**

```python
with open("sample.txt", "w") as file:
    file.write("Learning Python file handling.")

with open("sample.txt", "r") as file:
    content = file.read()
    print(content)
```

Output:

```text
Learning Python file handling.
```

Advantages:

- Automatically closes the file.
- Reduces resource-management errors.
- Makes code cleaner.
- Handles cleanup even if an exception occurs inside the block.

### 10. Closing a File

The `close()` method closes an opened file.

**Example:**

```python
file = open("sample.txt", "r")

print(file.read())

file.close()

print(file.closed)
```

Output depends on the file contents, followed by:

```text
True
```

The `closed` attribute indicates whether the file is closed.

### 11. File Pointer

A file pointer represents the current position in a file from which the next read or write operation takes place.

Python provides two important methods:

- `tell()`
- `seek()`

**A. tell()**

Returns the current file position.

Example:

```python
with open("sample.txt", "r") as file:
    print(file.tell())

    file.read(5)

    print(file.tell())
```

If the file contains `Hello Python`, output is:

```text
0
5
```

**B. seek()**

Moves the file pointer to a specified position.

Example:

```python
with open("sample.txt", "r") as file:
    file.seek(6)

    print(file.read())
```

If the file contains `Hello Python`, output is:

```text
Python
```

For text files, arbitrary seek positions can be restricted. The safest common uses are returning to the beginning with `seek(0)` or seeking to a position previously returned by `tell()`.

### 12. Creating a File

A new file can be created using `open()` with `x` mode.

**Example:**

```python
file = open("newfile.txt", "x")

file.write("This is a new file.")

file.close()
```

The `x` mode raises `FileExistsError` if the file already exists.

### 13. Renaming and Deleting Files

Python provides the `os` module for file management operations.

**A. Renaming a File**

The `os.rename()` function renames a file.

Example:

```python
import os

os.rename("old.txt", "new.txt")

print("File renamed successfully.")
```

**B. Deleting a File**

The `os.remove()` function deletes a file.

Example:

```python
import os

os.remove("new.txt")

print("File deleted successfully.")
```

These operations should be performed carefully because deleting or replacing files can cause permanent data loss.

### 14. Checking Whether a File Exists

The `os.path.exists()` function checks whether a file or directory exists at a specified path.

Example:

```python
import os

if os.path.exists("sample.txt"):
    print("File exists.")
else:
    print("File does not exist.")
```

Output depends on whether `sample.txt` exists.

To check specifically for a regular file:

```python
if os.path.isfile("sample.txt"):
    print("It is a file.")
```

### 15. Working with File Paths

A file path tells Python where a file is located.

There are two common types:

**A. Relative Path**

A relative path is specified with respect to the current working directory.

```python
file = open("data.txt", "r")
```

**B. Absolute Path**

An absolute path specifies the complete location of a file.

Example on Windows:

```python
file = open(r"C:\Users\HP\Documents\data.txt", "r")
```

The `r` before the string makes it a raw string, which is useful for Windows paths because backslashes are treated literally.

The `pathlib` module provides a modern way to work with paths.

Example:

```python
from pathlib import Path

file_path = Path("data.txt")

if file_path.exists():
    print("File found.")
```

### 16. Handling File Exceptions

File operations may produce exceptions.

Common file-related exceptions include:

| Exception | Description |
|---|---|
| `FileNotFoundError` | File does not exist |
| `PermissionError` | Permission to access the file is denied |
| `IsADirectoryError` | An operation expected a file but received a directory |
| `FileExistsError` | File already exists when using exclusive creation |
| `OSError` | General operating-system-related error |

**Example:**

```python
try:
    with open("unknown.txt", "r") as file:
        print(file.read())

except FileNotFoundError:
    print("The requested file does not exist.")

except PermissionError:
    print("You do not have permission to read this file.")
```

Output when the file is missing:

```text
The requested file does not exist.
```

### 17. Binary File Handling

Binary files store data as bytes.

Python uses binary modes such as:

- `rb` – Read binary data.
- `wb` – Write binary data.
- `ab` – Append binary data.

**Example: Reading an image file**

```python
with open("image.jpg", "rb") as file:
    data = file.read()

print(type(data))
print(len(data))
```

Output:

```text
<class 'bytes'>
```

The length depends on the image file.

**Example: Copying a binary file**

```python
with open("image.jpg", "rb") as source:
    data = source.read()

with open("image_copy.jpg", "wb") as destination:
    destination.write(data)

print("Image copied successfully.")
```

This copies the image data without converting it into text.

### 18. Working with CSV Files

CSV stands for Comma-Separated Values.

It is commonly used to store tabular data, such as student records, employee information and sales data.

Python provides the built-in `csv` module.

Example CSV content:

```text
Name,Age,Marks
Riya,20,90
Aman,21,85
Neha,19,95
```

**A. Reading a CSV File**

```python
import csv

with open("students.csv", "r", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

Output:

```text
['Name', 'Age', 'Marks']
['Riya', '20', '90']
['Aman', '21', '85']
['Neha', '19', '95']
```

**B. Writing a CSV File**

```python
import csv

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Name", "Age", "Marks"])

    writer.writerow(["Riya", 20, 90])
    writer.writerow(["Aman", 21, 85])

print("CSV file created.")
```

**C. Using DictReader**

`DictReader` reads each CSV row as a dictionary using the header names as keys.

```python
import csv

with open("students.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["Name"], row["Marks"])
```

### 19. Working with JSON Files

JSON stands for JavaScript Object Notation.

It is a lightweight data format commonly used for storing structured data and exchanging information between applications.

Python provides the built-in `json` module.

**A. Writing JSON Data**

```python
import json

student = {
    "name": "Riya",
    "age": 20,
    "course": "Python"
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

print("JSON file created.")
```

Contents of `student.json`:

```json
{
    "name": "Riya",
    "age": 20,
    "course": "Python"
}
```

**B. Reading JSON Data**

```python
import json

with open("student.json", "r") as file:
    student = json.load(file)

print(student)
print(student["name"])
```

Output:

```text
{'name': 'Riya', 'age': 20, 'course': 'Python'}
Riya
```

**C. Understanding dumps() and loads()**

| Function | Purpose |
|---|---|
| `dump()` | Writes a Python object into a JSON file |
| `load()` | Reads JSON data from a file |
| `dumps()` | Converts a Python object into a JSON string |
| `loads()` | Converts a JSON string into a Python object |

Example:

```python
import json

student = {"name": "Aman", "age": 20}

json_string = json.dumps(student)

print(json_string)

python_data = json.loads(json_string)

print(python_data["name"])
```

Output:

```text
{"name": "Aman", "age": 20}
Aman
```

### 20. Difference Between Text, CSV and JSON Files

| Feature | Text File | CSV File | JSON File |
|---|---|---|---|
| Format | Plain text | Tabular data | Structured data |
| Structure | Flexible | Rows and columns | Objects and arrays |
| Common use | Notes and logs | Spreadsheets and datasets | APIs and configuration |
| Python support | Built-in file functions | `csv` module | `json` module |

## Key concepts

1. **File handling:** Reading, writing, updating and managing files.
2. **open():** Opens a file in a specified mode.
3. **close():** Closes an opened file.
4. **read():** Reads file contents.
5. **readline():** Reads one line.
6. **readlines():** Reads all lines into a list.
7. **write():** Writes text into a file.
8. **append mode:** Adds content at the end of a file.
9. **with statement:** Automatically manages file closing.
10. **File pointer:** Represents the current position in a file.
11. **tell():** Returns the current file position.
12. **seek():** Changes the file position.
13. **Binary mode:** Reads or writes file data as bytes.
14. **CSV:** Stores tabular data in a text format.
15. **JSON:** Stores structured data in a standard data-interchange format.
16. **File exceptions:** Errors that occur during file operations.
17. **Path:** Specifies the location of a file.

## Examples

### Example 1: Create and read a file

```python
with open("hello.txt", "w") as file:
    file.write("Hello, Python!")

with open("hello.txt", "r") as file:
    content = file.read()

print(content)
```

Output:

```text
Hello, Python!
```

### Example 2: Count the number of lines in a file

```python
with open("data.txt", "r") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))
```

If the file contains three lines:

```text
Number of lines: 3
```

### Example 3: Count words in a file

```python
with open("data.txt", "r") as file:
    content = file.read()

words = content.split()

print("Total words:", len(words))
```

### Example 4: Copy one text file into another

```python
with open("source.txt", "r") as source:
    content = source.read()

with open("destination.txt", "w") as destination:
    destination.write(content)

print("File copied successfully.")
```

### Example 5: Search for a word in a file

```python
with open("data.txt", "r") as file:
    content = file.read()

word = "Python"

if word.lower() in content.lower():
    print("Word found.")
else:
    print("Word not found.")
```

### Example 6: Store student information

```python
student = {
    "name": "Riya",
    "age": 20,
    "marks": 95
}

with open("student.txt", "w") as file:
    for key, value in student.items():
        file.write(f"{key}: {value}\n")

print("Student information saved.")
```

Contents of the file:

```text
name: Riya
age: 20
marks: 95
```

### Example 7: Create a simple note-taking program

```python
note = input("Enter your note: ")

with open("notes.txt", "a") as file:
    file.write(note + "\n")

print("Note saved successfully.")
```

Sample input:

```text
Revise Python file handling.
```

Output:

```text
Note saved successfully.
```

### Example 8: Read a JSON student record

```python
import json

student = {
    "name": "Aman",
    "course": "Python",
    "marks": 88
}

with open("record.json", "w") as file:
    json.dump(student, file, indent=4)

with open("record.json", "r") as file:
    data = json.load(file)

print("Student:", data["name"])
print("Marks:", data["marks"])
```

Output:

```text
Student: Aman
Marks: 88
```

## Common mistakes

1. **Forgetting to close a file**
   - Use the `with` statement to close files automatically.

2. **Using the wrong file mode**
   - Choose `r`, `w`, `a` or another appropriate mode according to the operation.

3. **Using `w` when you want to preserve existing content**
   - `w` truncates the file.
   - Use `a` to append content.

4. **Trying to read a file that does not exist**
   - Check whether the file exists or handle `FileNotFoundError`.

5. **Forgetting newline characters**
   - Use `\n` when writing separate lines.

6. **Reading a large file completely into memory**
   - Process the file line by line when appropriate.

7. **Using text mode for binary files**
   - Use binary modes such as `rb` and `wb` for images, PDFs and other binary files.

8. **Using an incorrect file path**
   - Verify the working directory and file path.
   - Use `pathlib` for convenient path management.

9. **Assuming write() automatically adds a new line**
   - `write()` does not add a newline automatically.
   - Add `\n` when required.

10. **Forgetting that read() changes the file pointer**
    - After reading, the pointer moves forward.
    - Use `seek(0)` to return to the beginning.

11. **Using invalid JSON**
    - JSON requires valid syntax, including double quotes around string keys and string values.
    - Use `json.dump()` and `json.load()` instead of manually constructing JSON.

12. **Using incorrect CSV handling**
    - Use the `csv` module instead of manually splitting rows when CSV data may contain quoted commas or other special formatting.

13. **Deleting files without checking**
    - Confirm the file path before using `os.remove()`.

14. **Not handling file permissions**
    - Handle `PermissionError` when access may be restricted.

## Quick summary

- File handling allows Python programs to store and retrieve information permanently.
- Text files store readable characters, while binary files store bytes.
- `open()` opens a file.
- `close()` closes a file.
- `r` reads, `w` writes, `a` appends and `x` creates a new file exclusively.
- `read()`, `readline()` and `readlines()` read file contents.
- `write()` writes data to a file.
- `with` automatically closes files.
- `tell()` returns the file pointer position.
- `seek()` changes the file pointer position.
- `os` and `pathlib` help manage file paths and file operations.
- Binary modes include `rb`, `wb` and `ab`.
- The `csv` module handles CSV files.
- The `json` module handles JSON data.
- Exception handling helps manage file-related errors.

## Practice

### Beginner Level

1. Create a text file and write your name into it.
2. Read and display the contents of a file.
3. Write five lines into a file.
4. Append a new line to an existing file.
5. Read a file using `readline()`.
6. Count the number of lines in a file.

### Intermediate Level

7. Write a program that copies one file into another.
8. Create a program that counts the total number of words in a file.
9. Search for a specific word in a text file.
10. Write a program that checks whether a file exists.
11. Read a CSV file and display its contents.
12. Store student information in a JSON file and read it back.

### Advanced Level

13. Create a student record management system using files.
14. Create a note-taking application that appends notes to a file.
15. Write a program that handles missing files and permission errors.
16. Copy an image using binary file handling.
17. Create a program that reads a CSV file and calculates average marks.
18. Create a JSON-based contact book that supports adding and retrieving contacts.

### Practice Solutions

**Solution 1: Write and read a file**

```python
with open("test.txt", "w") as file:
    file.write("Learning Python.")

with open("test.txt", "r") as file:
    print(file.read())
```

Output:

```text
Learning Python.
```

**Solution 2: Append content**

```python
with open("test.txt", "a") as file:
    file.write("\nFile handling is useful.")

with open("test.txt", "r") as file:
    print(file.read())
```

Output:

```text
Learning Python.
File handling is useful.
```

**Solution 3: Count words**

```python
with open("test.txt", "r") as file:
    content = file.read()

words = content.split()

print("Total words:", len(words))
```

**Solution 4: Check whether a file exists**

```python
from pathlib import Path

file_path = Path("test.txt")

if file_path.exists() and file_path.is_file():
    print("File exists.")
else:
    print("File not found.")
```

**Solution 5: Handle missing files**

```python
try:
    with open("unknown.txt", "r") as file:
        print(file.read())

except FileNotFoundError:
    print("File does not exist.")
```

Output when the file is missing:

```text
File does not exist.
```

**Solution 6: Store data in JSON**

```python
import json

student = {
    "name": "Riya",
    "age": 20,
    "marks": 90
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

with open("student.json", "r") as file:
    data = json.load(file)

print(data)
```

Output:

```text
{'name': 'Riya', 'age': 20, 'marks': 90}
```

**Solution 7: Read CSV data**

```python
import csv

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Name", "Marks"])
    writer.writerow(["Riya", 90])
    writer.writerow(["Aman", 85])

with open("students.csv", "r", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

Output:

```text
['Name', 'Marks']
['Riya', '90']
['Aman', '85']
```

## Learning resources

- **PDF:** [File Input and Output PDF](https://drive.google.com/file/d/1TEapPenCa5yo7CUIGTR-wvD9ZvnSTj1r/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc