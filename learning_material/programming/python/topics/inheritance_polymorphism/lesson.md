
# Inheritance and Polymorphism

**Course:** Python
**Topic ID:** `inheritance_polymorphism`

## Learning objectives

After completing this topic, learners should be able to:

- Understand inheritance and polymorphism in object-oriented programming.
- Explain the advantages of inheritance.
- Create parent and child classes.
- Understand single, multiple, multilevel and hierarchical inheritance.
- Use the `super()` function.
- Understand method overriding.
- Differentiate between method overloading and method overriding.
- Understand polymorphism and its types.
- Implement polymorphism using inheritance and duck typing.
- Understand method resolution order (MRO).
- Use abstract classes and methods.
- Apply inheritance and polymorphism to real-world applications.

## Explanation

### 1. What is Inheritance?

Inheritance is an important concept in Object-Oriented Programming (OOP).

It allows one class to acquire the properties and methods of another class.

The class whose properties are inherited is called the **parent class**, **base class** or **superclass**.

The class that inherits those properties is called the **child class**, **derived class** or **subclass**.

Inheritance helps programmers reuse existing code instead of writing the same code repeatedly.

**Syntax:**

```python
class Parent:
    # Parent class properties and methods
    pass

class Child(Parent):
    # Child class properties and methods
    pass
```

**Example:**

```python
class Animal:
    def eat(self):
        print("Animal is eating.")

class Dog(Animal):
    def bark(self):
        print("Dog is barking.")

dog = Dog()

dog.eat()
dog.bark()
```

Output:

```text
Animal is eating.
Dog is barking.
```

Explanation:

- `Animal` is the parent class.
- `Dog` is the child class.
- `Dog` inherits the `eat()` method from `Animal`.
- The `Dog` class also has its own `bark()` method.

### 2. Advantages of Inheritance

Inheritance provides several advantages:

1. **Code reusability:** Existing methods can be reused in child classes.
2. **Reduced code duplication:** Common functionality can be written once.
3. **Easy maintenance:** Shared functionality can be updated in the parent class.
4. **Extensibility:** Child classes can add new features.
5. **Better organization:** Related classes can be arranged in a hierarchy.
6. **Polymorphism:** Different classes can provide different implementations of common methods.

### 3. Types of Inheritance

Python supports different types of inheritance.

The main types are:

1. Single inheritance
2. Multiple inheritance
3. Multilevel inheritance
4. Hierarchical inheritance
5. Hybrid inheritance

### 4. Single Inheritance

Single inheritance occurs when one child class inherits from one parent class.

**Structure:**

```text
Parent
  |
Child
```

**Example:**

```python
class Person:
    def introduce(self):
        print("I am a person.")

class Student(Person):
    def study(self):
        print("I am studying.")

student = Student()

student.introduce()
student.study()
```

Output:

```text
I am a person.
I am studying.
```

Here, `Student` inherits from only one parent class, `Person`.

### 5. Multiple Inheritance

Multiple inheritance occurs when one child class inherits from more than one parent class.

**Structure:**

```text
Parent1     Parent2
    \       /
      Child
```

**Example:**

```python
class Father:
    def father_quality(self):
        print("Father is hardworking.")

class Mother:
    def mother_quality(self):
        print("Mother is caring.")

class Child(Father, Mother):
    def child_quality(self):
        print("Child is learning.")

child = Child()

child.father_quality()
child.mother_quality()
child.child_quality()
```

Output:

```text
Father is hardworking.
Mother is caring.
Child is learning.
```

The `Child` class inherits methods from both `Father` and `Mother`.

### 6. Multilevel Inheritance

Multilevel inheritance occurs when a class inherits from another child class, creating multiple levels of inheritance.

**Structure:**

```text
Grandparent
     |
   Parent
     |
    Child
```

**Example:**

```python
class Grandparent:
    def property(self):
        print("Family property.")

class Parent(Grandparent):
    def parent_method(self):
        print("Parent method.")

class Child(Parent):
    def child_method(self):
        print("Child method.")

obj = Child()

obj.property()
obj.parent_method()
obj.child_method()
```

Output:

```text
Family property.
Parent method.
Child method.
```

The `Child` class can access methods from both `Parent` and `Grandparent`.

### 7. Hierarchical Inheritance

Hierarchical inheritance occurs when multiple child classes inherit from the same parent class.

**Structure:**

```text
       Parent
       /    \
   Child1  Child2
```

**Example:**

```python
class Animal:
    def eat(self):
        print("Animal eats food.")

class Dog(Animal):
    def bark(self):
        print("Dog barks.")

class Cat(Animal):
    def meow(self):
        print("Cat meows.")

dog = Dog()
cat = Cat()

dog.eat()
dog.bark()

cat.eat()
cat.meow()
```

Output:

```text
Animal eats food.
Dog barks.
Animal eats food.
Cat meows.
```

Both child classes inherit the common `eat()` method.

### 8. Hybrid Inheritance

Hybrid inheritance is a combination of two or more inheritance types.

**Example:**

```python
class Person:
    def show_person(self):
        print("Person information.")

class Student(Person):
    def show_student(self):
        print("Student information.")

class Employee(Person):
    def show_employee(self):
        print("Employee information.")

class TeachingAssistant(Student, Employee):
    def show_role(self):
        print("Teaching assistant.")

obj = TeachingAssistant()

obj.show_person()
obj.show_student()
obj.show_employee()
obj.show_role()
```

Output:

```text
Person information.
Student information.
Employee information.
Teaching assistant.
```

Here, hierarchical and multiple inheritance are combined.

### 9. The super() Function

The `super()` function is used to access methods from a parent class according to Python's method resolution order.

It is commonly used to:

- Call a parent class constructor.
- Reuse parent class methods.
- Extend inherited functionality.
- Support cooperative multiple inheritance.

**Example:**

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def display(self):
        print("Animal name:", self.name)

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def display(self):
        super().display()
        print("Breed:", self.breed)

dog = Dog("Tommy", "Labrador")

dog.display()
```

Output:

```text
Animal name: Tommy
Breed: Labrador
```

Explanation:

- `Dog` inherits from `Animal`.
- `super().__init__(name)` calls the parent constructor.
- `super().display()` calls the parent method.
- The child class adds its own `breed` property.

### 10. Method Overriding

Method overriding occurs when a child class provides its own implementation of a method already defined in the parent class.

The method name and compatible calling interface are generally kept the same.

**Example:**

```python
class Animal:
    def sound(self):
        print("Animal makes a sound.")

class Dog(Animal):
    def sound(self):
        print("Dog barks.")

animal = Animal()
dog = Dog()

animal.sound()
dog.sound()
```

Output:

```text
Animal makes a sound.
Dog barks.
```

The `Dog` class overrides the `sound()` method inherited from `Animal`.

### 11. Extending an Overridden Method Using super()

A child class can override a method and still execute the parent class implementation using `super()`.

**Example:**

```python
class Employee:
    def details(self):
        print("Employee details.")

class Manager(Employee):
    def details(self):
        super().details()
        print("Manager details.")

manager = Manager()

manager.details()
```

Output:

```text
Employee details.
Manager details.
```

This allows the child class to extend rather than completely replace the parent's behavior.

### 12. What is Polymorphism?

Polymorphism means "many forms".

In programming, polymorphism allows the same interface, method name or operation to behave differently depending on the object or data type involved.

For example, different animals can make different sounds using the same method name.

**Example:**

```python
class Dog:
    def sound(self):
        print("Dog barks.")

class Cat:
    def sound(self):
        print("Cat meows.")

class Cow:
    def sound(self):
        print("Cow moos.")

animals = [Dog(), Cat(), Cow()]

for animal in animals:
    animal.sound()
```

Output:

```text
Dog barks.
Cat meows.
Cow moos.
```

The same method name `sound()` produces different behavior for different objects.

### 13. Types and Forms of Polymorphism in Python

Polymorphism can be implemented in several ways:

1. Method overriding.
2. Duck typing.
3. Operator overloading.
4. Method overloading-like behavior through flexible arguments.
5. Polymorphism through common interfaces and abstract base classes.

### 14. Polymorphism Through Method Overriding

This occurs when different child classes override a method inherited from the same parent class.

**Example:**

```python
class Shape:
    def area(self):
        print("Calculating area.")

class Circle(Shape):
    def area(self):
        print("Area of circle.")

class Rectangle(Shape):
    def area(self):
        print("Area of rectangle.")

shapes = [Circle(), Rectangle()]

for shape in shapes:
    shape.area()
```

Output:

```text
Area of circle.
Area of rectangle.
```

The same method call produces different results depending on the object.

### 15. Duck Typing

Duck typing is a Python concept in which an object's suitability is determined by the methods and behavior it supports rather than its specific class.

It is often explained using the phrase:

"If it walks like a duck and quacks like a duck, it is treated like a duck."

**Example:**

```python
class Dog:
    def sound(self):
        print("Bark")

class Cat:
    def sound(self):
        print("Meow")

class Robot:
    def sound(self):
        print("Electronic sound")

def make_sound(obj):
    obj.sound()

make_sound(Dog())
make_sound(Cat())
make_sound(Robot())
```

Output:

```text
Bark
Meow
Electronic sound
```

The `make_sound()` function works with different objects because each object provides a `sound()` method.

### 16. Operator Overloading

Operator overloading allows operators such as `+`, `-` and `*` to work with user-defined objects.

Python supports operator overloading through special methods, also called magic methods or dunder methods.

Examples:

| Operator | Special method |
|---|---|
| `+` | `__add__()` |
| `-` | `__sub__()` |
| `*` | `__mul__()` |
| `==` | `__eq__()` |
| `<` | `__lt__()` |
| `>` | `__gt__()` |
| `str()` | `__str__()` |

**Example: Overloading the + operator**

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value

n1 = Number(10)
n2 = Number(20)

print(n1 + n2)
```

Output:

```text
30
```

Explanation:

- `n1 + n2` internally calls `n1.__add__(n2)`.
- The method defines how addition works for `Number` objects.

**Example: Overloading the == operator**

```python
class Student:
    def __init__(self, marks):
        self.marks = marks

    def __eq__(self, other):
        return self.marks == other.marks

s1 = Student(90)
s2 = Student(90)

print(s1 == s2)
```

Output:

```text
True
```

### 17. Method Overloading

Method overloading traditionally means defining multiple methods with the same name but different parameter lists.

Languages such as Java and C++ support traditional method overloading.

Python does not support traditional method overloading through multiple same-named definitions in a class. A later definition replaces an earlier one.

However, similar behavior can be achieved using:

- Default arguments.
- `*args`.
- `**kwargs`.
- Type checking.
- `functools.singledispatch` for type-based function dispatch.

**Example using default arguments:**

```python
class Calculator:
    def add(self, a, b, c=0):
        return a + b + c

calculator = Calculator()

print(calculator.add(10, 20))
print(calculator.add(10, 20, 30))
```

Output:

```text
30
60
```

**Example using *args:**

```python
class Calculator:
    def add(self, *numbers):
        return sum(numbers)

calculator = Calculator()

print(calculator.add(10, 20))
print(calculator.add(10, 20, 30, 40))
```

Output:

```text
30
100
```

### 18. Method Overloading vs Method Overriding

| Method Overloading | Method Overriding |
|---|---|
| Same method name with different parameter lists | Child class redefines an inherited method |
| Traditional overloading is not directly supported by Python | Supported by Python |
| Often implemented using flexible arguments in Python | Implemented through inheritance |
| Does not necessarily require inheritance | Requires an inherited method to override |
| Example: `add(a, b)` and `add(a, b, c)` | Child class provides its own `sound()` method |

### 19. Method Resolution Order (MRO)

Method Resolution Order determines the order in which Python searches classes for a method or attribute, particularly when multiple inheritance is involved.

Python uses the C3 linearization algorithm to calculate MRO.

The `mro()` method or `__mro__` attribute can be used to inspect it.

**Example:**

```python
class A:
    def show(self):
        print("Class A")

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

print(D.mro())
```

Output:

```text
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

The lookup order is:

```text
D -> B -> C -> A -> object
```

Python follows this order when searching for inherited methods and attributes.

### 20. Abstract Classes and Methods

An abstract class is a class designed to provide a common structure for child classes.

It cannot normally be instantiated while it still has unimplemented abstract methods.

Python provides the `abc` module to create abstract base classes.

An abstract method is a method declared in a base class that concrete subclasses are expected to implement.

**Example:**

```python
from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        print("Dog barks.")

dog = Dog()

dog.sound()
```

Output:

```text
Dog barks.
```

Trying to create an `Animal` object directly raises a `TypeError` because the abstract method has not been implemented.

### 21. isinstance() and issubclass()

Python provides two useful functions for checking class relationships.

**A. isinstance()**

Checks whether an object is an instance of a particular class or its subclass.

Example:

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

print(isinstance(dog, Dog))
print(isinstance(dog, Animal))
```

Output:

```text
True
True
```

A `Dog` object is also considered an instance of `Animal` because `Dog` inherits from `Animal`.

**B. issubclass()**

Checks whether one class inherits from another class.

Example:

```python
class Animal:
    pass

class Dog(Animal):
    pass

print(issubclass(Dog, Animal))
print(issubclass(Animal, Dog))
```

Output:

```text
True
False
```

### 22. Composition vs Inheritance

Inheritance represents an "is-a" relationship.

Composition represents a "has-a" relationship.

**Inheritance example:**

A dog is an animal.

```python
class Animal:
    def eat(self):
        print("Eating.")

class Dog(Animal):
    pass

dog = Dog()
dog.eat()
```

**Composition example:**

A car has an engine.

```python
class Engine:
    def start(self):
        print("Engine started.")

class Car:
    def __init__(self):
        self.engine = Engine()

    def start_car(self):
        self.engine.start()
        print("Car started.")

car = Car()

car.start_car()
```

Output:

```text
Engine started.
Car started.
```

Composition is often preferable when one object needs to use another object's functionality without being a specialized version of it.

## Key concepts

1. **Inheritance:** Allows a class to acquire properties and methods from another class.
2. **Parent class:** The class whose functionality is inherited.
3. **Child class:** The class that inherits from another class.
4. **Single inheritance:** One child inherits from one parent.
5. **Multiple inheritance:** One child inherits from multiple parents.
6. **Multilevel inheritance:** Inheritance takes place across multiple levels.
7. **Hierarchical inheritance:** Multiple children inherit from one parent.
8. **Hybrid inheritance:** A combination of inheritance types.
9. **super():** Accesses the next class implementation according to MRO.
10. **Method overriding:** A child class provides its own implementation of an inherited method.
11. **Polymorphism:** The same interface can provide different behavior for different objects.
12. **Duck typing:** Objects are used according to the behavior they provide.
13. **Operator overloading:** Defines how operators work with user-defined objects.
14. **Method overloading:** Traditional multiple same-named method definitions with different signatures; Python uses alternative techniques for similar behavior.
15. **MRO:** Defines the order in which Python searches classes.
16. **Abstract class:** A class that provides a common structure for subclasses.
17. **Abstract method:** A method declared for implementation by concrete subclasses.
18. **isinstance():** Checks an object's class relationship.
19. **issubclass():** Checks inheritance between classes.
20. **Composition:** Builds objects using other objects.

## Examples

### Example 1: Employee management system

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print("Name:", self.name)
        print("Salary:", self.salary)

class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department

    def display(self):
        super().display()
        print("Department:", self.department)

manager = Manager("Riya", 50000, "IT")

manager.display()
```

Output:

```text
Name: Riya
Salary: 50000
Department: IT
```

### Example 2: Vehicle inheritance

```python
class Vehicle:
    def start(self):
        print("Vehicle started.")

class Car(Vehicle):
    def drive(self):
        print("Car is moving.")

class Bike(Vehicle):
    def ride(self):
        print("Bike is moving.")

car = Car()
bike = Bike()

car.start()
car.drive()

bike.start()
bike.ride()
```

Output:

```text
Vehicle started.
Car is moving.
Vehicle started.
Bike is moving.
```

### Example 3: Polymorphism using shapes

```python
class Circle:
    def area(self, radius):
        return 3.14 * radius * radius

class Rectangle:
    def area(self, length, width):
        return length * width

circle = Circle()
rectangle = Rectangle()

print("Circle area:", circle.area(5))
print("Rectangle area:", rectangle.area(10, 5))
```

Output:

```text
Circle area: 78.5
Rectangle area: 50
```

Both classes provide an `area()` method, but their implementations differ.

### Example 4: Payment system using polymorphism

```python
class Payment:
    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement pay().")

class UPI(Payment):
    def pay(self, amount):
        print("Paid", amount, "using UPI.")

class Card(Payment):
    def pay(self, amount):
        print("Paid", amount, "using Card.")

class Cash(Payment):
    def pay(self, amount):
        print("Paid", amount, "using Cash.")

payments = [UPI(), Card(), Cash()]

for payment in payments:
    payment.pay(500)
```

Output:

```text
Paid 500 using UPI.
Paid 500 using Card.
Paid 500 using Cash.
```

### Example 5: Multiple inheritance

```python
class Camera:
    def take_photo(self):
        print("Photo captured.")

class MusicPlayer:
    def play_music(self):
        print("Music playing.")

class Smartphone(Camera, MusicPlayer):
    def make_call(self):
        print("Calling...")

phone = Smartphone()

phone.take_photo()
phone.play_music()
phone.make_call()
```

Output:

```text
Photo captured.
Music playing.
Calling...
```

### Example 6: Custom operator overloading

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __str__(self):
        return f"({self.x}, {self.y})"

p1 = Point(2, 3)
p2 = Point(4, 5)

result = p1 + p2

print(result)
```

Output:

```text
(6, 8)
```

### Example 7: Abstract class for payment methods

```python
from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

class UPI(Payment):
    def pay(self, amount):
        print("UPI payment:", amount)

class Card(Payment):
    def pay(self, amount):
        print("Card payment:", amount)

payments = [UPI(), Card()]

for payment in payments:
    payment.pay(1000)
```

Output:

```text
UPI payment: 1000
Card payment: 1000
```

### Example 8: Hierarchical inheritance

```python
class Person:
    def introduce(self):
        print("I am a person.")

class Student(Person):
    def study(self):
        print("I study.")

class Teacher(Person):
    def teach(self):
        print("I teach.")

student = Student()
teacher = Teacher()

student.introduce()
student.study()

teacher.introduce()
teacher.teach()
```

Output:

```text
I am a person.
I study.
I am a person.
I teach.
```

## Common mistakes

1. **Incorrect inheritance syntax**
   - Use parentheses after the child class name.
   - Example: `class Dog(Animal):`

2. **Confusing parent and child classes**
   - The parent provides inherited functionality.
   - The child inherits and may extend or override it.

3. **Forgetting to call the parent constructor**
   - Use `super().__init__()` when the child needs to initialize the parent portion of the object.

4. **Using super() without understanding MRO**
   - `super()` follows method resolution order rather than simply meaning "call my direct parent."

5. **Overriding a method unintentionally**
   - Defining a method with the same name in a child class replaces the inherited implementation for normal lookup on that child object.
   - Use `super()` when the parent behavior should also run.

6. **Confusing method overloading and overriding**
   - Overriding replaces or extends inherited behavior.
   - Traditional signature-based overloading is not directly supported through multiple same-named definitions in Python.

7. **Using multiple inheritance without understanding MRO**
   - Inspect `ClassName.mro()` when method lookup is unclear.

8. **Forgetting self in instance methods**
   - Instance methods normally require `self` as the first parameter.

9. **Trying to instantiate an incomplete abstract class**
   - Implement all inherited abstract methods before creating an object.

10. **Using inheritance for every relationship**
    - Use inheritance for an "is-a" relationship.
    - Use composition for a "has-a" relationship.

11. **Assuming every object must inherit from the same custom parent**
    - Duck typing allows Python code to work with objects that provide the required methods.

12. **Defining the same method multiple times in one class**
    - A later definition replaces an earlier definition with the same name.
    - Use flexible arguments or another appropriate design instead.

13. **Comparing objects without defining equality behavior**
    - By default, `==` may compare object identity.
    - Implement `__eq__()` when value-based equality is needed.

14. **Making inheritance hierarchies unnecessarily complicated**
    - Prefer simple, understandable class relationships.

## Quick summary

- Inheritance allows one class to reuse another class's functionality.
- The parent class is also called the base class.
- The child class is also called the derived class.
- Python supports single, multiple, multilevel, hierarchical and hybrid inheritance.
- `super()` accesses the next implementation according to MRO.
- Method overriding allows a child class to customize inherited behavior.
- Polymorphism allows the same interface to behave differently for different objects.
- Duck typing focuses on object behavior rather than its specific class.
- Operator overloading uses special methods such as `__add__()` and `__eq__()`.
- Python does not support traditional method overloading through multiple same-named definitions.
- Default arguments and `*args` can provide similar flexibility.
- MRO determines the method lookup order.
- Abstract classes define common structures for subclasses.
- `isinstance()` checks object relationships.
- `issubclass()` checks class inheritance.
- Inheritance represents an "is-a" relationship.
- Composition represents a "has-a" relationship.

## Practice

### Beginner Level

1. Create a parent class `Animal` with an `eat()` method.
2. Create a child class `Dog` that inherits from `Animal`.
3. Create a `Person` class and a `Student` child class.
4. Create a `Vehicle` parent class with `Car` and `Bike` child classes.
5. Override a parent class method in a child class.
6. Use `super()` to call a parent class constructor.

### Intermediate Level

7. Demonstrate single inheritance.
8. Create a program demonstrating multiple inheritance.
9. Create a program demonstrating multilevel inheritance.
10. Create a program demonstrating hierarchical inheritance.
11. Implement polymorphism using a common method named `sound()`.
12. Demonstrate method overriding with different shapes.
13. Create a calculator class using flexible arguments.
14. Demonstrate operator overloading using `__add__()`.

### Advanced Level

15. Create a hybrid inheritance structure.
16. Demonstrate method resolution order using `mro()`.
17. Create an abstract class using `ABC` and `abstractmethod`.
18. Build a payment system using polymorphism.
19. Create a class hierarchy for employees and managers.
20. Implement duck typing using different classes.
21. Create a class that overloads both `+` and `==`.
22. Build a library management system using inheritance and polymorphism.

### Practice Solutions

**Solution 1: Single inheritance**

```python
class Animal:
    def eat(self):
        print("Eating food.")

class Dog(Animal):
    def bark(self):
        print("Barking.")

dog = Dog()

dog.eat()
dog.bark()
```

Output:

```text
Eating food.
Barking.
```

**Solution 2: Multiple inheritance**

```python
class Father:
    def skill1(self):
        print("Driving")

class Mother:
    def skill2(self):
        print("Cooking")

class Child(Father, Mother):
    pass

child = Child()

child.skill1()
child.skill2()
```

Output:

```text
Driving
Cooking
```

**Solution 3: Method overriding**

```python
class Animal:
    def sound(self):
        print("Animal sound.")

class Dog(Animal):
    def sound(self):
        print("Bark.")

dog = Dog()

dog.sound()
```

Output:

```text
Bark.
```

**Solution 4: Using super()**

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course

student = Student("Riya", "Python")

print(student.name)
print(student.course)
```

Output:

```text
Riya
Python
```

**Solution 5: Polymorphism**

```python
class Dog:
    def sound(self):
        print("Bark")

class Cat:
    def sound(self):
        print("Meow")

animals = [Dog(), Cat()]

for animal in animals:
    animal.sound()
```

Output:

```text
Bark
Meow
```

**Solution 6: Operator overloading**

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Number(self.value + other.value)

n1 = Number(10)
n2 = Number(20)

result = n1 + n2

print(result.value)
```

Output:

```text
30
```

**Solution 7: Check inheritance**

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

print(isinstance(dog, Dog))
print(isinstance(dog, Animal))
print(issubclass(Dog, Animal))
```

Output:

```text
True
True
True
```

**Solution 8: Abstract class**

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

rectangle = Rectangle(10, 5)

print(rectangle.area())
```

Output:

```text
50
```

## Learning resources

- **PDF:** [Inheritance and Polymorphism PDF](https://drive.google.com/file/d/1uQ3seSyaFfb5A8ckRT5V-LaySp_nClLZ/view?usp=drive_link)
- **YouTube:** Temporary testing link — replace with a topic-specific video before publishing: https://youtu.be/ERCMXc8x7mc