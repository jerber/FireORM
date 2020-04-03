#FireORM
The easiest way to use Firestore with python.

##Instalation
```
pip install fireorm
```

##Example
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
