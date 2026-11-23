
# Classes, Objects and Encapsulation

**Course:** Python
**Topic ID:** `oop_classes`

## Learning objectives

After completing this topic, learners should be able to:

- Understand the meaning and importance of Object-Oriented Programming (OOP).
- Explain the difference between procedural and object-oriented programming.
- Understand classes and objects in Python.
- Create classes using the `class` keyword.
- Create objects from classes.
- Understand attributes and methods.
- Differentiate between instance attributes and class attributes.
- Understand the purpose of the `self` parameter.
- Create and use constructors with `__init__()`.
- Understand instance methods, class methods, and static methods.
- Understand encapsulation and data hiding.
- Differentiate between public, protected, and private naming conventions.
- Use getters and setters to access and modify attributes.
- Understand Python properties using `@property`.
- Work with object references and multiple objects.
- Apply OOP concepts to real-world programming problems.

## Explanation

### 1. What is Object-Oriented Programming (OOP)?

Object-Oriented Programming (OOP) is a programming approach in which programs are organized around objects rather than only functions and instructions.

An object combines:

- **Data:** Information or properties associated with the object.
- **Methods:** Functions that describe the actions an object can perform.

OOP helps developers organize large programs into reusable and manageable components.

**Real-life example:**

Consider a car.

A car has properties such as:
- Brand
- Model
- Color
- Speed

A car can perform actions such as:
- Start
- Stop
- Accelerate
- Brake

In OOP:
- Properties are represented using attributes.
- Actions are represented using methods.
- A class defines the structure.
- An object represents an individual car.

### 2. Why Do We Use OOP?

OOP is useful because it provides:

1. **Code Reusability:** Classes can be reused to create multiple objects.
2. **Organization:** Related data and functions are grouped together.
3. **Maintainability:** Code becomes easier to understand and modify.
4. **Data Protection:** Encapsulation helps control access to internal data.
5. **Scalability:** Large applications can be divided into manageable components.
6. **Real-World Modeling:** Real-world entities can be represented as objects.

### 3. Procedural Programming vs Object-Oriented Programming

| Procedural Programming | Object-Oriented Programming |
|---|---|
| Organized mainly around functions and procedures | Organized around classes and objects |
| Data and functions are often separate | Data and methods are grouped together |
| Suitable for many small and straightforward programs | Useful for structuring larger applications |
| Reuse is often achieved through functions | Reuse can be achieved through classes and objects |
| Example: A collection of functions | Example: Student, BankAccount, Car classes |

**Example of procedural programming:**

```python
name = "Riya"
marks = 90

def display_student():
    print(name, marks)

display_student()
```

**Example of object-oriented programming:**

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def display(self):
        print(self.name, self.marks)

student1 = Student("Riya", 90)

student1.display()
```

Both approaches can solve the same problem, but OOP groups related data and behavior into objects.

## 4. What is a Class?

A class is a blueprint or template used to create objects.

It defines the attributes and methods that its objects can have.

**Syntax:**

```python
class ClassName:
    # Attributes and methods
    pass
```

Here:
- `class` is a Python keyword.
- `ClassName` is the name of the class.
- The indented block contains class members.
- `pass` is used as a placeholder when no implementation is written yet.

**Example:**

```python
class Student:
    name = "Riya"
    age = 20

    def display(self):
        print(self.name)
        print(self.age)
```

In this example:
- `Student` is a class.
- `name` and `age` are class attributes.
- `display()` is a method.

### 5. What is an Object?

An object is an instance of a class.

A class defines the structure, while an object is an actual instance created using that structure.

**Syntax:**

```python
object_name = ClassName()
```

**Example:**

```python
class Student:
    name = "Riya"
    age = 20

student1 = Student()

print(student1.name)
print(student1.age)
```

Output:

```text
Riya
20
```

Here:
- `Student` is the class.
- `student1` is an object.
- `student1.name` accesses the object's attribute lookup.
- `student1.age` accesses its age.

We can create multiple objects from the same class.

```python
class Student:
    name = "Riya"

student1 = Student()
student2 = Student()

print(student1.name)
print(student2.name)
```

Output:

```text
Riya
Riya
```

Both objects access the class attribute `name`.

## 6. Attributes in Python

Attributes are variables associated with a class or an object.

There are two commonly discussed types of attributes:

1. Instance attributes
2. Class attributes

### A. Instance Attributes

Instance attributes belong to individual objects.

Different objects can have different values for the same instance attribute.

They are commonly created using `self`.

**Example:**

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("Riya", 20)
student2 = Student("Aman", 21)

print(student1.name)
print(student2.name)
```

Output:

```text
Riya
Aman
```

Here:
- `student1.name` is `"Riya"`.
- `student2.name` is `"Aman"`.
- Each object has its own instance attributes.

### B. Class Attributes

Class attributes belong to the class itself and are shared through normal attribute lookup by its instances unless an instance has an attribute with the same name.

**Example:**

```python
class Student:
    college = "ABC College"

    def __init__(self, name):
        self.name = name

student1 = Student("Riya")
student2 = Student("Aman")

print(student1.college)
print(student2.college)
```

Output:

```text
ABC College
ABC College
```

Both objects access the class attribute `college`.

We can also access it directly through the class:

```python
print(Student.college)
```

Output:

```text
ABC College
```

### Difference Between Class and Instance Attributes

| Class Attribute | Instance Attribute |
|---|---|
| Associated with the class | Associated with an individual object |
| Shared through normal lookup | Stored separately for each object |
| Commonly defined in the class body | Commonly defined using `self` |
| Can be accessed through the class | Usually accessed through an object |

**Important:** If an instance attribute is assigned the same name as a class attribute, it normally shadows that class attribute for that instance.

## 7. What is self in Python?

`self` is the conventional name for the first parameter of an instance method.

It refers to the current object on which the method is called.

It allows methods to access and modify the attributes of that particular object.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.name = name

    def display(self):
        print("Student Name:", self.name)

student1 = Student("Riya")
student2 = Student("Aman")

student1.display()
student2.display()
```

Output:

```text
Student Name: Riya
Student Name: Aman
```

Explanation:

- `self.name` stores the name for the current object.
- When `student1.display()` is called, `self` refers to `student1`.
- When `student2.display()` is called, `self` refers to `student2`.

**Important points about self:**

- `self` is not a Python keyword.
- It is a naming convention followed by Python programmers.
- It is normally the first parameter of an instance method.
- It allows an object to access its own attributes and methods.
- Python passes the instance automatically when an instance method is called through an object.

## 8. What is a Constructor?

A constructor is commonly described as a special method used to initialize a newly created object.

In Python, `__init__()` is the initializer method. Python calls it automatically after creating the instance.

**Syntax:**

```python
class ClassName:
    def __init__(self):
        # Initialization statements
        pass
```

**Example:**

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("Riya", 20)

print(student1.name)
print(student1.age)
```

Output:

```text
Riya
20
```

Explanation:

1. A `Student` object is created.
2. Python calls `__init__()` for the new object.
3. `"Riya"` is assigned to `self.name`.
4. `20` is assigned to `self.age`.

### Types of Constructors (Common Teaching Classification)

**1. Default-style initialization**

A class can define `__init__()` with no additional required arguments.

```python
class Student:
    def __init__(self):
        self.name = "Unknown"
        self.age = 0

student1 = Student()

print(student1.name)
print(student1.age)
```

Output:

```text
Unknown
0
```

**2. Parameterized initialization**

An initializer accepts arguments to set different values for different objects.

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("Riya", 20)
student2 = Student("Aman", 21)

print(student1.name, student1.age)
print(student2.name, student2.age)
```

Output:

```text
Riya 20
Aman 21
```

Note: Python does not provide separate constructor overloads in the same way as some other languages. Flexible defaults or argument handling can be used when different initialization options are needed.

## 9. Methods in Python Classes

A method is a function defined inside a class.

Methods describe the behavior or actions of objects.

Python commonly uses three method types:

1. Instance methods
2. Class methods
3. Static methods

### A. Instance Methods

Instance methods operate on an individual object.

They normally use `self` as the first parameter.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.name = name

    def display(self):
        print("Name:", self.name)

student1 = Student("Riya")

student1.display()
```

Output:

```text
Name: Riya
```

### B. Class Methods

Class methods operate on the class itself rather than a particular instance.

They use the `@classmethod` decorator and conventionally take `cls` as the first parameter.

**Example:**

```python
class Student:
    college = "ABC College"

    @classmethod
    def change_college(cls, new_name):
        cls.college = new_name

Student.change_college("XYZ College")

print(Student.college)
```

Output:

```text
XYZ College
```

Here:
- `@classmethod` marks the method as a class method.
- `cls` refers to the class.
- `cls.college` accesses the class attribute.

### C. Static Methods

Static methods are functions placed inside a class namespace.

They use the `@staticmethod` decorator and do not automatically receive `self` or `cls`.

**Example:**

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(10, 20))
```

Output:

```text
30
```

### Difference Between Instance, Class, and Static Methods

| Instance Method | Class Method | Static Method |
|---|---|---|
| Uses `self` conventionally | Uses `cls` conventionally | No automatic first argument |
| Works with an instance | Works with the class | Performs a related independent operation |
| Can access instance attributes | Can access class attributes | Does not automatically access instance or class state |
| Uses no special decorator by default | Uses `@classmethod` | Uses `@staticmethod` |

## 10. What is Encapsulation?

Encapsulation is an important concept of Object-Oriented Programming.

It means grouping data and the methods that operate on that data inside a class, while controlling how the internal state is accessed or modified.

Encapsulation helps protect an object's internal data from unintended changes.

**Real-life example: Bank Account**

Imagine a bank account.

It has:
- Account holder name.
- Account number.
- Account balance.

The account holder should not be able to change the balance through arbitrary operations.

Instead, the bank provides controlled operations such as:
- Deposit money.
- Withdraw money.
- Check balance.

Similarly, in Python, we can use methods and properties to control how object attributes are accessed and changed.

### 11. Access Conventions in Python

Python does not enforce traditional public, protected, and private access modifiers in exactly the same way as languages such as Java or C++.

Instead, Python uses naming conventions and name mangling.

The commonly taught categories are:

1. Public members
2. Protected members
3. Private members

### A. Public Members

Public attributes and methods can be accessed from outside the class.

They are written without a leading underscore.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.name = name

student1 = Student("Riya")

print(student1.name)
```

Output:

```text
Riya
```

Here, `name` is a public instance attribute.

### B. Protected Members

A single leading underscore indicates that an attribute or method is intended for internal use or use by subclasses.

It is a convention, not a strict access restriction.

**Example:**

```python
class Student:
    def __init__(self, name):
        self._name = name

student1 = Student("Riya")

print(student1._name)
```

Output:

```text
Riya
```

Python still allows access to `_name`, but programmers should treat it as an internal implementation detail.

### C. Private Members

A double leading underscore triggers name mangling.

Python changes the attribute name internally to reduce accidental naming conflicts, especially in subclasses.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.__name = name

student1 = Student("Riya")

print(student1.__name)
```

This raises an `AttributeError` because the attribute name is mangled.

The internal name becomes:

```text
_Student__name
```

It can technically be accessed using the mangled name:

```python
print(student1._Student__name)
```

Output:

```text
Riya
```

However, directly using the mangled name is generally discouraged.

**Important:** Double underscores do not create absolute privacy or security. They mainly help avoid accidental access and naming conflicts.

### Difference Between Public, Protected, and Private

| Type | Naming | Meaning |
|---|---|---|
| Public | `name` | Intended for general access |
| Protected convention | `_name` | Intended for internal or subclass use |
| Private-style | `__name` | Triggers name mangling |

## 12. Getters and Setters

Getters and setters are methods or properties used to read and update an object's attributes in a controlled way.

They are useful for:
- Validating input.
- Preventing invalid values.
- Applying rules before updating attributes.
- Controlling access to internal state.

### A. Getter Method

A getter returns the value of an attribute.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

student1 = Student("Riya")

print(student1.get_name())
```

Output:

```text
Riya
```

### B. Setter Method

A setter updates an attribute, optionally after validating the new value.

**Example:**

```python
class Student:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        if new_name.strip():
            self.__name = new_name
        else:
            print("Name cannot be empty")

student1 = Student("Riya")

print(student1.get_name())

student1.set_name("Aman")

print(student1.get_name())
```

Output:

```text
Riya
Aman
```

The setter checks that the new name is not empty before updating the attribute.

## 13. Using @property in Python

Python provides the `@property` decorator to create managed attributes.

It allows a method to be accessed like an attribute.

A property can also define a setter and a deleter.

**Example:**

```python
class Student:
    def __init__(self, marks):
        self.__marks = marks

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        if 0 <= value <= 100:
            self.__marks = value
        else:
            print("Marks must be between 0 and 100")

student1 = Student(90)

print(student1.marks)

student1.marks = 95

print(student1.marks)

student1.marks = 150
```

Output:

```text
90
95
Marks must be between 0 and 100
```

Explanation:

- `@property` defines a getter.
- `@marks.setter` defines a setter for the same property.
- The setter checks whether marks are between 0 and 100.
- Invalid values are rejected.

Properties provide a clean way to control attribute access without requiring callers to use separate getter and setter method names.

## 14. Encapsulation Using a Bank Account

Let's understand encapsulation with a practical example.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Deposit successful")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount")
        elif amount > self.__balance:
            print("Insufficient balance")
        else:
            self.__balance -= amount
            print("Withdrawal successful")

    def get_balance(self):
        return self.__balance

account = BankAccount("Riya", 5000)

account.deposit(1000)
account.withdraw(2000)

print("Balance:", account.get_balance())
```

Output:

```text
Deposit successful
Withdrawal successful
Balance: 4000
```

Explanation:

- `__balance` is a private-style attribute.
- `deposit()` controls how money is added.
- `withdraw()` checks whether enough money is available.
- `get_balance()` returns the current balance.
- The balance is updated through controlled methods.

This demonstrates encapsulation and validation.

## 15. Object Identity and Multiple Objects

Every object is created as an instance of a class.

We can use multiple objects to store different information.

**Example:**

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

student1 = Student("Riya", 90)
student2 = Student("Aman", 85)

print(student1.name, student1.marks)
print(student2.name, student2.marks)
```

Output:

```text
Riya 90
Aman 85
```

Each object stores its own instance attributes.

We can use the `is` operator to check whether two variables refer to the same object.

```python
class Student:
    pass

student1 = Student()
student2 = Student()
student3 = student1

print(student1 is student2)
print(student1 is student3)
```

Output:

```text
False
True
```

Here:
- `student1` and `student2` refer to different objects.
- `student3` refers to the same object as `student1`.

## 16. Practical Example: Employee Management System

Let's create a simple employee management program using classes, objects, and encapsulation.

```python
class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.__salary = salary

    def display_details(self):
        print("Name:", self.name)
        print("Employee ID:", self.employee_id)
        print("Salary:", self.__salary)

    def update_salary(self, new_salary):
        if new_salary > 0:
            self.__salary = new_salary
            print("Salary updated successfully")
        else:
            print("Invalid salary")

    def get_salary(self):
        return self.__salary


employee1 = Employee("Riya", 101, 30000)

employee1.display_details()

employee1.update_salary(35000)

print("Updated Salary:", employee1.get_salary())
```

Output:

```text
Name: Riya
Employee ID: 101
Salary: 30000
Salary updated successfully
Updated Salary: 35000
```

This example demonstrates:

- Class creation.
- Object creation.
- Constructor usage.
- Instance attributes.
- Instance methods.
- Private-style attributes.
- Controlled data modification.

## 17. Important OOP Terminology

| Term | Meaning |
|---|---|
| Class | Blueprint for creating objects |
| Object | Instance of a class |
| Attribute | Data associated with a class or object |
| Method | Function defined inside a class |
| self | Reference to the current instance |
| cls | Conventional reference to the class in class methods |
| Constructor (informal) | Initialization process commonly implemented using `__init__()` |
| Encapsulation | Grouping data and methods while controlling access |
| Getter | Method or property used to read a value |
| Setter | Method or property used to update a value |
| Property | Managed attribute interface created using `@property` |
| Instance | An individual object created from a class |
| Name mangling | Transformation of double-underscore attribute names |

## Key concepts

- **OOP:** A programming approach based on classes and objects.
- **Class:** A blueprint used to create objects.
- **Object:** An instance of a class.
- **Attribute:** A variable associated with a class or object.
- **Method:** A function defined inside a class.
- **Instance attribute:** An attribute associated with an individual object.
- **Class attribute:** An attribute associated with the class.
- **self:** Conventional reference to the current instance.
- **__init__():** Initializer method automatically called after object creation.
- **Instance method:** Method that operates on an instance.
- **Class method:** Method that receives the class as its first argument.
- **Static method:** Method that does not automatically receive an instance or class reference.
- **Encapsulation:** Grouping data and behavior and controlling access to internal state.
- **Public member:** Member intended for general access.
- **Protected convention:** Single underscore indicates intended internal use.
- **Private-style member:** Double leading underscore triggers name mangling.
- **Getter:** Reads an attribute.
- **Setter:** Updates an attribute, often with validation.
- **@property:** Provides managed attribute access.

## Common mistakes

1. **Forgetting to create an object**

   Incorrect:

   ```python
   class Student:
       def display(self):
           print("Hello")

   Student.display()
   ```

   Correct:

   ```python
   class Student:
       def display(self):
           print("Hello")

   student1 = Student()
   student1.display()
   ```

2. **Forgetting self in an instance method**

   Incorrect:

   ```python
   class Student:
       def display():
           print("Hello")
   ```

   Correct:

   ```python
   class Student:
       def display(self):
           print("Hello")
   ```

3. **Forgetting self when accessing instance attributes**

   Incorrect:

   ```python
   class Student:
       def __init__(self, name):
           name = name
   ```

   Correct:

   ```python
   class Student:
       def __init__(self, name):
           self.name = name
   ```

   The correct version stores the value on the object.

4. **Confusing class and instance attributes**

   Class attributes are associated with the class, while instance attributes belong to individual objects.

5. **Using incorrect capitalization for special methods**

   Incorrect:

   ```python
   def Init(self):
       pass
   ```

   Correct:

   ```python
   def __init__(self):
       pass
   ```

   Special method names require exact spelling.

6. **Confusing __init__() with object creation**

   `__init__()` initializes an already-created instance. It is not the method that actually creates the object.

7. **Trying to access a private-style attribute directly**

   An attribute such as `__name` is name-mangled. Use an appropriate method or property to access it.

8. **Assuming a single underscore enforces privacy**

   `_name` is a naming convention, not a strict access restriction.

9. **Using a setter without validation**

   Setters should validate values when the class has rules for its data.

10. **Forgetting to return a value from a getter**

    Use `return` when a method should provide a value.

11. **Confusing class methods and static methods**

    - Class methods receive `cls`.
    - Static methods receive no automatic `self` or `cls`.

12. **Modifying a mutable class attribute unintentionally**

    A mutable class attribute, such as a list, can be shared by instances through normal lookup. Use instance attributes when each object needs its own independent list.

## Quick summary

- OOP organizes programs around classes and objects.
- A class is a blueprint.
- An object is an instance of a class.
- Attributes store information.
- Methods define behavior.
- `self` refers to the current instance.
- `__init__()` initializes newly created objects.
- Instance attributes belong to individual objects.
- Class attributes are associated with the class.
- Instance methods operate on objects.
- Class methods receive the class through `cls`.
- Static methods do not automatically receive `self` or `cls`.
- Encapsulation groups data and methods and provides controlled access to internal state.
- Public members are intended for general access.
- A single underscore indicates intended internal use.
- Double leading underscores trigger name mangling.
- Getters read attributes.
- Setters update attributes.
- `@property` provides a convenient way to manage attribute access.
- Classes and objects make programs easier to organize and maintain.

## Practice

### Beginner Level

**1. Create a Class**

Create a class named `Student` with attributes for name and age.

Create an object and display both values.

**2. Create Multiple Objects**

Create a `Car` class with brand and color attributes.

Create three different objects with different values.

**3. Use a Constructor**

Create an `Employee` class that accepts employee name and ID through `__init__()`.

**4. Create an Instance Method**

Create a `Person` class with a method that displays the person's name and age.

**5. Understand self**

Create a class with a method that changes an object's name.

Create two objects and verify that their names remain independent.

### Intermediate Level

**6. Class Attributes**

Create a `Student` class with a class attribute named `college`.

Create two student objects and display their college name.

**7. Instance and Class Attributes**

Create a class containing both instance and class attributes.

Change the class attribute and observe how it affects normal attribute lookup.

**8. Create a Class Method**

Create a `Student` class with a class method that changes the college name.

**9. Create a Static Method**

Create a `Calculator` class with static methods for addition and multiplication.

**10. Implement Encapsulation**

Create a `BankAccount` class with a private-style balance attribute.

Implement deposit, withdrawal, and balance-checking methods.

**11. Create Getter and Setter Methods**

Create a `Person` class with a private-style age attribute.

Implement methods to retrieve and update age. Reject negative ages.

### Advanced Level

**12. Use @property**

Create an `Employee` class with a salary property.

Reject salary values that are zero or negative.

**13. Create a Student Result System**

Create a `Student` class containing:
- Student name.
- Roll number.
- Marks.
- Method to calculate average.
- Method to display the result.

**14. Create a Bank Account System**

Implement:
- Account holder name.
- Private-style balance.
- Deposit operation.
- Withdrawal operation.
- Balance inquiry.
- Input validation.

**15. Create an Employee Management System**

Create an `Employee` class with:
- Employee name.
- Employee ID.
- Private-style salary.
- Method to update salary.
- Method to calculate an annual salary.
- Method to display employee details.

### Sample Solutions

**Solution 1: Create a Class**

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("Riya", 20)

print(student1.name)
print(student1.age)
```

Output:

```text
Riya
20
```

**Solution 2: Create Multiple Objects**

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

car1 = Car("Toyota", "White")
car2 = Car("Honda", "Black")
car3 = Car("Hyundai", "Red")

print(car1.brand, car1.color)
print(car2.brand, car2.color)
print(car3.brand, car3.color)
```

Output:

```text
Toyota White
Honda Black
Hyundai Red
```

**Solution 3: Use a Constructor**

```python
class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

employee1 = Employee("Riya", 101)

print(employee1.name)
print(employee1.employee_id)
```

Output:

```text
Riya
101
```

**Solution 4: Create an Instance Method**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)

person1 = Person("Riya", 20)

person1.display()
```

Output:

```text
Name: Riya
Age: 20
```

**Solution 5: Understand self**

```python
class Student:
    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name

student1 = Student("Riya")
student2 = Student("Aman")

student1.change_name("Priya")

print(student1.name)
print(student2.name)
```

Output:

```text
Priya
Aman
```

**Solution 6: Class Attributes**

```python
class Student:
    college = "ABC College"

    def __init__(self, name):
        self.name = name

student1 = Student("Riya")
student2 = Student("Aman")

print(student1.college)
print(student2.college)
```

Output:

```text
ABC College
ABC College
```

**Solution 7: Instance and Class Attributes**

```python
class Student:
    college = "ABC College"

    def __init__(self, name):
        self.name = name

student1 = Student("Riya")
student2 = Student("Aman")

Student.college = "XYZ College"

print(student1.college)
print(student2.college)
```

Output:

```text
XYZ College
XYZ College
```

**Solution 8: Create a Class Method**

```python
class Student:
    college = "ABC College"

    @classmethod
    def change_college(cls, name):
        cls.college = name

Student.change_college("XYZ College")

print(Student.college)
```

Output:

```text
XYZ College
```

**Solution 9: Create a Static Method**

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

print(Calculator.add(10, 5))
print(Calculator.multiply(10, 5))
```

Output:

```text
15
50
```

**Solution 10: Implement Encapsulation**

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Deposit successful")
        else:
            print("Invalid amount")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > self.__balance:
            print("Insufficient balance")
        else:
            self.__balance -= amount
            print("Withdrawal successful")

    def get_balance(self):
        return self.__balance

account = BankAccount(5000)

account.deposit(1000)
account.withdraw(2000)

print("Balance:", account.get_balance())
```

Output:

```text
Deposit successful
Withdrawal successful
Balance: 4000
```

**Solution 11: Create Getter and Setter Methods**

```python
class Person:
    def __init__(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age >= 0:
            self.__age = age
        else:
            print("Age cannot be negative")

person1 = Person(20)

print(person1.get_age())

person1.set_age(21)

print(person1.get_age())

person1.set_age(-5)
```

Output:

```text
20
21
Age cannot be negative
```

**Solution 12: Use @property**

```python
class Employee:
    def __init__(self, salary):
        self.__salary = salary

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value > 0:
            self.__salary = value
        else:
            print("Salary must be positive")

employee1 = Employee(30000)

print(employee1.salary)

employee1.salary = 40000

print(employee1.salary)

employee1.salary = -100
```

Output:

```text
30000
40000
Salary must be positive
```

**Solution 13: Create a Student Result System**

```python
class Student:
    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

    def calculate_average(self):
        return sum(self.marks) / len(self.marks)

    def display_result(self):
        print("Name:", self.name)
        print("Roll Number:", self.roll_number)
        print("Average Marks:", self.calculate_average())

student1 = Student("Riya", 101, [85, 90, 95])

student1.display_result()
```

Output:

```text
Name: Riya
Roll Number: 101
Average Marks: 90.0
```

**Solution 14: Create a Bank Account System**

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Amount deposited")
        else:
            print("Invalid deposit")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal")
        elif amount > self.__balance:
            print("Insufficient balance")
        else:
            self.__balance -= amount
            print("Amount withdrawn")

    def check_balance(self):
        print("Current Balance:", self.__balance)

account = BankAccount("Riya", 10000)

account.deposit(2000)
account.withdraw(3000)
account.check_balance()
```

Output:

```text
Amount deposited
Amount withdrawn
Current Balance: 9000
```

**Solution 15: Employee Management System**

```python
class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.__salary = salary

    def update_salary(self, new_salary):
        if new_salary > 0:
            self.__salary = new_salary
            print("Salary updated")
        else:
            print("Invalid salary")

    def annual_salary(self):
        return self.__salary * 12

    def display_details(self):
        print("Name:", self.name)
        print("Employee ID:", self.employee_id)
        print("Salary:", self.__salary)
        print("Annual Salary:", self.annual_salary())

employee1 = Employee("Riya", 101, 30000)

employee1.display_details()

employee1.update_salary(35000)

employee1.display_details()
```

Output:

```text
Name: Riya
Employee ID: 101
Salary: 30000
Annual Salary: 360000
Salary updated
Name: Riya
Employee ID: 101
Salary: 35000
Annual Salary: 420000
```

## Learning resources

- **PDF:** [Classes, Objects and Encapsulation](https://drive.google.com/file/d/1fgfO6ZEVR-ePBE4HCAvxBsTGilnnpwIa/view?usp=drive_link)
- **YouTube:** [Python Video Resource](https://youtu.be/ERCMXc8x7mc)