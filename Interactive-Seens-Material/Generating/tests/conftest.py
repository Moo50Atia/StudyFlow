import pytest

@pytest.fixture
def sample_markdown_document():
    """Generates a sample markdown document with various elements for testing chunk boundaries."""
    return """# Unit 2: Objects and Classes

## 2.1 Introduction to Objects
An object is a basic unit of Object-Oriented Programming and represents the real-life entities.
A typical Java program creates many objects, which as you know, interact by invoking methods.

An object consists of:
1. State: It is represented by attributes of an object. It also reflects the properties of an object.
2. Behavior: It is represented by methods of an object. It also reflects the response of an object with other objects.
3. Identity: It gives a unique name to an object and enables one object to interact with other objects.

## 2.2 Classes in Java
A class is a user defined blueprint or prototype from which objects are created.
It represents the set of properties or methods that are common to all objects of one type.

```java
public class Dog {
    // Instance Variables
    String name;
    String breed;
    int age;
    String color;
  
    // Constructor Declaration of Class
    public Dog(String name, String breed,
               int age, String color)
    {
        this.name = name;
        this.breed = breed;
        this.age = age;
        this.color = color;
    }
  
    // method 1
    public String getName()
    {
        return name;
    }
}
```

## 2.3 Mathematical Proof
Here is a simple mathematical formula that should not be split:
$$
f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
This formula is very important.

## 2.4 Summary Table
| Feature | Description |
|---------|-------------|
| Class | Blueprint |
| Object | Instance |
| Method | Behavior |
| Field | State |

## 2.5 Summary
This is the final section.
"""
