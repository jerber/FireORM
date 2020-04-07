import os
from fireorm.Models import DateModel
from fireorm.Fields import TextField, NumberField

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/jeremyberman/Downloads/my-serv.json'

class User(DateModel):
	name = TextField(required=True, default='Jon')
	age = NumberField()

def test_date_model():
	user = User()
	print(user)
	user.save()
	print(user)

def test_null():
	user = User()
	print(user)
	user.save()
	print(user)
	user.update()
	print(user)