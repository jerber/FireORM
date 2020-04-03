# FireORM
The easiest way to use Firestore with python.

## Instalation
```
pip install fireorm
```

## Example
```python
from fireorm.Models import Model
from fireorm.Fields import TextField

class Salesman(Model):
    name = TextField()
    company = TextField()

s = Salesman()
s.name = 'Jim'
s.save()

# Get Salesman
s = Salesman.collection.get(s.id)
print(s.name) # Jim
```

## Fields
There are 9 types of builtin fields, consistant with Firestore: `BooleanField`, `DateField`, `ListField`, `MapField`, `NullField`, `ReferenceField`, `TextField`, and `NestedModel` (which we'll get in a bit).

Each field takes the optional parameters `default ` and `required`. If the field is not set, it will default to the value of `default`. If there is no `default`, the field is not set, and `required == True`, an `Exception` will be raised.


#### Fields Example
```python
class Manager(Model):
	name = TextField(required=True)
	age = NumberField(required=True)
	company = TextField(required=True, default='Dunder Mifflin')
	startedWorkingAt = DateField()

m = Manager(name='Michael Scott') # you can pass in fields or set them later
m.age = 45
m.save() # Success! New doc in collection "manager" as: { name: Michael Scott, age: 45, company: Dunder Mifflin }

m = Manager()
m.name = 'Dwight Schrute'
m.save() # Exception since age is required but not given

```

You can also add a NestedModel which lets you add a defined class as a Field.

### NestedModel Example
```python
class Dog(Model):
	age = NumberField()
	owner = Manager(required=True)

dog = Dog()
dog.age = 3
dog.owner = Manager(name='Robert California', age=59)
dog.save()

```


## Collections
The collection name for a class defaults to the class' name in lowercase. To set the collection name, use the `Meta` class. You can also specify which fields print when printing the class.

### Meta Example

```python
class Student(Model):
	name = TextField()
	school = TextField(required=True, default='UPenn')
	
	class Meta:
		collection_name = 'students'
		fields_to_print = ['name']

s = Student(name='Amy Gutman')
s.save() # creates a new document in the "students" collection
print(s) # <*Student* key: students/9AJ5DeSvzfD04uqyhhpL, id: 9AJ5DeSvzfD04uqyhhpL, name: Amy Gutman>

```

You can also inheret classes.

### Inheritance Example
```python
class ExchangeStudent(Student):
	originalCountry = TextField(required=True)
	
	class Meta:
		collection_name = 'exchangeStudents'
		fields_to_print = None # when this is None or does not exist, it prints all fields. When it is [] it only prints the defaults (key and id).

e = ExchangeStudent(originalCountry='UK')
print(e.school) # UPenn
e.save()
print(e) # <*ExchangeStudent* key: exchangeStudents/XbGdMjo9x9166MvZ79Zr, id: XbGdMjo9x9166MvZ79Zr, name: None, originalCountry: UK, school: UPenn>
```

## Queries
You can make queries with the same syntax you would using the Python firebase-admin SDK. But FireORM returns the objects.

### Queries Example
```python
managers = Manager.collection.where('name', '==', 'Michael Scott').limit(1).stream()
print(managers) # [<*Manager* key: manager/Z8S75KU2n7QQnIm2cExy, id: Z8S75KU2n7QQnIm2cExy, age: 45, company: Dunder Mifflin, name: Michael Scott, startedWorkingAt: None>]

manager = Manager.collection.get('Z8S75KU2n7QQnIm2cExy')
print(manager) # <*Manager* key: manager/Z8S75KU2n7QQnIm2cExy, id: Z8S75KU2n7QQnIm2cExy, age: 45, company: Dunder Mifflin, name: Michael Scott, startedWorkingAt: None>
```
